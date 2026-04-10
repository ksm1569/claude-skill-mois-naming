---
name: mois-naming
description: |
  행정안전부(MOIS) 공공데이터 공통표준 명명 규칙에 따라 DB 컬럼, 테이블, Java 클래스, 패키지, JSP/HTML 파일명, REST URL 등의 식별자를 생성·검증하고, 감리 대응 테이블정의서를 자동생성하는 통합 스킬.
  한국 공공 SI 프로젝트, eGovFrame 기반 개발, 감리사업 등에서 행안부 표준용어/약어를 적용해야 할 때 사용한다.
  다음 상황에서 반드시 이 스킬을 사용할 것:
  - 한글 명칭을 행안부 표준 영문약어로 변환할 때
  - DB 컬럼명, 테이블명을 표준에 맞게 작성할 때
  - Java 클래스/메서드/변수명을 표준 약어 기반으로 명명할 때
  - REST API 엔드포인트를 표준에 맞게 설계할 때
  - SI 프로젝트 감리 시 명명 표준 준수 여부를 검증할 때
  - 테이블정의서를 표준 기반으로 생성할 때
  - 기존 DB/코드의 표준 위반을 검증하고 위반리포트를 생성할 때
  - 감리 산출물(매핑표, 비표준 등록대장)을 생성할 때
  - "행안부 표준", "공통표준용어", "공통표준단어", "약어 변환", "컬럼명 변환", "표준 명명", "테이블정의서", "감리", "표준 검증" 등의 키워드가 나올 때
  - eGovFrame, 공공SI, 전자정부 프레임워크 관련 명명 작업일 때
---

# 행안부 공통표준 명명 스킬

## 개요

행정안전부 공공데이터 공통표준을 기반으로 모든 종류의 식별자를 표준에 맞게 생성·검증한다.

## ⚡ 확장 구조

이 스킬은 **행안부 표준 갱신, 프로젝트별 자체 약어 추가, 복수 사전 병합**을 전제로 설계되었다.

```
mois-naming/
├── SKILL.md
├── scripts/
│   └── search.py          ← references/*.csv를 모두 자동 탐지·병합 검색 + parse_domain() 도메인 파싱
└── references/
    ├── standard_terms.csv  ← 행안부 공통표준용어 (합성어, 도메인 정보 포함)
    ├── standard_words.csv  ← 행안부 공통표준단어 (원자 단위 약어, 합성어 조립 기반)
    ├── custom_terms.csv    ← 프로젝트 자체 약어 (비표준 용어 등록)
    └── guide.md            ← 상세 규칙 가이드
```

### CSV 교체/갱신 방법

행안부에서 새 표준이 나오면:
1. `references/standard_terms.csv`를 새 파일로 **덮어쓰기**
2. 끝. search.py가 자동으로 새 데이터를 읽는다.

파일명이 달라도 상관없다 — search.py는 `references/*.csv` **전체**를 자동 탐지한다.

### 프로젝트 자체 약어 추가

`references/custom_terms.csv`를 아래 형식으로 만든다:

```csv
용어명,영문약어명,도메인명,설명,출처
돌봄,CARE,,아동돌봄 서비스,자체생성
학부모,PRNT,,학생의 보호자,자체생성(parent 자음압축)
카테고리,CTGRY,,분류 카테고리,자체생성(CATEGORY 자음압축)
```

search.py는 이 파일도 자동으로 함께 검색한다. 행안부 표준과 자체 약어가 동시에 결과에 나오며, 출처 컬럼으로 구분된다.

### 외부 CSV 직접 지정

```bash
python scripts/search.py "키워드" --csv /path/to/other.csv
python scripts/search.py "키워드" --no-default --csv /only/this.csv
```

---

## 워크플로

### Step 1: 표준용어 검색

한글 명칭이 주어지면 **먼저 CSV를 검색**하여 표준 약어가 있는지 확인한다.

```bash
python SKILL_DIR/scripts/search.py "회원"
python SKILL_DIR/scripts/search.py "게시물" --top 5
python SKILL_DIR/scripts/search.py "카테고리" --exact
```

> `SKILL_DIR`은 이 SKILL.md가 있는 디렉터리 경로로 대체.

search.py 옵션:
- `--top N`: 최대 결과 수 (기본 10)
- `--exact`: 정확히 일치하는 용어만
- `--csv PATH`: 추가 CSV 경로 (복수 가능)
- `--no-default`: references/ 폴더 CSV 제외

### Step 2: 약어 조립 규칙

검색 결과가 있으면 그대로 사용. 없으면 아래 규칙으로 생성:

| 패턴 | 예시 |
|---|---|
| 영문 모음 제거 | NAME→`NM`, NUMBER→`NO`, AMOUNT→`AMT`, COUNT→`CNT` |
| 어근 보존+모음 제거 | MANAGER→`MNGR`, MEMBER→`MBR`, REGISTER→`REG` |
| 한국어→의미영문→압축 | 회원가입→MEMBER+JOIN→`MBR_JOIN` |
| 합성어는 `_`로 결합 | `MBR_JOIN_YMD` (회원가입일자) |
| 영어가 자연스러우면 영어 우선 | 카드→`CARD`, 홈→`HOME` |
| 3~5자 권장 | |

### Step 3: 식별자 유형별 변환

| 유형 | 표기법 | 예시 |
|---|---|---|
| DB 컬럼 | UPPER_SNAKE_CASE | `MBR_JOIN_YMD` |
| DB 테이블 | `TB_` + UPPER_SNAKE | `TB_MBR` |
| Java 클래스 | UpperCamelCase | `MbrMngService` |
| Java 패키지 | lowercase | `egovframework.proj.mbr` |
| 메서드/변수 | lowerCamelCase | `selectMbrList()` |
| JSP/HTML | lowerCamelCase / kebab | `mbrList.jsp` |
| REST 엔드포인트 | kebab-case | `/api/mbr-list` |

### Step 4: 검증

- 동일 의미에 두 약어가 쓰이지 않는지
- 약어 길이 2~8자 범위
- 같은 스코프 내 이름 충돌 시 상위 컨텍스트 prefix 추가
- 자체 생성 약어는 반드시 출처 명시

---

## 생성 워크플로 (한글 → 표준 식별자 전체 흐름)

한글 명칭을 입력받아 표준 식별자를 생성하는 전체 파이프라인:

1. **의미 토큰 분리**: 한글 명칭을 의미 단위로 분리
   - 예) "회원가입신청일자" → 회원가입 / 신청 / 일자
2. **표준단어 CSV 검색**: 각 토큰을 `standard_words.csv`에서 원자 약어 검색
   - `python SKILL_DIR/scripts/search.py "회원" --exact`
   - 없으면 `standard_terms.csv`에서 합성어 검색
3. **약어 조립**: 검색된 원자 약어를 `_`로 결합
   - 회원→MBR, 가입→JOIN, 신청→APLY, 일자→YMD → `MBR_JOIN_APLY_YMD`
4. **도메인 매핑**: `standard_terms.csv`의 `공통표준도메인명`에서 데이터타입 파싱
   - search.py의 `parse_domain()` 활용: `연월일C8` → CHAR(8), `명V100` → VARCHAR(100)
5. **식별자 유형 변환**: Step 3의 표기법에 따라 최종 변환
6. **비표준 처리**: 표준에 없으면 §약어 조립 규칙으로 생성 후 `custom_terms.csv`에 등록

---

## 검증 워크플로 (기존코드 → 표준대조 → 위반리포트)

기존 DB/Java 코드의 식별자를 표준과 대조하여 위반 항목을 리포트하는 절차:

1. **식별자 추출**: DDL, 테이블정의서, Java 코드에서 컬럼명/클래스명/변수명 수집
2. **표준 대조**: 각 식별자를 search.py로 표준용어/단어 CSV와 대조
3. **분류**: 표준 일치 / 비표준(custom_terms 등록) / 미등록 비표준으로 분류
4. **위반리포트 생성**: 아래 고정 템플릿으로 출력

### 위반리포트 고정 템플릿

```markdown
## 표준 준수 검증 결과

| # | 현재 식별자 | 표준 약어 | 상태 | 수정 제안 | 근거 |
|---|---|---|---|---|---|
| 1 | USER_NAME | USER_NM | 비표준 | USER_NM으로 변경 | 표준단어: 명→NM |
| 2 | REG_DATE | REG_YMD | 비표준 | REG_YMD로 변경 | 표준단어: 일자→YMD |
| 3 | MBR_NO | MBR_NO | 표준 | - | 표준용어 일치 |

### 요약
- 전체 컬럼: N개
- 표준 준수: N개 (xx%)
- 비표준 (custom_terms 등록): N개 (xx%)
- 미등록 비표준: N개 (xx%) ← 수정 또는 등록 필요
```

---

## 테이블정의서 생성 워크플로

한글 엔티티 설계를 입력받아 감리 대응 가능한 표준 테이블정의서를 생성하는 절차:

1. **엔티티 정보 수집**: 테이블명(한글), 컬럼 목록(한글명, 용도, PK/NN 여부)
2. **표준 변환**: 각 컬럼에 대해 생성 워크플로 실행 (약어 조립 + 도메인 매핑)
3. **고정 템플릿으로 출력**:

### 테이블정의서 고정 템플릿

```markdown
## 테이블정의서

### TB_MBR (회원)

| # | 컬럼명(한글) | 컬럼명(영문) | 도메인 | 데이터타입 | 길이 | PK | NN | 기본값 | 설명 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 회원번호 | MBR_NO | 번호V20 | VARCHAR | 20 | Y | Y | | 회원 식별 번호 |
| 2 | 회원명 | MBR_NM | 명V100 | VARCHAR | 100 | | Y | | 회원 이름 |
| 3 | 회원가입일자 | MBR_JOIN_YMD | 연월일C8 | CHAR | 8 | | Y | | YYYYMMDD |
| 4 | 삭제여부 | DEL_YN | 여부C1 | CHAR | 1 | | Y | 'N' | Y/N |

> - 도메인: `공통표준도메인명` 원본 값 (예: 명V100)
> - 데이터타입/길이: parse_domain()으로 파싱한 결과 (예: VARCHAR / 100)
> - 비표준 컬럼은 도메인 컬럼에 "(비표준)" 표기 후 custom_terms.csv 등록
```

---

## 감리 산출물 생성 가이드

감리 대응에 필요한 3종 산출물과 생성 방법:

| # | 산출물 | 생성 방법 | 참조 |
|---|---|---|---|
| 1 | **테이블정의서** | 테이블정의서 생성 워크플로 사용 | 위 고정 템플릿 |
| 2 | **표준 준수 검증 결과** | 검증 워크플로 사용 | 위 위반리포트 템플릿 |
| 3 | **비표준 약어 등록대장** | `custom_terms.csv` 내용을 아래 형식으로 출력 | references/custom_terms.csv |

### 비표준 약어 등록대장 템플릿

```markdown
## 비표준 약어 등록대장

| # | 한글 용어 | 영문 약어 | 생성 근거 | 비고 |
|---|---|---|---|---|
| 1 | 돌봄 | CARE | 자체생성(영어 우선) | 표준 미존재 |
| 2 | 학부모 | PRNT | 자체생성(parent 자음압축) | 표준 미존재 |
```

---

## 핵심 접미사 (Top 25)

| 접미사 | 의미 | 접미사 | 의미 |
|---|---|---|---|
| `NM` | 명/이름 | `YMD` | 일자 (8자리) |
| `YN` | 여부 (Y/N) | `CN` | 내용 |
| `DT` | 일시 | `AMT` | 금액 |
| `NO` | 번호 | `TM` | 시각 |
| `CNT` | 건수 | `RSN` | 사유 |
| `ADDR` | 주소 | `YR` | 연도 |
| `SN` | 일련번호 | `TELNO` | 전화번호 |
| `EXPLN` | 설명 | `YM` | 년월 |
| `SCR` | 점수 | `HR` | 시간(hour) |
| `RT` | 율/비율 | `SEQ` | 순번 |
| `QTY` | 수량 | `CD` | 코드 |
| `SE` | 구분 | `STTS` | 상태 |

## 고빈도 어근 약어 (빠른참조)

<details><summary>사람·조직</summary>

| 한글 | 약어 | 한글 | 약어 |
|---|---|---|---|
| 회원 | MBR | 사용자 | USER |
| 관리자 | MNGR | 담당자 | PIC |
| 신청자 | APLCNT | 학생 | STDNT |
| 학교 | SCHL | 기관 | INST |
| 부서 | DEPT | 업체 | BZENTY |
</details>

<details><summary>게시판·콘텐츠</summary>

| 한글 | 약어 | 한글 | 약어 |
|---|---|---|---|
| 게시판 | BBS | 게시물 | PST |
| 공지사항 | NTC | 댓글 | CMNT |
| 첨부 | ATCH | 파일 | FILE |
| 분류 | CLSF | 답변 | ANS |
</details>

<details><summary>행위·상태</summary>

| 한글 | 약어 | 한글 | 약어 |
|---|---|---|---|
| 등록 | REG | 수정 | MDFCN |
| 삭제 | DEL | 승인 | APRV |
| 반려 | RJCT | 신청 | APLY |
| 예약 | RSVT | 대기 | WTNG |
</details>

<details><summary>시간·운영·권한</summary>

| 한글 | 약어 | 한글 | 약어 |
|---|---|---|---|
| 일자 | YMD | 일시 | DT |
| 기간 | PRD | 일정 | SCHDL |
| 권한 | AUTHRT | 설정 | STNG |
| 로그인 | LGN | 접근 | ACS |
</details>

더 많은 약어: `references/guide.md` §4 참조.

---

## 출력 형식

변환 결과는 항상 매핑 표로 제공:

```
| 한글 명칭 | 표준 약어 | 출처 | DB컬럼 | Java변수 | 비고 |
|---|---|---|---|---|---|
| 회원가입일자 | MBR_JOIN_YMD | 표준용어 | MBR_JOIN_YMD | mbrJoinYmd | |
| 돌봄여부 | CARE_YN | 자체생성 | CARE_YN | careYn | 표준 미존재 |
```

- **출처**: "표준용어" / "표준단어" / "자체생성" 중 명시
- 자체생성 시 custom_terms.csv에 등록 권장

## 감리 검증 체크리스트

1. 컬럼/테이블이 행안부 표준과 매칭되는가
2. 동일 의미에 두 약어 혼용 없는가
3. 자체 생성 약어가 custom_terms.csv에 등록되어 있는가
4. 도메인(데이터타입)이 표준에 맞는가
5. 약어 길이 2~8자 범위인가

## 참조 파일

| 파일 | 용도 | 언제 읽는가 |
|---|---|---|
| `references/standard_terms.csv` | 행안부 표준용어 (합성어 + 도메인 정보) | 완성형 용어 검색 + 도메인 매핑 |
| `references/standard_words.csv` | 행안부 표준단어 (원자 약어) | 새 합성어 조립 시 원자 약어 검색 |
| `references/custom_terms.csv` | 프로젝트 자체 약어 (비표준) | 비표준 약어 조회 + 감리 산출물 |
| `references/guide.md` | 상세 가이드 전문 §1~§10 | 복잡한 규칙 확인 시 |
