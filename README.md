# Don't be late

Application web Django qui prévient les retards de transport en Île-de-France : elle croise l'emploi du temps de l'utilisateur, ses trajets habituels et les données d'Île-de-France Mobilités et de Météo-France. La vision et les fonctionnalités visées sont détaillées dans [SPECS.md](SPECS.md).

## Lancer le projet

```bash
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

Si `uv` n'est pas installé :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


En attendant que le docker compose soit réalisé, voici comment lancer celery:
```bash
docker run -d --name dbl-redis -p 6379:6379 redis:8-alpine
```

Cela suppose un Redis lancé au préalable
TODO: Reparer le celery ?