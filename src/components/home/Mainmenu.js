"use client";

import styles from "./mainmenu.module.css";
import HistoryLogo from "../../../public/history.svg";
import BanPickLogo from "../../../public/banpick.svg";
import ItemRuneLogo from "../../../public/item.svg";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

function Mainmenu({}) {
  const router = useRouter();

  const [element, setElement] = useState(null);

  useEffect(() => {
    setElement(document.getElementById("summonerName"));
  }, []);

  const redirectSummoner = () => {
    let summonerName = element.value;

    if (summonerName != "") {
      router.push(`/summoner/${summonerName}`);
    }
  };

  const redirectChampion = () => {
    let summonerName = element.value;

    if (summonerName != "") {
      router.push(`/banpick/${summonerName}`);
    }
  };

  const redirectItemRune = () => {
    let summonerName = element.value;

    if (summonerName != "") {
      router.push(`/item/${summonerName}`);
    }
  };

  return (
    <div className={styles.navigationContainer}>
      <div className={styles.navigationItemContainer}>
        <div className={styles.navigationBox}>
          <div
            className={styles.navigationBoxOverlap}
            onClick={redirectSummoner}
          />
          <HistoryLogo className={styles.logo} />
          <div className={styles.caption}>전적 검색</div>
        </div>
      </div>
      <div className={styles.navigationItemContainer}>
        <div className={styles.navigationBox}>
          <div
            className={styles.navigationBoxOverlap}
            onClick={redirectChampion}
          />
          <BanPickLogo className={styles.logo} />
          <div className={styles.caption}>실시간 밴픽 추천</div>
        </div>
      </div>
      <div className={styles.navigationItemContainer}>
        <div className={styles.navigationBox}>
          <div
            className={styles.navigationBoxOverlap}
            onClick={redirectItemRune}
          />
          <ItemRuneLogo className={styles.logo} />
          <div className={styles.caption}>아이템 추천</div>
        </div>
      </div>
    </div>
  );
}

export default Mainmenu;
