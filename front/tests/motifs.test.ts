import { expect, test } from "vitest";

import { estTransitoire, phrase } from "../src/motifs";

test("un refus connu s'affiche traduit", () => {
  expect(phrase("pseudo_pris")).toBe("Ce pseudo est déjà pris dans la room.");
});

test("un refus inattendu reste muet sur le message du serveur", () => {
  expect(phrase("motif_de_demain")).toBe("Demande refusée.");
});

test("un refus passager ne fait pas perdre sa place au joueur", () => {
  expect(estTransitoire("serveur_muet")).toBe(true);
  expect(estTransitoire("manche_en_cours")).toBe(true);
  expect(estTransitoire("code_inconnu")).toBe(false);
});
