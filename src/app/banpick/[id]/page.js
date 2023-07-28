import styles from "./page.module.css";
import Navbar from "@/components/layout/Navbar";
import ChampRec from "@/components/banpick/ChampRec";

import Curve from "../../../../public/curve.svg";
import Curveop from "../../../../public/curveop.svg";

async function getChampData() {
  const versionDataFetch = await fetch(
    "https://ddragon.leagueoflegends.com/api/versions.json",
    {
      cache: "force-cache",
      headers: {
        Accept: "application/json",
      },
    }
  );
  const versionData = await versionDataFetch.json();

  const champInfoKorFetch = await fetch(
    `https://ddragon.leagueoflegends.com/cdn/${versionData[0]}/data/ko_KR/champion.json`,
    {
      cache: "force-cache",
      headers: {
        Accept: "application/json",
      },
    }
  );
  const champInfoKorJSON = await champInfoKorFetch.json();
  const champInfoKor = Object.values(champInfoKorJSON)["3"];

  let champDataKor = [];
  let champMapKor = {};
  for (let i in champInfoKor) {
    champDataKor.push([i, champInfoKor[i]["name"]]);
    champMapKor[i] = champInfoKor[i]["name"];
  }

  return [
    champDataKor.sort((a, b) => (a[1] < b[1] ? -1 : a[1] == b[1] ? 0 : 1)),
    champMapKor,
  ];
}

export default async function Page({ params }) {
  const [champData, champMap] = await getChampData();

  return (
    <main className={`${styles.main}`}>
      <Navbar selectedPage="banpick" id={params.id} />

      <div className={styles.contents}>
        <div className={styles.header}>
          <div className={styles.title}>
            <Curve className={styles.curve} />
            <p>실시간 밴픽 추천</p>
            <div className={styles.titleDesc}>
              <p>실시간 화면을 바탕으로</p>
              <p>LOLRECS의 AI가 최적의 챔피언을 추천해 드립니다.</p>
            </div>
            <Curveop className={styles.curve} />
          </div>
        </div>

        <div className={styles.body}>
          <ChampRec  champData={champData} champMap={champMap} username={params.id}/>
        </div>
      </div>
    </main>
  );
}
