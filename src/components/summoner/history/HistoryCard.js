'use client'

import React, { useState } from 'react'
import style from './historycard.module.css'
import HistoryCardComplex from './HistoryCardComplex'
import HistoryCardSimple from './HistoryCardSimple'

function HistoryCard({ game, summonerInfo, runes, spells, items }) {
  const [open, setOpen] = useState(false)

  const clickArrow = () => {
    setOpen((prev) => !prev)
  }

  return (
    <div className={`${style.fadeIn}`}>
      <HistoryCardSimple open={open} game={game} clickArrow={clickArrow} />

      <HistoryCardComplex
        open={open}
        game={game}
        clickArrow={clickArrow}
        summonerInfo={summonerInfo}
        runes={runes}
        spells={spells}
        items={items}
      />
    </div>
  )
}

export default HistoryCard
