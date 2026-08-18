/** Ce qui n'existe qu'à l'affichage : les slugs mis en français lisible. */

/** Les trois niveaux du retour de fin de partie (le serveur ne voit que 1, 2, 3). */
export const NIVEAUX = [
  { niveau: 1, libelle: "Bof" },
  { niveau: 2, libelle: "Sympa" },
  { niveau: 3, libelle: "Excellent" },
] as const;

export function libelleArc(slug: string): string {
  return slug
    .split("_")
    .map((mot) => mot.charAt(0).toUpperCase() + mot.slice(1))
    .join(" ");
}
