/** Le fil vers le serveur : on émet des intentions, il répond par un ack.
 *
 * Le serveur est monté sur la même origine que le bundle qu'il sert ; en
 * développement, Vite fait suivre `/socket.io`.
 */

import { io, type Socket } from "socket.io-client";

import type { Ack } from "./contrat";

const DELAI = 8000;

export function connecter(): Socket {
  return io({ path: "/socket.io" });
}

/** Une demande et sa réponse — un serveur muet est un refus comme un autre. */
export async function demander(
  socket: Socket,
  evenement: string,
  charge?: unknown,
): Promise<Ack> {
  const arguments_ = charge === undefined ? [] : [charge];
  try {
    return (await socket.timeout(DELAI).emitWithAck(evenement, ...arguments_)) as Ack;
  } catch {
    return { ok: false, motif: "serveur_muet", message: "aucune réponse" };
  }
}
