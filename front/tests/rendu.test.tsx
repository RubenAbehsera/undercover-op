import { renderToStaticMarkup } from "react-dom/server";
import { expect, test } from "vitest";

import type { Fiche, Revelation as Bilan } from "../src/contrat";
import { Manche } from "../src/ecrans/Manche";
import { Revelation } from "../src/ecrans/Revelation";

const TOUR = { ordre: ["Zoro", "Nami", "Usopp"], orateur: "Zoro", tour: 1 };
const BILAN: Bilan = {
  majorite: { id: "luffy", nom: "Monkey D. Luffy" },
  imposteur: { id: "ace", nom: "Portgas D. Ace" },
  joueur_imposteur: "Usopp",
  lien: "Frères de serment",
  votes: [{ votant: "Nami", cible: "Usopp" }],
  designe: "Usopp",
  demasque: true,
  tours: 2,
};

/** Le rendu débarrassé de ce qui nomme le personnage : texte et portrait.
 *
 * React précharge l'image du personnage par un <link href> hissé en tête : lui
 * aussi porte le nom, lui aussi doit tomber avant la comparaison.
 */
function squelette(html: string): string {
  return html.replace(/>[^<]*</g, "><").replace(/(src|href)="[^"]*"/g, '$1=""');
}

type Options = { meconnaissance?: boolean; estOrateur?: boolean; estHote?: boolean };

function manche(personnage: Fiche, options: Options = {}): string {
  return renderToStaticMarkup(
    <Manche
      personnage={personnage}
      tour={TOUR}
      moi="Nami"
      estOrateur={options.estOrateur ?? false}
      estHote={options.estHote ?? false}
      meconnaissance={options.meconnaissance ?? false}
      passer={() => {}}
      ouvrirVote={() => {}}
      signaler={() => {}}
    />,
  );
}

function revelation(bilan: Bilan, moi: string): string {
  return renderToStaticMarkup(
    <Revelation revelation={bilan} moi={moi} ordre={TOUR.ordre} retourSalle={() => {}} />,
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
  const leve = manche({ id: "ace", nom: "Portgas D. Ace" }, { meconnaissance: true });
  const baisse = manche({ id: "ace", nom: "Portgas D. Ace" });

  expect(leve).not.toBe(baisse);
  expect(squelette(leve).replace(/ disabled=""/, "")).toBe(squelette(baisse));
});

test("au mur, seule sa propre affiche porte un portrait", () => {
  const html = manche({ id: "ace", nom: "Portgas D. Ace" });
  const portraits = html.match(/\/personnages\/ace\.webp/g) ?? [];

  // La sienne à la tablée, la grande au-dessus, son préchargement : pas une de
  // plus, aucun autre personnage n'affleure.
  expect(portraits).toHaveLength(3);
  expect(html.match(/class="silhouette"/g)).toHaveLength(TOUR.ordre.length - 1);
  expect(html.match(/class="tampon/g)).toBeNull();
});

test("hors de son tour, aucun bouton primaire ne traîne à l'écran", () => {
  const attend = manche({ id: "ace", nom: "Portgas D. Ace" });
  const parle = manche({ id: "ace", nom: "Portgas D. Ace" }, { estOrateur: true });

  expect(attend).not.toContain('class="principal"');
  expect(parle).toContain("Je passe la parole");
});

test("le contrôle d'hôte n'existe que chez l'hôte, et passe par une confirmation", () => {
  const joueur = manche({ id: "ace", nom: "Portgas D. Ace" });
  const hote = manche({ id: "ace", nom: "Portgas D. Ace" }, { estHote: true });

  expect(joueur).not.toContain("Ouvrir le vote");
  expect(hote).toContain('class="pastille"');
  // Le dialogue est rendu fermé : il ne s'ouvre que sur le geste de l'hôte.
  expect(hote).toContain("<dialog");
  expect(hote).not.toContain("open=");
  expect(hote).toContain("Oui, ouvrir le vote");
});

test("la révélation remplit tout le mur et tamponne chaque camp", () => {
  const html = revelation(BILAN, "Nami");

  expect(html.match(/\/personnages\/luffy\.webp/g)).toHaveLength(2);
  expect(html.match(/\/personnages\/ace\.webp/g)).toHaveLength(1);
  expect(html.match(/class="tampon gagne"/g)).toHaveLength(2);
  expect(html.match(/class="tampon perdu"/g)).toHaveLength(1);
});

test("le verdict est celui de son propre camp", () => {
  expect(revelation(BILAN, "Nami")).toContain("Vous avez gagné");
  expect(revelation(BILAN, "Usopp")).toContain("Vous avez perdu");

  const echappe = { ...BILAN, demasque: false, designe: null };
  expect(revelation(echappe, "Nami")).toContain("Vous avez perdu");
  expect(revelation(echappe, "Usopp")).toContain("Vous avez gagné");
});
