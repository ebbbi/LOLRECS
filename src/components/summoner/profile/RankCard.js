import React from "react";
import style from "./rankcard.module.css";
import Image from "next/image";

function RankCard({ rank, queue }) {

  const changeColor = () => {
    if (rank.tier === "IRON") {
      return "#815F5E";
    } else if (rank.tier === "BRONZE") {
      return "#A77157";
    } else if (rank.tier === "SILVER") {
      return "#87a1a8";
    } else if (rank.tier === "GOLD") {
      return "#fcdd7e";
    } else if (rank.tier === "PLATINUM") {
      return "#82b8b5";
    } else if (rank.tier === "EMERALD") {
      return "#7BDEB1";
    } else if (rank.tier === "DIAMOND") {
      return "#7daef5";
    } else if (rank.tier === "MASTER") {
      return "#bfaae6";
    } else if (rank.tier === "GRANDMASTER") {
      return "#fca9bb";
    } else  {
      return "#97eafc";
    }
  }
  

  return (
    <div className={`${style.singleCardContainer}`}>
      <div style={{ width: "70px" }}>
        <div className={style.emblemBack} style={{backgroundColor: changeColor()}}>
          <img
            alt={rank.tier}
            className={style.emblemImage}
            src={`https://raw.githubusercontent.com/InFinity54/LoL_DDragon/master/extras/tier/${rank.tier.toLowerCase()}.png`}
          />
        </div>
      </div>
      <div className={style.emblemContainer}>
        <span className={style.queue}>{queue}</span>
        <span className={style.rank} style={{color: changeColor()}}>
          {`${rank.tier} ${rank.rank} `}
        </span>{" "}
        <span className={style.points}>{`${rank.leaguePoints} LP`} </span>
        <div className={style.ratio}>
          <span> WIN / LOSE </span>
          <span className={style.win}>{rank.wins}</span>
          <span>-</span>
          <span className={style.loss}>{rank.losses}</span>
        </div>
      </div>
    </div>
  );
}

export default RankCard;
