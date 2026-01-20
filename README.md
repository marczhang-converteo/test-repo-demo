# Weather Data Collector

Ce projet se compose de deux conteneurs Docker :
1.  **Server** : Une base de données PostgreSQL qui stocke les données météorologiques.
2.  **Client** : Une application Python qui récupère les données de l'API OpenWeatherMap et les enregistre dans la base de données.

## Prérequis

-   Docker et Docker Compose installés.
-   Une clé API OpenWeatherMap (doit être présente dans le fichier `.env` à la racine).

## Structure du projet

-   `client/` : Contient le code source de l'application Python et son Dockerfile.
-   `server/db/` : Contient le script SQL d'initialisation de la base de données.
-   `docker-compose.yml` : Définit l'orchestration des services.

## Installation et Lancement

1.  Assurez-vous que le fichier `.env` contient votre clé API :
    ```env
    OPENWEATHERMAP_API_KEY=votre_cle_api
    ```

2.  Lancez les conteneurs avec Docker Compose :
    ```bash
    docker-compose up --build
    ```

## Détails techniques

-   **Base de données** : PostgreSQL 15. Les données sont persistées via un volume nommé `postgres_data`.
-   **Client** : Récupère les données toutes les 10 minutes (configurable via `FETCH_INTERVAL` dans le `docker-compose.yml`).
-   **Schéma** : La table `weather_data` contient les colonnes : `id`, `city`, `temperature`, `humidity`, `description`, et `timestamp`.
