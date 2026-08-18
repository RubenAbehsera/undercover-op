import type { SalleAttente as Salle } from "../contrat";
import { libelleArc } from "../libelles";

type Props = {
  salle: Salle;
  moi: string;
  estHote: boolean;
  lancer: () => void;
  terminer: () => void;
  quitter: () => void;
};

/** La salle d'attente : le code à dicter, qui est là, et les boutons de l'hôte. */
export function SalleAttente({ salle, moi, estHote, lancer, terminer, quitter }: Props) {
  return (
    <section className="ecran">
      <p className="etiquette">Code de la room</p>
      <p className="code-room">{salle.code}</p>
      <p className="aide">Calibrage : {libelleArc(salle.calibrage)}</p>

      <ul className="joueurs">
        {salle.joueurs.map((pseudo) => (
          <li key={pseudo}>
            {pseudo}
            {pseudo === salle.hote && <span className="badge">hôte</span>}
            {pseudo === moi && <span className="badge">vous</span>}
          </li>
        ))}
      </ul>

      {estHote && (
        <>
          <button type="button" className="principal" onClick={lancer}>
            Lancer la manche
          </button>
          <button type="button" className="discret" onClick={terminer}>
            Terminer la partie
          </button>
        </>
      )}
      <button type="button" className="discret" onClick={quitter}>
        Quitter
      </button>
    </section>
  );
}
