import { untrack } from 'svelte'

/**
 * Routeur minimal par hash, compatible GitHub Pages :
 *   #/?type=TGV&p=12m&r=Bretagne      #/methodologie#score
 */
export const ROUTES = [
  { path: '', label: 'Classement' },
  { path: 'methodologie', label: 'Méthodologie et sources' },
] as const

export type RoutePath = (typeof ROUTES)[number]['path']

interface Route { path: RoutePath; ancre: string; params: Record<string, string> }

function lire(): Route {
  const brut = location.hash.replace(/^#\/?/, '')
  const [avantAncre, ancre = ''] = brut.split('#')
  const [p, query = ''] = avantAncre.split('?')
  const path = (ROUTES.find((r) => r.path === p)?.path ?? '') as RoutePath
  return { path, ancre, params: Object.fromEntries(new URLSearchParams(query)) }
}

export const route = $state(lire())

addEventListener('hashchange', () => {
  const suivante = lire()
  const pageChangee = suivante.path !== route.path
  route.path = suivante.path
  route.ancre = suivante.ancre
  route.params = suivante.params
  if (pageChangee) scrollTo({ top: 0 })
})

/** Met à jour les paramètres de la page courante sans créer d'entrée d'historique. */
export function setParams(params: Record<string, string | null | undefined>) {
  untrack(() => {
    const q = new URLSearchParams()
    for (const [k, v] of Object.entries(params)) if (v != null && v !== '') q.set(k, v)
    const s = q.toString()
    const hash = `#/${route.path}${s ? `?${s}` : ''}`
    if (hash !== location.hash) history.replaceState(null, '', hash)
    route.params = Object.fromEntries(q)
  })
}

export function lien(path: RoutePath, params: Record<string, string> = {}): string {
  const s = new URLSearchParams(params).toString()
  return `#/${path}${s ? `?${s}` : ''}`
}
