import styles from './page.module.css'
import Logowords from "../../public/lolrecs_word.svg";
import Mainmenu from "@/components/home/Mainmenu";
import Searchform from "@/components/layout/Searchform";
import Link from "next/link";


export default function Home() {
  return (
    <main className={styles.main}>
      <div className={styles.content}>
        <Link href="/">
          <Logowords className={styles.logo} />
        </Link>
        <div className={styles.searchformContainer}>
          <Searchform navbar={false} selectedPage={"home"} />
        </div>
        <div className={styles.mainmenuContainer}>
          <Mainmenu />
        </div>
      </div>
    </main>
  );
}