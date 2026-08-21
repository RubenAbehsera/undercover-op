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
      <h1 className="enseigne">
        Undercover OP
        <Chapeau />
      </h1>

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

      <Mentions />
    </section>
  );
}

/** L'attribution doit suivre le jeu là où il se joue, pas seulement le dépôt. */
function Mentions() {
  return (
    <footer className="mentions">
      <p>
        Jeu de fan non officiel, sans lien avec Eiichiro Oda, Shueisha ou Toei
        Animation. <i>One Piece</i> et ses personnages leur appartiennent.
      </p>
      <p>
        Données de personnages et d'arcs dérivées du{" "}
        <a href="https://onepiece.fandom.com" target="_blank" rel="noreferrer">
          One Piece Wiki
        </a>
        , sous licence{" "}
        <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noreferrer">
          CC BY-SA 3.0
        </a>
        .
      </p>
    </footer>
  );
}

/** Le chapeau de paille, posé de travers sur la dernière lettre du nom. */
function Chapeau() {
  return (
    <svg className="chapeau" viewBox="0 0 120 72" aria-hidden="true">
      <ellipse
        cx="60"
        cy="52"
        rx="56"
        ry="17"
        fill="#ebcb84"
        stroke="#b0862f"
        strokeWidth="2.5"
      />
      <path
        d="M26 50c0-19 15-35 34-35s34 16 34 35z"
        fill="#f6dda6"
        stroke="#b0862f"
        strokeWidth="2.5"
      />
      <path d="M27 43c9 6 57 6 66 0l2.5 8c-10 6-61 6-71 0z" fill="#d6402c" />
      <path d="M26 50h68" stroke="#b0862f" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}
