# Cron Capital Dashboard

실시간 포트폴리오 대시보드 — **Unlimited Buying** + **Turtle Trading** 두 전략의 계좌 현황을 한눈에 모니터링합니다.

> GitHub Pages + Chart.js 정적 페이지. cron-capital.engine에서 GitHub Actions cron으로 데이터가推送됩니다.

---

## Features

### 탭 기반 뷰
| Tab | 내용 |
|-----|------|
| **📊 Total** | 전체 자산/예수금/시드 요약 + 모든 계좌 통합 주식 카드 + 전체 히스토리 차트 |
| **💰 Unlimited** | 무한매수 계좌 요약 + 해당 계좌 주식 카드 + Unlimited 히스토리 차트 |
| **🐢 Turtle** | 터틀트레이딩 계좌 요약 + 해당 계좌 주식 카드 + Turtle 히스토리 차트 |

### 대시보드 구성
- **Header**: Cron Capital 타이틀, 마지막 업데이트 시간, 환율 정보
- **Summary**: Total Assets / Available Cash / Seed (3개 항목)
- **차트**: 일별(1일 1포인트) 히스토리 라인 차트 (Total Assets + Stock Value + Seed 기준선)
- **Stock Cards**: 계좌별 💰/🐢 라벨이 붙은 주식 카드 (Quantity, Avg Price, Current Price, 수익률)

### 반응형
- 데스크탑: 3열 그리드
- 모바일 (768px 이하): 1열 그리드

---

## Seed.json 사용법

`seed.json`은 각 계좌에 입금한 시드 머니를 날짜별로 기록하는 파일입니다.

```json
{
    "unlimited": [
        { "date": "2026-01-15", "amount": 10000 }
    ],
    "turtle": [
        { "date": "2026-02-01", "amount": 5000 }
    ]
}
```

- 새로 입금할 때마다 `{ "date": "YYYY-MM-DD", "amount": 금액 }` 항목을 배열에 추가하세요.
- 금액은 USD 기준입니다.
- 차트에서 Seed 라인이 각 입금 시점마다 계단식으로 증가하여 표시됩니다.
- Summary에도 현재까지 누적 시드가 표시됩니다.

### 예시: 2026년 5월 20일에 $2,000 추가 입금

```json
{
    "unlimited": [
        { "date": "2026-01-15", "amount": 10000 },
        { "date": "2026-05-20", "amount": 2000 }
    ]
}
```

---

## 데이터 구조

### portfolio.json

`cron-capital.engine`에서 GitHub Actions을 통해 전달받은 병합 포트폴리오 데이터입니다.

```json
{
    "stocks": {
        "TQQQ": { "symbol": "TQQQ", "excg": "NASD", "qty": 4, "avg_price": 54.46, "now_price": 58.00, "account": "unlimited" }
    },
    "total_value": 1234.56,
    "exchange_rate": 1469.7,
    "accounts": {
        "unlimited": { "total_value": 800.00, "stock_value": 400.00 },
        "turtle": { "total_value": 434.56, "stock_value": 200.00 }
    },
    "history": [
        { "date": "2026-05-16", "total_value": 1200.00, "stock_value": 600.00, "accounts": { "unlimited": {...}, "turtle": {...} } }
    ]
}
```

### seed.json

사용자가 직접 관리하는 시드 기록 파일입니다. (위 Seed.json 사용법 참고)

---

## 로컬 개발

정적 HTML 파일이므로 별도 빌드 도구 없이 바로 실행됩니다.

```bash
# 로컬에서 확인
open index.html

# 또는 Python HTTP 서버
python3 -m http.server 8000
```

---

## 배포

GitHub Pages로 자동 배포됩니다. `main` 브랜치에 푸시하면 즉시 반영됩니다.

1. `index.html` 수정
2. 커밋 & 푸시
3. GitHub Actions이 Pages를 다시 빌드 (보통 1~2분 소요)

---

## Tech Stack

- [Chart.js](https://www.chartjs.org/) — CDN via jsdelivr
- GitHub Pages — 정적 호스팅
- GitHub Actions (cron-capital.engine) — 데이터 파이프라인
