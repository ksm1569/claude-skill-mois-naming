# mois-naming

> **행정안전부(MOIS) 공공데이터 공통표준 명명 규칙**을 자동으로 적용·검증하는 Claude Skill

한국 공공 SI 프로젝트, eGovFrame 기반 개발, 감리사업에서 **DB 컬럼·테이블, Java 클래스·패키지, JSP/HTML 파일명, REST API 엔드포인트** 등 모든 식별자를 행안부 표준에 맞게 생성·검증할 수 있도록 도와줍니다.

---

## 🎯 목적

공공·SI 프로젝트는 행정안전부가 배포하는 **공통표준단어/공통표준용어/공통표준도메인**을 따라야 합니다. 그러나 표준 사전은 13,000건이 넘고 정기적으로 갱신되며, 사람이 매번 수동으로 검색·변환하기 어렵습니다.

이 스킬은 Claude(Claude Code · Claude Desktop 등)에게 행안부 표준 명명 규칙을 학습시켜, 한글 명칭을 입력하면 **자동으로 표준 약어를 검색하고 식별자 유형별로 변환**해 주는 도구입니다.

### 이런 상황에 사용하세요

- 한글 명칭을 행안부 표준 영문약어로 변환할 때
- DB 컬럼명·테이블명을 표준에 맞게 작성할 때
- Java 클래스/메서드/변수명을 표준 약어 기반으로 명명할 때
- REST API 엔드포인트를 표준에 맞게 설계할 때
- SI 프로젝트 감리 시 명명 표준 준수 여부를 검증할 때

---

## 📦 구성

```
mois-naming/
├── SKILL.md                    # Claude가 읽는 스킬 정의서
├── scripts/
│   └── search.py               # references/*.csv 자동 탐지·병합 검색
└── references/
    ├── standard_terms.csv      # 행안부 공통표준용어 (교체 가능)
    ├── custom_terms.csv        # 프로젝트 자체 약어 (선택, 직접 추가)
    └── guide.md                # 상세 규칙 가이드 §1~§10
```

---

## 🚀 설치 및 사용

### 1. Claude Code에 스킬로 등록

이 저장소를 Claude Code 스킬 디렉터리에 두면 자동 인식됩니다.

```bash
git clone https://github.com/ksm1569/claude-skill-mois-naming.git ~/.claude/skills/mois-naming
```

이후 Claude Code에서 "회원가입일자를 행안부 표준으로 바꿔줘" 같은 요청을 하면 스킬이 자동으로 활성화됩니다.

### 2. CLI로 직접 검색

```bash
python scripts/search.py "회원"
python scripts/search.py "게시물" --top 5
python scripts/search.py "카테고리" --exact
```

옵션:
- `--top N` : 최대 결과 수 (기본 10)
- `--exact` : 정확히 일치하는 용어만
- `--csv PATH` : 추가 CSV 경로 (복수 가능)
- `--no-default` : `references/` 폴더 CSV 제외

---

## 🔁 표준 갱신 / 확장

### 행안부 표준이 갱신되면

`references/standard_terms.csv`를 새 파일로 **덮어쓰기**만 하면 됩니다.
`search.py`는 `references/*.csv` 전체를 자동 탐지하므로 파일명이 달라도 동작합니다.

> 원본 다운로드: [공공데이터포털 — 공통표준용어](https://www.data.go.kr/data/15156379/fileData.do)

### 프로젝트 자체 약어 추가

표준에 없는 도메인 용어는 `references/custom_terms.csv`에 추가하세요:

```csv
용어명,영문약어명,도메인명,설명,출처
돌봄,CARE,,아동돌봄 서비스,자체생성
학부모,PRNT,,학생의 보호자,자체생성(parent 자음압축)
```

검색 결과에 `출처` 컬럼으로 행안부 표준과 자체 약어가 구분되어 출력됩니다.

---

## 📋 변환 예시

| 한글 명칭 | 표준 약어 | DB컬럼 | Java변수 | REST URL |
|---|---|---|---|---|
| 회원 | MBR | `TB_MBR` | `mbr` | `/api/mbr` |
| 회원가입일자 | MBR_JOIN_YMD | `MBR_JOIN_YMD` | `mbrJoinYmd` | — |
| 게시물 목록 | PST_LIST | — | `pstList` | `/api/pst-list` |
| 돌봄여부 | CARE_YN | `CARE_YN` | `careYn` | — |

---

## 🧩 식별자 유형별 표기 규칙

| 유형 | 표기법 | 예시 |
|---|---|---|
| DB 컬럼 | `UPPER_SNAKE_CASE` | `MBR_JOIN_YMD` |
| DB 테이블 | `TB_` + `UPPER_SNAKE` | `TB_MBR` |
| Java 클래스 | `UpperCamelCase` | `MbrMngService` |
| Java 패키지 | `lowercase` | `egovframework.proj.mbr` |
| 메서드/변수 | `lowerCamelCase` | `selectMbrList()` |
| JSP/HTML | `lowerCamelCase` | `mbrList.jsp` |
| REST 엔드포인트 | `kebab-case` | `/api/mbr-list` |

---

## ✅ 감리 검증 체크리스트

1. 컬럼/테이블이 행안부 표준과 매칭되는가
2. 동일 의미에 두 약어가 혼용되지 않는가
3. 자체 생성 약어가 `custom_terms.csv`에 등록되어 있는가
4. 도메인(데이터타입)이 표준에 맞는가
5. 약어 길이가 2~8자 범위인가

---

## 📚 참고 자료

| 자료 | 데이터셋 ID | 다운로드 |
|---|---|---|
| 공통표준단어 | 15156439 | https://www.data.go.kr/data/15156439/fileData.do |
| 공통표준용어 | 15156379 | https://www.data.go.kr/data/15156379/fileData.do |
| 공통표준도메인 | 15156442 | https://www.data.go.kr/data/15156442/fileData.do |

상세 규칙은 [`references/guide.md`](references/guide.md) 참조.

---

## 📄 라이선스

MIT License

행안부 공공데이터(공통표준단어/용어/도메인)는 [공공누리 제1유형](https://www.kogl.or.kr/info/license.do#01-tab) 출처표시 조건으로 자유롭게 이용 가능합니다.
