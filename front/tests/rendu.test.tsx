import { renderToStaticMarkup } from "react-dom/server";
import { expect, test } from "vitest";

import type { Fiche } from "../src/contrat";
import { Manche } from "../src/ecrans/Manche";

const TOUR = { ordre: ["Zoro", "Nami", "Usopp"], orateur: "Zoro", tour: 1 };

/** Le rendu débarrassé de son texte : ne restent que les balises et attributs. */
function squelette(html: string): string {
  return html.replace(/>[^<]*</g, "><");
}

function manche(personnage: Fiche, meconnaissance = false): string {
  return renderToStaticMarkup(
    <Manche
      personnage={personnage}
      tour={TOUR}
      estOrateur={false}
      estHote={false}
      meconnaissance={meconnaissance}
      passer={() => {}}
      ouvrirVote={() => {}}
      signaler={() => {}}
    />,
  );
}

test("rien dans le DOM ne distingue le personnage reçu, hors son nom", () => {
  const majorite = manche({ id: "luffy", nom: "Monkey D. Luffy" });
  const imposteur = manche({ id: "ace", nom: "Portgas D. Ace" });

  expect(squelette(imposteur)).toBe(squelette(majorite));
});

test("l'écran de manche ne dit rien du rôle, du duo ni du lien", () => {
  expect(manche({ id: "ace", nom: "Portgas D. Ace" })).not.toMatch(
    /imposteur|majorit|difficult|paire/i,
  );
});

test("le drapeau levé ne change que le libellé du bouton, pour soi seul", () => {
  const leve = manche({ id: "ace", nom: "Portgas D. Ace" }, true);
  const baisse = manche({ id: "ace", nom: "Portgas D. Ace" }, false);

  expect(leve).not.toBe(baisse);
  expect(squelette(leve).replace(/ disabled=""/, "")).toBe(squelette(baisse));
});
