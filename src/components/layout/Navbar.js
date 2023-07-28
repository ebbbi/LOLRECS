"use client";

import style from "./navbar.module.css";
import Logo from "../../../public/lolrecs.svg";
import Searchform from "./Searchform";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";


function Navbar({ selectedPage, id }) {
  const router = useRouter();

  const [element, setElement] = useState(null);

  useEffect(() => {
    setElement(document.getElementById("summonerName"));
  }, []);

  const redirectHome = () => {
    router.push(`/`);
  };

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
    <nav className={style.navbar}>
      <div className={style.navHeaderContainer}>
        <div className={style.navHeader}>
          <Logo className={style.logo} onClick={redirectHome} />
          <div className={style.Searchform}>
            <Searchform id={id} navbar={true} selectedPage={selectedPage} />
          </div>
        </div>
      </div>
      <ul className={style.navMenu}>
        <li className={style.navItem}>
          <div
            onClick={redirectSummoner}
            className={
              selectedPage == "summoner"
                ? style.navLinksSelected
                : style.navLinks
            }
          >
            전적 검색
          </div>
        </li>
        <li className={style.navItem}>
          <div
            onClick={redirectChampion}
            className={
              selectedPage == "banpick"
                ? style.navLinksSelected
                : style.navLinks
            }
          >
            실시간 밴픽 추천
          </div>
        </li>
        <li className={style.navItem}>
          <div
            onClick={redirectItemRune}
            className={
              selectedPage == "item"
                ? style.navLinksSelected
                : style.navLinks
            }
          >
            아이템 추천
          </div>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
