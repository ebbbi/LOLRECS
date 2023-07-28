"use client";

import styles from "./bpchampbox.module.css";
import { useState, useRef, useEffect } from "react";
import Select from "react-select";

function ChampBox({ champ, setChamp, boxStyle, champData, champMap }) {
  const champBoxRef = useRef(null);
  const [visible, setVisible] = useState(false);

  // const champOptions = champData.map((elt) => {
  //   return { value: elt[0], label: elt[1] };
  // });

  const champOptions = [{ value: null, label: "선택 안 함" }].concat(
    champData.map((elt) => {
      return { value: elt[0], label: elt[1] };
    })
  );

  const onFocus = () => {
    setVisible(true);
  };

  const onBlur = () => {
    setVisible(false);
  };

  const onChange = (e) => {
    setChamp(e.value);
    setVisible(false);
  };

  useEffect(() => {
    if (champ) {
      setVisible(false);
    }
  }, [champ]);

  const colourStyles = {
    control: (styles) => ({
      ...styles,
      backgroundColor: `#E2DCC8`,
      borderRadius: "6px",
      color: `#100F0F`,
      fontWeight: 700,
      fontSize: "15px",
      border: 0,
      boxShadow: "none",
    }),
    menu: (styles) => ({
      ...styles,
      backgroundColor: `#E2DCC8`,
      border: 0,
      fontSize: "15px",
    }),
    menuList: (styles) => ({
      ...styles,
      maxHeight: "160px",
      overflowY: "auto",
      "&::-webkit-scrollbar": {
        width: "6px",
      },
      "&::-webkit-scrollbar-thumb": {
        backgroundColor: `rgba(16, 15, 15, 0.4)`,
        borderRadius: "8px",
      },
      "&::-webkit-scrollbar-thumb:hover": {
        backgroundColor: `rgba(16, 15, 15, 0.4)`,
      },
    }),
    option: (styles) => ({
      ...styles,
      backgroundColor: `transparent`,
      color: `#100F0F`,
      fontWeight: 700,
    }),
  };

  return (
    <div
      ref={champBoxRef}
      className={
        boxStyle == "box"
          ? styles.box
          : boxStyle == "allybox"
          ? styles.allybox
          : styles.enemybox
      }
      tabIndex="0"
      onFocus={onFocus}
      onBlur={onBlur}
    >

      {champ == "None" || !champ ? (
        <div className={styles.empty} />
      ) : (
        <div className={styles.champBox}>
          <img
            className={styles.img}
            src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/champion/${champ}.png`}
            alt={champ}
          />
        </div>
      )}
      {visible && (
        <Select
          className={styles.select}
          options={champOptions}
          isSearchable={true}
          onChange={onChange}
          value={
            champ ? { value: champMap[champ], label: champMap[champ] } : null
          }
          styles={colourStyles}
        ></Select>
      )}
    </div>
  );
}

export default ChampBox;
