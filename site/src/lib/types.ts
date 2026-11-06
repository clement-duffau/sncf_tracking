/** Types des fichiers produits par le pipeline (site/public/data/, voir pipeline/export.py). */

export type TypeTrain = 'TGV' | 'Intercités'

export interface Extremite { id: string; nom: string; gares: string[] }

export interface Tendance {
  etiquette: 'amelioration' | 'degradation' | 'stable' | 'nouvelle'
  etiquette_relative: 'amelioration' | 'degradation' | 'stable' | null
  reg_12m: number | null
  reg_avant: number | null
  delta: number | null
  delta_relatif: number | null
  z: number | null
  z_relatif: number | null
  pente_an: number | null
  pente_r2: number | null
}

export interface Liaison {
  id: string
  type: TypeTrain
  nom: string
  a: Extremite
  b: Extremite
  regions: string[]
  pays: string[]
  international: boolean
  duree: number | null
  premier_mois: string
  dernier_mois: string
  active: boolean
  tendance: Tendance | null
  spark: (number | null)[] | null
  trains_mois_12m: number | null
}

/** Ligne de score : voir `colonnes` de classement.json. */
export type LigneScore = [
  liaison: number, rang: number, score: number, bas: number, haut: number,
  regularite: number | null, annulation: number, sup30: number | null, circules: number,
  trains_mois: number, mois: number, partielle: boolean,
]

export interface Classement {
  liaisons: Liaison[]
  colonnes: string[]
  scores: Record<TypeTrain, Record<string, LigneScore[]>>
}

export interface Periode { cle: string; libelle: string; debut: string; fin: string; partielle: boolean }

export interface Source { titre: string; url: string; editeur: string; licence: string; donnees_mises_a_jour: string }

export interface Meta {
  genere_le: string
  version_methode: string
  sources: Record<string, Source>
  fenetres: Record<TypeTrain, { debut: string; fin: string }>
  periodes: Record<TypeTrain, Periode[]>
  parametres: {
    bareme: Record<string, number>
    poids_prior: Record<TypeTrain, number>
    surdispersion: Record<TypeTrain, number>
    moyennes_12m: Record<TypeTrain, { retard: number; annulation: number; sup30: number | null; sup60: number | null; q30: number; q60: number }>
    seuils_tendance: { z: number; delta: number }
  }
}

export interface Evenement {
  id: string
  titre: string
  type: string
  debut: string
  fin: string
  types: string[]
  exclure: string[]
  effet: string | null
  observe: string
  sources: string[]
}

// ------------------------------------------------------------------ fiche liaison (liaison/<id>.json)

export interface ScorePeriode {
  rang: number
  classees: number
  score: number
  intervalle: [number, number]
  regularite: number | null
  annulation: number
  sup30: number | null
  sup60: number | null
  gravite_estimee: boolean
  circules: number
  mois: number
  partielle: boolean
}

/** Série mensuelle d'un sens ; les colonnes de gravité et de causes n'existent que pour le TGV. */
export interface Serie {
  mois: string[]
  prevus: number[]
  annules: number[]
  circules: number[]
  retards: number[]
  sup15?: (number | null)[]
  sup30?: (number | null)[]
  sup60?: (number | null)[]
  retards_avec_causes?: number[]
  cause_externe?: (number | null)[]
  cause_infra?: (number | null)[]
  cause_gestion_trafic?: (number | null)[]
  cause_materiel_roulant?: (number | null)[]
  cause_gestion_gare?: (number | null)[]
  cause_prise_en_charge_voyageurs?: (number | null)[]
}

export type Sens = 'ab' | 'ba'

export interface MoisTrajet {
  mois: number
  proba: number
  ic: [number, number]
  prediction: [number, number]
  prior: number
  trains: number
  annees: { annee: number; p: number; trains: number }[]
  p_annulation: number | null
  p_sup30: number | null
  peu_de_donnees: boolean
}

export interface Fiche extends Omit<Liaison, 'spark' | 'trains_mois_12m'> {
  scores: Record<string, ScorePeriode>
  series: Partial<Record<Sens, Serie>>
  saisonnalite: { liaison: ({ effet: number; brut: number; annees: number } | null)[]; type: (number | null)[] }
  mon_trajet: Partial<Record<Sens, MoisTrajet[]>>
  evenements: string[]
  rupture_causes: string | null
}

export interface Gare {
  id: string
  nom: string
  region: string | null
  pays: string
  lat: number | null
  lon: number | null
  precision: string
  liaisons: number[]
}

export interface Stats {
  tgv_national: [number, number, number][]
  types: Record<TypeTrain, [number, number, number, number, number][]>
  types_colonnes: string[]
  causes_tgv: { colonnes: string[]; lignes: number[][] }
  saisonnalite: Record<TypeTrain, (number | null)[]>
  tendance_reseau: Record<TypeTrain, number | null>
}
