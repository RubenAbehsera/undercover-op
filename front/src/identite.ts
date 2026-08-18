/** L'identité sans compte : un ID opaque par room, rangé dans le navigateur.
 *
 * Le pseudo n'est que l'affichage ; l'ID est ce que le serveur reconnaît. Il
 * est tiré au premier passage et retenu sous le code de la room — un autre
 * navigateur, ou un autre code, est un autre joueur. La session dit où l'on
 * était, et le personnage de la manche en cours y attend un rechargement : le
 * serveur ne le redistribue qu'à la manche suivante.
 */

import type { Fiche } from "./contrat";

export type Stockage = Pick<Storage, "getItem" | "setItem" | "removeItem">;

export type Session = { code: string; joueur: string; pseudo: string };

const JOUEUR = "undercover-op:joueur:";
const PERSONNAGE = "undercover-op:personnage:";
const SESSION = "undercover-op:session";

export function identite(stockage: Stockage) {
  function session(): Session | null {
    return lire<Session>(stockage, SESSION);
  }

  return {
    /** L'ID de cette room : celui d'avant s'il existe, un neuf sinon. */
    idPour(code: string): string {
      const connu = stockage.getItem(JOUEUR + code);
      if (connu) return connu;
      const neuf = tirer();
      stockage.setItem(JOUEUR + code, neuf);
      return neuf;
    },

    /** Un ID avant de connaître le code — l'hôte n'a pas encore sa room. */
    nouvelId: tirer,

    retenir(session: Session): void {
      stockage.setItem(JOUEUR + session.code, session.joueur);
      stockage.setItem(SESSION, JSON.stringify(session));
    },

    session,

    retenirPersonnage(code: string, personnage: Fiche): void {
      stockage.setItem(PERSONNAGE + code, JSON.stringify(personnage));
    },

    personnageDe(code: string | undefined): Fiche | null {
      return code ? lire<Fiche>(stockage, PERSONNAGE + code) : null;
    },

    oublier(): void {
      const courante = session();
      if (courante) stockage.removeItem(PERSONNAGE + courante.code);
      stockage.removeItem(SESSION);
    },
  };
}

/** Un ID opaque sans `randomUUID` : celui-ci exige un contexte sécurisé, et
 *  une soirée se joue souvent en HTTP sur le réseau local. */
function tirer(): string {
  const octets = crypto.getRandomValues(new Uint8Array(16));
  return [...octets].map((octet) => octet.toString(16).padStart(2, "0")).join("");
}

function lire<T>(stockage: Stockage, cle: string): T | null {
  const brut = stockage.getItem(cle);
  if (!brut) return null;
  try {
    return JSON.parse(brut) as T;
  } catch {
    return null;
  }
}
