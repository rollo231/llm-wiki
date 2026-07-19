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
