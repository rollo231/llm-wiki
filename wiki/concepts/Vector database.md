---
type: concept
title: Vector database
area: [data-engineering]
aliases: [벡터 데이터베이스, 벡터 DB, Vector DB, ANN, 근접 이웃 검색, HNSW, IVF, Milvus, FAISS, Pinecone, Weaviate]
tags: [vector-database, ann, hnsw, ivf, vector-search, rag, data-engineering]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 Embeddings and vector search]]", "[[AI DE Course - Ch3-5,6 Unstructured data ingestion]]"]
---

# Vector database

**임베딩 벡터를 저장하고, 질의 벡터와 가까운 것들을 빠르게 찾아 주는 시스템.**

기존 인덱스(B-tree·해시)는 **같은 값**을 찾는 데 최적화돼 있다. 벡터 검색은 **가까운 값**을
찾아야 하고, 수백~수천 차원에서 정확한 최근접 탐색은 전수 비교와 다를 바 없어진다.
**그래서 정확도를 조금 포기하고 속도를 사는 ANN(근사 최근접 이웃)이 기본 전제다.**

## 검색 5단계

```
1. 문서 임베딩 생성  2. 벡터 인덱싱   3. 질의 임베딩  4. 근접 이웃 검색  5. 재랭킹/후처리
문서 분할·청킹        IVF/HNSW        쿼리 전처리      Top-K 후보 추출    필터링·정밀 채점
```

**1~2단계는 인덱싱 시점(오프라인), 3~5단계는 질의 시점(온라인)이다.**
[[Feature store]]의 offline/online 이원 구조와 같은 형태이고, **같은 위험도 공유한다** —
인덱싱에 쓴 임베딩 모델과 질의에 쓰는 모델이 어긋나면 조용히 망가진다
([[Data drift and training-serving skew]]).

## ANN 인덱스

강의는 **IVF·HNSW**를 이름만 언급한다. 최소한의 정리:

| | 방식 | 성격 |
|---|---|---|
| **IVF** (Inverted File) | 벡터를 클러스터로 나눠 두고, 질의와 가까운 몇 개 클러스터만 탐색 | 메모리 효율이 좋다. 탐색 클러스터 수(`nprobe`)가 정확도/속도 다이얼 |
| **HNSW** (계층적 그래프) | 벡터를 그래프로 연결해 두고 가까운 이웃을 따라 내려간다 | 검색이 빠르고 정확하다. **메모리를 많이 쓰고 빌드가 느리다** |

> ⭐ **어느 쪽이든 다이얼은 하나다 — 정확도(recall) ↔ 지연·메모리.**
> "벡터 검색이 느리다"는 대개 인덱스 문제가 아니라 **이 다이얼을 어디에 뒀는지**의 문제다.
> [[Caching strategies]]·[[Latency and throughput]]과 같은 종류의 트레이드오프.

## 제품

| 제품 | 성격 |
|---|---|
| **Milvus** | 오픈소스 벡터 DB. 분산·확장 지향 |
| **Pinecone** | **클라우드 관리형.** 운영 부담이 가장 적다 |
| **Weaviate** | AI 네이티브. **멀티모달** 검색에 강점 |
| **FAISS** | ⚠️ **DB가 아니라 라이브러리** — Meta(Facebook AI) 개발 |

> ⚠️ **FAISS를 나머지 셋과 나란히 놓으면 안 된다.** 강의는 넷을 같은 표에 나열하는데,
> **FAISS에는 서버·영속성·메타데이터 필터링·복제·인증이 없다.** 인덱싱/검색 알고리즘 라이브러리이고,
> 실제로 여러 벡터 DB가 내부에서 FAISS 계열 알고리즘을 쓴다.
> **"라이브러리를 쓸 것인가 시스템을 쓸 것인가"는 [[Distributed processing]]의
> *"단일 서버로도 감당 가능한가"*와 같은 판단이다.**

## 전용 DB가 필요한가

강의는 묻지 않지만 실무의 첫 질문이다.

- 벡터가 수만~수십만 개 수준이면 **PostgreSQL + pgvector**나 기존 검색 엔진(Elasticsearch·
  OpenSearch)의 벡터 기능으로 충분한 경우가 많다. 운영 포인트를 늘리지 않는 쪽이 이득이다
- **하이브리드 검색을 할 거라면 오히려 검색 엔진 쪽이 유리할 수 있다** — BM25가 이미 있다
  ([[Hybrid search and reranking]])
- 전용 DB의 값어치는 규모, 필터링과 결합된 ANN, 운영 도구에서 나온다

**[[NoSQL]]의 결론이 그대로 적용된다 — 새 저장소는 문제를 옮기지 없애지 않는다.
운영 포인트가 하나 늘어난다.**

## 메타데이터 필터링

실무에서 벡터 검색은 거의 항상 조건과 함께 온다 — *"최근 1년, 이 부서 문서 중에서"*.
**필터를 먼저 걸고 ANN을 돌릴지(pre-filter), ANN 결과를 걸러낼지(post-filter)에 따라 결과와 성능이
달라진다.** post-filter는 Top-K를 채우지 못할 수 있고, pre-filter는 인덱스 구조를 우회하게 될 수
있다. **강의에는 이 이야기가 없다.**

## 관련 페이지

- [[Text embeddings]] — 여기에 담기는 값을 만드는 단계
- [[Hybrid search and reranking]] — 벡터 검색만으로 부족한 지점
- [[Retrieval-augmented generation]] — 이 저장소를 쓰는 시스템
- [[Unstructured data ingestion]] — 벡터 DB로 가는 4단계 파이프라인
- [[Analytical data storage tiers]] — 저장소 계층 전체 지도에서 벡터 DB의 자리
- [[Graph database]] — 또 하나의 "특수 목적 저장소". 도입 판단의 구조가 닮았다

## 출처

- [[AI DE Course - Part5 Embeddings and vector search]] (Fast Campus, Part 5) — 제품 4종, 검색 5단계
- [[AI DE Course - Ch3-5,6 Unstructured data ingestion]] (Part 1) — ANN 인덱스와 재순위화
