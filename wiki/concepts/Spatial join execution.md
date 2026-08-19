---
type: concept
title: Spatial join execution
area: [data-engineering]
aliases:
  - 공간 조인 실행
  - spatial join
  - 공간 조인
  - filter-refine
  - 공간 파티셔닝
  - spatial partitioning
  - KDB-tree
  - R-tree
  - quadtree
  - 공간 인덱스
tags: [data-engineering, spatial-join, indexing, query-optimization, distributed-processing, geospatial]
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[Apache Sedona docs - Spatial join execution]]"
  - "[[SpatialData source - Shapes conversion and aggregation ops]]"
---

# Spatial join execution

**공간 조인이 일반 조인과 다른 이유는 조인 키가 없다는 것이다.**

equi-join은 해시 하나로 끝난다 — 같은 값끼리 같은 버킷에 간다. 공간 술어(`ST_Intersects`,
`ST_Within`, `ST_DWithin`)에는 **동등성이 없다.** "겹친다"는 관계는 값 비교가 아니라 기하 계산이고,
따라서 **어느 쌍을 비교할지부터 정해야 한다.** 그 문제를 푸는 구조가 세 층으로 갈린다.

```
① 공간 파티셔닝  전 클러스터의 공간을 격자로 쪼개 셔플 키를 만든다   ← grid
        ↓          (경계에 걸친 객체는 여러 파티션에 복제된다)
② 로컬 인덱스     파티션 안에서 MBR(경계 사각형)로 후보를 좁힌다      ← index
        ↓
③ refine         살아남은 쌍만 실제 기하 술어를 계산한다             ← JTS 등
```

**세 층은 서로 대체하지 않는다.** ①이 없으면 전량 셔플(또는 nested loop), ②가 없으면 파티션 안에서
전 쌍 비교, ③이 없으면 답이 틀린다. 성능 논의가 자꾸 헛도는 이유가 **"인덱스"라는 한 단어로 ①과 ②를
같이 부르는 것**이다.

## ① 격자 — 무엇이 같은 파티션에 가는가

| 격자 | 성질 |
|---|---|
| **Quad-tree** | 공간을 균등하게 4분할. 단순하고 예측 가능 |
| **KDB-tree** | **데이터 밀도에 적응**해 분할. 편향된 데이터에서 파티션 크기가 고르다 |
| **R-tree** | 객체 묶음의 MBR로 계층을 만든다. 겹치는 노드를 허용 |

공간 데이터는 거의 항상 편향돼 있다 — 인구는 도시에, 세포는 조직 절편에 몰린다. 균등 격자를 쓰면
**한 파티션이 전체 작업을 떠안는다**(skew). [[Apache Sedona]]의 SQL 경로 기본값이 `kdbtree`인 것이
그 대응이다.

⚠️ 밀도 적응이 기본값의 *이유*라는 설명은 자료구조 성질로부터의 추론이다 —
[[Apache Sedona docs - Spatial join execution|Sedona 문서]]는 기본값만 적고 근거를 말하지 않는다.

**격자는 반드시 양쪽이 공유해야 한다.** 서로 다른 격자로 파티셔닝한 두 데이터셋을 조인하면 조용히
답이 빠진다. Sedona RDD API가 `getPartitioner()`를 다른 쪽에 넘기라고 요구하는 이유다.

### ⭐ 파티셔닝은 복제를 전제한다

경계에 걸친 폴리곤은 **여러 파티션에 들어가야** 조인이 완전해진다. 그래서 공간 파티셔닝된 데이터는
원본보다 행이 많고, **결과에 중복 쌍이 생긴다.**

- point-in-polygon 조인은 무해하다 — 점은 한 파티션에만 속한다
- polygon × polygon, polygon × line, line × line 은 중복 제거가 필요하다

equi-join에는 없는 문제이고, **공간 조인 결과를 그대로 집계에 쓰면 값이 부풀 수 있다**는 뜻이다.

## ② 로컬 인덱스 — 후보를 좁힌다

파티션 안에서 R-tree나 quadtree를 세워 **MBR 교차하는 쌍만** 골라낸다. 여기서 나오는 것은 답이
아니라 **후보**다 — MBR이 겹쳐도 실제 기하는 안 겹칠 수 있다(L자 폴리곤 두 개를 생각하면 된다).

인덱스는 **한쪽에만** 만든다. 다른 쪽이 그 인덱스를 탐색한다(probe). 어느 쪽에 만드는지는
성능 선택이고, Sedona 문서는 *"더 큰 쪽에 만들라"* 고 권한다.

## ③ refine — 진짜 술어

후보 쌍마다 실제 기하 연산을 돈다. 이 층이 비용의 대부분을 차지할 수 있다 — 정점 수만 개짜리
폴리곤의 교차 판정은 싸지 않다.

refine을 싸게 만드는 두 방향:

- **기하를 단순화한다** — 축 정렬 사각형(bbox)끼리는 double 4개 비교로 끝난다. Sedona의 `Box2D`
  조인이 이걸 노린다.
- **refine을 건너뛴다** — 오차를 허용하면 ②의 결과를 그대로 답으로 쓴다. 아래 §다이얼.

## 두 가지 조인 전략

| 전략 | 조건 | 셔플 |
|---|---|---|
| **파티셔닝 조인** (range/distance join) | 양쪽 다 큼 | 양쪽 셔플 |
| **브로드캐스트 인덱스 조인** | 한쪽이 작음 | **없음** — 작은 쪽을 복사하고 그 위에 인덱스를 세운다 |

브로드캐스트가 가능하면 거의 항상 이긴다. ①을 건너뛰고 ②③만 하기 때문이다. 임계값은 설정으로
노출된다(Sedona: `sedona.join.autoBroadcastJoinThreshold`).

⚠️ **최악의 fallback은 nested loop**다. 옵티마이저가 술어를 공간 조인으로 인식하지 못하면
(예: `LEFT JOIN` + 공간 술어) 전 쌍 비교로 떨어진다. **공간 조인의 성능 사고는 대부분 튜닝 실패가
아니라 "인식되지 않았다"** 다 — 물리 플랜에 `RangeJoin`/`BroadcastIndexJoin` 이름이 뜨는지가
1차 확인 지점이다.

## ⭐ 정확도 다이얼 — 셀 ID로 공간을 equi-join으로 바꾼다

공간 조인이 어려운 이유가 "조인 키가 없다"는 것이었다면, **키를 만들어버리는** 우회가 있다.
기하를 공간 채움 곡선의 셀 ID 집합으로 바꾸고(S2·geohash·H3), 그 ID로 **평범한 equi-join**을 한다.

```
기하 → explode(cell_ids)  →  equi-join on cell_id  →  (선택) refine  →  (선택) dedup
```

- 셀이 크면 → 행이 적고 false positive가 많다
- 셀이 작으면 → 행이 늘고 정확해진다
- refine을 붙이면 정확하고, 빼면 빠르다

⭐ **[[Consumption layer]]의 오차 다이얼과 같은 형태다** — 근사 집계(DataSketches)가 유니크 카운트에
하는 일을 셀 ID가 공간 관계에 한다. *합의할 숫자*가 하나 더 있는 셈이다.

## 저장 층이 이 모든 것보다 먼저다

세 층 전부는 **읽어야 하는 데이터를 줄이지 못한다.** 프루닝은 파일 층에서 일어난다.

- 파일별 bbox 메타데이터 → 질의 창과 안 겹치는 파일을 통째로 건너뛴다
- row group 통계 → 파일 안에서도 건너뛴다
- ⭐ 둘 다 **쓰기 시점의 공간 정렬**에 달려 있다. 정렬하지 않으면 모든 파일의 bbox가 전체 범위에
  가까워 프루닝이 0이 된다

→ [[Apache Sedona docs - Storage and formats]], [[Columnar and in-memory data formats]]

## 단일 머신 버전에서도 같은 구조다

이 3층은 분산 고유의 것이 아니다. geopandas `sjoin`도 `sindex`(R-tree)로 ②를 하고 shapely로 ③을
한다 — 없는 것은 ①뿐이다. 그래서 **단일 머신 공간 조인의 한계는 인덱스가 아니라 메모리**다:
[[Spatial aggregation]]의 issue #210이 정확히 그 지점이다.

| | ① 격자 | ② 인덱스 | ③ refine |
|---|---|---|---|
| geopandas `sjoin` | ❌ | ✅ `sindex` | ✅ shapely |
| [[SedonaDB]] | (단일 노드, 런타임 적응) | ✅ | ✅ |
| SedonaSpark | ✅ kdbtree/quadtree | ✅ rtree/quadtree | ✅ JTS |

## 링크

- 출처: [[Apache Sedona docs - Spatial join execution]]
- 저장 층: [[Apache Sedona docs - Storage and formats]], [[Columnar and in-memory data formats]]
- 엔진: [[Apache Sedona]], [[SedonaDB]], [[Apache Spark]]
- 단일 머신 대응: [[Spatial aggregation]], [[Spatial queries in SpatialData]]
- 응용: [[SpatialData and Sedona interop]]
- DE 개념: [[Distributed processing]], [[Consumption layer]], [[SQL execution layer]]
- 영역 MOC: [[Data Engineering]]
