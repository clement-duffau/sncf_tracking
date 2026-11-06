<script lang="ts">
  import { pct } from '../format'
  import type { MoisTrajet } from '../types'

  /**
   * Probabilité qu'un train prévu arrive à l'heure, pour chaque mois de l'année (sens choisi).
   * Le point est l'estimation ; la colonne épaisse, la fourchette d'une année sur l'autre (8 cas sur 10).
   */
  let { mois }: { mois: MoisTrajet[] } = $props()

  const NOMS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
  const INITIALES = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
  const H = 150
  const MIN = 0.4
  const y = (v: number) => 6 + (1 - (Math.max(v, MIN) - MIN) / (1 - MIN)) * (H - 12)

  let choisi = $state<number | null>(null)
  const m = $derived(choisi == null ? null : mois[choisi])
</script>

<div class="trajet">
  <p class="lecture" aria-live="polite">
    {#if m}
      En {NOMS[m.mois - 1]} : <strong>{pct(m.proba, 0)}</strong> de chances d'arriver à l'heure, le plus souvent entre
      {pct(m.prediction[0], 0)} et {pct(m.prediction[1], 0)}.
      {#if m.p_annulation != null}Annulés : {pct(m.p_annulation)}.{/if}
      {#if m.p_sup30 != null}Plus de 30 min de retard : {pct(m.p_sup30)}.{/if}
      <span class="discret">
        D'après {m.annees.length} année{m.annees.length > 1 ? 's' : ''} ({m.annees.map((a) => `${a.annee} : ${pct(a.p, 0)}`).join(', ')}).
        {#if m.peu_de_donnees}Peu de données : l'estimation repose surtout sur la moyenne de la liaison.{/if}
      </span>
    {:else}
      Survolez ou sélectionnez un mois pour le détail.
    {/if}
  </p>
  <div class="colonnes" role="group" aria-label="Mois de l'année">
    {#each mois as mo, k (mo.mois)}
      <button type="button" class="colonne" class:actif={choisi === k} class:incertain={mo.peu_de_donnees} aria-pressed={choisi === k}
              aria-label="{NOMS[mo.mois - 1]} : {pct(mo.proba, 0)} de chances d'arriver à l'heure"
              onpointerenter={() => (choisi = k)} onfocus={() => (choisi = k)} onclick={() => (choisi = k)}>
        <svg viewBox="0 0 24 {H}" width="24" height={H} aria-hidden="true">
          <line x1="12" x2="12" y1={y(1)} y2={y(MIN)} class="rail" />
          <line x1="12" x2="12" y1={y(0.9)} y2={y(0.9)} class="repere" />
          <rect x="7" width="10" rx="3" y={y(mo.prediction[1])} height={Math.max(y(mo.prediction[0]) - y(mo.prediction[1]), 2)} class="fourchette" />
          <circle cx="12" cy={y(mo.proba)} r="4.5" class="point" />
        </svg>
        <span class="valeur">{Math.round(mo.proba * 100)}</span>
        <span class="initiale">{INITIALES[mo.mois - 1]}</span>
      </button>
    {/each}
  </div>
  <p class="echelle discret">Échelle de 40 à 100 %, repère à 90 %. Valeurs en pourcentage.</p>
</div>

<style>
  .lecture { margin: 0 0 10px; min-height: 3em; font-size: 0.9375rem; }
  .discret { color: var(--discret); }
  .colonnes { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 2px; max-width: 560px; }
  .colonne {
    display: flex; flex-direction: column; align-items: center; gap: 2px; background: none; border: 0; padding: 4px 0;
    border-radius: 4px; cursor: pointer;
  }
  .colonne:hover, .colonne.actif { background: var(--survol); }
  svg { display: block; overflow: visible; }
  .rail { stroke: var(--rail); stroke-width: 1; }
  .repere { stroke: var(--rail-fort); stroke-width: 1; }
  .fourchette { fill: var(--serie); opacity: 0.25; }
  .incertain .fourchette { opacity: 0.12; }
  .point { fill: var(--serie); stroke: var(--quai); stroke-width: 2; }
  .valeur { font-family: var(--police-etroite); font-weight: 600; font-size: 0.875rem; }
  .initiale { font-size: 0.75rem; color: var(--discret); }
  .echelle { font-size: 0.8125rem; margin: 6px 0 0; }
</style>
