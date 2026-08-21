# Une image, un conteneur : le serveur de jeu sert aussi le bundle du front.

FROM node:22-alpine AS front
WORKDIR /front
COPY front/package.json front/package-lock.json ./
RUN npm ci
COPY front/ ./
RUN npm run build

# Les portraits ne sont pas versionnés — ce sont des captures sous droits
# Toei/Shueisha (cf. README, « Licences »). Le dépôt n'en redistribue aucune ;
# c'est le build qui va les chercher, pour l'instance qui le lance. L'image
# produite les contient donc : elle se déploie sur une instance privée, pas
# publiée telle quelle.
FROM python:3.13-slim AS portraits
WORKDIR /fabrication
# telecharger() se rabat sur curl quand urllib échoue : sans lui, l'échec est
# un FileNotFoundError que personne n'attrape.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
# Deux étapes séparées pour deux caches : la moisson du wiki ne dépend que de
# pages.txt, l'extraction des portraits du contrat. Ajouter des paires sans
# nouveau personnage ne refait donc pas la moisson.
COPY fabrication/wiki_extract.py ./
COPY fabrication/seeds/pages.txt ./seeds/pages.txt
RUN python wiki_extract.py
COPY fabrication/portraits_extract.py fabrication/paires.json ./
RUN python portraits_extract.py

FROM python:3.13-slim
WORKDIR /app

COPY server/pyproject.toml ./server/pyproject.toml
COPY server/jeu ./server/jeu
RUN pip install --no-cache-dir ./server

COPY fabrication/paires.json ./fabrication/paires.json
COPY --from=front /front/dist ./front/dist
COPY --from=portraits /front/public/personnages ./front/dist/personnages

# Le paquet est installé en site-packages : les chemins relatifs au source ne
# valent plus rien, tout se dit ici.
ENV CONTRAT_PAIRES=/app/fabrication/paires.json \
    FRONT_DIST=/app/front/dist \
    SIGNAUX_SQLITE=/donnees/signaux.db

EXPOSE 8000
CMD ["python", "-m", "jeu"]
