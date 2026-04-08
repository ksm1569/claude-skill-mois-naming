---
name: mois-naming
description: |
  행정안전부(MOIS) 공공데이터 공통표준 명명 규칙에 따라 DB 컬럼, 테이블, Java 클래스, 패키지, JSP/HTML 파일명, REST URL 등의 식별자를 생성·검증하는 스킬.
  한국 공공 SI 프로젝트, eGovFrame 기반 개발, 감리사업 등에서 행안부 표준용어/약어를 적용해야 할 때 사용한다.
  다음 상황에서 반드시 이 스킬을 사용할 것:
  - 한글 명칭을 행안부 표준 영문약어로 변환할 때
  - DB 컬럼명, 테이블명을 표준에 맞게 작성할 때
  - Java 클래스/메서드/변수명을 표준 약어 기반으로 명명할 때
  - REST API 엔드포인트를 표준에 맞게 설계할 때
  - SI 프로젝트 감리 시 명명 표준 준수 여부를 검증할 때
  - "행안부 표준", "공통표준용어", "공통표준단어", "약어 변환", "컬럼명 변환", "표준 명명" 등의 키워드가 나올 때
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
│   └── search.py          ← references/*.csv를 모두 자동 탐지·병합 검색
└── references/
    ├── standard_terms.csv  ← 행안부 공통표준용어 (교체 가능)
    ├── custom_terms.csv    ← 프로젝트 자체 약어 (선택, 직접 추가)
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
| `references/standard_terms.csv` | 행안부 표준용어 원본 (교체 가능) | search.py로 검색 |
| `references/custom_terms.csv` | 프로젝트 자체 약어 (직접 생성) | search.py가 자동 포함 |
| `references/guide.md` | 상세 가이드 전문 §1~§10 | 복잡한 규칙 확인 시 |
