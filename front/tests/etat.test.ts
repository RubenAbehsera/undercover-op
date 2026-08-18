import { expect, test } from "vitest";

import { INITIAL, ecran, reduire } from "../src/etat";
import type { Geste } from "../src/etat";

const SALLE = {
  code: "AB12",
  calibrage: "arabasta",
  hote: "Nami",
  joueurs: ["Nami", "Zoro", "Usopp"],
};
const TOUR = { ordre: ["Zoro", "Nami", "Usopp"], orateur: "Zoro", tour: 1 };
const REVELATION = {
  majorite: { id: "luffy", nom: "Monkey D. Luffy" },
  imposteur: { id: "ace", nom: "Portgas D. Ace" },
  joueur_imposteur: "Usopp",
  lien: "Frères par serment",
  votes: [{ votant: "Nami", cible: "Usopp" }],
  designe: "Usopp",
  demasque: true,
  tours: 2,
};

function suite(...gestes: Geste[]) {
  return gestes.reduce(reduire, INITIAL);
}

test("l'écran suit les diffusions, de l'accueil à la révélation", () => {
  expect(ecran(INITIAL)).toBe("accueil");
  expect(ecran(suite({ type: "salle_attente", charge: SALLE }))).toBe("attente");
  expect(ecran(suite({ type: "tour", charge: TOUR }))).toBe("manche");
  expect(
    ecran(suite({ type: "vote_ouvert", charge: { joueurs: ["Nami", "Zoro"] } })),
  ).toBe("vote");
  expect(ecran(suite({ type: "revelation", charge: REVELATION }))).toBe("revelation");
});

test("un mouvement dans la salle ne chasse pas la manche de l'écran", () => {
  const etat = suite(
    { type: "tour", charge: TOUR },
    { type: "salle_attente", charge: SALLE },
  );

  expect(ecran(etat)).toBe("manche");
  expect(etat.salle).toEqual(SALLE);
});

test("la révélation tient jusqu'à ce qu'on revienne à la salle, ou qu'une manche reprenne", () => {
  const revele = suite(
    { type: "salle_attente", charge: SALLE },
    { type: "revelation", charge: REVELATION },
  );

  expect(ecran(reduire(revele, { type: "retour_salle" }))).toBe("attente");
  expect(ecran(reduire(revele, { type: "tour", charge: TOUR }))).toBe("manche");
});

test("une nouvelle distribution rend le vote et le drapeau à neuf", () => {
  const etat = suite(
    { type: "personnage", charge: { id: "luffy", nom: "Monkey D. Luffy" } },
    { type: "vote_emis", cible: "Zoro" },
    { type: "meconnaissance" },
  );

  expect(etat.vote).toBe("Zoro");
  expect(etat.meconnaissance).toBe(true);

  const suivante = reduire(etat, {
    type: "personnage",
    charge: { id: "ace", nom: "Portgas D. Ace" },
  });

  expect(suivante.vote).toBeNull();
  expect(suivante.meconnaissance).toBe(false);
});

test("la fin de partie prend le pas sur tout, et le retour ne se donne qu'une fois", () => {
  const finie = suite({ type: "tour", charge: TOUR }, { type: "partie_terminee" });

  expect(ecran(finie)).toBe("fin");
  expect(finie.retourDonne).toBe(false);
  expect(reduire(finie, { type: "retour_donne" }).retourDonne).toBe(true);
});

test("quitter la room ramène à l'accueil, sans rien garder de la partie", () => {
  const sorti = suite(
    { type: "salle_attente", charge: SALLE },
    { type: "revelation", charge: REVELATION },
    { type: "sortie" },
  );

  expect(ecran(sorti)).toBe("accueil");
  expect(sorti).toEqual(INITIAL);
});
