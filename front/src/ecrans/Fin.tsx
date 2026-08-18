import { useState } from "react";

import { NIVEAUX } from "../libelles";

type Props = {
  retourDonne: boolean;
  envoyer: (niveau: number, commentaire: string) => void;
  quitter: () => void;
};

/** La fin de partie : le retour, en un tap, une seule fois. */
export function Fin({ retourDonne, envoyer, quitter }: Props) {
  const [commentaire, setCommentaire] = useState("");

  if (retourDonne) {
    return (
      <section className="ecran">
        <h1 className="titre">Merci !</h1>
        <button type="button" className="principal" onClick={quitter}>
          Quitter
        </button>
      </section>
    );
  }

  return (
    <section className="ecran">
      <h1 className="titre">C'était comment ?</h1>
      <ul className="niveaux">
        {NIVEAUX.map(({ niveau, libelle }) => (
          <li key={niveau}>
            <button
              type="button"
              className="principal"
              onClick={() => envoyer(niveau, commentaire)}
            >
              {libelle}
            </button>
          </li>
        ))}
      </ul>
      <label>
        Un mot, si le cœur vous en dit
        <textarea
          value={commentaire}
          onChange={(evenement) => setCommentaire(evenement.target.value)}
          rows={3}
          maxLength={500}
        />
      </label>
      <button type="button" className="discret" onClick={quitter}>
        Quitter sans répondre
      </button>
    </section>
  );
}
