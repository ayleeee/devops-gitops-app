import os
import time

from fastapi import FastAPI, Response

APP_NAME = os.getenv("APP_NAME", "devops-gitops-app")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
STARTED_AT = time.time()

app = FastAPI(title=APP_NAME, version=APP_VERSION)


@app.get("/")
def root():
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "message": "Deployed by Jenkins, Helm, and ArgoCD",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"service": APP_NAME, "version": APP_VERSION}


@app.get("/metrics")
def metrics():
    uptime = int(time.time() - STARTED_AT)
    body = "\n".join(
        [
            "# HELP devops_app_up Application health status",
            "# TYPE devops_app_up gauge",
            "devops_app_up 1",
            "# HELP devops_app_uptime_seconds Application uptime in seconds",
            "# TYPE devops_app_uptime_seconds counter",
            f"devops_app_uptime_seconds {uptime}",
            "",
        ]
    )
    return Response(content=body, media_type="text/plain")
