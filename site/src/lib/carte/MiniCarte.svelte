<script lang="ts">
  import { CONTOUR_FRANCE, projeter } from './france'

  /** Petite carte de situation : contour de la France et gares des deux extrémités, reliées à vol d'oiseau. */
  interface Point { nom: string; lat: number | null; lon: number | null; approx?: boolean }
  let { a, b }: { a: Point[]; b: Point[] } = $props()

  const valides = (ps: Point[]) => ps.filter((p) => p.lat != null && p.lon != null).map((p) => ({ ...p, xy: projeter(p.lon!, p.lat!) }))
  const pa = $derived(valides(a))
  const pb = $derived(valides(b))
  const centre = (ps: { xy: [number, number] }[]) =>
    ps.length ? [ps.reduce((t, p) => t + p.xy[0], 0) / ps.length, ps.reduce((t, p) => t + p.xy[1], 0) / ps.length] : null
  const ca = $derived(centre(pa))
  const cb = $derived(centre(pb))

  // cadre : France métropolitaine, élargi aux gares étrangères
  const vue = $derived.by(() => {
    const [x0, y0] = projeter(-5.3, 51.2)
    const [x1, y1] = projeter(9.7, 41.2)
    const xs = [x0, x1, ...[...pa, ...pb].map((p) => p.xy[0])]
    const ys = [y0, y1, ...[...pa, ...pb].map((p) => p.xy[1])]
    const m = 40
    const minx = Math.min(...xs) - m
    const miny = Math.min(...ys) - m
    return `${minx} ${miny} ${Math.max(...xs) + m - minx} ${Math.max(...ys) + m - miny}`
  })
  const manquantes = $derived([...a, ...b].filter((p) => p.lat == null).map((p) => p.nom))
</script>

<figure class="carte">
  <svg viewBox={vue} role="img" aria-label="Situation : {a.map((p) => p.nom).join(', ')} et {b.map((p) => p.nom).join(', ')}">
    <path d={CONTOUR_FRANCE} class="france" />
    {#if ca && cb}<line x1={ca[0]} y1={ca[1]} x2={cb[0]} y2={cb[1]} class="trajet" />{/if}
    {#each [...pa, ...pb] as p (p.nom)}
      <circle cx={p.xy[0]} cy={p.xy[1]} r="18" class="gare" class:approx={p.approx} />
    {/each}
  </svg>
  <figcaption>
    Gares à vol d'oiseau{#if manquantes.length}, sans {manquantes.join(', ')} (pas une gare unique){/if}.
  </figcaption>
</figure>

<style>
  .carte { margin: 0; }
  svg { display: block; width: 100%; max-width: 260px; height: auto; }
  .france { fill: var(--surface); stroke: var(--rail-fort); stroke-width: 6; stroke-linejoin: round; }
  .trajet { stroke: var(--serie); stroke-width: 10; stroke-linecap: round; opacity: 0.6; }
  .gare { fill: var(--serie); stroke: var(--quai); stroke-width: 8; }
  .gare.approx { fill-opacity: 0.6; }
  figcaption { font-size: 0.8125rem; color: var(--discret); margin-top: 4px; }
</style>
