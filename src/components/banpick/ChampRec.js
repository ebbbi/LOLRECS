"use client";

import styles from "./champrec.module.css";

import BanChamp from "./BanChamp";
import PickChamp from "./PickChamp";
import ChampionPick from "./ChampionPick";
import ChampReader from "./ChampReader";

import React, { useState } from "react";

function ChampRec({ champData, champMap, username }) {
  const bans = Array.from({ length: 10 }, () => useState(null));
  const allies = Array.from({ length: 5 }, () => useState(null));
  const enemies = Array.from({ length: 5 }, () => useState(null));

  return (
    <>
      <ChampReader bans={bans} allies={allies} enemies={enemies} />
      <div className={styles.section}>
        <BanChamp bans={bans} champData={champData} champMap={champMap} />
      </div>
      <div className={styles.section}>
        <PickChamp
          allies={allies}
          enemies={enemies}
          champData={champData}
          champMap={champMap}
        />
      </div>
      <div className={styles.section}>
        <ChampionPick
          username={username}
          bans={bans}
          allies={allies}
          enemies={enemies}
          champMap={champMap}
        />
      </div>
    </>
  );
}

export default ChampRec;
