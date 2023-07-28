import styles from "./banchamp.module.css";
import ChampBox from "./BPChampBox";

function BanChamp({ bans, champData, champMap }) {
  return (
    <div className={styles.main}>
      <h1 className={styles.h1}>
        밴 Ban
        <span className={styles.h1Desc}>사진을 눌러 수정할 수 있습니다.</span>
      </h1>
      <div className={styles.parent}>
        {bans.map((elt, i) => (
          <ChampBox
            champ={elt[0]}
            setChamp={elt[1]}
            boxStyle={"box"}
            key={i}
            champData={champData}
            champMap={champMap}
          />
        ))}
      </div>
    </div>
  );
}

export default BanChamp;
