import style from "./profile.module.css";
import SummonerCard from "./SummonerCard";
import RankCard from "./RankCard";
import UnrankedCard from "./UnrankedCard";
import MatchHistory from "../history/MatchHistory";
import Lolrecscross from "../../../../public/lolrecscross.svg";

function Profile({ version, userData, rank, region, runes, spells, items }) {
  return (
    <>
      <div className={style.rowContainer}>
        <div className={style.row1}>
          <div className={style.emblemContainer}>
            <div className={style.nameLive}>
              <SummonerCard version={version} summonerInfo={userData} />
            </div>

            <div className={style.rankCardContainer}>
              <div className={style.rankContainer}>
                {(rank && !rank.length) ||
                (rank.length === 1 &&
                  rank[0].queueType === "RANKED_FLEX_SR") ? (
                  <UnrankedCard queue="Solo" />
                ) : (
                  rank.map((ranking, i) => {
                    return ranking.queueType === "RANKED_SOLO_5x5" ? (
                      <RankCard key={i} rank={ranking} queue="Solo" />
                    ) : (
                      ranking.queueType === "RANKED_FLEX_SR" && ""
                    );
                  })
                )}

                <Lolrecscross alt="Unranked" className={style.crosssymbol} />

                {(rank && !rank.length) ||
                (rank.length === 1 &&
                  rank[0].queueType === "RANKED_SOLO_5x5") ? (
                  <UnrankedCard queue="Flex" />
                ) : (
                  rank.map((ranking, i) => {
                    return ranking.queueType === "RANKED_FLEX_SR" ? (
                      <RankCard key={i} rank={ranking} queue="Flex" />
                    ) : (
                      ranking.queueType === "RANKED_SOLO_5x5" && ""
                    );
                  })
                )}
              </div>
            </div>
          </div>
        </div>

        <div className={style.row3}>
          <MatchHistory
            summonerInfo={userData}
            rgn={region}
            runes={runes}
            spells={spells}
            items={items}
          />
        </div>
      </div>
    </>
  );
}

export default Profile;
