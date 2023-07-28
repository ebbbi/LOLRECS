import React from "react";
import style from "./summonercard.module.css";
import Image from "next/image";

function SummonerCard({ version, summonerInfo }) {
  return (
    <div className={`${style.container}`}>
      <div className={style.summonerCardContainer}>
        <img
          alt="profile icon"
          className={style.profileIcon}
          src={`https://ddragon.leagueoflegends.com/cdn/${version}/img/profileicon/${summonerInfo.profileIconId}.png`}
        />
        <div className={style.summonerName}>{summonerInfo.name}</div>
        <div className={style.summonerLevel}>Lv. {summonerInfo.summonerLevel}</div>
      </div>
    </div>
  );
}

export default SummonerCard;
