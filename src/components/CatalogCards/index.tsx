import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import data from '@site/src/data/catalogs.json';
import styles from './styles.module.css';

export default function CatalogCards(): ReactNode {
  return (
    <div className={styles.grid}>
      {data.catalogs.map((c) => (
        <Link key={c.href} to={c.href} className={styles.card}>
          <span className={styles.domain}>{c.domainLabel}</span>
          <span className={styles.title}>
            {translate({id: `catalogCards.title.${c.href}`, message: c.title})}
          </span>
          <span className={styles.meta}>
            <Translate id="catalogCards.meta" values={{patterns: c.patterns, groups: c.groups}}>
              {'{patterns} padrões · {groups} grupos'}
            </Translate>
          </span>
        </Link>
      ))}
    </div>
  );
}
