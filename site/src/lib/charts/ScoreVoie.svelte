<script lang="ts">
  import { signal } from '../classement'

  /**
   * Barre de score dessinée comme une voie : un rail fin couvre l'échelle (70 à 100),
   * un tronçon épais montre l'intervalle à 80 %, un trait marque le score.
   */
  let { score, bas, haut }: { score: number; bas: number; haut: number } = $props()

  const MIN = 70
  const MAX = 100
  const x = (v: number) => (Math.min(Math.max(v, MIN), MAX) - MIN) / (MAX - MIN) * 100
  const couleur = $derived(`var(--${signal(score) === 'ambre' ? 'ambre-trait' : signal(score)})`)
</script>

<svg class="voie" viewBox="0 0 100 12" preserveAspectRatio="none" aria-hidden="true">
  <line x1="0" x2="100" y1="6" y2="6" class="rail" vector-effect="non-scaling-stroke" />
  {#each [80, 90] as repere (repere)}
    <line x1={x(repere)} x2={x(repere)} y1="3.5" y2="8.5" class="repere" vector-effect="non-scaling-stroke" />
  {/each}
  <rect x={x(bas)} width={Math.max(x(haut) - x(bas), 0.8)} y="3.5" height="5" rx="1" fill={couleur} opacity="0.35" />
  <rect x={x(score) - 0.7} width="1.4" y="0.5" height="11" fill={couleur} />
</svg>

<style>
  .voie { display: block; width: 100%; height: 12px; overflow: visible; }
  .rail { stroke: var(--rail-fort); stroke-width: 1; }
  .repere { stroke: var(--rail-fort); stroke-width: 1; }
</style>
