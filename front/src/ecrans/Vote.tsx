import type { VoteOuvert } from "../contrat";

type Props = {
  bulletin: VoteOuvert;
  moi: string;
  vote: string | null;
  estHote: boolean;
  voter: (cible: string) => void;
  forcer: () => void;
};

/** Le vote : la liste des joueurs, soi excepté, puis l'attente. */
export function Vote({ bulletin, moi, vote, estHote, voter, forcer }: Props) {
  return (
    <section className="ecran">
      <h1 className="titre">Qui est l'intrus ?</h1>

      {vote ? (
        <p className="parole">Votre voix est allée à {vote}. On attend les autres.</p>
      ) : (
        <ul className="joueurs">
          {bulletin.joueurs
            .filter((pseudo) => pseudo !== moi)
            .map((pseudo) => (
              <li key={pseudo}>
                <button type="button" className="principal" onClick={() => voter(pseudo)}>
                  {pseudo}
                </button>
              </li>
            ))}
        </ul>
      )}

      {estHote && (
        <button type="button" className="discret" onClick={forcer}>
          Forcer le dépouillement
        </button>
      )}
    </section>
  );
}
