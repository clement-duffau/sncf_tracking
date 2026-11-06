<script lang="ts">
  import { pct } from '../format'

  /**
   * Une barre par ligne (année), découpée en parts qui somment à 100 %.
   * Écart de 2 px entre les parts, coins de 4 px, la première part porte sa valeur si elle tient.
   * Survol ou focus d'une part : sa valeur s'affiche dans la ligne de lecture (et dans l'infobulle native).
   */
  interface Categorie { cle: string; libelle: string; couleur: string; texte?: string }
  interface Ligne { libelle: string; note?: string; parts: Record<string, number | null>; avantTexte?: string }

  let { categories, lignes, nom }: { categories: Categorie[]; lignes: Ligne[]; nom: string } = $props()

  let lecture = $state<string>('')
  const GAP = 2

  function segments(l: Ligne) {
    const presentes = categories.filter((c) => (l.parts[c.cle] ?? 0) > 0.0005)
    const total = presentes.reduce((t, c) => t + (l.parts[c.cle] ?? 0), 0) || 1
    let cumul = 0
    return presentes.map((c, k) => {
      const v = (l.parts[c.cle] ?? 0) / total
      const s = { c, v, debut: cumul, premier: k === 0, dernier: k === presentes.length - 1 }
      cumul += v
      return s
    })
  }
  const texte = (l: Ligne, c: Categorie, v: number) => `${l.libelle} : ${c.libelle.toLowerCase()} ${pct(v)}`
</script>

<div class="barres">
  <ul class="legende">
    {#each categories as c (c.cle)}<li><span class="cle" style:background={c.couleur}></span>{c.libelle}</li>{/each}
  </ul>
  <p class="lecture" aria-live="polite">{lecture || ' '}</p>
  <div role="list" aria-label={nom}>
    {#each lignes as l (l.libelle)}
      {#if l.avantTexte}<p class="separateur">{l.avantTexte}</p>{/if}
      <div class="ligne" role="listitem">
        <span class="libelle">{l.libelle}{#if l.note}<span class="note">{l.note}</span>{/if}</span>
        <div class="piste">
          {#each segments(l) as s (s.c.cle)}
            <button type="button"
              class="part" class:premier={s.premier} class:dernier={s.dernier}
              style:left="calc({s.debut * 100}% + {s.premier ? 0 : GAP / 2}px)"
              style:width="calc({s.v * 100}% - {(s.premier ? 0 : GAP / 2) + (s.dernier ? 0 : GAP / 2)}px)"
              style:background={s.c.couleur}
              aria-label={texte(l, s.c, s.v)} title={texte(l, s.c, s.v)}
              onpointerenter={() => (lecture = texte(l, s.c, s.v))} onfocus={() => (lecture = texte(l, s.c, s.v))}
              onpointerleave={() => (lecture = '')} onblur={() => (lecture = '')}
            >
              {#if s.premier && s.v >= 0.18}<span class="valeur" style:color={s.c.texte ?? '#fff'}>{pct(s.v, 0)}</span>{/if}
            </button>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .legende { display: flex; flex-wrap: wrap; gap: 4px 16px; list-style: none; padding: 0; margin: 0 0 4px; font-size: 0.875rem; color: var(--encre-2); }
  .cle { display: inline-block; width: 12px; height: 12px; border-radius: 3px; vertical-align: -1px; margin-right: 6px; }
  .lecture { margin: 0 0 8px; font-size: 0.9375rem; min-height: 1.5em; }
  .ligne { display: grid; grid-template-columns: 7.5rem 1fr; align-items: center; gap: 10px; margin: 0 0 6px; }
  .libelle { font-family: var(--police-etroite); font-weight: 600; font-size: 0.9375rem; line-height: 1.15; }
  .note { display: block; font-family: var(--police); font-weight: 400; font-size: 0.75rem; color: var(--discret); }
  .piste { position: relative; height: 24px; }
  .part { position: absolute; top: 0; bottom: 0; border: 0; padding: 0; margin: 0; border-radius: 0; cursor: default; outline-offset: 2px; }
  .part.premier { border-radius: 4px 0 0 4px; }
  .part.dernier { border-radius: 0 4px 4px 0; }
  .part.premier.dernier { border-radius: 4px; }
  .part:hover { filter: brightness(1.12); }
  .valeur { position: absolute; left: 6px; top: 50%; transform: translateY(-50%); font-size: 0.8125rem; font-weight: 600; white-space: nowrap; }
  .separateur { margin: 12px 0 8px; padding-top: 8px; border-top: 1px dashed var(--rail-fort); font-size: 0.875rem; color: var(--encre-2); }
</style>
