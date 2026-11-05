<script lang="ts">
  import { chargerEvenements, chargerMeta } from '../lib/data'
  import { date, mois, nombre, pct } from '../lib/format'
  import { lien } from '../lib/router.svelte'
  import type { Evenement, Meta } from '../lib/types'

  let meta = $state<Meta | null>(null)
  let evenements = $state<Evenement[]>([])
  chargerMeta().then((m) => (meta = m))
  chargerEvenements().then((e) => (evenements = e))

  const DEPOT = 'https://github.com/clement-duffau/sncf_tracking'
  const TYPES_EVT: Record<string, string> = {
    greve: 'Grève', covid: 'COVID-19', incident: 'Incident', meteo: 'Météo', donnees: 'Données', perimetre: 'Périmètre',
  }
  const periodeEvt = (e: Evenement) => (e.debut === e.fin ? mois(e.debut) : `${mois(e.debut)} – ${mois(e.fin)}`)
</script>

<article class="methode">
  <h2>Méthodologie et sources</h2>
  <p class="chapo">
    Ce site classe les liaisons TGV et Intercités selon la fiabilité de leurs trains, à partir des statistiques
    mensuelles publiées par la SNCF. Cette page dit d'où viennent les chiffres, comment le score est calculé et ce
    que les données ne permettent pas de dire.
  </p>

  <nav class="sommaire" aria-label="Sur cette page">
    <a href="#/methodologie#sources">Sources</a>
    <a href="#/methodologie#definitions">Ce qui est mesuré</a>
    <a href="#/methodologie#score">Le score</a>
    <a href="#/methodologie#tendances">Évolutions</a>
    <a href="#/methodologie#evenements">Événements</a>
    <a href="#/methodologie#limites">Limites</a>
    <a href="#/methodologie#licence">Licence et réutilisation</a>
  </nav>

  <section id="sources">
    <h3>Sources</h3>
    <p>
      Toutes les données viennent du portail open data de la SNCF,
      <a href="https://ressources.data.sncf.com">ressources.data.sncf.com</a>, sous licence
      <a href="https://opendatacommons.org/licenses/odbl/1-0/">Open Database License (ODbL)</a>.
      Elles sont téléchargées chaque semaine ; le site est reconstruit quand un jeu a été mis à jour.
    </p>
    {#if meta}
      <table>
        <thead><tr><th scope="col">Jeu de données</th><th scope="col">Producteur</th><th scope="col">Mis à jour le</th></tr></thead>
        <tbody>
          {#each Object.values(meta.sources) as s (s.url)}
            <tr>
              <th scope="row"><a href={s.url}>{s.titre}</a></th>
              <td>{s.editeur}</td>
              <td>{date(s.donnees_mises_a_jour)}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      <p class="discret">
        Derniers mois disponibles : TGV {mois(meta.fenetres.TGV.fin)}, Intercités {mois(meta.fenetres['Intercités'].fin)}.
        La SNCF publie les données TGV environ un mois après les faits, les données Intercités avec deux mois de décalage ou plus.
      </p>
    {/if}
  </section>

  <section id="definitions">
    <h3>Ce qui est mesuré</h3>
    <p>
      Les chiffres sont mensuels, par liaison (par exemple Paris Montparnasse → Toulouse Matabiau) et par sens.
      Un train est <strong>à l'heure</strong> s'il arrive à son terminus avec moins de :
    </p>
    <ul>
      <li>5 minutes de retard pour un trajet de moins de 1 h 30 ;</li>
      <li>10 minutes pour un trajet de 1 h 30 à 3 h ;</li>
      <li>15 minutes pour un trajet de plus de 3 h.</li>
    </ul>
    <p>
      C'est la « régularité composite » de la SNCF, la même pour les TGV et les Intercités. Le retard est mesuré à
      l'arrivée au terminus, à la minute inférieure, par des capteurs à l'entrée de la gare. Les gares intermédiaires
      ne sont pas mesurées.
    </p>
    <p>
      Les liaisons suivies sont celles choisies par l'Autorité de la qualité de service dans les transports (AQST) :
      surtout des liaisons depuis ou vers Paris, quelques transversales et les liaisons internationales de la SNCF.
      Un même train peut compter dans plusieurs liaisons. La somme des liaisons n'est donc pas la régularité nationale
      publiée par la SNCF.
    </p>
    <p>
      <strong>Annulations.</strong> Pour le TGV, les trains prévus incluent les trains annulés. Pour les Intercités, un
      train supprimé avant 16 h la veille n'est pas compté du tout : lors d'une grève annoncée, les trains
      disparaissent des chiffres au lieu d'apparaître comme annulés. Les taux d'annulation des deux types ne sont pas
      comparables.
    </p>
    <p>
      Les deux sens d'une liaison et, pour le TGV, les services national et international sont additionnés dans le
      classement.
    </p>
  </section>

  <section id="score">
    <h3>Le score</h3>
    <p>Chaque train prévu reçoit une note selon ce qui lui est arrivé :</p>
    <table class="bareme">
      <tbody>
        <tr><th scope="row">À l'heure</th><td>100</td></tr>
        <tr><th scope="row">En retard, jusqu'à 30 min</th><td>67</td></tr>
        <tr><th scope="row">En retard de 30 à 60 min</th><td>33</td></tr>
        <tr><th scope="row">En retard de plus de 60 min</th><td>0</td></tr>
        <tr><th scope="row">Annulé</th><td>0</td></tr>
      </tbody>
    </table>
    <p>
      Le score d'une liaison est la note moyenne de ses trains sur la période. Il combine ainsi la ponctualité, les
      annulations et la gravité des retards : un retard de 6 minutes ne pèse pas autant qu'un retard d'une heure.
      Ce barème pénalise un peu les trajets longs, plus exposés aux gros retards. Les couleurs suivent des seuils
      fixes : <span class="signal-vert">90 et plus</span>, <span class="signal-ambre">85 à 90</span>,
      <span class="signal-carmin">moins de 85</span>.
    </p>

    <h4>Les petites liaisons et les mois isolés</h4>
    <p>
      Une liaison de 20 trains par mois peut afficher 100 % de trains à l'heure par chance. Pour ne pas la placer en
      tête (ni la pénaliser sur un mauvais mois), chaque taux est rapproché de la moyenne de son type de train,
      d'autant plus que la liaison a peu de trains : c'est un rétrécissement bayésien, comme les notes pondérées des
      classements d'albums.
    </p>
    <p class="formule">taux retenu = (événements observés + M × moyenne du type) ÷ (trains + M)</p>
    {#if meta}
      <p>
        Le poids M vaut {nombre(meta.parametres.poids_prior.TGV)} trains pour le TGV et
        {nombre(meta.parametres.poids_prior['Intercités'])} pour les Intercités, soit environ un mois d'une liaison
        moyenne. Sur 12 mois, une liaison typique n'est presque pas modifiée ; sur un seul mois, une petite liaison
        l'est beaucoup.
      </p>
      <p>
        Ce poids a été estimé sur les données elles-mêmes, en tenant compte du fait que les retards d'un même mois
        ne sont pas indépendants : une panne ou une canicule touche beaucoup de trains à la fois. La variance
        mensuelle observée est environ {nombre(meta.parametres.surdispersion.TGV)} fois celle de trains
        indépendants pour le TGV. La même correction sert à calculer la marge d'incertitude du score (intervalle à
        80 %), dessinée en épaisseur sur la barre. Deux liaisons marquées « ≈ » sont au coude à coude : leur écart
        tient dans cette marge.
      </p>
      <h4>Intercités : gravité estimée</h4>
      <p>
        La SNCF ne publie pas les retards de plus de 30 ou 60 minutes des Intercités. Leurs trains en retard sont
        répartis comme ceux du TGV sur les mêmes mois (sur les 12 derniers mois :
        {pct(meta.parametres.moyennes_12m.TGV.q30)} de plus de 30 min et
        {pct(meta.parametres.moyennes_12m.TGV.q60)} de plus de 60 min parmi les trains en retard). Les Intercités sont donc
        départagés sur leurs retards et leurs annulations, sur la même échelle que le TGV.
      </p>
    {/if}
    <h4>Périodes</h4>
    <p>
      « 12 derniers mois » s'arrête au dernier mois publié pour chaque type de train. Les années civiles en cours sont
      partielles. Une liaison qui a moins de 6 mois de données sur la période est signalée.
    </p>
  </section>

  <section id="tendances">
    <h3>Évolutions</h3>
    <p>
      L'évolution compare la part de trains à l'heure des 12 derniers mois à celle des 12 mois précédents. Elle est
      dite en hausse ou en baisse si l'écart dépasse 2 points et reste net une fois prise en compte la variabilité
      d'un mois à l'autre (test statistique au seuil de 2 écarts-types). Les mois de grève et de confinement listés
      plus bas sont retirés de cette comparaison.
    </p>
    <p>
      Quand tout le réseau se dégrade, presque toutes les liaisons sont « en baisse ». L'infobulle de la colonne
      « Sur un an » donne aussi l'écart à l'évolution moyenne du réseau.
    </p>
  </section>

  <section id="evenements">
    <h3>Événements</h3>
    <p>
      Grèves, confinements et ruptures dans les données sont annotés à la main, avec leurs sources
      (<a href="{DEPOT}/blob/main/data/events.yaml">data/events.yaml</a>). Ils restent comptés dans le score, qui
      décrit ce qu'ont vécu les voyageurs, mais sont retirés des évolutions.
    </p>
    <ul class="evenements">
      {#each evenements as e (e.id)}
        <li>
          <span class="evt-quand">{periodeEvt(e)}</span>
          <span class="evt-type">{TYPES_EVT[e.type] ?? e.type}</span>
          <strong>{e.titre}</strong>
          <span class="evt-texte">{e.observe}</span>
          {#each e.sources as s, i (s)}<a href={s}>source{e.sources.length > 1 ? ` ${i + 1}` : ''}</a>{' '}{/each}
        </li>
      {/each}
    </ul>
  </section>

  <section id="limites">
    <h3>Limites</h3>
    <ul>
      <li>Les données sont mensuelles et par liaison : rien par train, par horaire ni par gare intermédiaire.</li>
      <li>On ne sait pas si les OUIGO sont inclus dans les liaisons : la SNCF ne le précise pas.</li>
      <li>
        De janvier à mars 2025, les nombres de trains en retard de plus de 30 et 60 minutes publiés sont incohérents
        (nuls ou négatifs) : ils sont ignorés.
      </li>
      <li>
        En mai 2026, la répartition des causes de retard change brutalement, probablement à cause d'un nouveau
        classement non documenté. Les causes d'avant et d'après ne sont pas comparées.
      </li>
      <li>
        Pour Lille et Montpellier (TGV) et Lyon (Intercités depuis 2018), la gare exacte n'est pas précisée dans les
        données.
      </li>
      <li>Les régularités TER ne sont publiées que par région : elles ne sont pas mélangées aux liaisons.</li>
    </ul>
  </section>

  <section id="licence">
    <h3>Licence et réutilisation</h3>
    <p>
      Données : SNCF Voyageurs (régularité TGV, Intercités, TER) et SNCF Gares &amp; Connexions (gares de voyageurs),
      via ressources.data.sncf.com, sous licence ODbL. Les tableaux calculés pour ce site forment une base de données
      dérivée, diffusée sous la même licence ODbL. Vous pouvez les télécharger :
    </p>
    <ul>
      <li><a href="data/donnees/scores.csv" download>Scores par liaison et période</a></li>
      <li><a href="data/donnees/mesures_mensuelles.csv" download>Nombres de trains par liaison, sens et mois</a></li>
      <li><a href="data/donnees/liaisons.csv" download>Liaisons</a> et <a href="data/donnees/gares.csv" download>gares</a></li>
      <li><a href="data/donnees/LICENCE.md">Conditions d'utilisation (ODbL)</a></li>
    </ul>
    <p>
      Le code du site et du traitement des données est publié sous licence MIT :
      <a href={DEPOT}>github.com/clement-duffau/sncf_tracking</a>. L'exploration détaillée des données y est
      décrite (<a href="{DEPOT}/blob/main/docs/DATA.md">docs/DATA.md</a>,
      <a href="{DEPOT}/blob/main/docs/PLAN.md">docs/PLAN.md</a>).
    </p>
    <p><a href={lien('')}>Retour au classement</a></p>
  </section>
</article>

<style>
  .methode { max-width: 74ch; }
  h2 { font-size: clamp(1.75rem, 4vw, 2.25rem); margin-bottom: 12px; }
  h3 { font-size: 1.5rem; margin: 40px 0 12px; padding-top: 12px; border-top: 1.5px solid var(--encre); }
  h4 { font-family: var(--police-etroite); font-size: 1.1875rem; margin: 24px 0 8px; }
  p, li { line-height: 1.6; }
  .chapo { font-size: 1.125rem; color: var(--encre-2); }
  .discret { color: var(--discret); font-size: 0.9375rem; }
  .sommaire { display: flex; flex-wrap: wrap; gap: 6px 18px; margin: 16px 0 8px; font-size: 0.9375rem; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 0.9375rem; }
  th, td { text-align: left; padding: 6px 8px 6px 0; border-bottom: 1px solid var(--rail); vertical-align: top; }
  thead th { font-weight: 500; color: var(--discret); border-bottom: 1.5px solid var(--encre); }
  tbody th { font-weight: 400; }
  .bareme { width: auto; min-width: 18rem; }
  .bareme td { text-align: right; font-family: var(--police-etroite); font-weight: 700; font-size: 1.125rem; padding-left: 24px; }
  .formule {
    font-family: var(--police-etroite); font-size: 1.125rem; padding: 10px 14px; border-left: 3px solid var(--voie);
    background: var(--surface);
  }
  .evenements { list-style: none; padding: 0; }
  .evenements li { padding: 10px 0; border-bottom: 1px solid var(--rail); }
  .evt-quand { font-family: var(--police-etroite); font-weight: 600; margin-right: 8px; }
  .evt-type { font-size: 0.8125rem; border: 1px solid var(--rail-fort); border-radius: 3px; padding: 0 5px; margin-right: 6px; color: var(--encre-2); }
  .evt-texte { display: block; color: var(--encre-2); font-size: 0.9375rem; margin: 2px 0; }
</style>
