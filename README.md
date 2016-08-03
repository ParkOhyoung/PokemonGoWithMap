#Pokemon Go with map

#####Please refer to [sokChoGo](https://github.com/cjeon/sokChoGo).
#####Only difference is character control.
#####sokchogo using keyboard but PokemonGoWithMap using mouse on map. 

![Running Image](https://cloud.githubusercontent.com/assets/8384193/17329134/39baa8b2-58fc-11e6-81b8-ddea92905ae3.png)

###간단한 실행 설명
1. 본 레파지토리의 `sample.gpx`를 `pikapika.gpx`로 이름을 변경한다. 
2. xcode를 실행하여 기본 프로젝트를 생성한다 (그냥 next, next...)
    * 생성 되었으면 `Product->Scheme->Edit Scheme` 로 가서 `Core location` 체크박스에 체크 되어 있는것 확인 (안되어 있으면 체크)
    * 바로 아래 `Default Location` select box에서 `Add GPX File to Project`를 클릭하여 본 레파지토리에 포함된 `pikapika.gpx`를 등록한다.
3. xcode를 최대한 줄여서 아래쪽에 놓고 아이폰을 연결한 후 xcode의 `▶` 를 클릭한다.
4. 터미널로 가서 `python runserver.py`로 실행
    * OS env에 `GOOGLE_API_KEY`가 있는지 체크하여 없으면 설명과 함께 실행을 멈춘다.
    * xcode의 gps 버튼 위에 마우스를 놓고 터미널로 돌아와(Cmd+tab을 이용) `Enter`
    * xcode의 gps 버튼을 누르면 '1.'에서 등록한 `pikapika.gpx`가 보인다 그위에 마우스를 놓고 위와 같은 방법으로 터미널로 돌아와 `Enter`
5. 간단한 웹서버가 돌기 시작하면서 Chrome이 자동으로 켜지면 게임을 플레이할 준비완료 
    * 마지막 좌표에서 실행할지 현재 위치에서 실행할지 물어 보고 해당 위치로 이동하면 준비 완료
    * 중요!! Chrome을 전체모드로 하지말고 xcode의 gps 버튼이 화면에 보이도록 해야한다.
    * 위 이미지는 설명을 위해 `Quicktime`과 `터미널`을 보이게 해 놓았으나 안보여도 게임에 지장 없습니다. 
6. 아이폰에서 현재 앱을 백그라운드로 돌리고 `Pokemon Go`를 실행하면 맵에 보이는 지역에서 게임을 시작하게 된다.
    * 작은 파란색 원은 10m, 빨간 원은 30m 거리를 나타내고 해당 원은 현재 위치 마커를 따라 다닌다.
    * 왼쪽 상단에 있는 검색 박스를 통해 전세계 어디든 이동 또는 시작할 수 있다.
7. 게임 시작.

#### *주의! 정상적 Play가 아니기에 언제든 Ban(block) 당할 수 있습니다.*

###동작 원리
apple은 개발 편의를 돕기위해 gpx파일을 통해 fake gps좌표를 등록 할 수 있게 해놓았습니다.
[설명 (영문)](https://blackpixel.com/writing/2013/05/simulating-locations-with-xcode.html)
(여담이지만 GPX파일은 하나의 좌표만 등록 가능한게 아니라 여러개의 좌표를 가질수 있고 그 좌표들마다 시간을 가질 수 있어 자동으로 계속 움직이게도 할 수 있습니다.)
이것과 Auto mouse를 이용한 것으로 지도위에서 마우스 클릭이 일어날때 마다 서버로 해당 좌표를 전송하면 서버는 들어온 좌표로 새 GPX를 찍어내고 곧바로 Auto mouse를 이용해서 인식 시킵니다.
그렇게 하면 해당 앱(구동을 위해 만든 빈 껍데기 앱)만 Fake gps좌표를 사용하는게 아니라 아이폰 전체가 해당 좌표를 실제 좌표로 인식하게 됩니다. `Pokemon Go`도 마찬가지 입니다.  
