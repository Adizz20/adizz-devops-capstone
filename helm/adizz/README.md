# Adizz Helm chart

This chart deploys the Adizz frontend, FastAPI backend, PostgreSQL, ClusterIP Services, and an optional NGINX Ingress. The backend image's existing startup command applies Alembic migrations before starting Uvicorn.

## Local Kind deployment

Run from the repository root in PowerShell. The Docker images should already exist locally.

```powershell
kind load docker-image adizz-devops-capstone-backend:latest --name aditya
kind load docker-image adizz-devops-capstone-frontend:latest --name aditya

helm lint .\helm\adizz
helm template adizz .\helm\adizz --namespace adizz

helm upgrade --install adizz .\helm\adizz `
  --namespace adizz --create-namespace `
  --wait --timeout 5m

kubectl get pods,svc,pvc -n adizz
kubectl port-forward -n adizz svc/frontend 3000:8080
```

Open `http://localhost:3000`. To test FastAPI directly in another terminal, run `kubectl port-forward -n adizz svc/backend 8000:8000`, then visit `http://localhost:8000/health` and `http://localhost:8000/metrics`.

## Ingress

Ingress is disabled by default because the cluster initially had no Ingress controller. Install a Kind-compatible NGINX Ingress controller before enabling it. Then set `ingress.enabled=true` and `ingress.host=adizz.local` in an override file and configure local host resolution if needed.

## Security and production notes

The default PostgreSQL password is for local development only. Override it for shared environments and never commit real credentials. For production, use a managed database, secret manager, a dedicated migration Job that runs once per release, and reviewed resource/security policies. This chart's local PostgreSQL PVC depends on the cluster's default StorageClass. The current backend image runs Alembic on container startup, so two replicas may attempt migrations concurrently; this is acceptable for a local first pass but should be changed before production.
