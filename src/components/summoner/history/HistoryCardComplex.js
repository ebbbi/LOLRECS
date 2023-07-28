import React from 'react'
import style from './historycardcomplex.module.css'
import { IoIosArrowUp } from 'react-icons/io'
import ItemHistory from './ItemHistory'
import { useRouter } from "next/navigation";
import Image from "next/image";

const QUEUETYPE = {
  400: "norm", //Normal Draft Pick
  420: "solo",
  430: "norm",
  440: "flex",
  450: "aram",
  700: "clash",
  800: "ai", // Deprecated
  810: "ai", // Deprecated
  820: "ai", // Deprecated
  830: "ai",
  840: "ai",
  850: "ai",
  900: "urf",
  920: "poro",
  1020: "ofa",
  1300: "nbg",
  1400: "usb", // Ultimate Spellbook
  2000: "tut",
  2010: "tut",
  2020: "tut",
};

const ko = {
  solo: "솔로 랭크",
  norm: "일반 게임",
  aram: "칼바람",
  flex: "자유 랭크",
  nbg: "돌격 넥서스",
  urf: "우르프 대전",
  ofa: "단일 대전",
  ai: "AI 대전",
  poro: "포로왕",
  tut: "튜토리얼",
  etc: "기타",
  clash: "격전",
};


function HistoryCardComplex({
  open,
  game,
  clickArrow,
  summonerInfo,
  runes,
  spells,
  items,
}) {
  const router = useRouter();

  const position = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']

  // Filters out team one
  const teamOne = game.participants.filter((participant) => {
    return participant.teamId === 100
  })

  // Filters out team two
  const teamTwo = game.participants.filter((participant) => {
    return participant.teamId === 200
  })

  const sortTeam = (team) => {
    const sortedTeam = [...team]

    if (sortedTeam[0]?.individualPosition === 'Invalid') {
      return sortedTeam
    } else {
      sortedTeam.sort(
        (a, b) =>
          position.indexOf(a.teamPosition) - position.indexOf(b.teamPosition)
      )
    }
    return sortedTeam
  }

  const getPlayerName = (e) => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    })

    const summonerName = e.target.getAttribute('name')
    router.push(`/summoner/${summonerName}`)
  }

  return game.playerInfo && summonerInfo && runes && spells ? (
    <div
      className={`${open ? style.historyCardComplex : style.hideHistoryCard} ${
        game.playerInfo.win ? style.historyCardWin : style.historyCardLoss
      }`}>

      <div className={`${style.historyCard} `}>

        <div className={style.firstCol}>
          <p>
            {game.gameType === 'Ultimate Spellbook games'
              ? 'Ult Spellbook'
              : !game.gameType
              ? 'Custom Games'
              : game.gameType.split(' ').slice(0, 3).join(' ')}
          </p>
          <p>{game.playerInfo.win ? 'Victory' : 'Defeat'}</p>
          <p
            className={
              game.playerInfo.win ? style.subTextWin : style.subTextLoss
            }>
            {game.gameCreation.split(' ').slice(0, 4).join(' ')}
          </p>

          <p
            className={
              game.playerInfo.win ? style.subTextWin : style.subTextLoss
            }>
            {JSON.stringify(game.gameDuration).length <= 4
              ? `${Math.floor(game.gameDuration / 60)}m ${Math.floor(
                  game.gameDuration % 60
                )}s `
              : `${Math.floor(game.gameDuration / 1000 / 60)}m ${Math.floor(
                  game.gameDuration % 60
                )}s `}
          </p>
        </div>
        

        <div className={style.secondCol}>
          <div className={style.secondCard}>
            <div className={style.imageContainer}>
              <div className={style.championImg}>
                <img
                  className={style.secondColImg}
                  alt={game.championImage}
                  src={`https://ddragon.leagueoflegends.com/cdn/${game.gameVersion}.1/img/champion/${game.championImage}`}
                />
              </div>

              <div className={style.summonerSpellContainer}>
                {spells.map(
                  (spell, i) =>
                    +spell.key === game.playerInfo.summoner1Id && (
                        <img
                          alt={spell.name}
                          className={style.summonerSpell}
                          src={`https://ddragon.leagueoflegends.com/cdn/${game.gameVersion}.1/img/spell/${spell.id}.png`}
                        />
                    )
                )}

                {spells.map(
                  (spell, i) =>
                    +spell.key === game.playerInfo.summoner2Id && (
                        <img
                          key={i}
                          alt={spell.name}
                          className={style.summonerSpell2}
                          src={`https://ddragon.leagueoflegends.com/cdn/${game.gameVersion}.1/img/spell/${spell.id}.png`}
                        />
                    )
                )}
              </div>
              <div className={style.summonerSpellContainer}>
                {runes
                  .filter((rune) => {
                    return rune.id === game.playerInfo.perks.styles[0].style
                  })
                  .map((rune, i) => {
                    const perk0 =
                      game.playerInfo.perks.styles[0].selections[0].perk
                    const perkImage = rune.slots[0].runes.filter((perk) => {
                      return perk.id === perk0
                    })
                    return (
                        <img
                          alt='runes'
                          className={style.summonerSpell}
                          src={`https://raw.communitydragon.org/${
                            game.gameVersion
                          }/plugins/rcp-be-lol-game-data/global/default/v1/${perkImage[0].icon.toLowerCase()}`}
                        />
                    )
                  })}

                {runes
                  .filter((rune) => {
                    return rune.id === game.playerInfo.perks.styles[1].style
                  })
                  .map((rune, i) => (
                      <img
                        alt='summoner spell'
                        className={style.summonerSpell2}
                        src={`https://raw.communitydragon.org/${
                          game.gameVersion
                        }/plugins/rcp-be-lol-game-data/global/default/v1/${rune.icon.toLowerCase()}`}
                      />
                  ))}
              </div>
            </div>
            <div className={style.championName}>{game.championName}</div>
          </div>
        </div>


        <div className={style.thirdCol}>
          <div>
            {(
              (game.playerInfo.kills + game.playerInfo.assists) /
              (game.playerInfo.deaths === 0 ? 1 : game.playerInfo.deaths)
            ).toFixed(2)}
            :1 KDA
          </div>
          <div className={style.killDeathAssists}>
            {`${game.playerInfo.kills} /
              ${game.playerInfo.deaths} /
              ${game.playerInfo.assists}`}
          </div>
          {game.playerInfo.largestMultiKill <= 1 ? (
            ''
          ) : (
            <div className={style.kdaRatio}>
              {game.playerInfo.largestMultiKill === 2
                ? 'Double Kill'
                : game.playerInfo.largestMultiKill === 3
                ? 'Triple Kill'
                : game.playerInfo.largestMultiKill === 4
                ? 'Quadra Kill'
                : 'Penta Kill'}
            </div>
          )}
        </div>


        <div className={style.fourthCol}>
          <span className={style.level}>
            Lv. {game.playerInfo.champLevel}
          </span>
            <div className={style.minionContainer}>
              <img
                className={style.minionIcon}
                alt='minion icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621958945/league-stats/role%20icons/Minion_icon_tgeisg.png'
              />
              <span className={style.minions}>
                {game.playerInfo.totalMinionsKilled +
                  game.playerInfo.neutralMinionsKilled}{' '}
              </span>
            </div>
            <span className={style.level}>
              {JSON.stringify(game.gameDuration).length <= 4
                ? (
                    ((game.playerInfo.totalMinionsKilled +
                      game.playerInfo.neutralMinionsKilled) /
                      game.gameDuration) *
                    60
                  ).toFixed(1)
                : (
                    ((game.playerInfo.totalMinionsKilled +
                      game.playerInfo.neutralMinionsKilled) /
                      game.gameDuration) *
                    60 *
                    1000
                  ).toFixed(1)}
              cs/min
            </span>
        </div>

        <div className={style.fifthCol}>
          <ItemHistory details={game.playerInfo} items={items}/>
        </div>

        <IoIosArrowUp className={style.sixthCol} onClick={clickArrow} />

      </div>

      <div className={game.playerInfo.win ? style.lineWin : style.lineLoss} />
      
      <div className={style.historyCard2}>
        <div className={style.statsContainer}>
          {sortTeam(teamOne).map((player, i) => {
            return (
              <div
                key={i}
                className={
                  game.playerInfo.win ? style.team100Win : style.team100Loss
                }>
                <div>{`${player.kills} / ${player.deaths} / ${player.assists}`}</div>

                <div>
                  {JSON.stringify(game.gameDuration).length <= 4
                    ? (
                        ((player.totalMinionsKilled +
                          player.neutralMinionsKilled) /
                          game.gameDuration) *
                        60
                      ).toFixed(1)
                    : (
                        ((player.totalMinionsKilled +
                          player.neutralMinionsKilled) /
                          game.gameDuration) *
                        60 *
                        1000
                      ).toFixed(1)}
                  cs/min
                </div>
              </div>
            )
          })}
        </div>


        <div className={style.sixthCard}>
          {sortTeam(teamOne).map((player, i) => (
            <div name={player.summonerName} className={style.col1} key={i}>
              <span
                onClick={
                  player.summonerName === summonerInfo.name
                    ? null
                    : getPlayerName
                }
                className={
                  summonerInfo.name
                    ? player.summonerName === summonerInfo.name
                      ? style.summonerName1
                      : style.name1
                    : style.name1
                }
                name={player.summonerName}
                region={game.platformId}>
                {player.summonerName.replace(/\s/g, '')}
              </span>
              <img
                name={player.summonerName}
                alt={player.image}
                src={`https://ddragon.leagueoflegends.com/cdn/${
                  game.gameVersion
                }.1/img/champion/${
                  player.championName === 'FiddleSticks'
                    ? 'Fiddlesticks'
                    : player.championName
                }.png`}
              />
            </div>
          ))}
        </div>


        <div className={style.iconContainer}>
          {game.gameType === '5v5 ARAM games' ? (
            <>
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/flairs/poro_happy_taunt_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/flairs/poro_happy_cheers_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/flairs/em_poro_buddies_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/rewards/essence/essence_poro_tier_1_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/rewards/essence/essence_poro_tier_2_selector.png'
                }
              />
            </>
          ) : game.gameType === 'URF games' ? (
            <>
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee_lubzjx.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee2_qace59.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee3_vu2ogp.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee4_r6vdvz.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee5_eikten.png'
              />
            </>
          ) : game.gameType === '5v5 Ranked Solo games' ||
            game.gameType === '5v5 Draft Pick games' ||
            game.gameType === '5v5 Ranked Flex games' ||
            game.gameType === '5v5 Blind Pick games' ? (
            <>
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898819/league-stats/role%20icons/Top_icon_reqrfv.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Jungle_icon_zde7ju.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Middle_icon_etwa26.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Bottom_icon_zkoaud.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Support_icon_h6uicp.png'
              />
            </>
          ) : (
            Array.from({ length: 5 }).map((num, i) => <h3 key={i}>-</h3>)
          )}
        </div>

        <div className={style.line2} />

        <div className={style.iconContainer2}>
          {game.gameType === '5v5 ARAM games' ? (
            <>
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/flairs/poro_happy_taunt_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/flairs/poro_happy_cheers_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/flairs/em_poro_buddies_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/rewards/essence/essence_poro_tier_1_selector.png'
                }
              />
              <img
                alt='poro'
                src={
                  'https://raw.communitydragon.org/10.1/game/assets/loadouts/summoneremotes/rewards/essence/essence_poro_tier_2_selector.png'
                }
              />
            </>
          ) : game.gameType === 'URF games' ? (
            <>
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee_lubzjx.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee2_qace59.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee3_vu2ogp.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee4_r6vdvz.png'
              />
              <img
                alt='manatee urf'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/manatee5_eikten.png'
              />
            </>
          ) : game.gameType === '5v5 Ranked Solo games' ||
            game.gameType === '5v5 Draft Pick games' ||
            game.gameType === '5v5 Ranked Flex games' ||
            game.gameType === '5v5 Blind Pick games' ? (
            <>
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898819/league-stats/role%20icons/Top_icon_reqrfv.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Jungle_icon_zde7ju.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Middle_icon_etwa26.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Bottom_icon_zkoaud.png'
              />
              <img
                alt='icon'
                src='https://res.cloudinary.com/mistahpig/image/upload/v1621898818/league-stats/role%20icons/Support_icon_h6uicp.png'
              />
            </>
          ) : (
            Array.from({ length: 5 }).map((num, i) => <h3 key={i}>-</h3>)
          )}
        </div>


        <div className={style.seventhCard}>
          {sortTeam(teamTwo).map((player, i) => (
            <div name={player.summonerName} className={style.col2} key={i}>
              <img
                name={player.summonerName}
                alt={`${player.championName}.png`}
                src={`https://ddragon.leagueoflegends.com/cdn/${
                  game.gameVersion
                }.1/img/champion/${
                  player.championName === 'FiddleSticks'
                    ? 'Fiddlesticks'
                    : player.championName
                }.png`}
              />
              <span
                onClick={
                  player.summonerName === summonerInfo.name
                    ? null
                    : getPlayerName
                }
                className={
                  summonerInfo.name
                    ? player.summonerName === summonerInfo.name
                      ? style.summonerName2
                      : style.name2
                    : style.name2
                }
                region={game.platformId}
                name={player.summonerName}>
                {player.summonerName.replace(/\s/g, '')}
              </span>
            </div>
          ))}
        </div>

        
        <div className={style.statsContainer2}>
          {sortTeam(teamTwo).map((player, i) => {
            return (
              <div
                key={i}
                className={
                  game.playerInfo.win ? style.team200Win : style.team200Loss
                }>
                <div>
                  {JSON.stringify(game.gameDuration).length <= 4
                    ? (
                        ((player.totalMinionsKilled +
                          player.neutralMinionsKilled) /
                          game.gameDuration) *
                        60
                      ).toFixed(1)
                    : (
                        ((player.totalMinionsKilled +
                          player.neutralMinionsKilled) /
                          game.gameDuration) *
                        60 *
                        1000
                      ).toFixed(1)}
                  cs/min
                </div>
                <div>{`${player.kills} / ${player.deaths} / ${player.assists}`}</div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  ) : null
}

export default HistoryCardComplex
