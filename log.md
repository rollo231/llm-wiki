# 로그

위키 활동의 시간순 기록. 추가만 하고, 새 항목은 맨 아래에 붙인다.
항목 머리 형식: `## [YYYY-MM-DD] <ingest|query|lint|schema> | 제목`

## [2026-09-14] schema | 위키 초기화 — gist 골격으로 재시작

- 이전 위키를 전부 지우고 다시 시작했다 — 페이지 200개(source 82 · concept 68 · entity 41 · note 7 ·
  MOC 2)와 로그 1,695줄. 이전 내용은 git 커밋 `12f3ead` 에 남아 있다.
- 원본은 `raw/data-engineering/ai-de-course/`(패스트캠퍼스 AI 데이터 엔지니어링 강의, 5파트 PDF 40개)만
  남겼다. 나머지 raw 자료(SpatialData·spatialdata-io·Apache Sedona·MinIO 문서, 데이터 지형 가이드,
  Apache 기술 지도 책)는 완전히 삭제했고, 거기 딸린 `docs/experiments/` 도 지웠다.
- 스키마(`CLAUDE.md`)와 README 를 한국어로 다시 썼다. 카파시 gist 의 골격 — raw 불변 · wiki 는 에이전트
  소유 · 스키마, 인제스트·질의·린트, index·log — 만 두고, 강의 인제스트에 필요한 규칙 두 가지(주제 단위
  source 페이지, 트래커 entity)를 더했다. `area` 필드·MOC·URL 스냅샷·실험 하네스 규칙은 뺐다 — 필요해지면
  그때 다시 들인다.
- 이름 규칙: 사람이 읽는 것(파일명·제목·링크·본문)은 한국어, 기계가 읽는 것(frontmatter 키·`type` 값·
  폴더명·로그 키워드)은 영어. 로그 키워드에 `schema` 를 더했다.
- 다음: AI DE 강의 Part 1 인제스트 — 트래커 entity 부터.
