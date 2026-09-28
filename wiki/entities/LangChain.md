---
type: entity
title: LangChain
aliases: [LangGraph, langchain]
tags: [LLM, 프레임워크, RAG]
created: 2026-09-28
updated: 2026-09-28
sources:
  - "[[AI DE 강의 5-03 LLM의 한계와 RAG]]"
---

# LangChain

LLM 애플리케이션을 만드는 오픈소스 프레임워크다. [[AI DE 강의 5-03 LLM의 한계와 RAG]] p15는 이를 데이터 연결, 검색·인덱싱, 메모리(대화 기록·컨텍스트 관리), 에이전트 기능을 주는 프레임워크로 소개하고, 구성 요소를 Prompts·LLMs·Chains·Agents 넷으로 든다. 강의에서 LangChain이 나오는 곳은 이 슬라이드 하나이고 코드 예시는 없다.

## 강의 서술과 현재

| 항목 | 슬라이드 (p15) | 2026-09 |
|---|---|---|
| GitHub 스타 | 50K+ | 147.2k (https://github.com/langchain-ai/langchain) |
| 월간 다운로드 | 1M+ | 169,366,312 (지난 한 달, https://pypistats.org/packages/langchain) |
| 에이전트 | Chains·Agents 구성 | LangChain 1.0의 `create_agent`, 내부는 LangGraph |

[2026-09-28 확인] 슬라이드의 통합 모델 수·통합 도구 수는 확인하지 않았다. 스타 수와 다운로드 수는 GitHub 페이지와 pypistats 웹 페이지 기준이다(API는 rate limit에 걸렸다).

## LangChain 1.0과 LangGraph

LangChain 1.0과 LangGraph 1.0은 2025-10-22에 함께 나왔다. 발표 글은 "The new `create_agent` function uses LangGraph under the hood to run this loop."라고 쓴다. [https://www.langchain.com/blog/langchain-langgraph-1dot0 , 2026-09-28 확인] LangGraph는 에이전트의 상태와 단계를 그래프로 정의하는 같은 회사의 라이브러리다. 슬라이드(PDF 생성일 2026-05-05)는 이 변화 전의 Chains·Agents 구성으로 설명하므로 작성 시점에 이미 낡았다.

## 위키에서의 자리

강의는 LangChain을 RAG 구현 도구로 소개하지만, RAG의 구조 자체는 프레임워크와 무관하다. 문서 로딩 → 청킹 → 임베딩 → 벡터 DB → 검색·생성의 단계는 [[검색 증강 생성]]과 [[벡터 데이터베이스]]에 있고, LangChain은 이 단계들의 부품(로더, 분할기, 벡터 스토어 연동, 리트리버)을 묶어 준다. 이 정리는 위키의 것이다.

## 관련

- [[검색 증강 생성]] · [[벡터 데이터베이스]] · [[임베딩]] · [[LLMOps]]
- [[AI 데이터 엔지니어링 강의]]
