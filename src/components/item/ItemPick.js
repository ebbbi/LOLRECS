import styles from "./itempick.module.css";

function ItemPick({ two, three, four }) {

  const images = two || [];

  const twoon = two.slice(0,2);
  const twotw = two.slice(2,4);
  const twoth = two.slice(4);

  const thron = three.slice(0,3);
  const thrtw = three.slice(3,6);
  const thrth = three.slice(6);

  const fouron = four.slice(0,4);
  const fourtw = four.slice(4,8);
  const fourth = four.slice(8);


  return (
    <div className={styles.main}>
      <div className={styles.parent}>
        <h2 className={styles.h2}>2개</h2>
        { images.length === 0 ? (
          <div className={styles.empty} />
        ) : (
          <>
            <div className={styles.middleone}>
              {twoon.map((ent, i) => (
                <div className={styles.box}>
                    <img 
                      src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                      alt={`Image ${ent}`}
                      className={styles.itemImage}
                      key={i}
                    />
                  </div>
              ))}
            </div>
            <hr />
            <div className={styles.middleone}>
              {twotw.map((ent, i) => (
                <div className={styles.box}>
                  <img 
                    src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                    alt={`Image ${ent}`}
                    className={styles.itemImage}
                    key={i+2}
                  />
                </div>
              ))}
            </div>
            <hr />
            <div className={styles.middleone}>
              {twoth.map((ent, i) => (
                <div className={styles.box}>
                  <img 
                    src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                    alt={`Image ${ent}`}
                    className={styles.itemImage}
                    key={i+4}
                  />
                </div>
              ))}
            </div>
          </>
        )}
      </div>


      <div className={styles.parent}>
        <h2 className={styles.h2}>3개</h2>
        { images.length === 0 ? (
          <div className={styles.empty} />
        ) : (
          <>
            <div className={styles.middletwo}>
              {thron.map((ent, i) => (
                <div className={styles.box}>
                    <img 
                      src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                      alt={`Image ${ent}`}
                      className={styles.itemImage}
                      key={i+6}
                    />
                  </div>
              ))}
            </div>
            <hr />
            <div className={styles.middletwo}>
              {thrtw.map((ent, i) => (
                <div className={styles.box}>
                  <img 
                    src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                    alt={`Image ${ent}`}
                    className={styles.itemImage}
                    key={i+9}
                  />
                </div>
              ))}
            </div>
            <hr />
            <div className={styles.middletwo}>
              {thrth.map((ent, i) => (
                <div className={styles.box}>
                  <img 
                    src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                    alt={`Image ${ent}`}
                    className={styles.itemImage}
                    key={i+12}
                  />
                </div>
              ))}
            </div>
          </>
        )}
      </div>


      <div className={styles.parent}>
        <h2 className={styles.h2}>4개</h2>
        { images.length === 0 ? (
          <div className={styles.empty} />
        ) : (
          <>
            <div className={styles.middlethree}>
              {fouron.map((ent, i) => (
                <div className={styles.box}>
                    <img 
                      src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                      alt={`Image ${ent}`}
                      className={styles.itemImage}
                      key={i+15}
                    />
                  </div>
              ))}
            </div>
            <hr />
            <div className={styles.middlethree}>
              {fourtw.map((ent, i) => (
                <div className={styles.box}>
                  <img 
                    src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                    alt={`Image ${ent}`}
                    className={styles.itemImage}
                    key={i+19}
                  />
                </div>
              ))}
            </div>
            <hr />
            <div className={styles.middlethree}>
              {fourth.map((ent, i) => (
                <div className={styles.box}>
                  <img 
                    src={`http://ddragon.leagueoflegends.com/cdn/13.14.1/img/item/${ent}.png`}
                    alt={`Image ${ent}`}
                    className={styles.itemImage}
                    key={i+23}
                  />
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ItemPick;