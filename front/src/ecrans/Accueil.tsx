import { useState } from "react";

import { libelleArc } from "../libelles";

type Props = {
  arcs: string[];
  occupe: boolean;
  creer: (pseudo: string, calibrage: string) => void;
  rejoindre: (code: string, pseudo: string) => void;
};

const LONGUEUR_CODE = 4;

/** L'entrée : son pseudo une fois, puis rejoindre une partie ou en créer une. */
export function Accueil({ arcs, occupe, creer, rejoindre }: Props) {
  const [pseudo, setPseudo] = useState("");
  const [calibrage, setCalibrage] = useState("");
  const [code, setCode] = useState("");
  const sansPseudo = !pseudo.trim();

  return (
    <section className="ecran">
      <h1 className="titre">Undercover OP</h1>

      <div className="carte">
        <label>
          Votre pseudo
          <input
            value={pseudo}
            onChange={(evenement) => setPseudo(evenement.target.value)}
            maxLength={16}
          />
        </label>
        <p className="aide">Le même, que vous rejoigniez une partie ou que vous en créiez une.</p>
      </div>

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
        <button type="submit" className="principal" disabled={occupe || sansPseudo}>
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
        <button
          type="submit"
          className="principal"
          disabled={occupe || sansPseudo || !arcs.length}
        >
          Créer
        </button>
      </form>
    </section>
  );
}
