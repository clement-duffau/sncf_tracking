/** Logique du classement : lignes d'une période, filtres, tris (fonctions pures, testées par Vitest). */

import type { Classement, Liaison, LigneScore, Meta, TypeTrain } from './types'

export type ChoixType = TypeTrain | 'Tous'
export type Tri = 'score' | 'regularite' | 'annulation' | 'sup30' | 'trains' | 'tendance' | 'nom'
export type Duree = '' | 'courte' | 'moyenne' | 'longue'
export type Frequence = '' | 'f1' | 'f2' | 'f3' | 'f4'
export type FiltreTendance = '' | 'amelioration' | 'degradation' | 'stable'

export interface Filtres {
  type: ChoixType
  periode: string
  region: string          // '' | nom de région | 'International'
  duree: Duree
  frequence: Frequence
  tendance: FiltreTendance
  q: string
  tri: Tri
}

export const FILTRES_DEFAUT: Filtres = {
  type: 'TGV', periode: '12m', region: '', duree: '', frequence: '', tendance: '', q: '', tri: 'score',
}

export interface Ligne {
  liaison: Liaison
  rang: number              // rang par score dans le type (ou dans « Tous ») et la période, avant filtres
  coudeACoude: boolean      // écart avec la liaison de devant inférieur à la moitié de la marge d'incertitude
  score: number
  bas: number
  haut: number
  regularite: number | null
  annulation: number
  sup30: number | null
  circules: number
  trainsMois: number
  mois: number
  partielle: boolean
}

export const TRIS: { cle: Tri; libelle: string }[] = [
  { cle: 'score', libelle: 'Score' },
  { cle: 'regularite', libelle: 'Trains à l’heure' },
  { cle: 'annulation', libelle: 'Moins d’annulations' },
  { cle: 'sup30', libelle: 'Moins de retards de plus de 30 min' },
  { cle: 'trains', libelle: 'Nombre de trains' },
  { cle: 'tendance', libelle: 'Évolution sur un an' },
  { cle: 'nom', libelle: 'Ordre alphabétique' },
]

export const DUREES: { cle: Duree; libelle: string }[] = [
  { cle: '', libelle: 'Toutes durées' },
  { cle: 'courte', libelle: 'Moins de 1 h 30' },
  { cle: 'moyenne', libelle: '1 h 30 à 3 h' },
  { cle: 'longue', libelle: 'Plus de 3 h' },
]

export const FREQUENCES: { cle: Frequence; libelle: string; min: number; max: number }[] = [
  { cle: '', libelle: 'Toutes fréquences', min: 0, max: Infinity },
  { cle: 'f1', libelle: 'Moins de 50 trains par mois', min: 0, max: 50 },
  { cle: 'f2', libelle: '50 à 200 trains par mois', min: 50, max: 200 },
  { cle: 'f3', libelle: '200 à 500 trains par mois', min: 200, max: 500 },
  { cle: 'f4', libelle: 'Plus de 500 trains par mois', min: 500, max: Infinity },
]

/** Classe de signal d'un score (seuils fixes, repris dans la méthodologie). */
export function signal(score: number): 'vert' | 'ambre' | 'carmin' {
  return score >= 90 ? 'vert' : score >= 85 ? 'ambre' : 'carmin'
}

function versLigne(l: Liaison, s: LigneScore): Omit<Ligne, 'rang' | 'coudeACoude'> {
  const [, , score, bas, haut, regularite, annulation, sup30, circules, trainsMois, mois, partielle] = s
  return { liaison: l, score, bas, haut, regularite, annulation, sup30, circules, trainsMois, mois, partielle }
}

/** Lignes d'une période, dans l'ordre du score, avec rang et « coude à coude ». */
export function lignesPeriode(c: Classement, type: ChoixType, periode: string): Ligne[] {
  const types: TypeTrain[] = type === 'Tous' ? ['TGV', 'Intercités'] : [type]
  const brutes = types.flatMap((t) => (c.scores[t][periode] ?? []).map((s) => versLigne(c.liaisons[s[0]], s)))
  brutes.sort((x, y) => y.score - x.score || x.liaison.id.localeCompare(y.liaison.id))
  return brutes.map((l, i) => {
    const devant = brutes[i - 1]
    // coude à coude : l'écart avec la liaison de devant est inférieur à la moitié de la marge d'incertitude
    const marge = devant ? Math.min(l.haut - l.score, devant.score - devant.bas) : 0
    return { ...l, rang: i + 1, coudeACoude: !!devant && devant.score - l.score < marge / 2 }
  })
}

/** Périodes proposées pour un choix de type (« Tous » : union des deux types). */
export function periodesProposees(meta: Meta, type: ChoixType): { cle: string; libelle: string }[] {
  const types: TypeTrain[] = type === 'Tous' ? ['TGV', 'Intercités'] : [type]
  const cles = new Map<string, string>()
  for (const t of types) for (const p of meta.periodes[t]) if (!cles.has(p.cle)) cles.set(p.cle, p.libelle)
  const annees = [...cles.keys()].filter((k) => /^\d{4}$/.test(k)).sort().reverse()
  return [
    { cle: '12m', libelle: '12 derniers mois' },
    ...annees.map((a) => ({ cle: a, libelle: a })),
    { cle: 'tout', libelle: 'Tout l’historique' },
  ]
}

export function sansAccents(s: string): string {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
}

export function filtrer(lignes: Ligne[], f: Filtres): Ligne[] {
  const q = sansAccents(f.q.trim())
  const freq = FREQUENCES.find((x) => x.cle === f.frequence) ?? FREQUENCES[0]
  return lignes.filter(({ liaison: l, trainsMois }) => {
    if (f.region === 'International' && !l.international) return false
    if (f.region && f.region !== 'International' && !l.regions.includes(f.region)) return false
    if (f.duree) {
      if (l.duree == null) return false
      if (f.duree === 'courte' && l.duree >= 90) return false
      if (f.duree === 'moyenne' && (l.duree < 90 || l.duree > 180)) return false
      if (f.duree === 'longue' && l.duree <= 180) return false
    }
    if (trainsMois < freq.min || trainsMois >= freq.max) return false
    if (f.tendance && l.tendance?.etiquette !== f.tendance) return false
    if (q && !sansAccents(l.nom).includes(q)) return false
    return true
  })
}

const dernier = (x: number | null | undefined, asc: boolean) => (x == null ? (asc ? Infinity : -Infinity) : x)

export function trier(lignes: Ligne[], tri: Tri): Ligne[] {
  const cmp: Record<Tri, (a: Ligne, b: Ligne) => number> = {
    score: (a, b) => a.rang - b.rang,
    regularite: (a, b) => dernier(b.regularite, false) - dernier(a.regularite, false),
    annulation: (a, b) => a.annulation - b.annulation,
    sup30: (a, b) => dernier(a.sup30, true) - dernier(b.sup30, true),
    trains: (a, b) => b.trainsMois - a.trainsMois,
    tendance: (a, b) => dernier(b.liaison.tendance?.delta, false) - dernier(a.liaison.tendance?.delta, false),
    nom: (a, b) => a.liaison.nom.localeCompare(b.liaison.nom, 'fr'),
  }
  return [...lignes].sort((a, b) => cmp[tri](a, b) || a.rang - b.rang)
}

/** Filtres ↔ paramètres d'URL (les valeurs par défaut sont omises). */
export function versParams(f: Filtres): Record<string, string> {
  const p: Record<string, string> = {}
  for (const [k, v] of Object.entries(f) as [keyof Filtres, string][]) if (v !== FILTRES_DEFAUT[k]) p[k] = v
  return p
}

export function depuisParams(p: Record<string, string>): Filtres {
  const f = { ...FILTRES_DEFAUT }
  if (p.type === 'TGV' || p.type === 'Intercités' || p.type === 'Tous') f.type = p.type
  if (p.periode) f.periode = p.periode
  if (p.region) f.region = p.region
  if (DUREES.some((d) => d.cle === p.duree)) f.duree = p.duree as Duree
  if (FREQUENCES.some((d) => d.cle === p.frequence)) f.frequence = p.frequence as Frequence
  if (['amelioration', 'degradation', 'stable'].includes(p.tendance)) f.tendance = p.tendance as FiltreTendance
  if (p.q) f.q = p.q
  if (TRIS.some((t) => t.cle === p.tri)) f.tri = p.tri as Tri
  return f
}
