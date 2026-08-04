#!/usr/bin/env python3
"""분리된 화면 파일에 건강·응급정보와 홈안내 전용 안내를 반영한다."""

from pathlib import Path
import re

index_path = Path("index.html")
app_path = Path("app.js")
styles_path = Path("styles.css")

index = index_path.read_text(encoding="utf-8")
app = app_path.read_text(encoding="utf-8")
styles = styles_path.read_text(encoding="utf-8")

# 공통 안전정보는 오늘 컨디션, 동료 이상징후, 응급조치만 유지한다.
hydration_pattern = r'''\s*<details class="info-block">\s*<summary>수분 섭취·냉방휴식</summary>.*?</details>\s*'''
index = re.sub(hydration_pattern, "\n", index, count=1, flags=re.S)

# 홈안내를 선택했을 때만 취약고객 안내가 펼침형으로 나타나게 한다.
home_support_replacement = '''function renderHomeSupport() {
const target = $("#homeSupport");
if (state.job !== "platform") {
target.innerHTML = "";
return;
}
target.innerHTML = `<details class="info-block home-support-block">
<summary>폭염 시 취약고객 안내</summary>
<div class="details-content">
<ul>
<li>고령자·어린이·임산부·거동이 불편한 고객이 장시간 더위에 노출되지 않도록 살피기</li>
<li>어지럼·기력저하·비틀거림 등 이상징후가 보이면 그늘 또는 냉방장소로 안내</li>
<li>혼자 이동하기 어려운 고객의 안전한 이동을 돕고 주변 직원에게 지원 요청</li>
<li>의식·말투·걸음에 이상이 있거나 상태가 회복되지 않으면 119 신고</li>
<li>고객 지원으로 직원의 옥외 노출이 길어지지 않도록 다른 직원에게 즉시 지원 요청</li>
</ul>
</div>
</details>`;
}
function renderGuide'''

home_support_pattern = r'''function renderHomeSupport\(\) \{.*?\n\}\nfunction renderGuide'''
app, support_count = re.subn(
    home_support_pattern,
    home_support_replacement,
    app,
    count=1,
    flags=re.S,
)
if support_count != 1:
    raise SystemExit("app.js의 취약고객 안내 함수를 찾지 못했습니다.")

required_index_markers = (
    'id="conditionResult"',
    '<summary>오늘 컨디션 확인</summary>',
    '<summary>동료의 이상징후 확인</summary>',
    '<summary>온열질환 응급조치</summary>',
)
missing = [marker for marker in required_index_markers if marker not in index]
if missing:
    raise SystemExit("index.html 필수 건강정보 누락: " + ", ".join(missing))
if "수분 섭취·냉방휴식" in index:
    raise SystemExit("중복된 수분 섭취·냉방휴식 메뉴가 남아 있습니다.")
if '<summary>폭염 시 취약고객 안내</summary>' not in app:
    raise SystemExit("홈안내 전용 취약고객 안내가 반영되지 않았습니다.")

index_path.write_text(index, encoding="utf-8")
app_path.write_text(app, encoding="utf-8")
styles_path.write_text(styles, encoding="utf-8")
print("건강·응급정보 3개 메뉴와 홈안내 전용 취약고객 안내를 반영했습니다.")
