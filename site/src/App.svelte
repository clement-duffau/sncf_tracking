<script lang="ts">
  import { tick } from 'svelte'
  import { chargerMeta } from './lib/data'
  import { date } from './lib/format'
  import { ROUTES, lien, route } from './lib/router.svelte'
  import type { Meta } from './lib/types'
  import Classement from './pages/Classement.svelte'
  import Methodologie from './pages/Methodologie.svelte'

  let meta = $state<Meta | null>(null)
  chargerMeta().then((m) => (meta = m)).catch(() => {})

  // ancre interne (#/methodologie#score) : défilement vers la section
  $effect(() => {
    const ancre = route.ancre
    if (ancre) tick().then(() => document.getElementById(ancre)?.scrollIntoView())
  })

  const titres: Record<string, string> = { '': 'Le classement des liaisons ferroviaires', methodologie: 'Méthodologie et sources' }
  $effect(() => {
    document.title = route.path ? `${titres[route.path]} – Le classement des liaisons ferroviaires` : titres['']
  })
</script>

<a class="evitement" href="#contenu" onclick={(e) => { e.preventDefault(); document.getElementById('contenu')?.focus() }}>
  Aller au contenu
</a>

<header class="entete">
  <div class="cadre">
    <h1><a href={lien('')}>Le classement des liaisons ferroviaires</a></h1>
    <p class="accroche">La fiabilité des TGV et Intercités, liaison par liaison, d'après les chiffres publiés par la SNCF.</p>
    <nav aria-label="Pages">
      {#each ROUTES as r (r.path)}
        <a href={lien(r.path)} aria-current={route.path === r.path ? 'page' : undefined}>{r.label}</a>
      {/each}
    </nav>
  </div>
</header>

<main id="contenu" tabindex="-1" class="cadre">
  {#if route.path === 'methodologie'}
    <Methodologie />
  {:else}
    <Classement />
  {/if}
</main>

<footer class="pied">
  <div class="cadre">
    <p>
      Données : SNCF Voyageurs et SNCF Gares &amp; Connexions,
      <a href="https://ressources.data.sncf.com">ressources.data.sncf.com</a>, licence ODbL{#if meta}. Données TGV mises à jour le
      {date(meta.sources.tgv_aqst.donnees_mises_a_jour)}{/if}.
      Données dérivées sous licence ODbL, code sous licence MIT.
    </p>
    <p>
      <a href={lien('methodologie')}>Méthodologie et sources</a>
      <span aria-hidden="true">|</span>
      <a href="https://github.com/clement-duffau/sncf_tracking">Code source</a>
    </p>
  </div>
</footer>

<style>
  .cadre { max-width: var(--largeur); margin: 0 auto; padding: 0 var(--gouttiere); }
  .entete { padding: clamp(20px, 4vw, 36px) 0 0; margin-bottom: 20px; }
  h1 { font-size: clamp(1.75rem, 5vw, 3rem); font-weight: 700; letter-spacing: -0.01em; max-width: 20ch; }
  h1 a { color: inherit; text-decoration: none; }
  .accroche { margin: 8px 0 0; color: var(--encre-2); font-size: 1.0625rem; max-width: 60ch; }
  nav { display: flex; gap: 20px; margin-top: 18px; border-bottom: 1px solid var(--rail); }
  nav a {
    color: var(--encre-2); text-decoration: none; padding: 8px 0; font-weight: 500;
    border-bottom: 3px solid transparent; margin-bottom: -1px;
  }
  nav a[aria-current='page'] { color: var(--encre); border-bottom-color: var(--encre); }
  nav a:hover { color: var(--encre); }
  main { min-height: 60vh; outline: none; }
  .pied { margin-top: 56px; padding: 20px 0 32px; border-top: 1px solid var(--rail); font-size: 0.875rem; color: var(--discret); }
  .pied p { margin: 0 0 6px; max-width: 90ch; }
  .pied span { margin: 0 6px; }
</style>
