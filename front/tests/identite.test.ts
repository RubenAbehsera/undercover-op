import { expect, test } from "vitest";

import { identite } from "../src/identite";

function stockageFactice() {
  const donnees = new Map<string, string>();
  return {
    getItem: (cle: string) => donnees.get(cle) ?? null,
    setItem: (cle: string, valeur: string) => void donnees.set(cle, valeur),
    removeItem: (cle: string) => void donnees.delete(cle),
    donnees,
  };
}

test("le même navigateur retrouve son joueur dans la même room", () => {
  const stockage = stockageFactice();

  const premier = identite(stockage).idPour("AB12");
  const second = identite(stockage).idPour("AB12");

  expect(second).toBe(premier);
});

test("la room créée est retenue avec son joueur, et retrouvée à la reconnexion", () => {
  const stockage = stockageFactice();
  const moi = identite(stockage);
  const joueur = moi.nouvelId();

  moi.retenir({ code: "CD34", joueur, pseudo: "Nami" });

  expect(identite(stockage).session()).toEqual({
    code: "CD34",
    joueur,
    pseudo: "Nami",
  });
  expect(identite(stockage).idPour("CD34")).toBe(joueur);
});

test("une autre room est un autre joueur, et la sortie oublie la session", () => {
  const stockage = stockageFactice();
  const moi = identite(stockage);

  moi.retenir({ code: "CD34", joueur: moi.nouvelId(), pseudo: "Nami" });

  expect(moi.idPour("ZZ99")).not.toBe(moi.idPour("CD34"));
  moi.oublier();
  expect(moi.session()).toBeNull();
});

test("le personnage reçu survit au rechargement, et part avec la session", () => {
  const stockage = stockageFactice();
  const moi = identite(stockage);
  const luffy = { id: "luffy", nom: "Monkey D. Luffy" };
  moi.retenir({ code: "CD34", joueur: moi.nouvelId(), pseudo: "Nami" });

  moi.retenirPersonnage("CD34", luffy);

  expect(identite(stockage).personnageDe("CD34")).toEqual(luffy);
  expect(moi.personnageDe("ZZ99")).toBeNull();

  moi.oublier();

  expect(moi.personnageDe("CD34")).toBeNull();
});
