/** Formats français : nombres, pourcentages, mois, durées. */

const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
const MOIS_COURT = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']

const nf = (d: number) => new Intl.NumberFormat('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d })

export function nombre(x: number | null | undefined, decimales = 0): string {
  return x == null ? '–' : nf(decimales).format(x)
}

/** Part (0–1) en pourcentage français : 0,8917 → « 89,2 % ». */
export function pct(x: number | null | undefined, decimales = 1): string {
  return x == null ? '–' : `${nf(decimales).format(x * 100)} %`
}

/** Écart en points : −0,046 → « −4,6 pts ». */
export function points(x: number | null | undefined, decimales = 1): string {
  if (x == null) return '–'
  const v = nf(decimales).format(Math.abs(x * 100))
  return `${x > 0 ? '+' : x < 0 ? '−' : ''}${v} pt${Math.abs(x * 100) >= 2 ? 's' : ''}`
}

/** « 2026-09 » → « septembre 2026 » ; court : « sept. 2026 ». */
export function mois(m: string, court = false): string {
  const [a, mm] = m.split('-').map(Number)
  return `${(court ? MOIS_COURT : MOIS)[mm - 1]} ${a}`
}

/** Période « d'octobre 2025 à septembre 2026 », avec élision devant voyelle. */
export function periodeTexte(debut: string, fin: string): string {
  const d = mois(debut)
  return `${/^[aeiouyéè]/.test(d) ? "d'" : 'de '}${d} à ${mois(fin)}`
}

/** 185 → « 3 h 05 » ; 50 → « 50 min ». */
export function duree(min: number | null | undefined): string {
  if (min == null) return '–'
  const h = Math.floor(min / 60)
  const m = Math.round(min % 60)
  return h ? `${h} h ${String(m).padStart(2, '0')}` : `${m} min`
}

/** Date ISO → « 2 octobre 2026 ». */
export function date(iso: string): string {
  const d = new Date(iso)
  return `${d.getUTCDate() === 1 ? '1er' : d.getUTCDate()} ${MOIS[d.getUTCMonth()]} ${d.getUTCFullYear()}`
}
