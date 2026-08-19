import { useRef } from "react";

import type { Fiche, Tour } from "../contrat";
import { Affiche, Tablee } from "../Tablee";

type Props = {
  personnage: Fiche;
  tour: Tour;
  moi: string;
  estOrateur: boolean;
  estHote: boolean;
  meconnaissance: boolean;
  passer: () => void;
  ouvrirVote: () => void;
  signaler: () => void;
};

/** La manche vue du joueur : son affiche, la tablée, et ses seuls boutons.
 *
 * Le personnage s'affiche tel qu'il est arrivé — même forme pour tous, rien
 * dans le rendu ne trahit qui a tiré l'autre nom. Les affiches des autres
 * restent vierges : on ne voit que la sienne.
 *
 * Trois natures de contrôle, trois places : rendre la parole est fréquent et
 * sans risque, il occupe la zone du pouce ; ouvrir le vote est irréversible et
 * réservé à l'hôte, il se retire dans le coin et se confirme ; « je ne connais
 * pas » n'est pas une action mais un aveu, il se glisse sous le personnage.
 */
export function Manche({
  personnage,
  tour,
  moi,
  estOrateur,
  estHote,
  meconnaissance,
  passer,
  ouvrirVote,
  signaler,
}: Props) {
  const dialogue = useRef<HTMLDialogElement>(null);

  return (
    <section className="ecran">
      <div className="entete">
        <p className="etiquette">Votre personnage</p>
        {estHote && (
          <button
            type="button"
            className="pastille"
            aria-haspopup="dialog"
            onClick={() => dialogue.current?.showModal()}
          >
            <IconeVote />
            Ouvrir le vote
          </button>
        )}
      </div>

      <Affiche fiche={personnage} grande />

      <button
        type="button"
        className="lien"
        onClick={signaler}
        disabled={meconnaissance}
      >
        {meconnaissance ? "Signalé" : "Je ne connais pas ce personnage"}
      </button>

      <p className="etiquette">Tour {tour.tour}</p>
      <Tablee
        places={tour.ordre.map((pseudo) => ({
          pseudo,
          fiche: pseudo === moi ? personnage : null,
          moi: pseudo === moi,
          parle: pseudo === tour.orateur,
        }))}
      />
      <p className="parole">
        {estOrateur ? "À vous de parler." : `${tour.orateur} a la parole.`}
      </p>

      {estOrateur && (
        <button type="button" className="principal" onClick={passer}>
          Je passe la parole
          <IconeSuivant />
        </button>
      )}

      {/* Le dialogue n'est rendu que chez l'hôte : personne d'autre n'a ce
          contrôle, personne d'autre n'en porte le balisage. */}
      {estHote && (
        <dialog className="confirmation" ref={dialogue} aria-labelledby="titre-vote">
          <h2 id="titre-vote">Ouvrir le vote ?</h2>
          <p>
            Les tours de parole s'arrêtent là : plus personne ne parlera avant
            la révélation.
          </p>
          <div className="choix">
            <button
              type="button"
              className="principal"
              onClick={() => {
                dialogue.current?.close();
                ouvrirVote();
              }}
            >
              Oui, ouvrir le vote
            </button>
            <button
              type="button"
              className="discret"
              onClick={() => dialogue.current?.close()}
            >
              Annuler
            </button>
          </div>
        </dialog>
      )}
    </section>
  );
}

function IconeVote() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M2 6.5 8 3l6 3.5v6.5H2z" />
      <path d="m5.4 9.4 1.8 1.6 3.4-3.4" />
    </svg>
  );
}

function IconeSuivant() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="m9 6 6 6-6 6" />
    </svg>
  );
}
