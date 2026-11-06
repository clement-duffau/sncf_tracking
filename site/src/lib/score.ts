/**
 * Score V2 : note moyenne d'un train prévu sur 100. Même formule que pipeline/score.py (fonction `note`).
 * R = part des trains circulés en retard, A = part des trains prévus annulés,
 * G30, G60 = part des trains circulés en retard de plus de 30 / 60 min.
 */

import type { Meta, TypeTrain } from './types'

export const BAREME = { a_l_heure: 100, retard_30: 67, retard_30_60: 33, retard_60: 0, annule: 0 }

export function note(R: number, A: number, G30: number, G60: number, b = BAREME): number {
  const ptsRetard = (R - G30) * b.retard_30 + (G30 - G60) * b.retard_30_60 + G60 * b.retard_60
  return (1 - A) * ((1 - R) * b.a_l_heure + ptsRetard) + A * b.annule
}

/** Score d'un train « moyen » du type sur les 12 derniers mois (sans lissage : c'est la moyenne elle-même). */
export function scoreMoyenType(meta: Meta, type: TypeTrain): number {
  const m = meta.parametres.moyennes_12m[type]
  const g30 = m.sup30 ?? m.retard * m.q30
  const g60 = m.sup60 ?? m.retard * m.q60
  return note(m.retard, m.annulation, g30, g60, meta.parametres.bareme as typeof BAREME)
}
