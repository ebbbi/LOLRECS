"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import style from "./choosechamp.module.css";
import CurrentInfo from "@/components/item/CurrentInfo";

import Top from "../../../public/position/top.svg";
import JUG from "../../../public/position/jug.svg";
import MID from "../../../public/position/mid.svg";
import ADC from "../../../public/position/adc.svg";
import SUP from "../../../public/position/sup.svg";

function ChooseChamp({ recResult, champMap }) {
  const [selectedMenu, setSelectedMenu] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [showImageDetails, setShowImageDetails] = useState(false);


  const resultPack = {
    top: recResult[0],
    jug: recResult[1],
    mid: recResult[2],
    adc: recResult[3],
    sup: recResult[4],
  };
  console.log(resultPack);

  const handleMenuClick = (menuName) => {
    if (resultPack) {
      setSelectedMenu(menuName);
      setSelectedImage(resultPack[menuName]);
      setShowImageDetails(false);
    }
  };

  const handleImageClick = (name) => {
    setSelectedImage(name);
    setShowImageDetails(false);
  };

  const images = recResult || [];

  const champ0 = selectedImage && resultPack[selectedMenu][0];
  const champ1 = selectedImage && resultPack[selectedMenu][1];
  const champ2 = selectedImage && resultPack[selectedMenu][2];


  // const sendChampPosition = () => {
  //   if (selectedImage && selectedMenu) {
  //     const routeAddress = `/item/${summoner}?selectedImage=${encodeURIComponent(selectedImage)}&selectedMenu=${encodeURIComponent(selectedMenu)}`;

  //     router.push(routeAddress);
  //   }
  // };

  return (
    <div className={style.main}>
      <ul className={style.fiveMenu}>
        <li className={style.posiItem}>
          <button
            onClick={() => handleMenuClick("top")}
            className={
              selectedMenu === "top" ? style.activeMenu : style.inactiveMenu
            }
          >
            <Top className={style.posiIcon} />
            TOP
          </button>
        </li>
        <li className={style.posiItem}>
          <button
            onClick={() => handleMenuClick("jug")}
            className={
              selectedMenu === "jug" ? style.activeMenu : style.inactiveMenu
            }
          >
            <JUG className={style.posiIcon} />
            JUG
          </button>
        </li>
        <li className={style.posiItem}>
          <button
            onClick={() => handleMenuClick("mid")}
            className={
              selectedMenu === "mid" ? style.activeMenu : style.inactiveMenu
            }
          >
            <MID className={style.posiIcon} />
            MID
          </button>
        </li>
        <li className={style.posiItem}>
          <button
            onClick={() => handleMenuClick("adc")}
            className={
              selectedMenu === "adc" ? style.activeMenu : style.inactiveMenu
            }
          >
            <ADC className={style.posiIcon} />
            ADC
          </button>
        </li>
        <li className={style.posiItem}>
          <button
            onClick={() => handleMenuClick("sup")}
            className={
              selectedMenu === "sup" ? style.activeMenu : style.inactiveMenu
            }
          >
            <SUP className={style.posiIcon} />
            SUP
          </button>
        </li>
      </ul>

      <div className={style.selectChamp}>
        {images.length === 0 ? (
          <p className={style.noImage}>'챔피언 추천받기' 버튼을 눌러주세요.</p>
        ) : selectedMenu === null ? (
          <p className={style.noImageBright}>
            포지션을 선택하시면 3명의 추천 챔피언을 보실 수 있습니다.
          </p>
        ) : (
          <>
            <div className={style.champImgContainer}>
              {champ0 === "None" ? (
                <div className={style.empty} />
              ) : (
                <div
                  className={
                    selectedImage === champ0 ? style.recChamp : style.unrecChamp
                  }
                  onClick={() => handleImageClick(champ0)}
                >
                  <div className={style.champImg}>
                    <img
                      src={`http://ddragon.leagueoflegends.com/cdn/img/champion/loading/${champ0}_0.jpg`}
                      alt={`Image ${champ0}`}
                      className={style.ChampImage}
                    />
                  </div>
                  <div className={style.champName}>
                    <div className={style.champKorName}> {champMap[champ0]} </div>
                    <div className={style.champEngName}> {champ0} </div>
                  </div>
                </div>
              )}
            </div>

            <div className={style.champImgContainer}>
              {!champ1 || champ1 === "None" ? (
                <div className={style.empty} />
              ) : (
                <div
                  className={
                    selectedImage === champ1 ? style.recChamp : style.unrecChamp
                  }
                  onClick={() => handleImageClick(champ1)}
                >
                  <div className={style.champImg}>
                    <img
                      src={`http://ddragon.leagueoflegends.com/cdn/img/champion/loading/${champ1}_0.jpg`}
                      alt={`Image ${champ1}`}
                      className={style.ChampImage}
                    />
                  </div>
                  <div className={style.champName}>
                    <div className={style.champKorName}> {champMap[champ1]} </div>
                    <div className={style.champEngName}> {champ1} </div>
                  </div>
                </div>
              )}
            </div>

            <div className={style.champImgContainer}>
              {!champ2 || champ2 === "None" ? (
                <div className={style.empty} />
              ) : (
                <div
                  className={
                    selectedImage === champ2 ? style.recChamp : style.unrecChamp
                  }
                  onClick={() => handleImageClick(champ2)}
                >
                  <div className={style.champImg}>
                    <img
                      src={`http://ddragon.leagueoflegends.com/cdn/img/champion/loading/${champ2}_0.jpg`}
                      alt={`Image ${champ2}`}
                      className={style.ChampImage}
                    />
                  </div>
                  <div className={style.champName}>
                    <div className={style.champKorName}> {champMap[champ2]} </div>
                    <div className={style.champEngName}> {champ2} </div>
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>

      <div className={style.body}>
        {/* <div className={style.buttonArea}>
          <div className={style.canChange}>
            {selectedImage &&
              !showImageDetails &&
              "* 다음 페이지에서 선택한 챔피언을 변경할 수 있습니다."}
          </div>
          <div>
            <button
              onClick={sendChampPosition}
              className={style.itemRecButtonBefore}
            >
              {selectedImage &&
                !showImageDetails && <CurrentInfo selectedImage={selectedImage} selectedMenu={selectedMenu} /> && (
                  <a className={style.itemRecButton}>
                    아이템 추천 받기
                  </a>
                )}
            </button>
          </div>
        </div> */}
      </div>

    </div>
  );
}

export default ChooseChamp;
