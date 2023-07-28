"use client";

import styles from "./itchampbox.module.css";
import { useState, useRef, useEffect } from "react";
import Select from "react-select";

function ChampBox({ champ, setChamp, boxStyle, champData, champMap }) {
  const champBoxRef = useRef(null);
  const [visible, setVisible] = useState(false);

  // const champOptions = champData.map((elt) => {
  //   return { value: elt, label: elt };
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
      backgroundColor: `#f1f1f1`,
      borderRadius: "6px",
      color: `#100F0F`,
      fontWeight: 700,
      fontSize: '15px',
      border: 0,
      boxShadow: "none",
    }),
    menu: (styles) => ({
      ...styles,
      backgroundColor: `#f1f1f1`,
      border: 0,
      fontSize: '15px',
    }),
    menuList: (styles) => ({
      ...styles,
      maxHeight: "200px",
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
        boxStyle == "profBox"
          ? styles.box
          : boxStyle == "item2Box"
          ? styles.item2Box
          : boxStyle == "item3Box"
          ? styles.item3Box
          : styles.item4Box
      }
      tabIndex="0"
      onFocus={onFocus}
      onBlur={onBlur}
    >
      
      {champ == 'None' || !champ ? (
        <div className={styles.empty} />
      ) : (
        <div className={styles.profCircle}>
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

      <p className={styles.champkorName}>{champMap[champ]}</p>
      <p className={styles.champengName}>{champ}</p>

    </div>
  );
}

export default ChampBox;
