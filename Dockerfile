# Une image, un conteneur : le serveur de jeu sert aussi le bundle du front.

FROM node:22-alpine AS front
WORKDIR /front
COPY front/package.json front/package-lock.json ./
RUN npm ci
COPY front/ ./
RUN npm run build

FROM python:3.13-slim
WORKDIR /app

COPY server/pyproject.toml ./server/pyproject.toml
COPY server/jeu ./server/jeu
RUN pip install --no-cache-dir ./server

COPY fabrication/paires.json ./fabrication/paires.json
COPY --from=front /front/dist ./front/dist

# Le paquet est installé en site-packages : les chemins relatifs au source ne
# valent plus rien, tout se dit ici.
ENV CONTRAT_PAIRES=/app/fabrication/paires.json \
    FRONT_DIST=/app/front/dist \
    SIGNAUX_SQLITE=/donnees/signaux.db

# Le point de montage du volume, pour que SQLite trouve son dossier même sans.
RUN mkdir -p /donnees

EXPOSE 8000
CMD ["python", "-m", "jeu"]
