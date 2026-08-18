/** Les refus du serveur, dits en français.
 *
 * Le serveur envoie un motif stable et un message technique : c'est le motif
 * qui s'affiche, traduit ici, jamais le message.
 */

const PHRASES: Record<string, string> = {
  payload_invalide: "Demande incomplète.",
  hors_room: "Vous n'êtes plus dans une room.",
  code_inconnu: "Aucune room ne porte ce code.",
  calibrage_inconnu: "Ce calibrage n'existe pas.",
  room_pleine: "La room est pleine.",
  pseudo_pris: "Ce pseudo est déjà pris dans la room.",
  pseudo_invalide: "Pseudo trop court : deux caractères au minimum.",
  manche_en_cours: "Une manche est en cours : on ne rejoint qu'entre les manches.",
  joueurs_insuffisants: "Il faut au moins trois joueurs pour lancer une manche.",
  pas_hote: "Réservé à l'hôte.",
  pas_de_manche: "Aucune manche en cours.",
  pas_ton_tour: "Ce n'est pas à vous de parler.",
  vote_impossible: "Le vote a déjà eu lieu.",
  pas_de_vote: "Aucun vote en cours.",
  vote_pour_soi: "On ne vote pas pour soi.",
  cible_inconnue: "Ce joueur n'est plus dans la manche.",
  hors_manche: "Vous ne participez plus à cette manche.",
  deja_vote: "Vous avez déjà voté.",
  manche_terminee: "La manche est terminée.",
  deja_signale: "C'est déjà signalé.",
  partie_terminee: "La partie est terminée.",
  partie_en_cours: "La partie n'est pas encore terminée.",
  niveau_invalide: "Ce niveau n'existe pas.",
  serveur_muet: "Le serveur ne répond pas.",
  deja_repondu: "Vous avez déjà donné votre retour.",
};

/** Les refus qui passeront : la place du joueur dans la room n'est pas perdue. */
const TRANSITOIRES = new Set(["serveur_muet", "manche_en_cours"]);

export function phrase(motif: string): string {
  return PHRASES[motif] ?? "Demande refusée.";
}

export function estTransitoire(motif: string): boolean {
  return TRANSITOIRES.has(motif);
}
