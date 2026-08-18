import type { Fiche, Tour } from "../contrat";

type Props = {
  personnage: Fiche;
  tour: Tour;
  estOrateur: boolean;
  estHote: boolean;
  meconnaissance: boolean;
  passer: () => void;
  ouvrirVote: () => void;
  signaler: () => void;
};

/** La manche vue du joueur : son personnage, l'ordre, et ses seuls boutons.
 *
 * Le personnage s'affiche tel qu'il est arrivé — même forme pour tous, rien
 * dans le rendu ne trahit qui a tiré l'autre nom.
 */
export function Manche({
  personnage,
  tour,
  estOrateur,
  estHote,
  meconnaissance,
  passer,
  ouvrirVote,
  signaler,
}: Props) {
  return (
    <section className="ecran">
      <p className="etiquette">Votre personnage</p>
      <h1 className="personnage">{personnage.nom}</h1>

      <p className="etiquette">Tour {tour.tour}</p>
      <ol className="ordre">
        {tour.ordre.map((pseudo) => (
          <li key={pseudo} className={pseudo === tour.orateur ? "parle" : undefined}>
            {pseudo}
          </li>
        ))}
      </ol>
      <p className="parole">
        {estOrateur ? "À vous de parler." : `${tour.orateur} a la parole.`}
      </p>

      {estOrateur && (
        <button type="button" className="principal" onClick={passer}>
          J'ai fini
        </button>
      )}
      {estHote && (
        <button type="button" className="principal" onClick={ouvrirVote}>
          Ouvrir le vote
        </button>
      )}
      <button
        type="button"
        className="discret"
        onClick={signaler}
        disabled={meconnaissance}
      >
        {meconnaissance ? "C'est signalé" : "Je ne connais pas ce personnage"}
      </button>
    </section>
  );
}
