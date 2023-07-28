import style from "./matchhistorycard.module.css";
import { CgSmileSad } from "react-icons/cg";
import HistoryCard from "./HistoryCard";
import MatchesLoader from "./MatchesLoader";

function MatchHistoryCard({
  summonerInfo,
  matchHistory,
  runes,
  spells,
  items,
}) {
  const refreshPage = () => window.location.reload();

  return (
    <div className={style.matchContainer}>
      <div>
        {matchHistory.length > 0 && !matchHistory.includes(null) ? (
          matchHistory
            .sort((a, b) => new Date(b.gameCreation) - new Date(a.gameCreation))
            .map((game, i) => {
              return (
                <HistoryCard
                  key={i}
                  game={game}
                  summonerInfo={summonerInfo}
                  runes={runes}
                  spells={spells}
                  items={items}
                />
              );
            })
        ) : (
          <div className={style.noMatchContainer}>
            <div className={style.noMatches}>
              {matchHistory.length === 0 ? (
                "기록된 전적이 없습니다."
              ) : (
                <div className={style.failedMatchContainer}>
                  <div className={style.failedMatch}>
                    전적을 불러오는데 실패하였습니다.
                    <CgSmileSad className={style.sad} />
                  </div>
                  <button className={style.retry} onClick={refreshPage}>
                    재시도
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
        {matchHistory.length < 5 ? null : (
          <MatchesLoader
            summonerInfo={summonerInfo}
            runes={runes}
            spells={spells}
            items={items}
          />
        )}
      </div>
    </div>
  );
}

export default MatchHistoryCard;
