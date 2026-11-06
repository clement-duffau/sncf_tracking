<script lang="ts">
  import {
    DUREES, FREQUENCES, TRIS, depuisParams, filtrer, lignesPeriode, periodesProposees, signal, trier, versParams,
    type ChoixType, type Filtres, type Ligne,
  } from '../lib/classement'
  import ScoreVoie from '../lib/charts/ScoreVoie.svelte'
  import Sparkline from '../lib/charts/Sparkline.svelte'
  import { chargerClassement, chargerMeta } from '../lib/data'
  import { duree, nombre, pct, periodeTexte, points } from '../lib/format'
  import { lien, lienLiaison, route, setParams } from '../lib/router.svelte'
  import type { Classement, Meta, TypeTrain } from '../lib/types'

  let meta = $state<Meta | null>(null)
  let classement = $state<Classement | null>(null)
  let erreur = $state<string | null>(null)

  Promise.all([chargerMeta(), chargerClassement()])
    .then(([m, c]) => { meta = m; classement = c })
    .catch((e: Error) => { erreur = e.message })

  const f = $derived(depuisParams(route.params))

  function maj(changement: Partial<Filtres>) {
    const suivant = { ...f, ...changement }
    // une année absente du type choisi (ex. 2015 pour le TGV) : retour aux 12 derniers mois
    if (meta && !periodesProposees(meta, suivant.type).some((p) => p.cle === suivant.periode)) suivant.periode = '12m'
    setParams(versParams(suivant))
  }

  const toutes = $derived(classement ? lignesPeriode(classement, f.type, f.periode) : [])
  const affichees = $derived(trier(filtrer(toutes, f), f.tri))
  const periodes = $derived(meta ? periodesProposees(meta, f.type) : [])
  const regions = $derived(classement
    ? [...new Set(classement.liaisons.flatMap((l) => l.regions))].sort((a, b) => a.localeCompare(b, 'fr'))
    : [])
  const filtresActifs = $derived(
    [f.region, f.duree, f.frequence, f.tendance, f.q].filter(Boolean).length)
  const avecTendance = $derived(f.periode === '12m')

  const TYPES: { cle: ChoixType; libelle: string }[] = [
    { cle: 'TGV', libelle: 'TGV' }, { cle: 'Intercités', libelle: 'Intercités' }, { cle: 'Tous', libelle: 'Tous' },
  ]

  /** « d'octobre 2025 à septembre 2026 » pour un type et une période. */
  function quand(t: TypeTrain): string {
    if (!meta) return ''
    const p = meta.periodes[t].find((x) => x.cle === f.periode)
    if (!p) return ''
    if (/^\d{4}$/.test(p.cle)) return p.partielle ? `en ${p.cle} (${periodeTexte(p.debut, p.fin).replace(/ \d{4}/g, '')})` : `en ${p.cle}`
    return periodeTexte(p.debut, p.fin)
  }

  const resume = $derived.by(() => {
    if (!meta) return ''
    if (f.type === 'Tous') {
      return `${toutes.length} liaisons classées : TGV ${quand('TGV')}, Intercités ${quand('Intercités')}.`
    }
    return `${toutes.length} liaisons ${f.type} classées, ${quand(f.type)}.`
  })

  const ouvertParDefaut = typeof matchMedia !== 'undefined' && matchMedia('(min-width: 760px)').matches

  function tendanceTexte(l: Ligne): { texte: string; classe: string; titre: string } {
    const t = l.liaison.tendance
    if (!t) return { texte: '–', classe: '', titre: 'Pas de données sur les 12 derniers mois' }
    if (t.etiquette === 'nouvelle') return { texte: 'nouvelle', classe: '', titre: 'Pas de données sur les 12 mois précédents' }
    const titre = `Part de trains à l'heure : ${pct(t.reg_avant)} sur les 12 mois précédents, ${pct(t.reg_12m)} sur les 12 derniers ; ` +
      `écart à l'évolution moyenne du réseau : ${points(t.delta_relatif)}.`
    if (t.etiquette === 'degradation') return { texte: `↘ ${points(t.delta)}`, classe: 'signal-carmin', titre }
    if (t.etiquette === 'amelioration') return { texte: `↗ ${points(t.delta)}`, classe: 'signal-vert', titre }
    return { texte: 'stable', classe: 'discret', titre }
  }
</script>

<section class="classement" aria-labelledby="titre-classement">
  <h2 id="titre-classement" class="visuellement-cache">Classement</h2>

  <form class="filtres" onsubmit={(e) => e.preventDefault()}>
    <div class="ligne-principale">
      <fieldset class="segments">
        <legend class="visuellement-cache">Type de train</legend>
        {#each TYPES as t (t.cle)}
          <label class:actif={f.type === t.cle}>
            <input type="radio" name="type" value={t.cle} checked={f.type === t.cle}
                   onchange={() => maj({ type: t.cle })} />
            {t.libelle}
          </label>
        {/each}
      </fieldset>

      <label class="champ">
        <span>Période</span>
        <select value={f.periode} onchange={(e) => maj({ periode: e.currentTarget.value })}>
          {#each periodes as p (p.cle)}<option value={p.cle}>{p.libelle}</option>{/each}
        </select>
      </label>

      <label class="champ recherche">
        <span>Gare ou liaison</span>
        <input type="search" placeholder="Rennes, Toulouse…" value={f.q}
               oninput={(e) => maj({ q: e.currentTarget.value })} />
      </label>
    </div>

    <details open={ouvertParDefaut}>
      <summary>Filtres et tri{filtresActifs ? ` (${filtresActifs} actif${filtresActifs > 1 ? 's' : ''})` : ''}</summary>
      <div class="ligne-secondaire">
        <label class="champ">
          <span>Région</span>
          <select value={f.region} onchange={(e) => maj({ region: e.currentTarget.value })}>
            <option value="">Toutes les régions</option>
            {#each regions as r (r)}<option value={r}>{r}</option>{/each}
            <option value="International">Liaisons internationales</option>
          </select>
        </label>
        <label class="champ">
          <span>Durée du trajet</span>
          <select value={f.duree} onchange={(e) => maj({ duree: e.currentTarget.value as Filtres['duree'] })}>
            {#each DUREES as d (d.cle)}<option value={d.cle}>{d.libelle}</option>{/each}
          </select>
        </label>
        <label class="champ">
          <span>Fréquence</span>
          <select value={f.frequence} onchange={(e) => maj({ frequence: e.currentTarget.value as Filtres['frequence'] })}>
            {#each FREQUENCES as d (d.cle)}<option value={d.cle}>{d.libelle}</option>{/each}
          </select>
        </label>
        <label class="champ">
          <span>Évolution sur un an</span>
          <select value={f.tendance} onchange={(e) => maj({ tendance: e.currentTarget.value as Filtres['tendance'] })}>
            <option value="">Toutes</option>
            <option value="degradation">En baisse</option>
            <option value="amelioration">En hausse</option>
            <option value="stable">Stables</option>
          </select>
        </label>
        <label class="champ">
          <span>Trier par</span>
          <select value={f.tri} onchange={(e) => maj({ tri: e.currentTarget.value as Filtres['tri'] })}>
            {#each TRIS as t (t.cle)}<option value={t.cle}>{t.libelle}</option>{/each}
          </select>
        </label>
        {#if filtresActifs || f.tri !== 'score'}
          <button type="button" class="effacer" onclick={() => maj({ region: '', duree: '', frequence: '', tendance: '', q: '', tri: 'score' })}>
            Effacer les filtres
          </button>
        {/if}
      </div>
    </details>
  </form>

  {#if erreur}
    <p class="message">Les données n'ont pas pu être chargées : {erreur} Rechargez la page pour réessayer.</p>
  {:else if !classement || !meta}
    <p class="message" aria-live="polite">Chargement du classement…</p>
  {:else}
    <p class="resume" aria-live="polite">
      {resume}
      {#if affichees.length !== toutes.length}
        <strong>{affichees.length} correspondent aux filtres.</strong>
      {/if}
    </p>

    {#if affichees.length === 0}
      <p class="message">Aucune liaison ne correspond à ces filtres. Élargissez la région, la durée ou la fréquence.</p>
    {:else}
      <table class:sans-tendance={!avecTendance}>
        <thead>
          <tr>
            <th scope="col" class="c-rang">Rang</th>
            <th scope="col" class="c-liaison">Liaison</th>
            <th scope="col" class="c-score">Score</th>
            <th scope="col" class="c-num" title="Part des trains ayant circulé arrivés à l'heure (seuil de 5, 10 ou 15 min selon la durée)">À l'heure</th>
            <th scope="col" class="c-num" title="Part des trains prévus qui ont été annulés">Annulés</th>
            <th scope="col" class="c-num" title="Part des trains ayant circulé arrivés avec plus de 30 min de retard">+ 30 min</th>
            <th scope="col" class="c-num" title="Trains prévus par mois en moyenne sur la période">Trains par mois</th>
            {#if avecTendance}
              <th scope="col" class="c-spark" title="Part des trains à l'heure, mois par mois (échelle de 60 à 100 %, pointillé à 90 %)">12 mois</th>
              <th scope="col" class="c-tendance" title="Part de trains à l'heure : 12 derniers mois comparés aux 12 précédents">Sur un an</th>
            {/if}
          </tr>
        </thead>
        <tbody>
          {#each affichees as l (l.liaison.id)}
            {@const t = tendanceTexte(l)}
            <tr>
              <td class="c-rang">
                <span class="rang">{l.rang}</span>
                {#if l.coudeACoude}
                  <span class="coude" title="Au coude à coude avec la liaison classée juste devant : la différence de score est dans la marge d'incertitude">≈</span>
                {/if}
              </td>
              <th scope="row" class="c-liaison">
                <a class="nom" href={lienLiaison(l.liaison.id, f.periode !== '12m' ? { periode: f.periode } : {})}>{l.liaison.a.nom}<span class="tiret">{'\u00a0– '}</span>{l.liaison.b.nom}</a>
                <span class="details">
                  <span class="type">{l.liaison.type}</span>
                  {#if l.liaison.duree}<span>{duree(l.liaison.duree)}</span>{/if}
                  {#if l.partielle}<span class="partielle">données sur {l.mois} mois</span>{/if}
                </span>
              </th>
              <td class="c-score">
                <span class="score signal-{signal(l.score)}" title="Intervalle à 80 % : {nombre(l.bas, 1)} à {nombre(l.haut, 1)}">{nombre(l.score, 1)}</span>
                <ScoreVoie score={l.score} bas={l.bas} haut={l.haut} />
              </td>
              <td class="c-num" data-libelle="À l'heure">{pct(l.regularite)}</td>
              <td class="c-num" data-libelle="Annulés">{pct(l.annulation)}</td>
              <td class="c-num" data-libelle="+ 30 min"
                  title={l.sup30 == null ? 'Non publié pour les Intercités' : undefined}>{pct(l.sup30)}</td>
              <td class="c-num" data-libelle="Trains par mois">{nombre(l.trainsMois)}</td>
              {#if avecTendance}
                <td class="c-spark">{#if l.liaison.spark}<Sparkline valeurs={l.liaison.spark} />{/if}</td>
                <td class="c-tendance {t.classe}" title={t.titre}>{t.texte}</td>
              {/if}
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}

    <div class="notes">
      <p>
        Le <strong>score</strong> est la note moyenne d'un train prévu sur 100 : 100 s'il arrive à l'heure, 67 s'il a
        jusqu'à 30 min de retard, 33 entre 30 et 60 min, 0 au-delà ou s'il est annulé. Les petites liaisons sont
        rapprochées de la moyenne de leur type tant qu'elles ont peu de trains. La barre montre le score (trait) et sa
        marge d'incertitude ; repères à 80 et 90.
        <a href={lien('methodologie')}>Méthode détaillée</a>
      </p>
      {#if f.type !== 'TGV'}
        <p>
          Intercités : la SNCF ne publie pas les retards de plus de 30 min ; ils sont estimés à partir de la moyenne
          TGV. Les trains supprimés la veille avant 16 h n'y sont pas comptés comme annulés, contrairement au TGV.
        </p>
      {/if}
    </div>
  {/if}
</section>

<style>
  .filtres { margin: 0 0 20px; }
  .ligne-principale, .ligne-secondaire { display: flex; flex-wrap: wrap; gap: 12px 16px; align-items: end; }
  .ligne-secondaire { padding-top: 12px; }

  .segments { display: flex; border: 1px solid var(--rail-fort); border-radius: 4px; padding: 0; margin: 0; }
  .segments label {
    position: relative; padding: 7px 14px; cursor: pointer; font-family: var(--police-etroite); font-weight: 600;
    font-size: 1.0625rem; border-right: 1px solid var(--rail-fort);
  }
  .segments label:last-child { border-right: 0; }
  .segments label.actif { background: var(--encre); color: var(--quai); }
  .segments input { position: absolute; opacity: 0; inset: 0; cursor: pointer; }
  .segments label:has(input:focus-visible) { outline: 2px solid var(--voie); outline-offset: 2px; }

  .champ { display: flex; flex-direction: column; gap: 2px; font-size: 0.875rem; color: var(--discret); }
  .champ select, .champ input {
    font-size: 1rem; color: var(--encre); background: var(--surface); border: 1px solid var(--rail-fort);
    border-radius: 4px; padding: 6px 8px; min-height: 38px;
  }
  .recherche { flex: 1 1 200px; max-width: 320px; }
  @media (max-width: 760px) {
    .ligne-principale .champ { flex: 1 1 140px; }
    .ligne-principale select, .ligne-principale input { width: 100%; }
  }
  .recherche input { width: 100%; }

  summary { cursor: pointer; margin-top: 12px; font-weight: 500; color: var(--encre-2); width: fit-content; }
  .effacer {
    background: none; border: 0; color: var(--voie); text-decoration: underline; cursor: pointer; padding: 8px 0;
  }

  .resume { color: var(--encre-2); margin: 0 0 8px; }
  .message { padding: 24px 0; color: var(--encre-2); }

  table { width: 100%; border-collapse: collapse; }
  thead th {
    font-family: var(--police-etroite); font-weight: 500; font-size: 0.875rem; color: var(--discret);
    text-align: left; padding: 8px 8px; border-bottom: 1.5px solid var(--encre); vertical-align: bottom;
  }
  tbody tr { border-bottom: 1px solid var(--rail); }
  tbody tr:hover { background: var(--survol); }
  td, tbody th { padding: 10px 8px; vertical-align: middle; text-align: left; font-weight: 400; }

  .c-rang { width: 3.5rem; white-space: nowrap; }
  .rang { font-family: var(--police-etroite); font-weight: 700; font-size: 1.5rem; line-height: 1; }
  .coude { color: var(--discret); margin-left: 2px; cursor: help; }

  .nom { display: block; font-family: var(--police-etroite); font-weight: 600; font-size: 1.125rem; line-height: 1.2; color: var(--encre); text-decoration: none; }
  .nom:hover { text-decoration: underline; }
  .tiret { color: var(--discret); }
  .details { display: flex; flex-wrap: wrap; gap: 4px 10px; font-size: 0.875rem; color: var(--discret); margin-top: 2px; }
  .type { border: 1px solid var(--rail-fort); border-radius: 3px; padding: 0 5px; font-size: 0.8125rem; color: var(--encre-2); }
  .partielle { color: var(--ambre); }

  .c-score { width: 150px; }
  .score { font-family: var(--police-etroite); font-weight: 700; font-size: 1.375rem; display: block; line-height: 1.1; margin-bottom: 3px; }
  .c-num { text-align: right; white-space: nowrap; }
  thead .c-num { text-align: right; }
  .c-spark { width: 84px; }
  .c-tendance { white-space: nowrap; font-size: 0.9375rem; }
  .discret { color: var(--discret); }

  .notes { margin-top: 24px; max-width: 72ch; font-size: 0.9375rem; color: var(--encre-2); }
  .notes p { margin: 0 0 10px; }

  /* Mobile : chaque liaison devient un bloc (rang, nom, score sur une ligne ; indicateurs dessous) */
  @media (max-width: 760px) {
    thead { display: none; }
    table, tbody { display: block; }
    tbody tr { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 4px 12px; padding: 12px 0; }
    td, tbody th { padding: 0; }
    .c-rang { width: 2.4rem; flex: 0 0 auto; }
    .c-liaison { flex: 1 1 calc(100% - 2.4rem - 6.5rem - 24px); min-width: 0; }
    .c-score { width: 6.5rem; flex: 0 0 auto; }
    /* indicateurs en 2 × 2, alignés sous le nom de la liaison */
    .c-num {
      text-align: left; font-size: 0.875rem; color: var(--encre-2);
      flex: 0 0 calc((100% - 2.4rem - 36px) / 2);
    }
    .c-num::before { content: attr(data-libelle) " "; color: var(--discret); }
    .c-score + .c-num, .c-score + .c-num + .c-num + .c-num { margin-left: calc(2.4rem + 12px); }
    .c-spark { display: none; }
    .c-tendance { flex-basis: 100%; padding-left: calc(2.4rem + 12px); font-size: 0.875rem; }
  }
</style>
