<img src="https://user-images.githubusercontent.com/17819874/79853717-5db2f900-8403-11ea-99ba-ed0bb3cdb9ef.png" height="100"/>

# personal curation


> 프로젝트 간략 소개 한 문장 
- 성별, 피부톤, 상황별로 코디 큐레이션 해주는 서비스입니다.

## 핵심 기능  Key Feature
- 자신의 현재 T.P.O를 고려하여 직관적으로 조건을 선택하면, 쿠팡의 상품 콘텐츠 중 적합한 것들만
선별하여 제안합니다. 제목 누르면 해당 상세 페이지로 넘어가도록 구현했습니다.

## 기술 설명(서버)
- 기본적으로 함께 학습했던 기술들 활용해 진행하였습니다.
- import requests
from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient
- 추가적으로 데이터양이 방대하여 schedule 패키지를 통해, 서버에서 매일 1am에 자동적으로 크롤링 진행하도록 했습니다.
- import schedule
from jobs import job_at_everyday_1am

## 기술 설명(프론트)
- radio 타입의 인풋박스 사용했습니다. 함수 적용할 때, 데이터 값 받아오는 방식 첨부!
-             let gender = $('input[name="gender"]:checked').val();
            let tone = $('input[name="tone"]:checked').val();
            let keyword = $('input[name="keyword"]:checked').val();

## 어려웠던 점 & 극복 방법
- 어려웠던 점 : A to Z.. 다 어려웠습니다.. 특히 어려웠던 점은 서버에서 원하는 규칙을 지정하는 과정(각 조건에 맞는 값 가져오게 정하는거!)이었습니다.
- 극복 방법 : 구글링으로 해결해보려고 노력했지만.. 삽질만 되어서^^..바로바로 튜터님께 질문해서 해결 가능했습니다!! 감사합니다 >< 
- 또, 금요일에 본진가서 막히는 부분 여쭤본 것도 큰 도움이 되었어요!

## 8주간의 코딩 첫걸음 후기
**
-  초반만 해도 이 언어들이, 어디서 어떻게 사용되는거지 이해가 안되었는데 계속 부딪히며 진행하고, 특히 개인 프로젝트를 진행하면서 거시적인 서버와 프론트의 흐름을 알 수 있어 좋았습니다.
- 상상했던 서비스를 직접 구현해볼 수 있다는 점이 너무 신기했어요!! 
- 물론 아직 넘어야할 산이 많지만.. 이후에도 완성을 위해 쭉 나아갈 예정입니다!!

## 남은 과정
- 두번째 탭은 상품 검색하면 그것에 대한 리뷰를 보여주고, 해당 상품 상세페이지로 넘어가게 하는 것인데 .. 여기서 추가적으로 selenium 활용하여 크롤링하고 있습니다.. 잘 안되어서 계속 삽질해보아야할 거 같은데 이 탭까지 완성해서 퍼스널 큐레이션 탭과 한데 모으는 것이 최종 목표입니다!! 
- p.s. 튜터님,,, 연락 받으셔야해요,,?☆

## License 
김미화 – [alghk0528@naver.com]