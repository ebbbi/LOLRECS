import styles from "./pickchamp.module.css";
import ChampBox from "./BPChampBox";

function PickChamp({ allies, enemies, champData, champMap }) {
  return (
    <div className={styles.main}>
      <h1 className={styles.h1}>
        픽 Pick
        <span className={styles.h1Desc}>사진을 눌러 수정할 수 있습니다.</span>
      </h1>
      <div className={styles.pickAlly}>
        {allies.map((elt, i) => (
          <ChampBox
            champ={elt[0]}
            setChamp={elt[1]}
            boxStyle={"allybox"}
            key={i + 10}
            champData={champData}
            champMap={champMap}
          />
        ))}
        <div className={styles.allytext}>나의 팀</div>
      </div>
      <div className={styles.pickEnemy}>
        {enemies.map((elt, i) => (
          <ChampBox
            champ={elt[0]}
            setChamp={elt[1]}
            boxStyle={"enemybox"}
            key={i + 15}
            champData={champData}
            champMap={champMap}
          />
        ))}
        <div className={styles.enemytext}>상대 팀</div>
      </div>
    </div>
  );
}

export default PickChamp;
