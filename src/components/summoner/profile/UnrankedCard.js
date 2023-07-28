import React from 'react'
import style from './unrankedcard.module.css'
import Excla from "../../../../public/exclamation.svg";

function UnrankedCard({ queue }) {
  return (
    <div className={`${style.singleCardContainer}`}>
      <div style={{ width: '70px' }}>
        <div className={style.emblemBack}>
          <Excla
            alt='Unranked'
            className={style.emblemImage}
          />
        </div>
      </div>
      <div className={style.emblemContainer}>
        <span className={style.queue}>{queue}</span>
        <span className={style.rank}>UNRANKED</span>
        <span className={style.points}>{`0 LP`} </span>
        <div className={style.ratio}>
          <span> WIN / LOSE </span>
          <span className={style.win}>0</span>
          <span>-</span>
          <span className={style.loss}>0</span>
        </div>
      </div>
    </div>
  )
}

export default UnrankedCard
