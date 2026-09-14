---
type: entity
title: Designing Machine Learning Systems
aliases: [DMLS]
tags: [책, MLOps]
created: 2026-09-14
updated: 2026-09-14
sources:
  - "[[AI DE 강의 2-02 MLOps와 ML 생애주기]]"
  - "[[AI DE 강의 2-05 서빙 파이프라인 설계]]"
  - "[[AI DE 강의 2-04 ML 데이터 파이프라인]]"
---

# Designing Machine Learning Systems

Chip Huyen이 쓴 ML 시스템 설계 책. [[AI 데이터 엔지니어링 강의]] Part 2가 그림과 표를 가져온다 — 한 번은 책 제목을
달고, 한 번은 출처 없이.

## 서지

| 항목 | 내용 |
|---|---|
| 제목 | *Designing Machine Learning Systems: An Iterative Process for Production-Ready Applications* |
| 저자 | Chip Huyen |
| 출판 | O'Reilly Media, 2022-05-17 (Google Books 표기), 388쪽 |
| 바탕이 된 강의 | Stanford CS 329S "Machine Learning Systems Design" (Winter 2022). 강의 노트마다 "For the fully developed text, see the book Designing Machine Learning Systems (Chip Huyen, O'Reilly 2022)"라고 적는다 |
| URL | https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/ · 저자 요약 https://github.com/chiphuyen/dmls-book |

책 본문은 직접 확인하지 못했다(O'Reilly 페이지 접근 차단, 2026-09-14). 아래의 그림·표 번호는 **슬라이드에 찍힌 캡션**이나
**CS 329S 강의 노트** 기준이다.

## 코스가 가져온 것

| 강의 | 가져온 것 | 표기 | 확인 |
|---|---|---|---|
| [[AI DE 강의 2-02 MLOps와 ML 생애주기]] | ML 라이프사이클 6단계 순환 그림 — Project scoping → Data engineering → ML model development → Deployment → Monitoring and continual learning → Business analysis | 책 제목만. 캡처 이미지의 캡션에 "Figure 2-2" | 단계 이름이 CS 329S Lecture 1 노트와 일치(노트에서는 Figure 1-7). 책에서는 2장 "Introduction to Machine Learning Systems Design" |
| [[AI DE 강의 2-05 서빙 파이프라인 설계]] | 배치 예측 vs 온라인 예측 표(빈도 "4시간마다" / 요청 즉시, 추천 / 사기 탐지, 처리량 / 지연) | **출처 표기 없음.** 원표의 Examples 행(Netflix 추천 / Google Assistant 음성 인식)은 빠졌다 | CS 329S Lecture 8 노트의 Table 6-1과 거의 같은 문구. 책에서는 7장 "Model Deployment and Prediction Service"(표 번호 미확인) |
| [[AI DE 강의 2-04 ML 데이터 파이프라인]] | (인용 아님) 시간 기반 분할·그룹 단위 누수 권고 | — | 같은 권고가 저자의 5장 요약("Split data by time into train/valid/test splits instead of doing it randomly.")과 CS 329S Lecture 5의 "Group leakage"에 있다. *(위키의 연결)* → [[데이터 누수]] |

[CS 329S Lecture 1 노트 https://docs.google.com/document/d/1C3dlLmFdYHJmACVkz99lSTUPF4XQbWb_Ah7mPE12Igo ·
Lecture 8 노트 https://docs.google.com/document/d/1hNuW6bqWYZjlwpit_8W1cu7kllb-jTfy3Liof1GJWug ·
Lecture 5 슬라이드 https://docs.google.com/presentation/d/1X_w55MfBhXGQbZkT_fbW9wdNrOs4sOuydRGPUI_yYCo ,
2026-09-14 확인]

## 주의

- 저자 GitHub 저장소에 적힌 ISBN(978-1801819312)은 서점 표기(978-1-098-10796-3)와 맞지 않는다. 인용에는 쓰지 않는다.
- Part 2의 MLOps 절반(생애주기·서빙 방식)이 이 책의 틀을 따르는데, 코스는 저자 이름을 한 번도 적지 않는다. 슬라이드의
  단계 설명 가운데 어디까지가 책이고 어디부터가 강사의 정리인지 구분되지 않는다. → [[AI DE 강의 2-02 MLOps와 ML 생애주기]]

## 관련

- [[MLOps]] · [[모델 서빙]] · [[데이터 누수]]
