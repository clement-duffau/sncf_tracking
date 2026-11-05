import type { Classement, Evenement, Meta } from './types'

const cache = new Map<string, Promise<unknown>>()

/** Charge un fichier de site/public/data/ une seule fois (chemin relatif : fonctionne sous /<dépôt>/). */
export function charger<T>(fichier: string): Promise<T> {
  if (!cache.has(fichier)) {
    cache.set(fichier, fetch(`data/${fichier}`).then((r) => {
      if (!r.ok) throw new Error(`Impossible de charger ${fichier} (erreur ${r.status}).`)
      return r.json()
    }))
  }
  return cache.get(fichier) as Promise<T>
}

export const chargerMeta = () => charger<Meta>('meta.json')
export const chargerClassement = () => charger<Classement>('classement.json')
export const chargerEvenements = () => charger<Evenement[]>('evenements.json')
