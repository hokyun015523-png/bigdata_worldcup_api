# 2026 FIFA 월드컵 데이터 API

**사용 데이터셋:** 2026 FIFA 월드컵(북중미) 선수·경기·팀 기록(players/matches/teams, 총 3개 테이블).
**선정 사유:** 팀에서 직접 전처리(인코딩 정리, 한국어 변환, KST 시간대 변환)까지 마친 정제 데이터가 있어 그대로 활용.

PostgreSQL에 저장된 데이터를 FastAPI로 조회·수정하는 실습 프로젝트입니다. (Todo/User 실습 때 배운 구조를 그대로 재사용했습니다)

---

## 1. 프로젝트 구조

```
worldcup-api/
├── main.py                # FastAPI 앱 진입점
├── database/
│   ├── db_connection.py    # DB 엔진 + SessionFactory
│   └── orm.py               # Base 클래스
├── models.py                # SQLAlchemy ORM 모델 (Player/Match/Team)
├── schema/
│   ├── request.py           # 요청 Pydantic 모델
│   └── response.py          # 응답 Pydantic 모델
├── auth/
│   └── jwt.py                # JWT 발급/검증 (PyJWT)
├── routers/
│   ├── users.py              # 로그인
│   ├── players.py            # 선수 CRUD
│   ├── matches.py            # 경기 조회
│   ├── teams.py               # 팀 조회
│   └── stats.py                # pandas 통계
├── data/                       # players.csv, matches.csv, teams.csv
├── schema.sql                  # 테이블 정의 (한국어 컬럼 코멘트 포함, 전체 컬럼 버전)
├── setup_database.py           # schema.sql 실행 + CSV 적재
└── .env                        # 환경설정 값
```

## 2. 서버 실행
```bash
uvicorn main:app --reload
```
브라우저에서 http://127.0.0.1:8000/docs 접속 → Swagger UI에서 바로 테스트 가능.

쓰기(POST/PUT/DELETE) API는 로그인이 필요합니다. `/docs` 우측 상단 **Authorize** 버튼 클릭 →
`username: admin`, `password: admin1234` (`.env`에서 변경 가능)로 로그인하면 이후 요청에 토큰이 자동으로 붙습니다.

---

## 3. 엔드포인트

| Method | URL | 설명 | 로그인 |
|---|---|---|---|
| POST | `/users/login` | 로그인, JWT 토큰 발급 | - |
| GET | `/players` | 선수 목록 (team/position/search 필터, 정렬, 페이지네이션) | - |
| GET | `/players/{id}` | 선수 상세 | - |
| POST | `/players` | 선수 추가 | ✅ |
| PUT | `/players/{id}` | 선수 정보 수정 (일부 필드만 전송 가능) | ✅ |
| DELETE | `/players/{id}` | 선수 삭제 | ✅ |
| GET | `/matches` | 경기 목록 (team/round 필터) | - |
| GET | `/matches/{id}` | 경기 상세 | - |
| GET | `/teams` | 팀 목록 (이름 검색) | - |
| GET | `/teams/{id}` | 팀 상세 | - |
| GET | `/stats/top-scorers` | pandas로 계산한 90분당 득점 상위 선수 | - |
| GET | `/stats/team-goal-diff` | pandas로 집계한 팀별 득실차/승점 순위표 | - |

## 4. 시도해본 것들

- 필터링/검색/정렬/페이지네이션 (`/players`, `/matches`)
- pandas로 SQL 결과 후처리 통계 API (`/stats/*`)
- JWT 로그인 붙여서 쓰기 API 보호 (PyJWT, jwt_create.py/jwt_checked.py 실습 확장)
- 컬럼이 250개 넘는 테이블 중 핵심 컬럼만 ORM으로 매핑하고, 나머지는 pandas로 직접 접근
- 컬럼 화이트리스트로 `sort_by` SQL 인젝션 방지
- PUT에서 일부 필드만 보내도 되도록 Optional 처리 (`exclude_unset=True`)

## 5. 팀원별 작업 내용

| 팀원 | 담당 |
|---|---|
| OOO |
| OOO | 
| OOO |
