# SO:EUM🌸  
### 13조 미니 프로젝트  
*잠 못드는 현대인들의 숙면을 위한 ASMR 공유 플랫폼입니다.*  
*기간 : 2022. 03. 07 ~ 2022. 03. 10*


## 팀원소개 
* 최서라 : 좋아요 기능 / 키워드 순위 리스트
* 이경태 : 영상리스트 조회 / 등록 
* 박지연 : 로그인  / 회원가입/ 로그아웃


## 웹사이트 링크
http://kbong00.shop/ (3/17 서버 Close)


## 시연영상 링크

영상 주소 : https://youtu.be/SvPc0G4LMU4


## 핵심기능
* 유튜브 채널 등록
  * youtube 채널 url 입력 시 영상의 썸네일을 웹스크랩핑합니다. 
  * 사용자 이름, 키워드를 가져와 붙입니다.
* 좋아요 기능
  * JWT 를 이용하여 회원을 확인하고 좋아요 수를 카운트 및 변경합니다.
* Keyword 카테고리별 순위
  * 영상 등록 시 카테고리 수를 카운트하고 순위를 목록화하여 보여줍니다. 
* Keyword 카테고리별 조회
  * 카테고리별로 분류하여 조회가 가능합니다. 


## 사용기술
* PyJWT
* Jinja2
* Flask
* bulma
* bs4
* mongoDB
