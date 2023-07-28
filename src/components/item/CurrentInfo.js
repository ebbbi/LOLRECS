"use client";

import styles from "./currentinfo.module.css";
import ChampBox from "./ItChampBox";
import ItemPick from '@/components/item/ItemPick'

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

import Top from "../../../public/position/top.svg"
import JUG from "../../../public/position/jug.svg"
import MID from "../../../public/position/mid.svg"
import ADC from "../../../public/position/adc.svg"
import SUP from "../../../public/position/sup.svg"


function CurrentInfo({ champData, api, champMap, selectedImage, selectedMenu }) {
  const [myChamp, setmyChamp] = useState(null);
  const [opChamp, setopchamp] = useState(null);
  const [curPosition, setcurposition] = useState(null);

  const [itemResult, setItemresult] = useState([])

  const SubmiItemData = () => {
    fetch(`https://www.lolrecs.com/api/get-item-data`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        my: myChamp,
        posi: curPosition,
        op: opChamp,
        })
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        console.log(response);
        return response.json();
      })
      .then((data) => {
        setItemresult(data["results"])
        console.log(itemResult);
      })
      .catch((error) => {
        console.error("Error:", error);
      }
    );
  };

  const handleMenuClick = (menuName) => {
    setcurposition(menuName);
  };

  const processeditemResult = itemResult ? itemResult : [];
  const twoList = processeditemResult.slice(0, 6);
  const threeList = processeditemResult.slice(6, 15);
  const fourList = processeditemResult.slice(15);

  return (
    <div className={styles.main}>
      <div className={styles.category}>
        <div className={styles.categoryBig}>
          나의 챔피언
          <div className={styles.categoryMiddle}>
            <ChampBox
              champ={myChamp}
              setChamp={setmyChamp}
              boxStyle={"profBox"}
              key={21}
              champData={champData}
              champMap={champMap}
            />
          </div>
        </div>

        <div className={styles.categoryBig}>
          상대 챔피언
          <div className={styles.categoryMiddleEnemy}>
            <ChampBox
              champ={opChamp}
              setChamp={setopchamp}
              boxStyle={"profBox"}
              key={23}
              champData={champData}
              champMap={champMap}
            />
          </div>
        </div>

        <div className={styles.categoryBig}>
          나의 포지션
          <ul className={styles.fiveMenu}>
            <li className={styles.posiItem}>
              <button 
                onClick={() => handleMenuClick('top')}
                className={curPosition === 'top' ? styles.activeMenu : styles.inactiveMenu}
              >
                <Top className={styles.posiIcon} />TOP
              </button>
            </li>
            <li className={styles.posiItem}>
              <button 
                onClick={() => handleMenuClick('jug')}
                className={curPosition === 'jug' ? styles.activeMenu : styles.inactiveMenu}
              >
                <JUG className={styles.posiIcon} />JUG
              </button>
            </li>
            <li className={styles.posiItem}>
              <button 
                onClick={() => handleMenuClick('mid')}
                className={curPosition === 'mid' ? styles.activeMenu : styles.inactiveMenu}
              >
                <MID className={styles.posiIcon} />MID
              </button>
            </li>
            <li className={styles.posiItem}>
              <button 
                onClick={() => handleMenuClick('adc')}
                className={curPosition === 'adc' ? styles.activeMenu : styles.inactiveMenu}
              >
                <ADC className={styles.posiIcon} />ADC
              </button>
            </li>
            <li className={styles.posiItem}>
              <button 
                onClick={() => handleMenuClick('sup')}
                className={curPosition === 'sup' ? styles.activeMenu : styles.inactiveMenu}
              >
                <SUP className={styles.posiIcon} />SUP
              </button>
            </li>
          </ul>
        </div>

      </div>

      <div className={styles.buttonArea}>
        <button className={styles.recButton} onClick={() => {SubmiItemData();}}>추천 받기</button>
      </div>

      <div className={styles.body}>
        <div className={styles.section}>
          <ItemPick two={twoList} three={threeList} four={fourList} />
        </div>
      </div>

    </div>
  );
}

export default CurrentInfo;