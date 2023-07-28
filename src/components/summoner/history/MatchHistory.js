import React from "react";
import MatchHistoryCard from "./MatchHistoryCard";

async function getMatches(summonerName) {
  const summonerInfoFetch = await fetch(
    `${process.env.API_ENDPOINT}/matches/${summonerName}/0/5`,
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

  return await summonerInfoFetch.json();
}

async function MatchHistory({ api, summonerInfo, rgn, runes, spells, items }) {
  const matchHistory = await getMatches(summonerInfo.name);

  return matchHistory.length === 0 ? null : (
    <MatchHistoryCard
      summonerInfo={summonerInfo}
      matchHistory={matchHistory["matchHistory"]}
      rgn={rgn}
      runes={runes}
      spells={spells}
      items={items}
    />
  );
}

export default MatchHistory;
