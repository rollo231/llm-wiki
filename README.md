# LLM Wiki

**LLM Wiki** 패턴([karpathy 의 gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f))으로
만든 개인 지식 베이스. [Obsidian](https://obsidian.md) 안에서 LLM 에이전트가 유지·관리합니다.

> Obsidian 은 IDE, LLM 은 프로그래머, 위키는 코드베이스.

사람은 자료를 큐레이팅하고, 분석 방향을 정하고, 질문합니다. LLM 에이전트는 읽기·요약·교차참조·
정리·장부 기록을 합니다. 지식은 **한 번 통합되면 최신 상태로 유지**됩니다 — 질문할 때마다 다시
만들어내는 것이 아니라, 계속 쌓이는(compounding) 지속적 산물입니다.

이 위키는 **source-first** 입니다: 지식은 자료를 ingest 하며 들어오고, 위키는 그 주위로 자랍니다.
**일반(general)** 지식의 여러 영역을 조직합니다 (이 repo 는 공개):

- **bioinformatics** — 공간 전사체학, 단일세포, 방법론, 개념.
- **programming** — 언어·프레임워크·분야 (Python, FastAPI, React, K8s, …).
- **data-engineering** — 데이터 파이프라인, 오케스트레이션, 저장, 인프라.
- **resume-guide** — 강한 이력서/CV 작성법과 채용 측의 기대치.

## 레이어

1. **`raw/`** — 원본 자료. 영역별 하위 폴더에 정리. **Gitignore 됨 — 로컬 전용 입력 캐시**이며
   버전 관리하지 않습니다. 버전 관리되는 산물은 `wiki/` 이고, 출처는 각 source 페이지의 인용에 남습니다.
2. **`wiki/`** — 에이전트가 만들고 유지하는 Markdown 페이지.
3. **`CLAUDE.md`** — 스키마: 에이전트가 따르는 구조·컨벤션·워크플로우.

## 구조

```
llm-wiki/
├─ CLAUDE.md          # 에이전트가 따르는 스키마
├─ index.md           # 콘텐츠 카탈로그 (영역 우선)
├─ log.md             # 활동 타임라인 (append-only)
├─ docs/              # 이 repo 용 메타 작업 문서 (스펙·계획·핸드오프)
├─ raw/               # 원본 자료, 영역별 하위 폴더 — gitignored (로컬 전용)
└─ wiki/
   ├─ entities/       # 제품·도구·프레임워크, 사람, 조직, 데이터셋, 장소
   ├─ concepts/       # 아이디어, 방법론, 주제, 테마
   ├─ sources/        # raw 자료 1개당 페이지 1개: 요약 + 핵심
   ├─ notes/          # 질문 결과·종합·비교를 되돌려 저장
   └─ maps/           # MOC — 내비게이션 허브 페이지 (진입점)
```

페이지는 YAML frontmatter(`type`, `title`, `area`, `aliases`, `tags`, `created`, `updated`,
`sources`)를 갖고 Obsidian `[[wikilinks]]` 로 연결됩니다. `wiki/` 안에서 페이지의 영역은 별도
폴더가 아니라 `area` 필드와 tags 로 정해지므로, 한 페이지가 여러 영역에 속할 수 있습니다
(예: Python 으로 된 생명정보학 도구 → `area: [bioinformatics, programming]`). `raw/` 안에서는
자료를 영역별 하위 폴더에 정리합니다.

## 워크플로우

- **Ingest** — 자료가 `raw/` 에 들어옵니다. 에이전트가 읽고, 핵심을 논의하고, `source` 페이지를
  쓰고, 관련 `entity`/`concept` 페이지를 만들거나 갱신하고, 영역 MOC 에 연결하고, `index.md` 와
  `log.md` 를 갱신합니다.
- **Query** — 에이전트가 `index.md` 를 읽고 `[[links]]` 를 따라가 **인용과 함께** 답합니다.
  가치 있는 답은 `note` 페이지로 되돌려 저장해 탐색이 쌓이게 합니다.
- **Lint** — 요청 시 에이전트가 볼트를 건강검진합니다: 모순, 오래된 주장, 고아 페이지,
  누락된 `area`, 누락된 교차참조, 데이터 공백.

변경은 곧장 `main` 에 커밋합니다 — 개인·단일 관리자 repo 이기 때문입니다. 전체 스키마는
[`CLAUDE.md`](CLAUDE.md) 를 보세요.

## 시작하기

1. 이 폴더를 [Obsidian](https://obsidian.md) 볼트로 엽니다.
2. `raw/` 에 자료 문서를 넣습니다.
3. LLM 에이전트에게 ingest 를 요청하고 — 결과 커밋을 검토합니다.
