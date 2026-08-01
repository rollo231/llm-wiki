---
type: entity
title: LangChain
area: [programming, data-engineering]
aliases: [랭체인, LangChain 프레임워크]
tags: [langchain, llm, framework, rag, agent, python, programming, data-engineering]
created: 2026-08-01
updated: 2026-08-01
sources: ["[[AI DE Course - Part5 RAG pipeline and LangChain]]", "[[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]]"]
---

# LangChain

**LLM 애플리케이션을 조립하기 위한 프레임워크.** 모델 호출, 데이터 연결, 검색, 대화 기록, 에이전트를
공통 인터페이스로 묶는다.

## 구성 요소

| | 역할 |
|---|---|
| **Prompts** | 프롬프트 템플릿과 관리 |
| **LLMs** | 다양한 LLM 모델 연동 (모델 교체를 코드 변경 없이) |
| **Chains** | 작업 체인 구성 — 여러 단계를 순서대로 엮는다 |
| **Agents** | 자율적 작업 수행 — 도구를 골라 쓰고 반복한다 |

기능 축 넷: **데이터 연결**(다양한 소스 ↔ LLM) · **검색**(문서 검색·인덱싱) ·
**메모리 시스템**(대화 기록·컨텍스트 관리) · **에이전트**.

## 위치

**RAG를 만들 때 [[Vector database]]·임베딩 모델·LLM을 각각 직접 붙이는 대신, 이미 정의된 추상 위에서
조립하게 해 준다.** [[Model serving platforms]]이 *"축은 추상화 수준 하나"*였던 것과 같은 구도 —
**추상을 얻고 제어를 내준다.**

- **얻는 것** — 빠른 프로토타이핑, 모델/벡터 DB 교체 용이, 통합 목록
- **내주는 것** — 내부 동작의 불투명성, 버전 변화의 잦음, 디버깅 난이도

> 이 위키에는 아직 LangChain을 실제로 써 본 기록이 없다. **위 트레이드오프는 프레임워크 일반의
> 성질에서 온 서술이지 검증된 평가가 아니다.**

## 이 코스에서

- [[AI DE Course - Part5 RAG pipeline and LangChain]] — 유일하게 실체로 다뤄지는 지점(1슬라이드)
- [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]] — [[Neo4j]] 고객 사례 아키텍처 도식에
  이름만 등장 (Neo4j ↔ **LangChain** ↔ SageMaker/Bedrock)

⚠️ **강의의 통계 배지**(`50K+ GitHub Stars` · `1M+ 월간 다운로드` · `100+ 통합 모델` ·
`200+ 통합 도구`)**에는 기준 시점이 없다.** 라이브러리 통계는 시점 없이는 의미가 없다.

## 관련 페이지

- [[Retrieval-augmented generation]] — 이 프레임워크가 주로 조립하는 것
- [[Vector database]] · [[Text embeddings]] — 연결 대상
- [[LLMOps]] — 조립한 것을 운영에 올릴 때
- [[Context engineering]] — 프롬프트·메모리가 다루는 문제
- [[Model serving platforms]] — 추상화 수준 트레이드오프의 다른 사례

## 출처

- [[AI DE Course - Part5 RAG pipeline and LangChain]] (Fast Campus, Part 5)
- [[AI DE Course - Part3 Ch4 GraphRAG concepts and cases]] (Part 3)
