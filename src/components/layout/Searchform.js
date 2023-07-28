"use client";

import { useState } from "react";
import { AiOutlineSearch } from "react-icons/ai";
import style from "./searchform.module.css";
import { useRouter } from "next/navigation";

function Searchform({ id, navbar, selectedPage }) {
  const router = useRouter();

  const [inputValue, setInputValue] = useState(
    id == undefined ? "" : decodeURIComponent(id)
  );

  const handleChange = (e) => {
    setInputValue(e.target.value);
  };

  const redirect = () => {
    router.push(`/${selectedPage}/${inputValue}`);
  };

  const redirectEnter = () => {
    if (window.event.keyCode == 13) {
      if (selectedPage != "home") {
        router.push(`/${selectedPage}/${inputValue}`);
      }
    }
  };

  return (
    <div className={style.form}>
      <input
        className={navbar ? style.navbarinput : style.input}
        id="summonerName"
        spellCheck="false"
        autoComplete="off"
        type="text"
        placeholder="소환사 검색"
        name="summoner"
        value={inputValue}
        onChange={handleChange}
        onKeyUp={redirectEnter}
      />
      {navbar ? (
        <AiOutlineSearch className={style.logo} onClick={redirect} />
      ) : null}
    </div>
  );
}

export default Searchform;
