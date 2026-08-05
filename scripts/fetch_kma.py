#!/usr/bin/env python3
"""기상청 초단기실황과 단기예보를 역별로 수집해 weather.json을 갱신한다."""

from __future__ import annotations

import copy
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

KST = timezone(timedelta(hours=9))
CURRENT_URL = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
FORECAST_URL = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
FORECAST_BASE_TIMES = [2, 5, 8, 11, 14, 17, 20, 23]
OUTPUT_PATH = Path("weather.json")
STATIONS = {
    "suncheon": {"name": "순천역", "lat": 34.9456, "lon": 127.5022},
    "gokseong": {"name": "곡성역", "lat": 35.2820, "lon": 127.2916},
    "gurye": {"name": "구례구역", "lat": 35.1632, "lon": 127.4511},
    "beolgyo": {"name": "벌교역", "lat": 34.8443, "lon": 127.3422},
    "boseong": {"name": "보성역", "lat": 34.7634, "lon": 127.0802},
}


def latlon_to_grid(lat: float, lon: float) -> tuple[int, int]:
    re = 6371.00877 / 5.0
    slat1, slat2 = math.radians(30.0), math.radians(60.0)
    olon, olat = math.radians(126.0), math.radians(38.0)
    xo, yo = 43.0, 136.0
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(
        math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    )
    sf = math.pow(math.tan(math.pi * 0.25 + slat1 * 0.5), sn) * math.cos(slat1) / sn
    ro = re * sf / math.pow(math.tan(math.pi * 0.25 + olat * 0.5), sn)
    ra = re * sf / math.pow(math.tan(math.pi * 0.25 + math.radians(lat) * 0.5), sn)
    theta = math.radians(lon) - olon
    if theta > math.pi:
        theta -= 2 * math.pi
    if theta < -math.pi:
        theta += 2 * math.pi
    theta *= sn
    return int(math.floor(ra * math.sin(theta) + xo + 0.5)), int(math.floor(ro - ra * math.cos(theta) + yo + 0.5))


def apparent_temperature(t: float, rh: float) -> float:
    tw = (
        t * math.atan(0.151977 * math.sqrt(rh + 8.313659))
        + math.atan(t + rh)
        - math.atan(rh - 1.67633)
        + 0.00391838 * math.pow(rh, 1.5) * math.atan(0.023101 * rh)
        - 4.686035
    )
    value = -0.2442 + 0.55399 * tw + 0.45535 * t - 0.0022 * tw * tw + 0.00278 * tw * t + 3.0
    return round(value, 1)


def choose_forecast_base(now: datetime) -> tuple[str, str]:
    available = now - timedelta(minutes=20)
    for hour in reversed(FORECAST_BASE_TIMES):
        candidate = available.replace(hour=hour, minute=0, second=0, microsecond=0)
        if candidate <= available:
            return candidate.strftime("%Y%m%d"), candidate.strftime("%H00")
    previous = (available - timedelta(days=1)).replace(hour=23, minute=0, second=0, microsecond=0)
    return previous.strftime("%Y%m%d"), "2300"


def current_base_candidates(now: datetime, attempts: int = 6) -> list[tuple[str, str]]:
    """현재 정시부터 직전 정시까지 조회해 실제 제공된 가장 최신 실황을 선택한다."""
    anchor = now.replace(minute=0, second=0, microsecond=0)
    return [
        (
            (anchor - timedelta(hours=offset)).strftime("%Y%m%d"),
            (anchor - timedelta(hours=offset)).strftime("%H00"),
        )
        for offset in range(attempts)
    ]


def request_items(
    url: str,
    service_key: str,
    base_date: str,
    base_time: str,
    nx: int,
    ny: int,
    rows: int,
    retries: int = 3,
) -> list[dict[str, Any]]:
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": str(rows),
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": str(nx),
        "ny": str(ny),
    }
    request = urllib.request.Request(
        url + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "suncheon-heat-safety/2.0"},
    )
    errors: list[str] = []

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
            header = payload.get("response", {}).get("header", {})
            if header.get("resultCode") != "00":
                raise RuntimeError(f"KMA API error {header.get('resultCode')}: {header.get('resultMsg')}")
            items = payload.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if not isinstance(items, list) or not items:
                raise RuntimeError("기상청 응답에 항목이 없습니다.")
            return items
        except Exception as exc:  # 네트워크·API 일시 오류를 함께 재시도
            errors.append(str(exc))
            if attempt + 1 < retries:
                time.sleep(2 ** attempt)

    raise RuntimeError(" / ".join(errors))


def build_current(items: list[dict[str, Any]], base_date: str, base_time: str) -> dict[str, Any]:
    values: dict[str, float] = {}
    for item in items:
        category = item.get("category")
        if category not in {"T1H", "REH"}:
            continue
        try:
            values[category] = float(item.get("obsrValue"))
        except (TypeError, ValueError):
            continue
    if "T1H" not in values or "REH" not in values:
        raise RuntimeError("초단기실황에 T1H 또는 REH가 없습니다.")
    t, rh = values["T1H"], values["REH"]
    observed_at = datetime.strptime(base_date + base_time, "%Y%m%d%H%M").replace(tzinfo=KST)
    return {
        "time": observed_at.isoformat(timespec="minutes"),
        "temp": round(t, 1),
        "rh": round(rh),
        "hi": apparent_temperature(t, rh),
        "source": "초단기실황",
    }


def fetch_latest_current(service_key: str, now: datetime, nx: int, ny: int) -> tuple[dict[str, Any], str, str]:
    errors: list[str] = []
    for base_date, base_time in current_base_candidates(now):
        try:
            items = request_items(CURRENT_URL, service_key, base_date, base_time, nx, ny, 100)
            return build_current(items, base_date, base_time), base_date, base_time
        except Exception as exc:
            errors.append(f"{base_date} {base_time}: {exc}")
    raise RuntimeError("최근 초단기실황 조회 실패: " + " | ".join(errors))


def build_hourly(items: list[dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, float]] = {}
    for item in items:
        category = item.get("category")
        if category not in {"TMP", "REH"}:
            continue
        stamp = f"{item.get('fcstDate', '')}{item.get('fcstTime', '')}"
        try:
            grouped.setdefault(stamp, {})[category] = float(item.get("fcstValue"))
        except (TypeError, ValueError):
            continue

    cutoff = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    end = now + timedelta(hours=42)
    hourly: list[dict[str, Any]] = []
    for stamp in sorted(grouped):
        values = grouped[stamp]
        if "TMP" not in values or "REH" not in values:
            continue
        forecast_at = datetime.strptime(stamp, "%Y%m%d%H%M").replace(tzinfo=KST)
        if cutoff <= forecast_at <= end:
            t, rh = values["TMP"], values["REH"]
            hourly.append(
                {
                    "time": forecast_at.isoformat(timespec="minutes"),
                    "temp": round(t, 1),
                    "rh": round(rh),
                    "hi": apparent_temperature(t, rh),
                }
            )
    if not hourly:
        raise RuntimeError("TMP와 REH가 함께 있는 시간별 예보가 없습니다.")
    return hourly


def load_previous() -> dict[str, Any]:
    if not OUTPUT_PATH.exists():
        return {}
    try:
        return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def main() -> int:
    service_key = os.environ.get("KMA_SERVICE_KEY", "").strip()
    if not service_key:
        print("KMA_SERVICE_KEY가 설정되지 않았습니다.", file=sys.stderr)
        return 2

    now = datetime.now(KST)
    previous = load_previous()
    previous_stations = previous.get("stations", {}) if isinstance(previous.get("stations"), dict) else {}
    forecast_date, forecast_time = choose_forecast_base(now)
    forecast_changed = (
        previous.get("baseDate") != forecast_date
        or previous.get("baseTime") != forecast_time
        or not previous_stations
    )

    output: dict[str, Any] = {
        "source": {"current": "기상청 초단기실황", "forecast": "기상청 단기예보"},
        "formula": "기상청 여름철 체감온도 산식",
        "generatedAt": previous.get("generatedAt"),
        "currentBaseDate": previous.get("currentBaseDate"),
        "currentBaseTime": previous.get("currentBaseTime"),
        "baseDate": previous.get("baseDate"),
        "baseTime": previous.get("baseTime"),
        "stations": {},
    }

    current_bases: list[tuple[str, str]] = []
    forecast_success_count = 0

    for key, station in STATIONS.items():
        nx, ny = latlon_to_grid(station["lat"], station["lon"])
        old_station = previous_stations.get(key, {}) if isinstance(previous_stations.get(key), dict) else {}
        old_current = old_station.get("current")
        old_hourly = old_station.get("hourly") if isinstance(old_station.get("hourly"), list) else []

        try:
            current, current_date, current_time = fetch_latest_current(service_key, now, nx, ny)
            current_bases.append((current_date, current_time))
            print(f"{station['name']}: {current_date} {current_time} 실황 수집 완료")
        except Exception as exc:
            if not old_current:
                raise
            current = old_current
            print(f"::warning::{station['name']} 실황 갱신 실패, 직전 값 유지: {exc}")

        hourly = old_hourly
        if forecast_changed or not hourly:
            try:
                forecast_items = request_items(FORECAST_URL, service_key, forecast_date, forecast_time, nx, ny, 1000)
                hourly = build_hourly(forecast_items, now)
                forecast_success_count += 1
                print(f"{station['name']}: {forecast_date} {forecast_time} 단기예보 수집 완료")
            except Exception as exc:
                if not hourly:
                    raise
                print(f"::warning::{station['name']} 예보 갱신 실패, 직전 예보 유지: {exc}")

        output["stations"][key] = {
            "name": station["name"],
            "nx": nx,
            "ny": ny,
            "current": current,
            "hourly": hourly,
        }

    if current_bases:
        # 모든 역이 같은 시각을 받는 것이 보통이지만, 가장 오래된 시각을 전체 기준으로 기록한다.
        output["currentBaseDate"], output["currentBaseTime"] = min(current_bases)

    if forecast_changed and forecast_success_count == len(STATIONS):
        output["baseDate"] = forecast_date
        output["baseTime"] = forecast_time

    comparable_previous = copy.deepcopy(previous)
    comparable_output = copy.deepcopy(output)
    comparable_previous.pop("generatedAt", None)
    comparable_output.pop("generatedAt", None)

    if comparable_output == comparable_previous:
        print("새로운 기상청 실황·예보가 없어 weather.json을 변경하지 않습니다.")
        return 0

    output["generatedAt"] = now.isoformat(timespec="seconds")
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"weather.json 갱신 완료: {output['generatedAt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
