import { untrack } from 'svelte'

/**
 * Routeur minimal par hash, compatible GitHub Pages :
 *   #/?type=TGV&periode=2025&region=Bretagne     #/liaison/tgv-paris-est--reims?sens=ab     #/methodologie#score
 */
export const ROUTES = [
  { path: '', label: 'Classement' },
  { path: 'methodologie', label: 'Méthodologie et sources' },
] as const

/** Pages du menu, plus les pages atteintes par un lien (fiche liaison). */
export type RoutePath = (typeof ROUTES)[number]['path'] | 'liaison'

interface Route { path: RoutePath; id: string; ancre: string; params: Record<string, string> }

function lire(): Route {
  const brut = location.hash.replace(/^#\/?/, '')
  const [avantAncre, ancre = ''] = brut.split('#')
  const [chemin, query = ''] = avantAncre.split('?')
  const [p, ...reste] = chemin.split('/')
  const path: RoutePath = p === 'liaison' && reste.length ? 'liaison' : (ROUTES.find((r) => r.path === p)?.path ?? '')
  return { path, id: path === 'liaison' ? decodeURIComponent(reste.join('/')) : '', ancre, params: Object.fromEntries(new URLSearchParams(query)) }
}

export const route = $state(lire())

addEventListener('hashchange', () => {
  const suivante = lire()
  const pageChangee = suivante.path !== route.path || suivante.id !== route.id
  route.path = suivante.path
  route.id = suivante.id
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
    const hash = `#/${route.path}${route.id ? `/${route.id}` : ''}${s ? `?${s}` : ''}`
    if (hash !== location.hash) history.replaceState(null, '', hash)
    route.params = Object.fromEntries(q)
  })
}

export function lien(path: RoutePath, params: Record<string, string> = {}): string {
  const s = new URLSearchParams(params).toString()
  return `#/${path}${s ? `?${s}` : ''}`
}

export function lienLiaison(id: string, params: Record<string, string> = {}): string {
  const s = new URLSearchParams(params).toString()
  return `#/liaison/${id}${s ? `?${s}` : ''}`
}
