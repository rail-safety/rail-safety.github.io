#!/usr/bin/env python3
"""index.html을 기상청 자료와 최신 행동·건강안내 구조로 정리한다."""

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

style_marker = ".health-info{margin-top:18px}"
if style_marker not in text:
    extra_style = r'''
    .health-info{margin-top:18px}.health-info>.section-label{margin-bottom:6px}.info-block{margin-top:9px;border:1px solid var(--line);border-radius:14px;padding:0 14px;background:#fff;overflow:hidden}.info-block summary{padding:14px 0;color:var(--text);font-size:16px}.info-block[open] summary{color:var(--level)}.info-block ul,.info-block ol{margin:0 0 15px;padding-left:22px}.info-block li{margin:7px 0}.support-note{margin-top:12px;border-left:5px solid var(--level);background:#f7f9fa;border-radius:12px;padding:12px 14px}.check-intro{margin:0 0 7px;color:var(--muted);font-size:14px}.check-list{border-top:1px solid var(--line);margin-top:8px}.condition-row{display:flex;align-items:center;gap:10px;padding:12px 2px;border-bottom:1px solid var(--line);font-weight:800}.condition-row input{width:22px;height:22px;accent-color:var(--ok);flex:0 0 auto}.condition-result{margin:13px 0 15px;padding:14px;border-radius:13px;background:#f7f9fa;border-left:5px solid var(--level)}.condition-result strong{display:block;color:var(--level);font-size:18px;margin-bottom:4px}.condition-result p{margin:0;color:var(--muted)}.subhead{font-weight:900;color:var(--level);margin:12px 0 4px}.call119{display:inline-flex;margin:4px 0 15px;padding:10px 15px;border-radius:12px;background:#d12626;color:#fff;text-decoration:none;font-weight:900}
'''
    text = text.replace("    .contacts{", extra_style + "    .contacts{", 1)

action_section = r'''  <section class="card"><h2>행동지침</h2><div class="source-row"><button class="choice active" data-source="auto">✓ 기상 자동값</button><button class="choice" data-source="field">현장 입력값</button></div><div class="job-row" style="margin-top:9px"><button class="choice active" data-job="yard">수송</button><button class="choice" data-job="platform">홈안내</button></div><div class="status-banner"><strong id="guideStatus">기상정보 확인 중</strong><div id="guideSummary">현재 단계에 맞는 행동지침을 준비하고 있습니다.</div></div><div class="key-list" id="keyList"></div><div id="homeSupport"></div><div class="health-info"><div class="section-label">건강·응급정보</div><details class="info-block"><summary>오늘 컨디션 확인</summary><p class="check-intro">오늘 해당하는 항목을 눌러보세요. 선택 결과는 저장되지 않습니다.</p><div class="check-list"><label class="condition-row"><input class="condition-check" type="checkbox" value="sleep">수면이 매우 부족함</label><label class="condition-row"><input class="condition-check" type="checkbox" value="illness">발열·설사·구토</label><label class="condition-row"><input class="condition-check" type="checkbox" value="heat">두통·어지럼·메스꺼움</label><label class="condition-row"><input class="condition-check" type="checkbox" value="fatigue">평소와 다른 과도한 피로</label></div><div class="condition-result" id="conditionResult"><strong>현재 선택한 증상이 없습니다</strong><p>근무 중 상태가 달라지면 다시 확인하세요.</p></div><p class="hint">이 확인은 의학적 진단이 아닙니다. 의식·말투·걸음이 평소와 다르거나 증상이 회복되지 않으면 119 또는 의료기관의 도움을 받으세요.</p></details><details class="info-block"><summary>동료의 이상징후 확인</summary><div class="subhead">작업을 멈추고 상태를 확인할 모습</div><ul><li>두통·어지럼·메스꺼움을 호소함</li><li>심하게 지치거나 힘이 빠짐</li><li>비틀거리거나 작업 동작이 평소보다 서툼</li><li>짜증·멍함·반응 저하 등 평소와 다름</li><li>근육경련이 생기거나 땀을 지나치게 많이 흘림</li></ul><div class="subhead">즉시 119에 신고할 위험징후</div><ul><li>말이 어눌하거나 횡설수설함</li><li>질문에 제대로 대답하지 못함</li><li>걷거나 서 있지 못함</li><li>의식저하·실신·경련이 나타남</li></ul></details><details class="info-block"><summary>온열질환 응급조치</summary><div class="subhead">의식이 있고 대화가 가능할 때</div><ol><li>즉시 작업을 중지시킵니다.</li><li>냉방장소나 그늘로 이동시킵니다.</li><li>안전모와 불필요한 겉옷을 벗기거나 느슨하게 합니다.</li><li>냉각팩이나 젖은 수건으로 몸을 식힙니다.</li><li>스스로 삼킬 수 있을 때만 시원한 물을 조금씩 마시게 합니다.</li><li>빠르게 회복하지 않으면 119에 신고합니다.</li></ol><div class="subhead">의식·말투·행동에 이상이 있을 때</div><ol><li>즉시 119에 신고합니다.</li><li>냉방장소나 그늘로 이동시킵니다.</li><li>옷을 느슨하게 하고 적극적으로 몸을 식힙니다.</li><li>구급대가 올 때까지 혼자 두지 않습니다.</li><li>물·이온음료·캔디를 먹이지 않습니다.</li></ol><a class="call119" href="tel:119">119 전화하기</a></details></div></section>'''

action_pattern = r'  <section class="card"><h2>행동지침</h2>.*?</section>\n(?=  <section class="card"><div class="section-label">순천관리역 비상연락망)'
text, action_count = re.subn(action_pattern, action_section + "\n", text, count=1, flags=re.S)
if action_count != 1:
    raise SystemExit("행동지침 화면 영역을 찾지 못했습니다.")

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

render_replacement = r'''function renderHomeSupport(){
  if(state.job!=='platform'){
    homeSupport.innerHTML='';
    return;
  }
  homeSupport.innerHTML=`<details class="info-block"><summary>폭염 시 취약고객 안내</summary><ul><li>고령자·어린이·임산부·거동이 불편한 고객이 장시간 더위에 노출되지 않도록 살핍니다.</li><li>어지럼·기력저하·비틀거림 등 이상징후가 보이면 그늘이나 냉방장소로 안내합니다.</li><li>혼자 이동하기 어려운 고객은 안전한 이동을 돕고 주변 직원에게 지원을 요청합니다.</li><li>의식·말투·걸음에 이상이 있거나 상태가 회복되지 않으면 119에 신고합니다.</li><li>고객 지원으로 직원의 옥외 노출이 길어지면 다른 직원에게 즉시 지원을 요청합니다.</li></ul></details>`;
}
function updateConditionCheck(){
  const selected=[...document.querySelectorAll('.condition-check:checked')].map(x=>x.value);
  let title='현재 선택한 증상이 없습니다';
  let body='근무 중 상태가 달라지면 다시 확인하세요.';
  let color='#26834a';
  if(selected.includes('heat')){
    title='지금은 작업을 멈추고 몸을 식히세요';
    body='냉방장소로 이동해 상태를 알리고, 증상이 빠르게 회복되지 않으면 119 또는 의료기관의 도움을 받으세요.';
    color='#d12626';
  }else if(selected.includes('illness')){
    title='옥외작업 전 관리자 확인이 필요합니다';
    body='탈수와 체온 상승 위험이 커질 수 있습니다. 시원한 곳에서 수분을 보충하고 증상이 계속되면 의료기관의 안내를 받으세요.';
    color='#d76500';
  }else if(selected.length>=2){
    title='업무 강도와 더위 노출을 줄이세요';
    body='동료나 관리자에게 현재 상태를 알리고 혼자 버티지 마세요. 증상이 심해지면 즉시 작업을 중지하세요.';
    color='#d76500';
  }else if(selected.includes('fatigue')){
    title='업무 강도와 더위 노출을 줄이세요';
    body='동료나 관리자에게 상태를 알리고, 피로가 심해지거나 두통·어지럼이 더해지면 즉시 작업을 중지하세요.';
    color='#9a6b00';
  }else if(selected.includes('sleep')){
    title='수면 상태를 알리고 무리하지 마세요';
    body='동료와 관리자에게 먼저 알리고, 업무 강도와 더위 노출을 줄일 수 있도록 휴식계획을 확인하세요.';
    color='#9a6b00';
  }
  conditionResult.style.setProperty('--level',color);
  conditionResult.innerHTML=`<strong>${title}</strong><p>${body}</p>`;
}
function renderGuide(){
  let value=state.source==='field'?state.fieldValue:state.autoValue;
  if(value===null){
    guideStatus.textContent=state.source==='field'?'현장값을 입력하세요':'기상정보 확인 중';
    guideSummary.textContent='값이 준비되면 단계별 행동지침이 표시됩니다.';
    keyList.innerHTML='';
    renderHomeSupport();
    return;
  }
  const lv=getLevel(value),g=guides[lv.key],items=g[state.job];
  setLevelColor(lv);
  guideStatus.textContent=`체감 ${value.toFixed(1)}℃ · ${lv.name}`;
  guideSummary.textContent=g.summary;
  keyList.innerHTML=items.map((x,i)=>`<div class="key"><span class="num">${i+1}</span><div><b>${x}</b></div></div>`).join('');
  renderHomeSupport();
}
document.querySelectorAll'''

render_pattern = r"function renderGuide\(\)\{.*?\}\ndocument\.querySelectorAll"
text, render_count = re.subn(render_pattern, render_replacement, text, count=1, flags=re.S)
if render_count != 1:
    raise SystemExit("renderGuide 함수를 찾지 못했습니다.")

events_replacement = r'''document.querySelectorAll('[data-shift]').forEach(b=>b.onclick=()=>{state.shift=b.dataset.shift;document.querySelectorAll('[data-shift]').forEach(x=>x.classList.toggle('active',x===b));renderForecast()});document.querySelectorAll('[data-source]').forEach(b=>b.onclick=()=>{state.source=b.dataset.source;document.querySelectorAll('[data-source]').forEach(x=>x.classList.toggle('active',x===b));renderGuide()});document.querySelectorAll('[data-job]').forEach(b=>b.onclick=()=>{state.job=b.dataset.job;document.querySelectorAll('[data-job]').forEach(x=>x.classList.toggle('active',x===b));renderGuide()});tempInput.oninput=rhInput.oninput=updateField;useField.onclick=()=>{state.source='field';document.querySelectorAll('[data-source]').forEach(x=>x.classList.toggle('active',x.dataset.source==='field'));renderGuide();document.querySelector('[data-source="field"]').scrollIntoView({behavior:'smooth',block:'center'})};document.querySelectorAll('.condition-check').forEach(x=>x.addEventListener('change',updateConditionCheck));updateConditionCheck();renderStations();loadWeather();'''

events_pattern = r"document\.querySelectorAll\('\[data-shift\]'\).*?renderStations\(\);loadWeather\(\);"
text, events_count = re.subn(events_pattern, events_replacement, text, count=1, flags=re.S)
if events_count != 1:
    raise SystemExit("이벤트 연결 코드를 찾지 못했습니다.")

path.write_text(text, encoding="utf-8")
print("index.html에 건강·응급정보와 취약고객 안내를 반영했습니다.")
