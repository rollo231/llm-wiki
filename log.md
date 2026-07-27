# Log

Chronological record of wiki activity. Append-only; the newest entry goes at the bottom.
Each entry follows the format: `## [YYYY-MM-DD] <ingest|query|lint> | <title>`

## [2026-07-19] schema | Reset to clean slate

Reorganized `raw/` into per-area subfolders and added the `data-engineering` and
`resume-guide` areas, then removed the initial worked examples (Squidpy pages + raw source)
and prior working docs to start fresh. The vault now holds only the schema and one raw source
awaiting ingest: `raw/resume-guide/tech-director-resume-guide-v1.pdf`.

## [2026-07-19] ingest | Tech Director's Resume Guide

이력서 가이드 PDF(`raw/resume-guide/tech-director-resume-guide-v1.pdf`)를 `resume-guide`
영역의 첫 소스로 인제스트. source 페이지 [[Tech Director's Resume Guide]], concept 4개
([[Tech resume best practices]], [[Tech resume anti-patterns]], [[How resume screeners read]],
[[Resume writing for new grads]]), MOC [[Resume Guide]]를 생성. `index.md`에 등록. entity 없음
(소스에 해당 없음); 모순 없음(빈 vault).

## [2026-07-19] ingest | AI DE Course - Ch1-1 OT

Fast Campus 데이터 엔지니어링 강의의 CH01-1 [OT]
(`raw/data-engineering/ch01-1-de-vs-ai-de-ot.pdf`)를 `data-engineering` 영역 첫 소스로 인제스트.
강의 entity [[AI Data Engineering (Fast Campus course)]], source [[AI DE Course - Ch1-1 OT]],
concept [[Traditional data engineering]]·[[AI data engineering]] 생성. `index.md`에 등록.
파일은 `raw/data-engineering/`로 이동·영문명 변경. area MOC는 페이지가 더 쌓이면 생성(lazy).

## [2026-07-27] ingest | SpatialData docs - Design doc

`https://spatialdata.scverse.org/en/stable/`(URL 소스)를 `bioinformatics` 영역 첫 소스로
인제스트. 사이트가 Cloudflare 봇 차단(HTTP 429)으로 직접 fetch되지 않아, 동일 내용의 원문
MyST markdown을 `scverse/spatialdata` repo에서 **태그 `v0.8.0`에 핀**해 가져왔다. 스냅샷은
`raw/bioinformatics/spatialdata-docs/`(`SOURCE.md` 매니페스트 + `index--v0.8.0.md` +
`design_doc--v0.8.0.md`).

첫 슬라이스로 design doc + 랜딩 페이지만 인제스트(섹션별 진진적 방식). entity
[[SpatialData]](문서 섹션 트래커 겸함)·[[OME-NGFF]], concept [[SpatialData elements]]·
[[Coordinate systems and transformations]], source [[SpatialData docs - Design doc]],
영역 MOC [[Bioinformatics]] 생성. `index.md`에 등록.

핵심: SpatialData는 분석 라이브러리가 아닌 IO·공간질의 **인프라**이며, element를 전용 클래스
없이 표준 파이썬 클래스 + 메타데이터로 표현하고, element 간 명시적 링크 대신 좌표계로 의미적
그룹핑을 한다. 모순 없음(영역이 비어 있었음). 문서의 2025 로드맵이 미완 체크박스로 남아 있어
소스 페이지에 신선도 주의를 명시하고 MOC 열린 질문으로 남겼다.

URL 소스 처리 컨벤션을 이번 건으로 확정해 `CLAUDE.md` Ingest 절에 명문화했다.
