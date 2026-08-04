#!/usr/bin/env python3
"""index.html을 기상청 weather.json 구조와 최신 문구·행동지침으로 정리한다."""

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

guides_replacement = r'''const guides={
normal:{
summary:'기본 온열질환 예방수칙을 지키며 업무를 수행하세요.',
yard:['토시, 넥쿨러 등 온열질환 예방용품을 준비하세요.','입환 시작 전 불필요한 옥외 대기시간을 줄이세요.','작업이 끝나면 실내 또는 그늘로 이동하세요.'],
platform:['적절한 시간에 승강장으로 나가세요.','대기시간에는 그늘을 이용하세요.','안내와 안내 사이에는 실내로 복귀하세요.']
},
caution:{
summary:'옥외 체류시간을 줄이고 작업 사이에 몸을 식히세요.',
yard:['작업 동선과 역할을 미리 정해 옥외 체류시간을 줄이세요.','작업 사이의 대기와 불필요한 이동을 최소화하세요.','작업 사이에 실내 또는 냉방장소에서 몸을 식히세요.'],
platform:['안내 및 대기 중에는 그늘을 이용하세요.','안내가 끝나면 실내 또는 냉방장소로 복귀하세요.','홈안내가 장시간 연속되는 경우에는 교대하거나 냉방휴식을 확보하세요.']
},
warning:{
summary:'작업 순서와 휴식계획을 확인하고 냉방휴식을 확보하세요.',
yard:['작업 전 작업 순서와 휴식계획을 관리자와 확인하세요.','2인 이상 작업 원칙을 지키고 서로의 말투·걸음·반응을 확인하세요.','작업을 짧은 단위로 나누고 선로 주변 대기시간을 최소화하세요.','작업이 끝나면 즉시 냉방장소에서 몸을 식히세요.'],
platform:['홈으로 이동하기 전 안내 위치와 대기 위치, 실내 복귀 동선을 확인하세요.','안내 전 대기는 가능한 차양이나 그늘을 이용하고, 안내가 끝나면 실내로 복귀하세요.','연속 홈안내가 예정된 경우 사전에 교대자와 냉방휴식 시간을 정하세요.','인턴사원의 안내 구간과 복귀 동선을 확인하고, 장시간 혼자 옥외에 머물지 않도록 관리하세요.']
},
danger:{
summary:'현재 시행하려는 업무가 즉시 필요한 업무인지, 연기 가능한 업무인지 관리자와 먼저 확인하세요.',
yard:['연기 가능한 업무는 조정하고, 반드시 필요한 업무만 시행하세요.','작업 전 역할과 동선을 실내에서 정리해 옥외 체류시간을 줄이세요.','2인 이상이 서로 상태를 확인하며 최소 인원·최단시간으로 작업하세요.','작업 종료 후 즉시 냉방장소로 이동해 몸을 충분히 식히세요.'],
platform:['홈안내 시행 전 안내 동선과 대기 위치, 실내 복귀 경로를 확인하세요.','안내 전 대기시간과 안내 종료 후 홈 체류시간을 최소화하세요.','연속 안내가 예정된 경우 교대자와 냉방휴식 시간을 미리 정하세요.','인턴사원의 안내 동선과 옥외 체류시간을 확인하고, 무리하게 안내를 계속하지 않도록 관리하세요.','어지럼, 메스꺼움, 반응 저하 등 이상징후가 있으면 즉시 교대를 요청하세요.']
},
extreme:{
summary:'업무가 긴급하거나 반드시 필요한 업무인지 관리자와 확인하세요. 연기 가능한 업무는 시행하지 않습니다.',
yard:['반드시 필요한 업무만 최소 인원·최단시간으로 수행하세요.','2인 이상이 서로 상태를 계속 확인하고 단독 행동을 하지 마세요.','보냉장구와 연락수단을 준비하고 옥외 대기시간을 만들지 마세요.','말투·걸음·반응이 평소와 다르면 즉시 작업을 중지하세요.','작업이 끝나면 즉시 냉방장소로 이동하세요.'],
platform:['안내 전 이동·대기·복귀 동선을 사전에 확인해 옥외 체류시간을 최소화하세요.','연속 홈안내가 발생하지 않도록 교대자와 업무를 조정하세요.','인턴사원이 단독으로 장시간 안내하지 않도록 담당 직원이 동선과 상태를 확인하세요.','몸 상태가 평소와 다르면 안내를 계속하지 말고 즉시 교대를 요청하세요.','의식·말투·걸음에 이상이 있으면 즉시 냉방장소로 이동시키고 응급조치를 시행하세요.']
}};
function heatIndex'''

guides_pattern = r"const guides=\{.*?\};\nfunction heatIndex"
text, guides_count = re.subn(guides_pattern, guides_replacement, text, count=1, flags=re.S)
if guides_count != 1:
    raise SystemExit("행동지침 데이터를 찾지 못했습니다.")

weather_replacement = r'''async function loadWeather(){
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

weather_pattern = r"async function loadWeather\(\)\{.*?\}\nfunction isInShift"
text, weather_count = re.subn(weather_pattern, weather_replacement, text, count=1, flags=re.S)
if weather_count != 1:
    raise SystemExit("loadWeather 함수를 찾지 못했습니다.")

path.write_text(text, encoding="utf-8")
print("index.html 문구·기상청 실황 표시·행동지침을 수정했습니다.")
