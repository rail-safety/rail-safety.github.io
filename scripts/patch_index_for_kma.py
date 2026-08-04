#!/usr/bin/env python3
"""행동지침과 건강·응급정보를 현장 확인용 개조식 문안으로 정리한다."""

from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(pattern: str, replacement: str, label: str) -> None:
    global text
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}을 찾지 못했습니다.")


action_section = r'''  <section class="card"><h2>행동지침</h2><div class="source-row"><button class="choice active" data-source="auto">✓ 기상 자동값</button><button class="choice" data-source="field">현장 입력값</button></div><div class="job-row" style="margin-top:9px"><button class="choice active" data-job="yard">수송</button><button class="choice" data-job="platform">홈안내</button></div><div class="status-banner"><strong id="guideStatus">기상정보 확인 중</strong><div id="guideSummary">현재 단계에 맞는 행동지침을 준비하고 있습니다.</div></div><div class="key-list" id="keyList"></div><div id="homeSupport"></div><div class="health-info"><div class="section-label">건강·응급정보</div><details class="info-block"><summary>오늘 컨디션 확인</summary><p class="check-intro">오늘 해당하는 항목을 눌러보세요. 선택 결과는 저장되지 않습니다.</p><div class="check-list"><label class="condition-row"><input class="condition-check" type="checkbox" value="sleep">수면이 매우 부족함</label><label class="condition-row"><input class="condition-check" type="checkbox" value="illness">발열·설사·구토</label><label class="condition-row"><input class="condition-check" type="checkbox" value="heat">두통·어지럼·메스꺼움</label><label class="condition-row"><input class="condition-check" type="checkbox" value="fatigue">평소와 다른 과도한 피로</label></div><div class="condition-result" id="conditionResult"><strong>선택한 증상 없음</strong><p>근무 중 상태 변화 시 다시 확인하세요.</p></div><p class="hint">이 확인은 의학적 진단이 아닙니다. 의식·말투·걸음이 평소와 다르거나 증상이 회복되지 않으면 119 또는 의료기관의 도움을 받으세요.</p></details><details class="info-block"><summary>동료의 이상징후 확인</summary><div class="subhead">작업 중지 및 상태 확인 필요</div><ul><li>두통·어지럼·메스꺼움 호소</li><li>심한 피로 또는 기력 저하</li><li>비틀거림 또는 평소보다 서툰 작업 동작</li><li>짜증·멍함·반응 저하 등 평소와 다른 모습</li><li>근육경련 또는 과도한 발한</li></ul><div class="subhead">즉시 119 신고 필요</div><ul><li>어눌한 말투 또는 횡설수설</li><li>질문에 부정확하거나 느린 반응</li><li>걷기·서 있기 어려움</li><li>의식저하·실신·경련</li></ul></details><details class="info-block"><summary>온열질환 응급조치</summary><div class="subhead">의식이 있고 대화가 가능한 경우</div><ol><li>즉시 작업 중지</li><li>냉방장소 또는 그늘로 이동</li><li>안전모·불필요한 겉옷 제거 또는 느슨하게 조정</li><li>냉각팩·젖은 수건을 이용한 신속한 냉각</li><li>스스로 삼킬 수 있는 경우에만 시원한 물 소량씩 제공</li><li>빠르게 회복하지 않으면 119 신고</li></ol><div class="subhead">의식·말투·행동에 이상이 있는 경우</div><ol><li>즉시 119 신고</li><li>냉방장소 또는 그늘로 이동</li><li>옷을 느슨하게 하고 적극적인 신체 냉각</li><li>구급대 도착 전까지 곁에서 상태 관찰</li><li>물·이온음료·캔디 제공 금지</li></ol><a class="call119" href="tel:119">119 전화하기</a></details></div></section>'''
replace_once(
    r'  <section class="card"><h2>행동지침</h2>.*?</section>\n(?=  <section class="card"><div class="section-label">순천관리역 비상연락망)',
    action_section + "\n",
    "행동지침 화면 영역",
)


guides_replacement = r'''const guides={
normal:{
summary:'기본 예방수칙을 지키며 업무를 수행하세요.',
yard:['쿨토시, 넥쿨러 등 온열질환 예방용품 준비','입환 시작 전 불필요한 옥외 대기시간 최소화','작업 종료 후 실내 또는 그늘로 이동'],
platform:['적절한 시간에 승강장으로 이동','안내 및 대기 중 그늘 이용','안내와 안내 사이 실내 복귀']
},
caution:{
summary:'옥외 체류시간을 줄이고 작업 사이에 몸을 식히세요.',
yard:['작업 동선·역할 사전 확인 및 옥외 체류시간 단축','작업 사이 대기 및 불필요한 이동 최소화','작업 사이 실내 또는 냉방장소에서 냉각·휴식'],
platform:['안내 및 대기 중 그늘 이용','안내 종료 후 실내 또는 냉방장소 복귀','장시간 연속 홈안내 시 교대 또는 냉방휴식 확보']
},
warning:{
summary:'작업 순서와 휴식계획을 확인하고 냉방휴식을 확보하세요.',
yard:['작업 전 작업 순서·휴식계획 관리자 확인','2인 이상 작업 및 상호 말투·걸음·반응 확인','작업 단위 단축 및 선로 주변 대기시간 최소화','작업 종료 후 즉시 냉방장소에서 냉각·휴식'],
platform:['안내 위치·대기 위치·실내 복귀 동선 사전 확인','안내 전 차양·그늘 대기 및 안내 종료 후 실내 복귀','연속 홈안내 예정 시 교대자·냉방휴식 시간 사전 지정','인턴사원 안내 구간·복귀 동선 확인 및 장시간 단독 옥외체류 방지']
},
danger:{
summary:'현재 시행하려는 업무가 즉시 필요한지, 연기 가능한지 관리자와 먼저 확인하세요.',
yard:['연기 가능한 업무 조정 및 반드시 필요한 업무만 시행','역할·동선 실내 사전 정리 및 옥외 체류시간 단축','2인 이상 상호 상태 확인 및 최소 인원·최단시간 작업','작업 종료 후 즉시 냉방장소 이동 및 충분한 냉각·휴식'],
platform:['안내 동선·대기 위치·실내 복귀 경로 사전 확인','안내 전 대기시간 및 안내 종료 후 홈 체류시간 최소화','연속 안내 예정 시 교대자·냉방휴식 시간 사전 지정','인턴사원 안내 동선·옥외 체류시간 확인 및 무리한 연속 안내 방지','어지럼·메스꺼움·반응 저하 발생 시 즉시 교대']
},
extreme:{
summary:'업무가 긴급하거나 반드시 필요한지 관리자와 확인하세요. 연기 가능한 업무는 시행하지 않습니다.',
yard:['반드시 필요한 업무만 최소 인원·최단시간 수행','2인 이상 상호 상태 지속 확인 및 단독 행동 금지','보냉장구·연락수단 준비 및 옥외 대기시간 제거','말투·걸음·반응 이상 시 즉시 작업 중지','작업 종료 후 즉시 냉방장소 이동'],
platform:['이동·대기·복귀 동선 사전 확인 및 옥외 체류시간 최소화','연속 홈안내 방지를 위한 교대자·업무 조정','인턴사원 단독 장시간 안내 방지 및 담당 직원 상태 확인','평소와 다른 몸 상태 발생 시 즉시 교대','의식·말투·걸음 이상 시 즉시 냉방장소 이동 및 응급조치']
}};
function heatIndex'''
replace_once(
    r"const guides=\{.*?\};\nfunction heatIndex",
    guides_replacement,
    "행동지침 데이터",
)


support_condition_replacement = r'''function renderHomeSupport(){
  if(state.job!=='platform'){
    homeSupport.innerHTML='';
    return;
  }
  homeSupport.innerHTML=`<details class="info-block"><summary>폭염 시 취약고객 안내</summary><ul><li>고령자·어린이·임산부·거동 불편 고객의 장시간 더위 노출 여부 확인</li><li>어지럼·기력저하·비틀거림 등 이상징후 발견 시 그늘 또는 냉방장소 안내</li><li>단독 이동이 어려운 고객의 안전한 이동 지원 및 주변 직원 지원 요청</li><li>의식·말투·걸음 이상 또는 상태 미회복 시 119 신고</li><li>고객 지원으로 직원 옥외 노출이 길어질 경우 즉시 지원 인력 요청</li></ul></details>`;
}
function updateConditionCheck(){
  const selected=[...document.querySelectorAll('.condition-check:checked')].map(x=>x.value);
  let title='선택한 증상 없음';
  let body='근무 중 상태 변화 시 다시 확인하세요.';
  let color='#26834a';
  if(selected.includes('heat')){
    title='지금은 작업을 멈추고 몸을 식히세요.';
    body='냉방장소 이동·상태 공유 후 빠르게 회복하지 않으면 119 또는 의료기관 도움 요청';
    color='#d12626';
  }else if(selected.includes('illness')){
    title='옥외작업 전 관리자 확인이 필요합니다.';
    body='탈수 위험 확인·시원한 장소에서 수분 보충·증상 지속 시 의료기관 안내 확인';
    color='#d76500';
  }else if(selected.length>=2){
    title='업무 강도와 더위 노출을 줄이세요.';
    body='현재 상태 공유·혼자 버티지 않기·증상 악화 시 즉시 작업 중지';
    color='#d76500';
  }else if(selected.includes('fatigue')){
    title='업무 강도와 더위 노출을 줄이세요.';
    body='동료·관리자에게 상태 공유 및 피로 악화·두통·어지럼 발생 시 즉시 작업 중지';
    color='#9a6b00';
  }else if(selected.includes('sleep')){
    title='수면 상태를 알리고 무리하지 마세요.';
    body='동료·관리자에게 상태 공유 및 업무 강도·더위 노출·휴식계획 확인';
    color='#9a6b00';
  }
  conditionResult.style.setProperty('--level',color);
  conditionResult.innerHTML=`<strong>${title}</strong><p>${body}</p>`;
}
function renderGuide(){'''
replace_once(
    r"function renderHomeSupport\(\)\{.*?\nfunction renderGuide\(\)\{",
    support_condition_replacement,
    "취약고객·컨디션 확인 함수",
)

path.write_text(text, encoding="utf-8")
print("행동지침과 건강·응급정보를 개조식 최종 문안으로 반영했습니다.")
