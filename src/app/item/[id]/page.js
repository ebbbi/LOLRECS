import styles from "./page.module.css";
import Navbar from "@/components/layout/Navbar";
import CurrentInfo from '@/components/item/CurrentInfo'

import Curve from "../../../../public/curve.svg";
import Curveop from "../../../../public/curveop.svg";

async function getUserExists(summonerName) {
  const summonerInfoFetch = await fetch(
    `${process.env.API_ENDPOINT}/summoners/${summonerName}/exists`,
    {
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    }
  );

  if (!summonerInfoFetch.ok) {
    return {};
  }

  return summonerInfoFetch.json();
}

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
  const userExists = await getUserExists(params.id);
  const [champData, champMap] = await getChampData();

  return (
    <main className={`${styles.main}`}>
      <Navbar selectedPage="item" id={params.id} />

      {userExists.existence ? (
        <div className={styles.contents}>
          <div className={styles.header}>
            <div className={styles.title}>
              <Curve className={styles.curve} />
              <p>아이템 추천</p>
              <div className={styles.titleDesc}>
                <p>챔피언이 능력을 최대한 발휘하도록</p>
                <p>LOLRECS의 AI가 최적의 아이템을 추천해 드립니다.</p>
              </div>
              <Curveop className={styles.curve} />
            </div>
          </div>

          <CurrentInfo
            champData={champData} 
            api={process.env.API_ENDPOINT} 
            champMap={champMap}
          />

        </div>
      ) : (
        <div className={styles.notFound}>소환사를 찾을 수 없습니다.</div>
      )}
    </main>
  );
}
