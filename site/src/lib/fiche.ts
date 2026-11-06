/** Calculs de la fiche liaison (fonctions pures, testées par Vitest). */

import type { Fiche, Sens, Serie, Stats, TypeTrain } from './types'

export type ChoixSens = Sens | 'deux'

export const CAUSES = [
  { cle: 'externe', libelle: 'Causes externes', detail: 'météo, obstacles, colis suspects, malveillance, mouvements sociaux…' },
  { cle: 'infra', libelle: 'Infrastructure', detail: 'maintenance et travaux sur les voies' },
  { cle: 'gestion_trafic', libelle: 'Gestion du trafic', detail: 'circulation sur la ligne, interactions entre réseaux' },
  { cle: 'materiel_roulant', libelle: 'Matériel roulant', detail: 'pannes et défauts des trains' },
  { cle: 'gestion_gare', libelle: 'Gestion en gare', detail: 'gestion en gare et réutilisation du matériel' },
  { cle: 'prise_en_charge_voyageurs', libelle: 'Voyageurs', detail: 'affluence, assistance, correspondances' },
] as const

export type CleCause = (typeof CAUSES)[number]['cle']

/** Série mensuelle du sens choisi ; « les deux sens » additionne les deux séries mois par mois. */
export function serieSens(f: Fiche, sens: ChoixSens): Serie | null {
  if (sens !== 'deux') return f.series[sens] ?? null
  const series = (['ab', 'ba'] as Sens[]).map((s) => f.series[s]).filter((s): s is Serie => !!s)
  if (series.length < 2) return series[0] ?? null
  const mois = [...new Set(series.flatMap((s) => s.mois))].sort()
  const index = series.map((s) => new Map(s.mois.map((m, i) => [m, i])))
  const cles = Object.keys(series[0]).filter((k) => k !== 'mois') as (keyof Serie)[]
  const out: Record<string, unknown[]> = { mois }
  for (const k of cles) {
    out[k] = mois.map((m) => {
      let total: number | null = 0
      for (let j = 0; j < series.length; j++) {
        const i = index[j].get(m)
        if (i === undefined) continue
        const v = (series[j][k] as (number | null)[])[i]
        // une valeur inconnue dans un sens rend la somme inconnue (gravité invalide, causes absentes)
        total = v == null || total == null ? null : total + v
      }
      return total
    })
  }
  return out as unknown as Serie
}

/** Part mensuelle des trains circulés arrivés à l'heure. */
export function regulariteMensuelle(s: Serie): { mois: string; valeur: number | null }[] {
  return s.mois.map((m, i) => ({ mois: m, valeur: s.circules[i] > 0 ? 1 - s.retards[i] / s.circules[i] : null }))
}

/** Part mensuelle à l'heure pour l'ensemble des liaisons du type (référence sur les graphiques). */
export function regulariteType(stats: Stats, type: TypeTrain): Map<string, number> {
  const m = new Map<string, number>()
  for (const [mois, , , circules, retards] of stats.types[type]) {
    if (circules > 0) m.set(`${String(mois).slice(0, 4)}-${String(mois).slice(4)}`, 1 - retards / circules)
  }
  return m
}

export interface Annee {
  annee: number
  mois: number
  prevus: number
  aLHeure: number        // parts des trains prévus (somme = 1)
  retard30: number       // en retard de 30 min au plus (TGV) ; tous les retards (Intercités)
  retard30a60: number | null
  retard60: number | null
  annules: number
  graviteEstimee: boolean // une partie des mois sans gravité valide : répartition extrapolée
}

/** Issue des trains prévus, année par année. */
export function parAnnee(s: Serie, type: TypeTrain): Annee[] {
  const groupes = new Map<number, number[]>()
  s.mois.forEach((m, i) => {
    const a = Number(m.slice(0, 4))
    if (!groupes.has(a)) groupes.set(a, [])
    groupes.get(a)!.push(i)
  })
  return [...groupes.entries()].map(([annee, idx]) => {
    const somme = (xs: number[]) => idx.reduce((t, i) => t + xs[i], 0)
    const prevus = somme(s.prevus)
    const annules = somme(s.annules)
    const retards = somme(s.retards)
    const circules = prevus - annules
    let r30a60: number | null = null
    let r60: number | null = null
    let estimee = false
    if (type === 'TGV' && s.sup30 && s.sup60) {
      const valides = idx.filter((i) => s.sup30![i] != null && s.sup60![i] != null)
      const retV = valides.reduce((t, i) => t + s.retards[i], 0)
      if (retV > 0) {
        const q30 = valides.reduce((t, i) => t + (s.sup30![i] ?? 0), 0) / retV
        const q60 = valides.reduce((t, i) => t + (s.sup60![i] ?? 0), 0) / retV
        r30a60 = (retards * (q30 - q60)) / prevus
        r60 = (retards * q60) / prevus
        estimee = valides.length < idx.length
      } else if (retards === 0) {
        r30a60 = 0
        r60 = 0
      }
    }
    const partRetards = retards / prevus
    return {
      annee, mois: idx.length, prevus,
      aLHeure: Math.max(circules - retards, 0) / prevus,
      retard30: partRetards - (r30a60 ?? 0) - (r60 ?? 0),
      retard30a60: r30a60, retard60: r60,
      annules: annules / prevus,
      graviteEstimee: estimee,
    }
  })
}

export interface PeriodeCauses {
  libelle: string
  nomenclature: 1 | 2
  retards: number
  parts: Record<CleCause, number>
}

const MOIS_COURTS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']

/** Répartition des causes des trains en retard, par année, en coupant l'année de la rupture de nomenclature. */
export function causesParPeriode(s: Serie, rupture: string | null): PeriodeCauses[] {
  if (!s.retards_avec_causes) return []
  const groupes = new Map<string, { idx: number[]; nomenclature: 1 | 2; annee: number }>()
  s.mois.forEach((m, i) => {
    const annee = Number(m.slice(0, 4))
    const nomenclature: 1 | 2 = rupture && m >= rupture ? 2 : 1
    const cle = `${annee}-${nomenclature}`
    if (!groupes.has(cle)) groupes.set(cle, { idx: [], nomenclature, annee })
    groupes.get(cle)!.idx.push(i)
  })
  const out: PeriodeCauses[] = []
  for (const { idx, nomenclature, annee } of groupes.values()) {
    const retards = idx.reduce((t, i) => t + (s.retards_avec_causes![i] ?? 0), 0)
    if (retards <= 0) continue
    const parts = {} as Record<CleCause, number>
    for (const c of CAUSES) {
      const col = s[`cause_${c.cle}` as keyof Serie] as (number | null)[]
      parts[c.cle] = idx.reduce((t, i) => t + (col[i] ?? 0), 0) / retards
    }
    const coupee = rupture && Number(rupture.slice(0, 4)) === annee
    const premier = Number(s.mois[idx[0]].slice(5)) - 1
    const dernier = Number(s.mois[idx[idx.length - 1]].slice(5)) - 1
    const libelle = coupee || idx.length < 12
      ? `${annee} (${MOIS_COURTS[premier]}${premier !== dernier ? `–${MOIS_COURTS[dernier]}` : ''})`
      : String(annee)
    out.push({ libelle, nomenclature, retards, parts })
  }
  return out
}

/** Export CSV (séparateur « ; », nombres entiers) de la série affichée. */
export function versCSV(s: Serie, nom: string, sens: string): string {
  const colonnes: [keyof Serie, string][] = [
    ['mois', 'mois'], ['prevus', 'trains_prevus'], ['annules', 'trains_annules'], ['circules', 'trains_circules'],
    ['retards', 'trains_en_retard'], ['sup15', 'retard_plus_15_min'], ['sup30', 'retard_plus_30_min'],
    ['sup60', 'retard_plus_60_min'], ['retards_avec_causes', 'retards_avec_causes'],
    ...CAUSES.map((c) => [`cause_${c.cle}` as keyof Serie, `cause_${c.cle}`] as [keyof Serie, string]),
  ]
  const presentes = colonnes.filter(([k]) => s[k])
  const lignes = [
    `# ${nom} (${sens}). Source : SNCF Voyageurs, ressources.data.sncf.com, licence ODbL. Données dérivées sous ODbL.`,
    presentes.map(([, t]) => t).join(';'),
    ...s.mois.map((_, i) => presentes.map(([k]) => (s[k] as unknown[])[i] ?? '').join(';')),
  ]
  return lignes.join('\n') + '\n'
}
