import { useState } from "react";

import type { Fiche } from "./contrat";
import { portrait } from "./libelles";

/** Une place à table : le joueur, et son personnage quand on a le droit de le voir. */
export type Place = {
  pseudo: string;
  fiche: Fiche | null;
  moi?: boolean;
  parle?: boolean;
  gagne?: boolean;
};

type ProprietesAffiche = {
  fiche: Fiche | null;
  /** Hors révélation : absent. Sinon le tampon, vert ou rouge. */
  gagne?: boolean;
  grande?: boolean;
};

/** Un avis de recherche : le portrait, ou la silhouette de celui qu'on n'a pas vu. */
export function Affiche({ fiche, gagne, grande }: ProprietesAffiche) {
  const Nom = grande ? "h1" : "p";
  // Les portraits ne sont pas versionnés (droits d'auteur, cf. README) : sur un
  // dépôt fraîchement cloné le fichier manque, et la silhouette reprend la main
  // plutôt qu'une image cassée. On retient l'id, pas un booléen — la manche
  // suivante amène une autre fiche, qui a droit à sa chance.
  const [rate, setRate] = useState<string | null>(null);

  return (
    <div className={grande ? "affiche grande" : "affiche"}>
      <span className="affiche-bandeau" aria-hidden="true">
        Avis de recherche
      </span>
      <span className="affiche-vue">
        {fiche && rate !== fiche.id ? (
          <img
            className="portrait"
            src={portrait(fiche.id)}
            alt=""
            decoding="async"
            loading={grande ? undefined : "lazy"}
            fetchPriority={grande ? "high" : undefined}
            onError={() => setRate(fiche.id)}
          />
        ) : (
          <span className="silhouette" />
        )}
      </span>
      <Nom className="affiche-nom">{fiche ? fiche.nom : "?"}</Nom>
      {gagne !== undefined && (
        <span className={gagne ? "tampon gagne" : "tampon perdu"}>
          {gagne ? "Gagné" : "Perdu"}
        </span>
      )}
    </div>
  );
}

/** La tablée : le mur d'affiches, une par joueur.
 *
 * Une affiche reste vierge tant que le personnage n'est pas connu — et il ne
 * l'est que pour soi, jusqu'à la révélation qui les tamponne toutes.
 */
export function Tablee({ places }: { places: Place[] }) {
  return (
    <ul className="tablee">
      {places.map((place) => (
        <li key={place.pseudo} className={classes(place)}>
          <Affiche fiche={place.fiche} gagne={place.gagne} />
          <span className="pseudo">{place.pseudo}</span>
        </li>
      ))}
    </ul>
  );
}

function classes(place: Place): string | undefined {
  const etats = [place.moi && "moi", place.parle && "parle"].filter(Boolean);
  return etats.length ? etats.join(" ") : undefined;
}
