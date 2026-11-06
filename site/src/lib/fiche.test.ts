import { describe, expect, it } from 'vitest'
import { causesParPeriode, parAnnee, regulariteMensuelle, regulariteType, serieSens, versCSV } from './fiche'
import { note } from './score'
import type { Fiche, Serie, Stats } from './types'

describe('score identique au pipeline', () => {
  // Valeurs exportées par le pipeline (site/public/data/donnees/scores.csv, 12 derniers mois)
  it('Paris Est – Reims (TGV)', () => {
    expect(note(0.11555336005929312, 0.002839210731588188, 0.036690520202975176, 0.013256601414927004))
      .toBeCloseTo(94.23348307795028, 8)
  })
  it('Briançon – Paris Austerlitz (Intercités, gravité estimée)', () => {
    expect(note(0.30956904445704797, 0.014693096901914268, 0.12271470427588682, 0.05150103194149071))
      .toBeCloseTo(82.67945469216784, 8)
  })
})

const serieTGV = (mois: string[], extra: Partial<Serie> = {}): Serie => ({
  mois,
  prevus: mois.map(() => 100), annules: mois.map(() => 2), circules: mois.map(() => 98), retards: mois.map(() => 18),
  sup15: mois.map(() => 10), sup30: mois.map(() => 6), sup60: mois.map(() => 2),
  retards_avec_causes: mois.map(() => 18),
  cause_externe: mois.map(() => 9), cause_infra: mois.map(() => 9), cause_gestion_trafic: mois.map(() => 0),
  cause_materiel_roulant: mois.map(() => 0), cause_gestion_gare: mois.map(() => 0), cause_prise_en_charge_voyageurs: mois.map(() => 0),
  ...extra,
})

const fiche = (series: Fiche['series']): Fiche => ({ series } as unknown as Fiche)

describe('serieSens', () => {
  it('additionne les deux sens mois par mois, y compris un mois présent dans un seul sens', () => {
    const f = fiche({ ab: serieTGV(['2026-01', '2026-02']), ba: serieTGV(['2026-02', '2026-03']) })
    const s = serieSens(f, 'deux')!
    expect(s.mois).toEqual(['2026-01', '2026-02', '2026-03'])
    expect(s.prevus).toEqual([100, 200, 100])
  })
  it('une gravité inconnue dans un sens rend la somme inconnue', () => {
    const f = fiche({ ab: serieTGV(['2025-02'], { sup30: [null] }), ba: serieTGV(['2025-02']) })
    expect(serieSens(f, 'deux')!.sup30).toEqual([null])
    expect(serieSens(f, 'ba')!.sup30).toEqual([6])
  })
})

describe('parAnnee', () => {
  it('répartit les trains prévus entre à l’heure, retards par gravité et annulés (somme = 1)', () => {
    const [a] = parAnnee(serieTGV(['2026-01', '2026-02']), 'TGV')
    expect(a.annee).toBe(2026)
    expect(a.aLHeure).toBeCloseTo(0.8)
    expect(a.annules).toBeCloseTo(0.02)
    expect(a.retard30).toBeCloseTo(0.12)
    expect(a.retard30a60).toBeCloseTo(0.04)
    expect(a.retard60).toBeCloseTo(0.02)
    expect(a.aLHeure + a.retard30 + a.retard30a60! + a.retard60! + a.annules).toBeCloseTo(1)
    expect(a.graviteEstimee).toBe(false)
  })
  it('extrapole la gravité quand certains mois sont invalides, et le signale', () => {
    const [a] = parAnnee(serieTGV(['2025-01', '2025-06'], { sup30: [null, 6], sup60: [null, 2] }), 'TGV')
    expect(a.graviteEstimee).toBe(true)
    expect(a.retard60).toBeCloseTo(0.02)
  })
  it('Intercités : pas de gravité', () => {
    const s: Serie = { mois: ['2026-01'], prevus: [50], annules: [1], circules: [49], retards: [9] }
    const [a] = parAnnee(s, 'Intercités')
    expect(a.retard30a60).toBeNull()
    expect(a.retard30).toBeCloseTo(0.18)
  })
})

describe('causesParPeriode', () => {
  it('coupe l’année de la rupture de nomenclature', () => {
    const p = causesParPeriode(serieTGV(['2026-03', '2026-04', '2026-05', '2026-06']), '2026-05')
    expect(p.map((x) => [x.libelle, x.nomenclature])).toEqual([['2026 (mars–avr.)', 1], ['2026 (mai–juin)', 2]])
    expect(p[0].parts.externe).toBeCloseTo(0.5)
  })
})

describe('régularité', () => {
  it('mensuelle de la liaison et du type', () => {
    expect(regulariteMensuelle(serieTGV(['2026-01']))[0].valeur).toBeCloseTo(1 - 18 / 98)
    const stats = { types: { TGV: [[202601, 100, 0, 100, 20]], 'Intercités': [] } } as unknown as Stats
    expect(regulariteType(stats, 'TGV').get('2026-01')).toBeCloseTo(0.8)
  })
})

describe('export CSV', () => {
  it('écrit l’attribution ODbL, un en-tête et une ligne par mois', () => {
    const csv = versCSV(serieTGV(['2026-01', '2026-02']), 'Paris Est – Reims', 'les deux sens').trim().split('\n')
    expect(csv[0]).toContain('ODbL')
    expect(csv[1].startsWith('mois;trains_prevus;trains_annules')).toBe(true)
    expect(csv).toHaveLength(4)
  })
})
