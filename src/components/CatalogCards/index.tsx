import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import data from '@site/src/data/catalogs.json';
import styles from './styles.module.css';

export default function CatalogCards(): ReactNode {
  return (
    <div className={styles.grid}>
      {data.catalogs.map((c) => (
        <Link key={c.href} to={c.href} className={styles.card}>
          <span className={styles.domain}>{c.domainLabel}</span>
          <span className={styles.title}>{c.title}</span>
          <span className={styles.meta}>
            {c.patterns} padrões · {c.groups} grupos
          </span>
        </Link>
      ))}
    </div>
  );
}
