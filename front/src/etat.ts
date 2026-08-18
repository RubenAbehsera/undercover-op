/** Ce que le client sait : le dernier mot du serveur, et ses propres gestes.
 *
 * Aucune règle de jeu ici — pas un tour compté, pas une majorité calculée. On
 * range les diffusions à mesure qu'elles tombent et on en déduit l'écran.
 */

import type { Fiche, Revelation, SalleAttente, Tour, VoteOuvert } from "./contrat";

export type Phase =
  | { ecran: "manche"; tour: Tour }
  | { ecran: "vote"; bulletin: VoteOuvert }
  | { ecran: "revelation"; revelation: Revelation };

export type Etat = {
  salle: SalleAttente | null;
  personnage: Fiche | null;
  phase: Phase | null;
  /** Le pseudo pour qui l'on a voté cette manche — le serveur, lui, l'a compté. */
  vote: string | null;
  /** Le drapeau « je ne connais pas » : une fois levé, il reste levé. */
  meconnaissance: boolean;
  terminee: boolean;
  retourDonne: boolean;
};

export type Ecran =
  | "accueil"
  | "attente"
  | "manche"
  | "vote"
  | "revelation"
  | "fin";

export type Geste =
  | { type: "salle_attente"; charge: SalleAttente }
  | { type: "personnage"; charge: Fiche }
  | { type: "tour"; charge: Tour }
  | { type: "vote_ouvert"; charge: VoteOuvert }
  | { type: "revelation"; charge: Revelation }
  | { type: "retour_salle" }
  | { type: "vote_emis"; cible: string }
  | { type: "meconnaissance" }
  | { type: "partie_terminee" }
  | { type: "retour_donne" }
  | { type: "sortie" };

export const INITIAL: Etat = {
  salle: null,
  personnage: null,
  phase: null,
  vote: null,
  meconnaissance: false,
  terminee: false,
  retourDonne: false,
};

export function reduire(etat: Etat, geste: Geste): Etat {
  switch (geste.type) {
    case "salle_attente":
      return { ...etat, salle: geste.charge };
    case "personnage":
      return { ...etat, personnage: geste.charge, vote: null, meconnaissance: false };
    case "tour":
      return { ...etat, phase: { ecran: "manche", tour: geste.charge } };
    case "vote_ouvert":
      return { ...etat, phase: { ecran: "vote", bulletin: geste.charge } };
    case "revelation":
      return { ...etat, phase: { ecran: "revelation", revelation: geste.charge } };
    case "retour_salle":
      return { ...etat, phase: null };
    case "vote_emis":
      return { ...etat, vote: geste.cible };
    case "meconnaissance":
      return { ...etat, meconnaissance: true };
    case "partie_terminee":
      return { ...etat, terminee: true };
    case "retour_donne":
      return { ...etat, retourDonne: true };
    case "sortie":
      return INITIAL;
  }
}

export function ecran(etat: Etat): Ecran {
  if (etat.terminee) return "fin";
  if (etat.phase) return etat.phase.ecran;
  return etat.salle ? "attente" : "accueil";
}
