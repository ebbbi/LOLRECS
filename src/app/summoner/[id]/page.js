import style from "./page.module.css";
import Navbar from "@/components/layout/Navbar";
import Profile from "@/components/summoner/profile/Profile";

async function getStaticData() {
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

  const itemsFetch = await fetch(
    `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json`,
    {
      cache: "force-cache",
      headers: {
        Accept: "application/json",
      },
    }
  );
  const items = await itemsFetch.json();

  const spellsFetch = await fetch(
    `https://ddragon.leagueoflegends.com/cdn/${versionData[0]}/data/en_US/summoner.json`,
    {
      cache: "force-cache",
      headers: {
        Accept: "application/json",
      },
    }
  );
  const spells = await spellsFetch.json();

  const runesFetch = await fetch(
    `https://ddragon.leagueoflegends.com/cdn/${versionData[0]}/data/en_US/runesReforged.json`,
    {
      cache: "force-cache",
      headers: {
        Accept: "application/json",
      },
    }
  );
  const runes = await runesFetch.json();

  const data = {
    version: versionData[0],
    items: items,
    spells: Object.values(spells.data),
    runes: runes,
  };

  return data;
}

async function getUserData(summonerName) {
  const summonerInfoFetch = await fetch(
    `${process.env.API_ENDPOINT}/summoners/${summonerName}`,
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

export default async function Page({ params }) {
  const staticData = await getStaticData();
  const userData = await getUserData(params.id);

  return (
    <>
      <Navbar selectedPage="summoner" id={params.id} />
      <main className={style.main}>
        <div className={style.summonerPageContainer}>
          {userData.summonerInfo ? (
            <Profile
              version={staticData.version}
              userData={userData.summonerInfo}
              rank={userData.rank}
              runes={staticData.runes}
              spells={staticData.spells}
              items={staticData.items}
            />
          ) : (
            <div className={style.notFound}>소환사를 찾을 수 없습니다.</div>
          )}
        </div>
      </main>
    </>
  );
}
