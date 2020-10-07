# moockt

## Data Preprocessing
- [Question - Anwser] 쌍의 csv 파일
- 입력 형식은 자유
- 파일 경로를 generate_dataset.py 에 전달 (default: ../data/os_qna.csv)

## Model
  1.AIML
  
  2.Dialogflow Chatbot
   - QnA dataset 생성 [Question-Anwser 쌍의 csv 파일을 intent 별 json 파일로 저장] : generate_dataset.py 실행
   - os_chatbot.py 실행 
  
       - 카카오톡 서버 연동 코드 : os_chatbot.py
       - 다이얼로그플로우 챗봇 연동 코드 : testDialogflow.py 
    
   - codes/acquired-ripple-285306-8da5f9a63c48.json : 구글 Api credential key
  
 

## 시스템 통합 버전
- https://github.com/yangjae33/moockt



