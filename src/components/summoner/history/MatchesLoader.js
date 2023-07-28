"use client";

import style from "./matchesloader.module.css";
import React, { useState } from "react";
import HistoryCard from "./HistoryCard";
import Spinner from "react-spinkit";

function MatchesLoader({ summonerInfo, runes, spells, items }) {
  const [matchHistory, setMatchHistory] = useState(null);
  const [matchesLoader, setMatchesLoader] = useState(false);
  const [count, setCount] = useState(1);

  const getMoreMatches = () => {
    setMatchesLoader(true);
    fetch(
      `https://www.lolrecs.com/api/matches/${summonerInfo.name}/${count * 5}/5`
    )
      .then((res) => res.json())
      .then((data) => {
        if (matchHistory == null) {
          setMatchHistory(data["matchHistory"]);
        } else {
          setMatchHistory(matchHistory.concat(data["matchHistory"]));
        }
        setCount(count + 1);
        setMatchesLoader(false);
      });
  };

  return (
    <>
      {matchHistory == null ? null : (
        <>
          {matchHistory.length > 0 && !matchHistory.includes(null)
            ? matchHistory.map((game, i) => {
                return (
                  <HistoryCard
                    key={(count - 1) * 5 + i}
                    game={game}
                    summonerInfo={summonerInfo}
                    runes={runes}
                    spells={spells}
                    items={items}
                  />
                );
              })
            : null}
        </>
      )}

      <button
        disabled={matchesLoader}
        className={style.moreMatchesContainer}
        onClick={getMoreMatches}
      >
        <span className={style.downarrow}>
          <i className="bi bi-caret-down-fill"></i>{" "}
        </span>
        더보기{" "}
        {matchesLoader && (
          <div>
            <Spinner
              style={{ marginLeft: "15px" }}
              color="#E2DCC8"
              name="circle"
              fadeIn="none"
            />
          </div>
        )}
      </button>
    </>
  );
}

export default MatchesLoader;
