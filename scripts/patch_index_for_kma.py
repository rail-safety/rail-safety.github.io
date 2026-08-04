#!/usr/bin/env python3
"""index.html을 기상청 weather.json 구조와 최신 문구로 정리한다."""

from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = {
    "<h2>현장측정값을 입력하세요</h2>": "<h2>현장 체감온도 계산기</h2>",
    "<div class=\"section-label\">직무별 행동지침</div><h2>지금 이렇게 하세요</h2>": "<h2>행동지침</h2>",
    ">↔ 수송·입환</button>": ">수송</button>",
    ">● 홈안내</button>": ">홈안내</button>",
    "현재 체감온도(기상청 예보 기준)": "현재 체감온도(기상청 초단기실황)",
}
for old, new in replacements.items():
    text = text.replace(old, new)

replacement = r'''async function loadWeather(){
  const s=stationData[state.station];
  weatherTitle.textContent='현재 체감온도(기상청 초단기실황)';
  currentTemp.textContent='--℃';
  weatherMeta.textContent='기상청 초단기실황을 확인하고 있습니다.';
  try{
    const res=await fetch(`weather.json?v=${Date.now()}`,{cache:'no-store'});
    if(!res.ok)throw new Error(`weather.json ${res.status}`);
    const data=await res.json();
    const station=data.stations?.[state.station];
    if(!station||!station.current||!Array.isArray(station.hourly)||!station.hourly.length)throw new Error('역별 기상자료 없음');
    const row=station.current;
    const t=Number(row.temp),rh=Number(row.rh),hi=Number(row.hi);
    if(!Number.isFinite(t)||!Number.isFinite(rh)||!Number.isFinite(hi))throw new Error('잘못된 실황값');
    state.autoValue=hi;
    state.hourly=station.hourly.map(x=>({time:x.time,temp:Number(x.temp),rh:Number(x.rh),hi:Number(x.hi)}));
    const lv=getLevel(hi);
    currentTemp.textContent=`${hi.toFixed(1)}℃`;
    const observed=row.time?new Date(row.time):null;
    const observedText=observed&&!Number.isNaN(observed.getTime())?observed.toLocaleString('ko-KR',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'}):'최근';
    weatherMeta.textContent=`기온 ${t.toFixed(1)}℃ · 습도 ${Math.round(rh)}% · ${observedText} 관측`;
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
    weatherMeta.textContent='기상청 실황 파일을 불러오지 못했습니다. 현장값을 직접 입력하세요.';
    currentBadge.textContent='현장값 우선';
    currentBadge.style.background='#697887';
    forecast.innerHTML='<div class="hint">기상청 시간별 예보를 불러오지 못했습니다.</div>';
    renderGuide();
  }
}
function isInShift'''

pattern = r"async function loadWeather\(\)\{.*?\}\nfunction isInShift"
text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit("loadWeather 함수를 찾지 못했습니다.")

path.write_text(text, encoding="utf-8")
print("index.html 문구와 기상청 실황 표시를 수정했습니다.")
