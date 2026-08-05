# KORAIL Safety Design System v1

이 저장소의 폭염·태풍·화재·침수·비상상황 화면은 동일한 토큰과 컴포넌트 규칙을 사용한다.

## 파일 구조

- `design-tokens.css`: 허용된 색상, 간격, 반경, 테두리, 그림자 토큰
- `design-system.css`: 카드·버튼·입력·상태카드·목록·배지의 공통 규칙
- `design-system.js`: 기상 단계처럼 동적으로 바뀌는 상태를 토큰과 연결

## 허용 색상군

새 기능은 아래 토큰만 사용한다.

- Brand: 일반 화면, 설정, 입력, 링크, 선택 상태
- Safe: 안전 또는 관심 미만·관심 상태
- Caution: 주의 상태
- Warning: 경고 상태
- Danger: 위험·응급 상태

각 상태는 반드시 `Surface → Border → Text → Solid → Accent` 순서로 사용한다.

## 컴포넌트 원칙

- 일반 카드는 흰색과 Brand 계열만 사용한다.
- 상태카드는 해당 상태의 Surface·Border·Text·Solid·Accent만 사용한다.
- 카드 그림자는 `--ds-shadow` 하나만 사용한다.
- 카드 반경은 `--ds-card-radius`, 컨트롤 반경은 `--ds-control-radius`를 사용한다.
- 상태는 색상만으로 표현하지 않고 단계명, 글자 크기, 굵기를 함께 사용한다.
- 새로운 HEX·RGB 색상값을 컴포넌트 파일에 직접 추가하지 않는다.

## 새 기능 추가 예시

태풍 위험카드를 추가할 때 임의의 파란색이나 빨간색을 만들지 않는다.

- 일반 태풍 정보: Brand 토큰
- 주의보 수준 안내: Caution 토큰
- 경보 수준 안내: Warning 토큰
- 즉시 대피·운행중지: Danger 토큰

색상을 바꿔야 할 때는 `design-tokens.css`만 수정한다.
