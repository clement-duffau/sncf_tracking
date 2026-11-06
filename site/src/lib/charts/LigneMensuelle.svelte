<script lang="ts">
  import { mois as moisTexte, pct } from '../format'

  /**
   * Part des trains à l'heure, mois par mois : la liaison (trait plein) et l'ensemble du type (référence).
   * Réticule au survol et au clavier (flèches gauche / droite) ; bandes grisées pour les événements annotés.
   */
  interface Point { mois: string; valeur: number | null }
  interface Bande { debut: string; fin: string; titre: string }

  let { points, reference, nomSerie, nomReference, bandes = [] }: {
    points: Point[]; reference: Map<string, number>; nomSerie: string; nomReference: string; bandes?: Bande[]
  } = $props()

  let largeur = $state(640)
  const H = 240
  const M = { h: 12, d: 16, b: 26, g: 40 }

  const ajouter = (m: string, n: number) => {
    const t = Number(m.slice(0, 4)) * 12 + Number(m.slice(5)) - 1 + n
    return `${Math.floor(t / 12)}-${String((t % 12) + 1).padStart(2, '0')}`
  }
  // tous les mois de la période, même ceux sans donnée (la courbe s'interrompt)
  const mois = $derived.by(() => {
    if (!points.length) return [] as string[]
    const out = [points[0].mois]
    while (out[out.length - 1] < points[points.length - 1].mois) out.push(ajouter(out[out.length - 1], 1))
    return out
  })
  const valeurs = $derived(new Map(points.map((p) => [p.mois, p.valeur])))
  const ymin = $derived.by(() => {
    const vs = [...points.map((p) => p.valeur), ...mois.map((m) => reference.get(m) ?? null)].filter((v): v is number => v != null)
    return Math.max(0, Math.min(0.6, Math.floor(Math.min(...vs) * 10) / 10))
  })
  const x = (i: number) => M.g + (i / Math.max(mois.length - 1, 1)) * (largeur - M.g - M.d)
  const y = (v: number) => M.h + (1 - (v - ymin) / (1 - ymin)) * (H - M.h - M.b)

  function chemin(get: (m: string) => number | null | undefined): string {
    let d = ''
    let enCours = false
    mois.forEach((m, i) => {
      const v = get(m)
      if (v == null) { enCours = false; return }
      d += `${enCours ? 'L' : 'M'}${x(i).toFixed(1)},${y(v).toFixed(1)}`
      enCours = true
    })
    return d
  }
  const cheminSerie = $derived(chemin((m) => valeurs.get(m)))
  const cheminRef = $derived(chemin((m) => reference.get(m)))
  const graduations = $derived([1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3].filter((v) => v >= ymin))
  const annees = $derived.by(() => {
    const idx = mois.map((m, i) => [m, i] as const).filter(([m]) => m.endsWith('-01'))
    const pas = largeur < 480 ? 2 : 1
    return idx.filter((_, k) => k % pas === 0)
  })
  const rects = $derived(bandes.map((b) => {
    const i0 = mois.indexOf(b.debut < mois[0] ? mois[0] : b.debut)
    const fin = b.fin > mois[mois.length - 1] ? mois[mois.length - 1] : b.fin
    const i1 = mois.indexOf(fin)
    if (i0 < 0 || i1 < 0) return null
    const pasX = (largeur - M.g - M.d) / Math.max(mois.length - 1, 1)
    return { x: x(i0) - pasX / 2, l: (i1 - i0 + 1) * pasX, titre: b.titre }
  }).filter((r) => r !== null))

  let actif = $state<number | null>(null)
  const dernierValide = $derived(mois.findLastIndex((m) => valeurs.get(m) != null))
  const i = $derived(actif ?? dernierValide)
  const lecture = $derived.by(() => {
    if (i < 0) return null
    const m = mois[i]
    const v = valeurs.get(m)
    const r = reference.get(m)
    const evt = bandes.find((b) => b.debut <= m && m <= b.fin)
    return { m, v, r, evt }
  })

  function survol(e: PointerEvent) {
    const svg = e.currentTarget as SVGSVGElement
    const bx = svg.getBoundingClientRect()
    const px = ((e.clientX - bx.left) / bx.width) * largeur
    const k = Math.round(((px - M.g) / (largeur - M.g - M.d)) * (mois.length - 1))
    actif = Math.min(Math.max(k, 0), mois.length - 1)
  }
  function clavier(e: KeyboardEvent) {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return
    e.preventDefault()
    const k = (actif ?? dernierValide) + (e.key === 'ArrowRight' ? 1 : -1)
    actif = Math.min(Math.max(k, 0), mois.length - 1)
  }
</script>

<div class="graphique" bind:clientWidth={largeur}>
  <ul class="legende">
    <li><span class="cle serie"></span>{nomSerie}</li>
    <li><span class="cle reference"></span>{nomReference}</li>
    {#if rects.length}<li><span class="cle bande"></span>grève, confinement ou incident annoté</li>{/if}
  </ul>
  <p class="lecture" aria-live="polite">
    {#if lecture}
      <strong>{lecture.v == null ? 'pas de données' : pct(lecture.v)}</strong> à l'heure en {moisTexte(lecture.m)}
      <span class="discret">({nomReference} : {pct(lecture.r)}){lecture.evt ? `, ${lecture.evt.titre.toLowerCase()}` : ''}</span>
    {/if}
  </p>
  <svg width={largeur} height={H} viewBox="0 0 {largeur} {H}" role="slider" tabindex="0"
       aria-label="{nomSerie} : part des trains à l'heure par mois. Flèches gauche et droite pour parcourir les mois."
       aria-valuemin={0} aria-valuemax={Math.max(mois.length - 1, 0)} aria-valuenow={Math.max(i, 0)}
       aria-valuetext={lecture ? `${moisTexte(lecture.m)} : ${lecture.v == null ? 'pas de données' : pct(lecture.v)}` : ''}
       onpointermove={survol} onpointerleave={() => (actif = null)} onkeydown={clavier}>
    {#each rects as r (r.x)}
      <rect x={r.x} y={M.h} width={r.l} height={H - M.h - M.b} class="bande"><title>{r.titre}</title></rect>
    {/each}
    {#each graduations as g (g)}
      <line x1={M.g} x2={largeur - M.d} y1={y(g)} y2={y(g)} class="grille" />
      <text x={M.g - 6} y={y(g)} dy="0.32em" text-anchor="end" class="axe">{Math.round(g * 100)} %</text>
    {/each}
    {#each annees as [m, k] (m)}
      <text x={x(k)} y={H - 8} text-anchor="middle" class="axe">{m.slice(0, 4)}</text>
    {/each}
    <path d={cheminRef} class="ligne reference" />
    <path d={cheminSerie} class="ligne serie" />
    {#if lecture && i >= 0}
      <line x1={x(i)} x2={x(i)} y1={M.h} y2={H - M.b} class="reticule" />
      {#if lecture.r != null}<circle cx={x(i)} cy={y(lecture.r)} r="4" class="point reference" />{/if}
      {#if lecture.v != null}<circle cx={x(i)} cy={y(lecture.v)} r="4.5" class="point serie" />{/if}
    {/if}
  </svg>
</div>

<style>
  .graphique { width: 100%; }
  svg { display: block; overflow: visible; touch-action: pan-y; }
  svg:focus-visible { outline: 2px solid var(--voie); outline-offset: 4px; }
  .legende { display: flex; flex-wrap: wrap; gap: 4px 18px; list-style: none; padding: 0; margin: 0 0 4px; font-size: 0.875rem; color: var(--encre-2); }
  .cle { display: inline-block; width: 16px; height: 2px; vertical-align: middle; margin-right: 6px; }
  .cle.serie { background: var(--serie); height: 3px; }
  .cle.reference { background: var(--reference); }
  .cle.bande { height: 12px; width: 12px; background: var(--bande); outline: 1px solid var(--rail); }
  .lecture { margin: 0 0 6px; min-height: 1.5em; font-size: 0.9375rem; }
  .discret { color: var(--discret); }
  .grille { stroke: var(--rail); stroke-width: 1; }
  .axe { fill: var(--discret); font-size: 12px; font-family: var(--police); }
  .bande { fill: var(--bande); }
  .ligne { fill: none; stroke-linejoin: round; stroke-linecap: round; }
  .ligne.serie { stroke: var(--serie); stroke-width: 2; }
  .ligne.reference { stroke: var(--reference); stroke-width: 1.5; }
  .reticule { stroke: var(--rail-fort); stroke-width: 1; }
  .point { stroke: var(--quai); stroke-width: 2; }
  .point.serie { fill: var(--serie); }
  .point.reference { fill: var(--reference); }
</style>
