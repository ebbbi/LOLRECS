![background](./assets/background.png)

<img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black"> <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&flat-square&amp;logo=Next.js&amp;logoColor=white">
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white"> <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&amp;logo=MongoDB&logoColor=white">
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV&logoColor=white"> <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white">
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&amp;logo=Docker&logoColor=white">
<br>

---

<a href="https://youtu.be/nMr_Gkqbw_E" style="color: green; font-weight: bold">LOLRECS 시연 영상</a>

<a href="https://youtu.be/Y-EqgeUZQFc" style="color: green; font-weight: bold">LOLRECS 발표 영상</a>

---
# Introduction🎮
## BackGround📋

**LOLRECS는 리그오브레전드 플레이어에게 최적화된 챔피언과 아이템을 추천해주는 서비스입니다.**

- 롤 게임에서 플레이어들은 승리를 위한 챔피언과 아이템을 선택하기 위해 심사숙고해야 합니다. 롤은 출시된 이래, 지속적인 업데이트로 현재 선택할 수 있는 챔피언 수가 164가지, 전체 아이템 개수는 279개에 달합니다. 이렇게 방대한 선택지 중에서 최적의 선택을 하는 것은 숙련자에게도 어려운 일이며, 신규 플레이어의 롤 진입장벽은 점점 높아지게 됩니다.
- 롤과 관련한 여러 사이트에서는 이러한 문제를 해결하고자 통계 기반의 방식으로 아이템과 챔피언을 추천해 주고 있지만, 이는 실시간으로 플레이어가 처한 상황을 반영하지 못합니다. 
- **LOLRECS**는 기본적인 전적 검색과 더불어 실시간 밴픽 과정에서의 밴픽 조합을 고려한 챔피언 추천, 그리고 사용자의 포지션과 상대방의 챔피언을 고려한 아이템 추천을 제공합니다. 

<br>

## Contribution💡

- 랭크 게임을 시작한 지 얼마 되지 않은 플레이어들을 위한 코파일럿 추천 서비스입니다.
- Deep Learning 모델을 이용해 실시간 상황과 플레이어에게 맞춤화되어 있는 챔피언과 아이템을 추천해 드립니다.
- 응용 프로그램 설치 없이 모든 기능을 이용할 수 있습니다.

</br>
매일 고르고 싶은 챔피언과, 조합에 맞지 않는 챔피언으로만 게임을 하다 보면 티어는 제자리에 머물게 되기 마련입니다. 

실시간으로 밴이 된 챔피언과 아군, 적군이 픽한 챔피언을 토대로 추천받은 챔피언과 함께라면 당신의 티어는 수직 상승할 것입니다. 

**지금 바로 함께할 챔피언을 찾아보세요!**

<a href="https://www.lolrecs.com"><img src="./assets/lolrecsbanner.png" alt="www.lolrecs.com"></a>

<br>

## Feature🌟

1. 전적검색
<p align = "center">
<img src = "./assets/match_history.gif" width="700" height="350">
</p>



2. 실시간 밴픽 추천
- 밴픽창 화면 인식을 통해 플레이어에게 가장 적합한 챔피언을 추천해 드립니다.
<p align = "center">
<img src = "./assets/champion_rec.gif" width="700" height="350">
</p>



3. 아이템 추천
- 내 챔피언, 상대방의 챔피언 및 담당 포지션에 가장 적합한 아이템을 추천해 드립니다.
<p align = "center">
<img src = "./assets/item_rec.gif" width="700" height="350">
</p>




<br>

## MODEL🚀

1. 챔피언 분류 모델
<p align = "center">
 <img src="./assets/champ_class.png" width="680">
</p>

- 화면 인식기를 통해 현재 게임 창 이미지를 캡처해서 20명의 챔피언 이미지를 잘라내고, 이미지 분류 모델을 거쳐, 최종적으로 어떤 챔피언이 밴픽 되었는지 알아내는 모델입니다. 
- 이미지 분류 모델로는 잘 알려진 CNN을 사용하였고, 서버 통신 간 속도 저하를 최대한 막기 위해 층을 적게 쌓아 용량을 줄였습니다. 입력 데이터 이미지가 이미 정해진 기존 프로필 챔피언 이미지에서 크게 벗어나지 않기 때문에 가능했습니다.
- 훈련 데이터를 만들기 위해 imgaug 라이브러리를 이용해서, 기존 챔피언 프로필 이미지에 다양한 변형을 가하여 데이터를 증가시켰습니다. 웹페이지 이용자가 화면 인식 기능을 사용할 때, 다른 창이나 마우스 기호 등으로 인해 이미지 캡처가 정확히 이루어지지 않는 경우도 고려해 일부분을 마스킹 처리한 이미지도 포함하여 훈련했습니다.
<br/>

2. 챔피언 추천 모델
<p align = "center">
 <img src="./assets/champ_rec2.png" width="600" height="500">
</p>

- 밴픽은 플레이어들이 순차적으로 챔피언을 선택하는 과정으로, 챔피언을 추천하기 위해선 이전 플레이어가 선택한 챔피언이 다음 플레이어의 선택에 영향을 준다는 점과 선택된 챔피언들 간의 관계를 모두 고려해야 합니다. 
- 상대 팀과 내 팀이 픽한 챔피언을 하나의 시퀀스로 처리하여 다음에 선택할 챔피언을 예측하고, 플레이어의 챔피언별 숙련도를 반영하여 플레이어에게 적합한 챔피언을 포지션별로 추천합니다.
 <br/>  


3. 아이템 추천 모델
<p align = "center">
 <img src="./assets/item_rec.png" width="500">
</p>

- 사용자의 챔피언, 예상되는 상대 챔피언 그리고 포지션을 고려하여 아이템 조합을 추천합니다.
- 라이엇 Match v5 API로부터 수집한 raw 데이터를 [사용자 챔피언, 상대 챔피언, 사용자 챔피언이 사용한 아이템, 승리 여부]로 구성된 데이터로 재가공하였습니다.
- 챔피언이 사용한 아이템들에 대해서 등장 횟수, 승률 등을 고려하여 협업 필터링과 연관 규칙 학습을 활용한 통계 기반 모델입니다.
<br/>
  

<br>

## Architecture🔧

<p align = "center">
  <img src="./assets/ARCHI.png" width="90%">
</p>


<br>

## Members👨‍💻

<table align='center'>
  <tr height="110px">
    <td align="center" width="125px">
      <a href="https://github.com/Puer-Hyun"><img src="https://avatars.githubusercontent.com/Puer-Hyun"/></a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/ebbbi"><img src="https://avatars.githubusercontent.com/ebbbi"/></a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/Risk-boy"><img src="https://avatars.githubusercontent.com/Risk-boy"/></a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/serulean"><img src="https://avatars.githubusercontent.com/serulean"/></a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/Aiden-Jung"><img src="https://avatars.githubusercontent.com/Aiden-Jung"/></a>
  </tr>
  <tr height="50px">
    <td align="center" width="125px">
      <a href="https://github.com/Puer-Hyun">박성현</a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/ebbbi">강은비</a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/Risk-boy">김철현</a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/serulean">임서연</a>
    </td>
    <td align="center" width="125px">
      <a href="https://github.com/Aiden-Jung">정현석</a>
    </td>
  </tr>
  <tr>
    <td align="center">PM, DB<br/>BE, Modeling</td>
    <td align="center">Modeling<br/>DB</td>
    <td align="center">DB, BE<br/>Modeling</td>
    <td align="center">FE, UI/UX</br>Modeling</td>
    <td align="center">FE, BE</br>CI/CD</td>
  </tr>
</table>

