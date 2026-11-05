import { describe, expect, it } from 'vitest'
import {
  FILTRES_DEFAUT, depuisParams, filtrer, lignesPeriode, periodesProposees, signal, trier, versParams,
} from './classement'
import { duree, mois, pct, periodeTexte, points } from './format'
import type { Classement, Liaison, LigneScore, Meta } from './types'

function liaison(id: string, extra: Partial<Liaison> = {}): Liaison {
  return {
    id, type: 'TGV', nom: id, a: { id: 'a', nom: 'A', gares: ['a'] }, b: { id: 'b', nom: 'B', gares: ['b'] },
    regions: ['Bretagne'], pays: ['France'], international: false, duree: 120, premier_mois: '2018-01',
    dernier_mois: '2026-09', active: true, tendance: null, spark: null, trains_mois_12m: 300, ...extra,
  }
}

// [liaison, rang, score, bas, haut, regularite, annulation, sup30, circules, trains_mois, mois, partielle]
const ligne = (i: number, score: number, marge = 0.8, trains = 300): LigneScore =>
  [i, 0, score, score - marge, score + marge, 0.85, 0.01, 0.05, trains * 12, trains, 12, false]

const classement: Classement = {
  liaisons: [
    liaison('Paris – Rennes', { regions: ['Bretagne', 'Île-de-France'], duree: 100 }),
    liaison('Paris – Zurich', { regions: ['Île-de-France'], international: true, duree: 240 }),
    liaison('Paris – Reims', { regions: ['Grand Est', 'Île-de-France'], duree: 46 }),
    liaison('Clermont – Paris Bercy', { type: 'Intercités', regions: ['Auvergne-Rhône-Alpes'], duree: null }),
  ],
  colonnes: [],
  scores: {
    TGV: { '12m': [ligne(0, 91.5), ligne(1, 91.4), ligne(2, 94.2, 0.7, 40)] },
    'Intercités': { '12m': [ligne(3, 92.9)] },
  },
}

describe('lignesPeriode', () => {
  it('classe par score décroissant et numérote', () => {
    const l = lignesPeriode(classement, 'TGV', '12m')
    expect(l.map((x) => [x.liaison.id, x.rang])).toEqual([['Paris – Reims', 1], ['Paris – Rennes', 2], ['Paris – Zurich', 3]])
  })
  it('signale le coude à coude quand l’écart est sous la moitié de la marge', () => {
    const l = lignesPeriode(classement, 'TGV', '12m')
    expect(l.map((x) => x.coudeACoude)).toEqual([false, false, true])
  })
  it('fusionne les deux types dans « Tous »', () => {
    expect(lignesPeriode(classement, 'Tous', '12m').map((x) => x.rang)).toEqual([1, 2, 3, 4])
    expect(lignesPeriode(classement, 'Tous', '12m')[1].liaison.type).toBe('Intercités')
  })
  it('renvoie une liste vide pour une période absente', () => {
    expect(lignesPeriode(classement, 'TGV', '1999')).toEqual([])
  })
})

describe('filtrer et trier', () => {
  const toutes = lignesPeriode(classement, 'Tous', '12m')
  it('filtre par région, international, durée, fréquence et recherche sans accents', () => {
    expect(filtrer(toutes, { ...FILTRES_DEFAUT, region: 'Bretagne' }).map((x) => x.liaison.id)).toEqual(['Paris – Rennes'])
    expect(filtrer(toutes, { ...FILTRES_DEFAUT, region: 'International' }).map((x) => x.liaison.id)).toEqual(['Paris – Zurich'])
    expect(filtrer(toutes, { ...FILTRES_DEFAUT, duree: 'courte' }).map((x) => x.liaison.id)).toEqual(['Paris – Reims'])
    expect(filtrer(toutes, { ...FILTRES_DEFAUT, duree: 'longue' }).map((x) => x.liaison.id)).toEqual(['Paris – Zurich'])
    expect(filtrer(toutes, { ...FILTRES_DEFAUT, frequence: 'f1' }).map((x) => x.liaison.id)).toEqual(['Paris – Reims'])
    expect(filtrer(toutes, { ...FILTRES_DEFAUT, q: 'BERCY' })).toHaveLength(1)
    expect(filtrer(toutes, { ...FILTRES_DEFAUT, q: 'clérmont' })).toHaveLength(1)
  })
  it('trie par nombre de trains puis par rang', () => {
    expect(trier(toutes, 'trains').at(-1)?.liaison.id).toBe('Paris – Reims')
    expect(trier(toutes, 'nom')[0].liaison.id).toBe('Clermont – Paris Bercy')
  })
})

describe('paramètres d’URL', () => {
  it('omet les valeurs par défaut et relit les valeurs valides seulement', () => {
    expect(versParams({ ...FILTRES_DEFAUT, region: 'Bretagne' })).toEqual({ region: 'Bretagne' })
    expect(depuisParams({ type: 'Intercités', tri: 'nom', duree: 'nimporte' })).toEqual(
      { ...FILTRES_DEFAUT, type: 'Intercités', tri: 'nom' })
  })
})

describe('périodes proposées', () => {
  const meta = {
    periodes: {
      TGV: [{ cle: '12m' }, { cle: '2025' }, { cle: '2026' }, { cle: 'tout' }],
      'Intercités': [{ cle: '12m' }, { cle: '2014' }, { cle: '2026' }, { cle: 'tout' }],
    },
  } as unknown as Meta
  it('liste 12 mois, les années récentes d’abord, puis tout l’historique', () => {
    expect(periodesProposees(meta, 'TGV').map((p) => p.cle)).toEqual(['12m', '2026', '2025', 'tout'])
    expect(periodesProposees(meta, 'Tous').map((p) => p.cle)).toEqual(['12m', '2026', '2025', '2014', 'tout'])
  })
})

describe('formats', () => {
  it('écrit les nombres à la française', () => {
    expect(pct(0.8917)).toBe('89,2 %'.replace(' ', ' '))
    expect(points(-0.046)).toBe('−4,6 pts')
    expect(points(0.012)).toBe('+1,2 pt')
    expect(duree(185)).toBe('3 h 05')
    expect(duree(46)).toBe('46 min')
    expect(mois('2026-09')).toBe('septembre 2026')
    expect(periodeTexte('2025-10', '2026-09')).toBe('d\'octobre 2025 à septembre 2026')
    expect(periodeTexte('2025-06', '2026-05')).toBe('de juin 2025 à mai 2026')
  })
  it('colore le score selon des seuils fixes', () => {
    expect([signal(94), signal(87), signal(80)]).toEqual(['vert', 'ambre', 'carmin'])
  })
})
