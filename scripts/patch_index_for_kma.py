#!/usr/bin/env python3
"""기존 index.html의 Open-Meteo 호출을 weather.json 기반으로 교체한다."""

from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

text = text.replace("<h2>오늘 날씨 예보</h2>", "<h2>오늘의 체감온도</h2>")
text = text.replace("<div class=\"weather-title\" id=\"weatherTitle\">현재 체감온도</div>", "<div class=\"weather-title\" id=\"weatherTitle\">현재 체감온도(기상청 예보 기준)</div>")
text = text.replace(
    "시간별 예보 기온·습도에 기상청 여름철 체감온도 산식을 적용한 참고값입니다. 실제 판단은 현장 측정값과 회사 지침을 우선하세요.",
    "기상청 단기예보의 시간별 기온·습도에 기상청 여름철 체감온도 산식을 적용한 값입니다. 실제 판단은 현장 측정값과 회사 지침을 우선하세요.",
)

replacement = r'''async function loadWeather(){
  const s=stationData[state.station];
  weatherTitle.textContent='현재 체감온도(기상청 예보 기준)';
  currentTemp.textContent='--℃';
  weatherMeta.textContent='기상청 단기예보를 확인하고 있습니다.';
  try{
    const res=await fetch(`weather.json?v=${Date.now()}`,{cache:'no-store'});
    if(!res.ok)throw new Error(`weather.json ${res.status}`);
    const data=await res.json();
    const station=data.stations?.[state.station];
    if(!station||!Array.isArray(station.hourly)||!station.hourly.length)throw new Error('역별 예보 없음');
    const row=station.current||station.hourly[0];
    const t=Number(row.temp),rh=Number(row.rh),hi=Number(row.hi);
    if(!Number.isFinite(t)||!Number.isFinite(rh)||!Number.isFinite(hi))throw new Error('잘못된 예보값');
    state.autoValue=hi;
    state.hourly=station.hourly.map(x=>({time:x.time,temp:Number(x.temp),rh:Number(x.rh),hi:Number(x.hi)}));
    const lv=getLevel(hi);
    currentTemp.textContent=`${hi.toFixed(1)}℃`;
    weatherMeta.textContent=`기온 ${t.toFixed(1)}℃ · 습도 ${Math.round(rh)}% · 기상청 ${data.baseTime?.slice(0,2)||'--'}시 발표`;
    currentBadge.textContent=lv.name;
    currentBadge.style.background=lv.color;
    const generated=data.generatedAt?new Date(data.generatedAt):new Date();
    updated.textContent=`${generated.toLocaleString('ko-KR')} 갱신`;
    renderForecast();
    renderGuide();
  }catch(e){
    console.error(e);
    state.autoValue=null;
    state.hourly=[];
    currentTemp.textContent='확인 실패';
    weatherMeta.textContent='기상청 예보 파일을 불러오지 못했습니다. 현장값을 직접 입력하세요.';
    currentBadge.textContent='현장값 우선';
    currentBadge.style.background='#697887';
    forecast.innerHTML='<div class="hint">기상청 시간별 예보를 불러오지 못했습니다.</div>';
    renderGuide();
  }
}
function isInShift'''

pattern = r"async function loadWeather\(\)\{.*?\}\nfunction isInShift"
new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit("loadWeather 함수를 찾지 못해 index.html을 수정하지 못했습니다.")

path.write_text(new_text, encoding="utf-8")
print("index.html을 기상청 weather.json 방식으로 수정했습니다.")
