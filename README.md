# DevOps GitOps App

Sample FastAPI application for a k3s-based Jenkins, Helm, ArgoCD, and internal registry GitOps portfolio project.

## Endpoints

| Path | Purpose |
|---|---|
| `/` | Service status and deployment message |
| `/health` | Health check |
| `/version` | Application version |
| `/metrics` | Minimal Prometheus-compatible metrics |

## Local Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker Build

```bash
docker build -t localhost:30500/devops-gitops-app:0.1.0 .
docker push localhost:30500/devops-gitops-app:0.1.0
```

## Kubernetes Platform Flow

```text
Jenkins -> Internal Registry(zot) -> GitOps Repo(Helm values) -> ArgoCD -> k3s devops-app namespace
```
