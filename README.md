# Adizz

Adizz is a Travel & Booking Management System built as a DevOps capstone
project.

## Technology stack

- React and Vite
- FastAPI and PostgreSQL
- Docker and Docker Compose
- GitHub Actions, GHCR, and Trivy
- Kubernetes, Helm, Prometheus, and Grafana
- Terraform and AWS EKS

## Project structure

```text
backend/            FastAPI backend, migrations, and tests
frontend/           React/Vite frontend and nginx image
terraform/          AWS VPC and EKS preparation
helm/               Kubernetes Helm chart
k8s/                Supporting Kubernetes manifests
monitoring/         Prometheus and Grafana configuration
troubleshooting/    Troubleshooting documentation
.github/workflows/  CI/CD workflows
```

## Local development

Run backend tests from `backend`:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Install and build the frontend from `frontend`:

```powershell
npm ci
npm run build
```

Run the complete local stack with Docker Compose:

```powershell
docker compose up --build
```

The Compose frontend is available at `http://localhost:3000`, the backend at
`http://localhost:8000`, and PostgreSQL at `localhost:5432`.

## Local Kind and Helm deployment

The local cluster is named `aditya`. Build and load the images, render the
chart, then upgrade the release:

```powershell
docker build -t adizz-devops-capstone-backend:latest .\backend
docker build -t adizz-devops-capstone-frontend:latest .\frontend
kind load docker-image adizz-devops-capstone-backend:latest --name aditya
kind load docker-image adizz-devops-capstone-frontend:latest --name aditya
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.13.2/deploy/static/provider/kind/deploy.yaml
helm template adizz .\helm\adizz
helm upgrade --install adizz .\helm\adizz --namespace adizz --create-namespace --wait
```

The chart runs two backend replicas, two frontend replicas, PostgreSQL with a
persistent volume, and an nginx Ingress for the `adizz.local` host. The
Ingress preserves the `/api` prefix, so `/api/bookings` reaches the FastAPI
route unchanged.

The current Kind cluster has no host port mapping for HTTP or HTTPS. Test the
Ingress without changing or recreating the cluster by forwarding its service:

```powershell
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 18080:80
curl.exe -H "Host: adizz.local" http://127.0.0.1:18080/
curl.exe -H "Host: adizz.local" http://127.0.0.1:18080/health
curl.exe -H "Host: adizz.local" http://127.0.0.1:18080/api/bookings
```

## Monitoring

Prometheus scrapes both backend replicas through the `adizz-backend`
ServiceMonitor. Access the local UIs with:

```powershell
kubectl -n monitoring port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090
kubectl -n monitoring port-forward svc/monitoring-grafana 3002:80
```

The provisioned Grafana dashboard is `Adizz Application Monitoring`. It
contains request totals, request rate, latency, and healthy backend replica
queries.

## Terraform AWS checkpoint

The `terraform` directory prepares an AWS VPC with two public subnets across
availability zones, an internet gateway, an EKS control plane, and an EKS
managed node group. It does not provision anything by itself.

Prerequisites are Terraform, AWS CLI credentials configured for the intended
account, and permission to create VPC, IAM, EKS, EC2, and related resources.
Review the example variables, then validate locally:

```powershell
Copy-Item .\terraform\terraform.tfvars.example .\terraform\terraform.tfvars
terraform -chdir=terraform init
terraform -chdir=terraform fmt -check
terraform -chdir=terraform validate
terraform -chdir=terraform plan -var-file=terraform.tfvars
```

Do not run `terraform apply` until the plan, account, region, and budget have
been explicitly reviewed. EKS control planes, EC2 nodes, load balancers, public
IPv4 addresses, storage, and any NAT gateway are chargeable AWS resources.
This configuration intentionally uses public subnets and no NAT gateway to
avoid an automatic NAT gateway charge; worker nodes still incur EC2 costs.

After an approved deployment, configure `kubectl` with
`aws eks update-kubeconfig`, push or reference the images in GHCR, and deploy
the Helm chart to the EKS context. Cleanup is:

```powershell
terraform -chdir=terraform destroy -var-file=terraform.tfvars
```

Then verify that the EKS cluster, node group, load balancers, volumes, and
other chargeable resources are gone.
