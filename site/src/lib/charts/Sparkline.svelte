<script lang="ts">
  /** Part des trains à l'heure, mois par mois, sur une échelle fixe (60 à 100 %) commune à toutes les lignes. */
  let { valeurs }: { valeurs: (number | null)[] } = $props()

  const L = 72
  const H = 22
  const MIN = 0.6
  const y = (v: number) => H - 1 - (Math.min(Math.max(v, MIN), 1) - MIN) / (1 - MIN) * (H - 2)
  const x = (i: number) => (i / Math.max(valeurs.length - 1, 1)) * (L - 4) + 2

  // segments continus (un mois sans donnée coupe la courbe)
  const segments = $derived.by(() => {
    const out: string[] = []
    let cur: string[] = []
    valeurs.forEach((v, i) => {
      if (v == null) { if (cur.length) out.push(cur.join(' ')); cur = []; return }
      cur.push(`${x(i).toFixed(1)},${y(v).toFixed(1)}`)
    })
    if (cur.length) out.push(cur.join(' '))
    return out
  })
  const dernier = $derived(valeurs.findLastIndex((v) => v != null))
</script>

<svg width={L} height={H} viewBox="0 0 {L} {H}" aria-hidden="true">
  <line x1="0" x2={L} y1={y(0.9)} y2={y(0.9)} class="repere" />
  {#each segments as pts, i (i)}
    <polyline points={pts} />
  {/each}
  {#if dernier >= 0}
    <circle cx={x(dernier)} cy={y(valeurs[dernier]!)} r="2" />
  {/if}
</svg>

<style>
  svg { display: block; overflow: visible; }
  polyline { fill: none; stroke: var(--encre-2); stroke-width: 1.4; stroke-linejoin: round; }
  circle { fill: var(--encre); }
  .repere { stroke: var(--rail); stroke-width: 1; stroke-dasharray: 2 2; }
</style>
