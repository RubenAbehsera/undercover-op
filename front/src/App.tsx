import { useCallback, useEffect, useMemo, useReducer, useState } from "react";

import type { Ack, Fiche, Revelation as Bilan, SalleAttente as Salle, Tour, VoteOuvert } from "./contrat";
import { Accueil } from "./ecrans/Accueil";
import { Fin } from "./ecrans/Fin";
import { Manche } from "./ecrans/Manche";
import { Revelation } from "./ecrans/Revelation";
import { SalleAttente } from "./ecrans/SalleAttente";
import { Vote } from "./ecrans/Vote";
import { INITIAL, ecran, reduire } from "./etat";
import { identite, type Session } from "./identite";
import { estTransitoire, phrase } from "./motifs";
import { connecter, demander } from "./socket";

/** Le client : il écoute les diffusions, envoie des intentions, n'arbitre rien. */
export function App() {
  const socket = useMemo(() => connecter(), []);
  const memoire = useMemo(() => identite(localStorage), []);

  const [session, setSession] = useState<Session | null>(() => memoire.session());
  const [etat, geste] = useReducer(reduire, {
    ...INITIAL,
    // Un rechargement en pleine manche ne se rejoue pas : le serveur ne
    // redistribue les personnages qu'à la manche suivante.
    personnage: memoire.personnageDe(session?.code),
  });
  const [arcs, setArcs] = useState<string[]>([]);
  const [refus, setRefus] = useState<string | null>(null);
  const [occupe, setOccupe] = useState(false);

  useEffect(() => {
    socket.on("salle_attente", (charge: Salle) => geste({ type: "salle_attente", charge }));
    socket.on("personnage", (charge: Fiche) => {
      const courante = memoire.session();
      if (courante) memoire.retenirPersonnage(courante.code, charge);
      geste({ type: "personnage", charge });
    });
    socket.on("tour", (charge: Tour) => geste({ type: "tour", charge }));
    socket.on("vote_ouvert", (charge: VoteOuvert) => geste({ type: "vote_ouvert", charge }));
    socket.on("revelation", (charge: Bilan) => geste({ type: "revelation", charge }));
    socket.on("partie_terminee", () => geste({ type: "partie_terminee" }));
    return () => void socket.removeAllListeners();
  }, [socket, memoire]);

  useEffect(() => {
    /** À chaque (re)connexion : les arcs, puis la room d'où l'on vient. */
    async function reprendre() {
      const ack = await demander(socket, "arcs");
      if (ack.ok) setArcs(ack.arcs as string[]);
      const precedente = memoire.session();
      if (!precedente) return;
      const retour = await demander(socket, "rejoindre_room", {
        joueur: precedente.joueur,
        code: precedente.code,
        pseudo: precedente.pseudo,
      });
      if (retour.ok || estTransitoire(retour.motif)) return;
      memoire.oublier();
      setSession(null);
      geste({ type: "sortie" });
    }
    socket.on("connect", reprendre);
    return () => void socket.off("connect", reprendre);
  }, [socket, memoire]);

  const agir = useCallback(
    async (evenement: string, charge?: unknown): Promise<Ack> => {
      setOccupe(true);
      setRefus(null);
      const ack = await demander(socket, evenement, charge);
      setOccupe(false);
      if (!ack.ok) setRefus(phrase(ack.motif));
      return ack;
    },
    [socket],
  );

  const entrer = useCallback(
    async (evenement: string, joueur: string, pseudo: string, charge: object) => {
      const ack = await agir(evenement, { joueur, pseudo, ...charge });
      if (!ack.ok) return;
      const retenue = { code: ack.code as string, joueur, pseudo };
      memoire.retenir(retenue);
      setSession(retenue);
    },
    [agir, memoire],
  );

  const sortir = useCallback(async () => {
    await agir("quitter_room");
    memoire.oublier();
    setSession(null);
    geste({ type: "sortie" });
  }, [agir, memoire]);

  const moi = session?.pseudo ?? "";
  const estHote = etat.salle !== null && etat.salle.hote === moi;
  const vue = ecran(etat);

  return (
    <main>
      {refus && (
        <p className="refus" onClick={() => setRefus(null)}>
          {refus}
        </p>
      )}
      {vue === "accueil" && (
        <Accueil
          arcs={arcs}
          occupe={occupe}
          creer={(pseudo, calibrage) =>
            entrer("creer_room", memoire.nouvelId(), pseudo.trim(), { calibrage })
          }
          rejoindre={(code, pseudo) => {
            const propre = code.trim().toUpperCase();
            const precedente = memoire.session();
            // Le serveur garde le pseudo d'un ID qu'il connaît déjà : le
            // reprendre tel quel, sinon l'écran ne se reconnaîtrait plus.
            const retenu = precedente?.code === propre ? precedente.pseudo : pseudo.trim();
            entrer("rejoindre_room", memoire.idPour(propre), retenu, { code: propre });
          }}
        />
      )}
      {vue === "attente" && etat.salle && (
        <SalleAttente
          salle={etat.salle}
          moi={moi}
          estHote={estHote}
          lancer={() => agir("lancer_manche")}
          terminer={() => agir("terminer_partie")}
          quitter={sortir}
        />
      )}
      {vue === "manche" && etat.phase?.ecran === "manche" && etat.personnage && (
        <Manche
          personnage={etat.personnage}
          tour={etat.phase.tour}
          estOrateur={etat.phase.tour.orateur === moi}
          estHote={estHote}
          meconnaissance={etat.meconnaissance}
          passer={() => agir("passer")}
          ouvrirVote={() => agir("ouvrir_vote")}
          signaler={async () => {
            const ack = await agir("je_ne_connais_pas");
            if (ack.ok) geste({ type: "meconnaissance" });
          }}
        />
      )}
      {vue === "vote" && etat.phase?.ecran === "vote" && (
        <Vote
          bulletin={etat.phase.bulletin}
          moi={moi}
          vote={etat.vote}
          estHote={estHote}
          voter={async (cible) => {
            const ack = await agir("voter", { cible });
            if (ack.ok) geste({ type: "vote_emis", cible });
          }}
          forcer={() => agir("forcer_vote")}
        />
      )}
      {vue === "revelation" && etat.phase?.ecran === "revelation" && (
        <Revelation
          revelation={etat.phase.revelation}
          retourSalle={() => geste({ type: "retour_salle" })}
        />
      )}
      {vue === "fin" && (
        <Fin
          retourDonne={etat.retourDonne}
          envoyer={async (niveau, commentaire) => {
            const ack = await agir("retour", {
              niveau,
              commentaire: commentaire.trim() || null,
            });
            if (ack.ok) geste({ type: "retour_donne" });
          }}
          quitter={sortir}
        />
      )}
    </main>
  );
}
