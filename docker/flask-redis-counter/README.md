# Flask + Redis Visit Counter

A small multi-container app. A Flask web app counts page visits and stores the count in Redis. Both run together with Docker Compose.

Built as the capstone challenge for the Docker module of the CoderCo DevOps Academy.

<img src="screenshots/count.png" alt="The /count page" width="500">
![Docker Compose starting both services](screenshots/compose-up.png)

![The Compose file with the volume](screenshots/compose-yml.png)



## What it does

- `/` shows a welcome message.
- `/count` adds 1 to a visit counter stored in Redis and shows the new total.

## Architecture

Two containers share one Compose network:

| Service | Image | Role |
|---|---|---|
| `web` | built from the Dockerfile (`python:3.8-slim`) | Flask app on port 5003 |
| `redis` | official `redis` image | key-value store that holds the counter |

Flask reaches Redis by its service name (`redis`), not `localhost`. Inside a container, `localhost` means that container itself, so the other service has to be found by name.

```
flask-redis-counter/
├── app.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## How to run

Requires Docker Desktop.

```bash
docker compose up --build
```

Then open:

- http://localhost:5003 for the welcome message
- http://localhost:5003/count and refresh. The number goes up each time.

Stop it:

```bash
docker compose down      # removes the containers, keeps the saved count
docker compose down -v   # also deletes the volume, so the count resets
```

## Persistent storage

Redis keeps its data in `/data`. That folder is mounted on a named volume, `redis-data`, which lives outside the container.

Before the volume, removing the containers reset the count to 1. With the volume, a new Redis container finds the saved data and loads it on start-up, so the counter carries on.

## What I learned

- Inside a container, `localhost` is the container itself. Services find each other by their Compose service name.
- A container's data disappears with the container unless it is stored in a volume.
- The addresses a container prints (such as `127.0.0.1` or `172.x.x.x`) are internal. The port mapping in `docker-compose.yml` is what makes the app reachable from my browser at `localhost:5003`.
- `docker compose logs` is the first place to look when something doesn't work.

## Status

- [x] Flask app with `/` and `/count`
- [x] Dockerfile for the Flask app
- [x] Docker Compose with two services
- [x] Bonus: persistent storage for Redis (volume)
- [x]Bonus: environment variables for the Redis connection
- [ ] Bonus: scaling the Flask service with load balancing
