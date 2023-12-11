## Open SW Platform (23-2) 
🐑🐑🐑양 여섯마리🐑🐑🐑
#### [Our Tech Blog](https://sudden-suede-4ad.notion.site/Ewha-Market-cc137c52d11e4f068e7fc7c451419745?pvs=4)

### Ewha-Market
이화여대 학생들만을 위한 거래 웹 사이트

**주요 기능**
- 로그인/로그아웃/회원가입
- 마이페이지/위시리스트
- 검색 및 가격순 정렬
- 상품 및 리뷰 등록/조회
- 이화이언 인증 
------

### flask 초기 세팅 
1. 레포지토리 포크 후, 구름에서 컨테이너 생성하여 깃허브 불러오기 진행
2. URL 생성 후, 포트 5000번 열기
3. 터미널에 아래 명령어 실행하여 pyrebase 설치하기 
    ```
   pip3 install pyrebase --use-feature=2020-resolve
4. 'application.py' 실행
5. 해당 URL 열기
   
-----
### firebase와 flask 연결 
1. firebase 프로젝트 및 realtime database 생성
2. 앱  추가 후 해당 SDK json 파일 내용을 복사 후 'Authentication/firebase_auth.json'에 붙여넣기 
-----

### 파일 디렉토리 구조 
```
📦 flask_project
├─ LICENSE
├─ application.py
├─ authentication
│  └─ firebase_auth.json
├─ database.py
├─ static
│  ├─ style.css
│  └─ images
└─ templates
   └─ index.html
```

----

### 기술 스택

**FrontEnd:** HTML, CSS, JavaScript

**BackEnd:** Flask, Firebase 

**협업 툴:** Github, Git Kraken, Notion, Google Drive

---
### Team Members
**BE**

* 2176255 이서연
* 2276330 최유선
  
**FE**

* 2276167 신성현
* 2276216 이서연
* 2271063 하지연
* 2276188 양인경
