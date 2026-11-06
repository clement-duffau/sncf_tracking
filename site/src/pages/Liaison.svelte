<script lang="ts">
  import { signal } from '../lib/classement'
  import BarresSegmentees from '../lib/charts/BarresSegmentees.svelte'
  import LigneMensuelle from '../lib/charts/LigneMensuelle.svelte'
  import MoisTrajet from '../lib/charts/MoisTrajet.svelte'
  import ScoreVoie from '../lib/charts/ScoreVoie.svelte'
  import MiniCarte from '../lib/carte/MiniCarte.svelte'
  import { chargerEvenements, chargerFiche, chargerGares, chargerMeta, chargerStats } from '../lib/data'
  import { CAUSES, causesParPeriode, parAnnee, regulariteMensuelle, regulariteType, serieSens, versCSV, type ChoixSens } from '../lib/fiche'
  import { duree, mois, nombre, pct, periodeTexte, points } from '../lib/format'
  import { lien, route, setParams } from '../lib/router.svelte'
  import { scoreMoyenType } from '../lib/score'
  import type { Evenement, Fiche, Gare, Meta, Stats } from '../lib/types'

  let fiche = $state<Fiche | null>(null)
  let meta = $state<Meta | null>(null)
  let stats = $state<Stats | null>(null)
  let evenements = $state<Evenement[]>([])
  let gares = $state<Gare[]>([])
  let erreur = $state<string | null>(null)

  $effect(() => {
    const id = route.id
    fiche = null
    erreur = null
    Promise.all([chargerFiche(id), chargerMeta(), chargerStats(), chargerEvenements(), chargerGares()])
      .then(([f, m, s, e, g]) => { fiche = f; meta = m; stats = s; evenements = e; gares = g })
      .catch(() => { erreur = id })
  })

  $effect(() => { if (fiche) document.title = `${fiche.nom} – Le classement des liaisons ferroviaires` })

  const sens = $derived<ChoixSens>(route.params.sens === 'ab' || route.params.sens === 'ba' ? route.params.sens : 'deux')
  const sensTrajet = $derived(sens === 'ba' ? 'ba' : 'ab')
  const periodes = $derived(fiche ? Object.keys(fiche.scores).sort((a, b) => (a === '12m' ? -1 : b === '12m' ? 1 : a === 'tout' ? 1 : b === 'tout' ? -1 : b.localeCompare(a))) : [])
  const periode = $derived(route.params.periode && fiche?.scores[route.params.periode] ? route.params.periode : (fiche?.scores['12m'] ? '12m' : 'tout'))
  const sc = $derived(fiche?.scores[periode])
  const infoPeriode = $derived(meta && fiche ? meta.periodes[fiche.type].find((p) => p.cle === periode) : undefined)

  function maj(p: Record<string, string>) {
    const suivant = { ...route.params, ...p }
    if (suivant.sens === 'deux') delete suivant.sens
    if (suivant.periode === '12m') delete suivant.periode
    setParams(suivant)
  }

  const nomSens = (s: ChoixSens) => !fiche ? '' : s === 'deux' ? 'Les deux sens' : s === 'ab' ? `${fiche.a.nom} → ${fiche.b.nom}` : `${fiche.b.nom} → ${fiche.a.nom}`
  const serie = $derived(fiche ? serieSens(fiche, sens) : null)
  const reference = $derived(stats && fiche ? regulariteType(stats, fiche.type) : new Map<string, number>())
  const bandes = $derived(evenements
    .filter((e) => fiche?.evenements.includes(e.id) && ['greve', 'covid', 'incident', 'meteo'].includes(e.type))
    .map((e) => ({ debut: e.debut, fin: e.fin, titre: e.titre })))
  const notesDonnees = $derived(evenements.filter((e) => fiche?.evenements.includes(e.id) && (e.type === 'donnees' || e.type === 'perimetre')))

  const ISSUES_TGV = [
    { cle: 'aLHeure', libelle: 'À l’heure', couleur: 'var(--issue-heure)', texte: 'var(--quai)' },
    { cle: 'retard30', libelle: 'En retard, 30 min au plus', couleur: 'var(--issue-r30)' },
    { cle: 'retard30a60', libelle: 'De 30 à 60 min', couleur: 'var(--issue-r60)' },
    { cle: 'retard60', libelle: 'Plus de 60 min', couleur: 'var(--issue-r60p)' },
    { cle: 'annules', libelle: 'Annulé', couleur: 'var(--issue-annule)' },
  ]
  const ISSUES_IC = [
    { cle: 'aLHeure', libelle: 'À l’heure', couleur: 'var(--issue-heure)', texte: 'var(--quai)' },
    { cle: 'retard30', libelle: 'En retard', couleur: 'var(--issue-r60)' },
    { cle: 'annules', libelle: 'Annulé', couleur: 'var(--issue-annule)' },
  ]
  const annees = $derived(serie && fiche ? parAnnee(serie, fiche.type).reverse() : [])
  const lignesIssues = $derived(annees.map((a) => ({
    libelle: String(a.annee),
    note: [a.mois < 12 ? `${a.mois} mois` : '', a.graviteEstimee ? 'gravité en partie estimée' : ''].filter(Boolean).join(', ') || undefined,
    parts: { aLHeure: a.aLHeure, retard30: a.retard30, retard30a60: a.retard30a60, retard60: a.retard60, annules: a.annules },
  })))

  const CAT_CAUSES = CAUSES.map((c, k) => ({ cle: c.cle, libelle: c.libelle, couleur: `var(--cause-${k + 1})` }))
  const periodesCauses = $derived(serie && fiche?.type === 'TGV' ? causesParPeriode(serie, fiche.rupture_causes).reverse() : [])
  const lignesCauses = $derived(periodesCauses.map((p, k) => ({
    libelle: p.libelle,
    note: `${nombre(p.retards)} trains en retard`,
    parts: p.parts as Record<string, number>,
    avantTexte: p.nomenclature === 1 && k > 0 && periodesCauses[k - 1].nomenclature === 2
      ? `Avant ${mois(fiche!.rupture_causes!)} : la SNCF classait les causes autrement. Les deux périodes ne se comparent pas.`
      : undefined,
  })))

  const coords = (ids: string[]) => ids.map((id) => {
    const g = gares.find((x) => x.id === id)
    return { nom: g?.nom ?? id, lat: g?.lat ?? null, lon: g?.lon ?? null, approx: g?.precision !== 'gare' }
  })

  const moyenneType = $derived(meta && fiche ? scoreMoyenType(meta, fiche.type) : null)

  function telecharger() {
    if (!serie || !fiche) return
    const blob = new Blob([versCSV(serie, fiche.nom, nomSens(sens))], { type: 'text/csv;charset=utf-8' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = `${fiche.id}${sens === 'deux' ? '' : `-${sens}`}.csv`
    a.click()
    URL.revokeObjectURL(a.href)
  }

  const quand = $derived(infoPeriode
    ? (/^\d{4}$/.test(infoPeriode.cle) ? `en ${infoPeriode.cle}${infoPeriode.partielle ? ` (${periodeTexte(infoPeriode.debut, infoPeriode.fin).replace(/ \d{4}/g, '')})` : ''}` : periodeTexte(infoPeriode.debut, infoPeriode.fin))
    : '')
</script>

<p class="retour"><a href={lien('')}>Retour au classement</a></p>

{#if erreur}
  <p class="message">Aucune liaison ne correspond à l'adresse « {erreur} ». Elle a peut-être changé de nom. <a href={lien('')}>Voir le classement</a>.</p>
{:else if !fiche || !meta}
  <p class="message" aria-live="polite">Chargement de la fiche…</p>
{:else}
  <article class="fiche">
    <header class="entete">
      <div class="identite">
        <h2>{fiche.a.nom}<span class="tiret">{' – '}</span>{fiche.b.nom}</h2>
        <p class="details">
          <span class="type">{fiche.type}</span>
          {#if fiche.duree}<span>{duree(fiche.duree)} de trajet en moyenne</span>{/if}
          <span>{[...fiche.regions, ...fiche.pays.filter((p) => p !== 'France')].join(', ')}</span>
          <span>
            {fiche.active ? `Suivie depuis ${mois(fiche.premier_mois)}` : `Suivie de ${mois(fiche.premier_mois)} à ${mois(fiche.dernier_mois)}`}
          </span>
        </p>

        {#if sc}
          <div class="score-bloc">
            <div class="score-principal">
              <span class="score signal-{signal(sc.score)}">{nombre(sc.score, 1)}</span>
              <span class="sur">/ 100</span>
            </div>
            <div class="score-contexte">
              <p>
                <strong>{sc.rang}<sup>{sc.rang === 1 ? 're' : 'e'}</sup> sur {sc.classees}</strong> liaisons {fiche.type} {quand}.
                {#if moyenneType && periode === '12m'}Score de l'ensemble des trains {fiche.type} : {nombre(moyenneType, 1)}.{/if}
              </p>
              <div class="voie"><ScoreVoie score={sc.score} bas={sc.intervalle[0]} haut={sc.intervalle[1]} /></div>
              <p class="discret">Marge d'incertitude : {nombre(sc.intervalle[0], 1)} à {nombre(sc.intervalle[1], 1)}.
                {#if sc.partielle}Données sur {sc.mois} mois seulement.{/if}</p>
            </div>
          </div>
          <dl class="chiffres">
            <div><dt>À l'heure</dt><dd>{pct(sc.regularite)}</dd></div>
            <div><dt>Annulés</dt><dd>{pct(sc.annulation)}</dd></div>
            <div>
              <dt>Plus de 30 min de retard</dt>
              <dd>{sc.sup30 == null ? 'non publié' : pct(sc.sup30)}</dd>
            </div>
            <div><dt>Trains ayant circulé</dt><dd>{nombre(sc.circules)}</dd></div>
          </dl>
          <label class="champ">
            <span>Période</span>
            <select value={periode} onchange={(e) => maj({ periode: e.currentTarget.value })}>
              {#each periodes as p (p)}
                <option value={p}>{p === '12m' ? '12 derniers mois' : p === 'tout' ? 'Tout l’historique' : p}</option>
              {/each}
            </select>
          </label>
        {/if}

        {#if fiche.tendance && fiche.tendance.delta != null}
          <p class="tendance">
            Sur un an, la part de trains à l'heure est passée de {pct(fiche.tendance.reg_avant)} à {pct(fiche.tendance.reg_12m)}
            ({points(fiche.tendance.delta)}) :
            {#if fiche.tendance.etiquette === 'degradation'}<strong class="signal-carmin">en baisse</strong>{:else if fiche.tendance.etiquette === 'amelioration'}<strong class="signal-vert">en hausse</strong>{:else}<strong>stable</strong>{/if}.
            {#if stats?.tendance_reseau[fiche.type] != null}
              Sur la même période, l'ensemble des liaisons {fiche.type} a varié de {points(stats.tendance_reseau[fiche.type])} ;
              {#if fiche.tendance.etiquette_relative === 'degradation'}cette liaison fait nettement moins bien que le réseau.
              {:else if fiche.tendance.etiquette_relative === 'amelioration'}cette liaison fait nettement mieux que le réseau.
              {:else if Math.abs(fiche.tendance.delta_relatif ?? 0) < 0.02}cette liaison suit le réseau.
              {:else}l'écart avec le réseau ({points(fiche.tendance.delta_relatif)}) reste dans la variabilité habituelle d'un mois à l'autre : on ne peut pas conclure.{/if}
            {/if}
          </p>
        {/if}
      </div>
      <aside class="situation">
        <MiniCarte a={coords(fiche.a.gares)} b={coords(fiche.b.gares)} />
      </aside>
    </header>

    <fieldset class="segments">
      <legend>Sens de circulation</legend>
      {#each ['deux', 'ab', 'ba'] as const as s (s)}
        {#if s === 'deux' || fiche.series[s]}
          <label class:actif={sens === s}>
            <input type="radio" name="sens" value={s} checked={sens === s} onchange={() => maj({ sens: s })} />
            {nomSens(s)}
          </label>
        {/if}
      {/each}
    </fieldset>

    {#if serie}
      <section>
        <h3>Mois par mois</h3>
        <p class="intro">Part des trains ayant circulé arrivés à l'heure, comparée à l'ensemble des liaisons {fiche.type} suivies.</p>
        <LigneMensuelle points={regulariteMensuelle(serie)} {reference} nomSerie={nomSens(sens)}
                        nomReference="ensemble des liaisons {fiche.type}" {bandes} />
      </section>

      <section>
        <h3>Ce que deviennent les trains prévus</h3>
        <p class="intro">
          Pour 100 trains prévus, combien arrivent à l'heure, en retard ou sont annulés, année par année.
          {#if fiche.type === 'Intercités'}La SNCF ne publie pas la durée des retards des Intercités.{/if}
        </p>
        <BarresSegmentees categories={fiche.type === 'TGV' ? ISSUES_TGV : ISSUES_IC} lignes={lignesIssues}
                          nom="Issue des trains prévus par année" />
      </section>

      {#if lignesCauses.length}
        <section>
          <h3>Causes des retards</h3>
          <p class="intro">Répartition des trains arrivés en retard selon la cause principale déclarée par la SNCF.</p>
          <BarresSegmentees categories={CAT_CAUSES} lignes={lignesCauses} nom="Causes des retards par année" />
          <details class="definitions">
            <summary>Que recouvre chaque cause ?</summary>
            <ul>{#each CAUSES as c (c.cle)}<li><strong>{c.libelle}</strong> : {c.detail}</li>{/each}</ul>
          </details>
        </section>
      {/if}
    {/if}

    {#if fiche.mon_trajet[sensTrajet]}
      <section>
        <h3>Arriver à l'heure selon le mois</h3>
        <p class="intro">
          Chances qu'un train prévu de <strong>{sensTrajet === 'ab' ? fiche.a.nom : fiche.b.nom}</strong> vers
          <strong>{sensTrajet === 'ab' ? fiche.b.nom : fiche.a.nom}</strong> arrive à l'heure, d'après les cinq dernières
          années (grèves et confinements exclus). Un train annulé compte comme pas à l'heure.
          {#if sens === 'deux'}<button type="button" class="lien" onclick={() => maj({ sens: 'ba' })}>Voir l'autre sens</button>{/if}
        </p>
        <MoisTrajet mois={fiche.mon_trajet[sensTrajet]!} />
      </section>
    {/if}

    <section>
      <h3>Classement année par année</h3>
      <table class="historique">
        <thead>
          <tr><th scope="col">Période</th><th scope="col">Score</th><th scope="col">Rang</th><th scope="col">À l'heure</th>
              <th scope="col">Annulés</th><th scope="col">+ 30 min</th></tr>
        </thead>
        <tbody>
          {#each periodes as p (p)}
            {@const s = fiche.scores[p]}
            <tr class:courante={p === periode}>
              <th scope="row">{p === '12m' ? '12 derniers mois' : p === 'tout' ? 'Tout l’historique' : p}{s.partielle ? ` (${s.mois} mois)` : ''}</th>
              <td class="num"><span class="signal-{signal(s.score)}">{nombre(s.score, 1)}</span></td>
              <td class="num">{s.rang} / {s.classees}</td>
              <td class="num">{pct(s.regularite)}</td>
              <td class="num">{pct(s.annulation)}</td>
              <td class="num">{pct(s.sup30)}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </section>

    {#if notesDonnees.length}
      <section>
        <h3>À savoir sur ces données</h3>
        <ul class="notes">
          {#each notesDonnees as e (e.id)}<li><strong>{e.titre}</strong> ({e.debut === e.fin ? mois(e.debut) : `${mois(e.debut)} – ${mois(e.fin)}`}) : {e.observe}</li>{/each}
        </ul>
      </section>
    {/if}

    {#if serie}
      <section>
        <h3>Données</h3>
        <p class="intro">
          Nombres de trains par mois ({nomSens(sens).toLowerCase() === 'les deux sens' ? 'les deux sens additionnés' : nomSens(sens)}).
          <button type="button" class="lien" onclick={telecharger}>Télécharger en CSV</button> (licence ODbL).
        </p>
        <details>
          <summary>Afficher le tableau ({serie.mois.length} mois)</summary>
          <div class="defilement">
            <table class="donnees">
              <thead>
                <tr><th scope="col">Mois</th><th scope="col">Prévus</th><th scope="col">Annulés</th><th scope="col">En retard</th>
                    {#if serie.sup30}<th scope="col">+ 30 min</th><th scope="col">+ 60 min</th>{/if}<th scope="col">À l'heure</th></tr>
              </thead>
              <tbody>
                {#each serie.mois.map((m, i) => i).reverse() as i (i)}
                  <tr>
                    <th scope="row">{mois(serie.mois[i], true)}</th>
                    <td class="num">{nombre(serie.prevus[i])}</td>
                    <td class="num">{nombre(serie.annules[i])}</td>
                    <td class="num">{nombre(serie.retards[i])}</td>
                    {#if serie.sup30}<td class="num">{nombre(serie.sup30[i])}</td><td class="num">{nombre(serie.sup60?.[i])}</td>{/if}
                    <td class="num">{serie.circules[i] ? pct(1 - serie.retards[i] / serie.circules[i]) : '–'}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </details>
      </section>
    {/if}
  </article>
{/if}

<style>
  .retour { margin: 0 0 12px; font-size: 0.9375rem; }
  .message { padding: 24px 0; color: var(--encre-2); }
  .entete { display: grid; grid-template-columns: minmax(0, 1fr) 260px; gap: 24px 40px; align-items: start; }
  h2 { font-size: clamp(1.75rem, 4.5vw, 2.5rem); }
  .tiret { color: var(--discret); }
  .details { display: flex; flex-wrap: wrap; gap: 4px 14px; margin: 8px 0 20px; color: var(--encre-2); font-size: 0.9375rem; }
  .type { border: 1px solid var(--rail-fort); border-radius: 3px; padding: 0 6px; font-size: 0.875rem; }

  .score-bloc { display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap; }
  .score-principal { line-height: 1; }
  .score { font-family: var(--police-etroite); font-weight: 700; font-size: 4rem; font-variant-numeric: proportional-nums; }
  .sur { font-family: var(--police-etroite); font-size: 1.25rem; color: var(--discret); }
  .score-contexte { flex: 1 1 260px; max-width: 420px; }
  .score-contexte p { margin: 4px 0; }
  .voie { margin: 10px 0 4px; max-width: 320px; }
  .discret { color: var(--discret); font-size: 0.875rem; }

  .chiffres { display: flex; flex-wrap: wrap; gap: 12px 32px; margin: 20px 0 12px; }
  .chiffres dt { font-size: 0.875rem; color: var(--discret); }
  .chiffres dd { margin: 0; font-family: var(--police-etroite); font-weight: 600; font-size: 1.5rem; }
  .champ { display: inline-flex; flex-direction: column; gap: 2px; font-size: 0.875rem; color: var(--discret); }
  .champ select { font-size: 1rem; color: var(--encre); background: var(--surface); border: 1px solid var(--rail-fort); border-radius: 4px; padding: 6px 8px; min-height: 38px; }
  .tendance { max-width: 70ch; margin: 16px 0 0; }

  .segments { display: flex; flex-wrap: wrap; border: 0; padding: 0; margin: 32px 0 0; gap: 0; }
  .segments legend { font-size: 0.875rem; color: var(--discret); margin-bottom: 4px; padding: 0; }
  .segments label {
    position: relative; padding: 7px 14px; cursor: pointer; font-family: var(--police-etroite); font-weight: 600;
    border: 1px solid var(--rail-fort); margin-right: -1px;
  }
  .segments label:first-of-type { border-radius: 4px 0 0 4px; }
  .segments label:last-of-type { border-radius: 0 4px 4px 0; }
  .segments label.actif { background: var(--encre); color: var(--quai); }
  .segments input { position: absolute; opacity: 0; inset: 0; cursor: pointer; }
  .segments label:has(input:focus-visible) { outline: 2px solid var(--voie); outline-offset: 2px; }

  section { margin-top: 40px; }
  h3 { font-size: 1.5rem; padding-top: 12px; border-top: 1.5px solid var(--encre); margin-bottom: 6px; }
  .intro { color: var(--encre-2); max-width: 72ch; margin: 0 0 14px; }
  .lien { background: none; border: 0; padding: 0; color: var(--voie); text-decoration: underline; cursor: pointer; font: inherit; }
  .definitions { margin-top: 12px; font-size: 0.9375rem; }
  .definitions summary { cursor: pointer; color: var(--encre-2); }
  .notes li { margin-bottom: 8px; max-width: 80ch; }

  table { border-collapse: collapse; font-size: 0.9375rem; }
  th, td { padding: 6px 12px 6px 0; border-bottom: 1px solid var(--rail); text-align: left; font-weight: 400; }
  thead th { color: var(--discret); font-weight: 500; border-bottom: 1.5px solid var(--encre); }
  .num { text-align: right; white-space: nowrap; }
  .historique .courante { background: var(--survol); }
  .historique td span { font-family: var(--police-etroite); font-weight: 700; }
  details > summary { cursor: pointer; color: var(--encre-2); margin-bottom: 8px; }
  .defilement { max-height: 420px; overflow: auto; }

  @media (max-width: 760px) {
    .entete { grid-template-columns: 1fr; }
    .situation { max-width: 220px; }
    .score { font-size: 3.25rem; }
  }
</style>
