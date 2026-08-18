import type { Revelation as Bilan } from "../contrat";

type Props = { revelation: Bilan; retourSalle: () => void };

/** La révélation : le duo, l'imposteur, le lien, le dépouillement nominatif. */
export function Revelation({ revelation, retourSalle }: Props) {
  return (
    <section className="ecran">
      <h1 className="titre">{revelation.demasque ? "Démasqué !" : "L'intrus s'en tire"}</h1>

      <p className="duo">
        <strong>{revelation.majorite.nom}</strong> et{" "}
        <strong>{revelation.imposteur.nom}</strong>
      </p>
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
