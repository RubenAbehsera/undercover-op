/** Le contrat socket, tel que le serveur le tient — les payloads, rien de plus.
 *
 * Le front n'ajoute aucun champ, n'en dérive aucun : tout ce qu'il affiche est
 * arrivé par une diffusion.
 */

export type Fiche = { id: string; nom: string };

export type SalleAttente = {
  code: string;
  calibrage: string;
  hote: string;
  joueurs: string[];
};

export type Tour = { ordre: string[]; orateur: string; tour: number };

export type VoteOuvert = { joueurs: string[] };

export type Bulletin = { votant: string; cible: string };

export type Revelation = {
  majorite: Fiche;
  imposteur: Fiche;
  joueur_imposteur: string;
  lien: string;
  votes: Bulletin[];
  designe: string | null;
  demasque: boolean;
  tours: number;
};

export type Ack =
  | ({ ok: true } & Record<string, unknown>)
  | { ok: false; motif: string; message: string };
