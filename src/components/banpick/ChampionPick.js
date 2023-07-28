"use client";

import React, { useState } from "react";
import styles from "./championpick.module.css";
import Choosechamp from "@/components/banpick/ChooseChamp";

function ChampionPick({ username, bans, allies, enemies, champMap }) {
  const [recResult, setrecresult] = useState([]);

  const Submitchampdata = () => {
    fetch(`https://www.lolrecs.com/api/get-pick-data`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        bans: bans.map((banState) => banState[0]),
        allies: allies.map((allyState) => allyState[0]),
        enemies: enemies.map((enemyState) => enemyState[0]),
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        console.log(response);
        return response.json();
      })
      .then((data) => {
        setrecresult(data["results"]);
        console.log(recResult);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className={styles.main}>
      <div>
        <h1 className={styles.h1}>
          챔피언 추천
          <span className={styles.h1Desc}>
            포지션 별 최적의 챔피언을 추천해 드립니다.
          </span>
          <button
            className={styles.champRecButton}
            onClick={() => {
              Submitchampdata();
            }}
          >
            챔피언 추천받기
            <span className={styles.refreshIcon}>
              <i className="bi bi-arrow-clockwise" />
            </span>
          </button>
        </h1>
        <div className={styles.positionMenu}>
          <Choosechamp recResult={recResult} champMap={champMap} />
        </div>
      </div>
    </div>
  );
}

export default ChampionPick;
