# Deployment guide
1. Install Docker Desktop and start Docker Engine.
2. Copy `.env.example` to `.env`; configure strong unique credentials.
3. Ensure the required database name/password match the intended local database configuration.
4. Run `docker compose up --build -d`.
5. Create an admin using `docker compose exec -it backend python -m app.cli create-admin --username admin --email admin@example.com`.
6. Place permitted model weights at `vision/models/yolo11n.pt`.
7. Open frontend and upload a representative video.
8. Calibrate queue polygon and compare results against manual review.
9. Only then configure a compatible NVIDIA host/RTSP source for edge deployment.

Docker Compose creates a persistent Docker volume named `qsr_postgres_data`; this is a fresh project's database volume and does not automatically connect to a separately existing pgAdmin database on the host.
