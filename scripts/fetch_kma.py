#!/usr/bin/env python3
"""기상청 단기예보(TMP, REH)를 역별로 수집해 weather.json을 생성한다."""

from __future__ import annotations

import json
import math
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

KST = timezone(timedelta(hours=9))
API_URL = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
BASE_TIMES = [2, 5, 8, 11, 14, 17, 20, 23]

STATIONS = {
    "suncheon": {"name": "순천역", "lat": 34.9456, "lon": 127.5022},
    "gokseong": {"name": "곡성역", "lat": 35.2820, "lon": 127.2916},
    "gurye": {"name": "구례구역", "lat": 35.1632, "lon": 127.4511},
    "beolgyo": {"name": "벌교역", "lat": 34.8443, "lon": 127.3422},
    "boseong": {"name": "보성역", "lat": 34.7634, "lon": 127.0802},
}


def latlon_to_grid(lat: float, lon: float) -> tuple[int, int]:
    """기상청 DFS 격자 변환 공식."""
    re = 6371.00877 / 5.0
    grid = 5.0
    slat1 = 30.0
    slat2 = 60.0
    olon = 126.0
    olat = 38.0
    xo = 43.0
    yo = 136.0
    degrad = math.pi / 180.0

    slat1 *= degrad
    slat2 *= degrad
    olon *= degrad
    olat *= degrad

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)

    ra = math.tan(math.pi * 0.25 + lat * degrad * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = lon * degrad - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn

    x = int(math.floor(ra * math.sin(theta) + xo + 0.5))
    y = int(math.floor(ro - ra * math.cos(theta) + yo + 0.5))
    return x, y


def choose_base(now: datetime) -> tuple[str, str]:
    """발표 후 약 20분의 API 반영 지연을 고려해 최신 발표시각을 고른다."""
    available = now - timedelta(minutes=20)
    for hour in reversed(BASE_TIMES):
        candidate = available.replace(hour=hour, minute=0, second=0, microsecond=0)
        if candidate <= available:
            return candidate.strftime("%Y%m%d"), candidate.strftime("%H00")
    previous = (available - timedelta(days=1)).replace(hour=23, minute=0, second=0, microsecond=0)
    return previous.strftime("%Y%m%d"), "2300"


def apparent_temperature(t: float, rh: float) -> float:
    """기상청 여름철 체감온도 산식."""
    tw = (
        t * math.atan(0.151977 * math.sqrt(rh + 8.313659))
        + math.atan(t + rh)
        - math.atan(rh - 1.67633)
        + 0.00391838 * math.pow(rh, 1.5) * math.atan(0.023101 * rh)
        - 4.686035
    )
    value = -0.2442 + 0.55399 * tw + 0.45535 * t - 0.0022 * tw * tw + 0.00278 * tw * t + 3.0
    return round(value, 1)


def request_forecast(service_key: str, base_date: str, base_time: str, nx: int, ny: int) -> list[dict[str, Any]]:
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": str(nx),
        "ny": str(ny),
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "suncheon-heat-safety/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.load(response)

    header = payload.get("response", {}).get("header", {})
    if header.get("resultCode") != "00":
        raise RuntimeError(f"KMA API error {header.get('resultCode')}: {header.get('resultMsg')}")

    items = payload.get("response", {}).get("body", {}).get("items", {}).get("item", [])
    if not isinstance(items, list):
        raise RuntimeError("기상청 응답에 예보 항목이 없습니다.")
    return items


def build_hourly(items: list[dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, float]] = {}
    for item in items:
        category = item.get("category")
        if category not in {"TMP", "REH"}:
            continue
        stamp = f"{item.get('fcstDate', '')}{item.get('fcstTime', '')}"
        try:
            value = float(item.get("fcstValue"))
        except (TypeError, ValueError):
            continue
        grouped.setdefault(stamp, {})[category] = value

    cutoff = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    end = now + timedelta(hours=42)
    hourly: list[dict[str, Any]] = []
    for stamp in sorted(grouped):
        values = grouped[stamp]
        if "TMP" not in values or "REH" not in values:
            continue
        dt = datetime.strptime(stamp, "%Y%m%d%H%M").replace(tzinfo=KST)
        if dt < cutoff or dt > end:
            continue
        t = values["TMP"]
        rh = values["REH"]
        hourly.append(
            {
                "time": dt.isoformat(timespec="minutes"),
                "temp": round(t, 1),
                "rh": round(rh),
                "hi": apparent_temperature(t, rh),
            }
        )
    if not hourly:
        raise RuntimeError("TMP와 REH가 함께 있는 시간별 예보가 없습니다.")
    return hourly


def main() -> int:
    service_key = os.environ.get("KMA_SERVICE_KEY", "").strip()
    if not service_key:
        print("KMA_SERVICE_KEY가 설정되지 않았습니다.", file=sys.stderr)
        return 2

    now = datetime.now(KST)
    base_date, base_time = choose_base(now)
    output: dict[str, Any] = {
        "source": "기상청 단기예보 조회서비스",
        "formula": "기상청 여름철 체감온도 산식",
        "generatedAt": now.isoformat(timespec="seconds"),
        "baseDate": base_date,
        "baseTime": base_time,
        "stations": {},
    }

    for key, station in STATIONS.items():
        nx, ny = latlon_to_grid(station["lat"], station["lon"])
        items = request_forecast(service_key, base_date, base_time, nx, ny)
        hourly = build_hourly(items, now)
        current = min(hourly, key=lambda row: abs(datetime.fromisoformat(row["time"]) - now))
        output["stations"][key] = {
            "name": station["name"],
            "nx": nx,
            "ny": ny,
            "current": current,
            "hourly": hourly,
        }
        print(f"{station['name']}: nx={nx}, ny={ny}, {len(hourly)}시간 수집")

    Path("weather.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
