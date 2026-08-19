import type { Revelation as Bilan } from "../contrat";
import { Tablee } from "../Tablee";

type Props = {
  revelation: Bilan;
  moi: string;
  ordre: string[];
  retourSalle: () => void;
};

/** La révélation : le mur d'affiches tamponné, le lien, le dépouillement.
 *
 * Chaque affiche se remplit — le personnage de chacun — et reçoit son tampon :
 * l'imposteur gagne tant qu'il n'est pas démasqué, la majorité l'inverse.
 */
export function Revelation({ revelation, moi, ordre, retourSalle }: Props) {
  const gagne = aGagne(revelation, moi);

  return (
    <section className="ecran">
      <p className={gagne ? "verdict gagne" : "verdict perdu"}>
        {gagne ? "Vous avez gagné" : "Vous avez perdu"}
      </p>
      <h1 className="titre">{revelation.demasque ? "Démasqué !" : "L'intrus s'en tire"}</h1>

      <Tablee places={tablee(revelation, ordre)} />

      <p className="aide">{revelation.lien}</p>
      <p className="parole">
        {revelation.imposteur.nom}, c'était {revelation.joueur_imposteur}.
      </p>

      <p className="etiquette">Dépouillement</p>
      <ul className="joueurs">
        {revelation.votes.map((bulletin) => (
          <li key={bulletin.votant}>
            {bulletin.votant} → {bulletin.cible}
          </li>
        ))}
      </ul>
      <p className="aide">
        {revelation.designe
          ? `Désigné : ${revelation.designe}`
          : "Aucune majorité : personne n'est désigné."}
      </p>

      <button type="button" className="principal" onClick={retourSalle}>
        Retour à la salle
      </button>
    </section>
  );
}

/** Qui l'emporte : l'imposteur s'il file, la majorité si elle le démasque. */
function aGagne(revelation: Bilan, pseudo: string): boolean {
  return revelation.demasque !== (pseudo === revelation.joueur_imposteur);
}

function tablee(revelation: Bilan, ordre: string[]) {
  // Un imposteur parti en cours de manche a quitté l'ordre de parole : sa place
  // à table lui revient quand même, c'est celle que tout le monde attend.
  const places = ordre.includes(revelation.joueur_imposteur)
    ? ordre
    : [...ordre, revelation.joueur_imposteur];
  return places.map((pseudo) => ({
    pseudo,
    fiche:
      pseudo === revelation.joueur_imposteur ? revelation.imposteur : revelation.majorite,
    gagne: aGagne(revelation, pseudo),
  }));
}
