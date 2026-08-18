import { useState } from "react";

import { libelleArc } from "../libelles";

type Props = {
  arcs: string[];
  occupe: boolean;
  creer: (pseudo: string, calibrage: string) => void;
  rejoindre: (code: string, pseudo: string) => void;
};

const LONGUEUR_CODE = 4;

/** L'entrée : on crée une partie, ou on en rejoint une avec son code. */
export function Accueil({ arcs, occupe, creer, rejoindre }: Props) {
  const [pseudo, setPseudo] = useState("");
  const [calibrage, setCalibrage] = useState("");
  const [code, setCode] = useState("");

  return (
    <section className="ecran">
      <h1 className="titre">Undercover OP</h1>

      <form
        className="carte"
        onSubmit={(evenement) => {
          evenement.preventDefault();
          rejoindre(code, pseudo);
        }}
      >
        <h2>Rejoindre une partie</h2>
        <label>
          Code de la room
          <input
            className="code"
            value={code}
            onChange={(evenement) => setCode(evenement.target.value.toUpperCase())}
            maxLength={LONGUEUR_CODE}
            autoCapitalize="characters"
            autoCorrect="off"
            spellCheck={false}
            inputMode="text"
            required
          />
        </label>
        <label>
          Votre pseudo
          <input
            value={pseudo}
            onChange={(evenement) => setPseudo(evenement.target.value)}
            maxLength={16}
            required
          />
        </label>
        <button type="submit" className="principal" disabled={occupe}>
          Rejoindre
        </button>
      </form>

      <form
        className="carte"
        onSubmit={(evenement) => {
          evenement.preventDefault();
          creer(pseudo, calibrage || arcs[0]);
        }}
      >
        <h2>Créer une partie</h2>
        <label>
          Jusqu'où l'histoire est connue
          <select
            value={calibrage || arcs[0] || ""}
            onChange={(evenement) => setCalibrage(evenement.target.value)}
          >
            {arcs.map((arc) => (
              <option key={arc} value={arc}>
                {libelleArc(arc)}
              </option>
            ))}
          </select>
        </label>
        <button type="submit" className="principal" disabled={occupe || !arcs.length}>
          Créer
        </button>
        <p className="aide">Le pseudo saisi ci-dessus sera le vôtre.</p>
      </form>
    </section>
  );
}
