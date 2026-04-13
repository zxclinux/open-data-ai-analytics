# Monitoring stack runbook

This project uses Prometheus + Grafana + node-exporter + cAdvisor in the same Docker Compose stack.

## Start or update containers

```bash
cd src
docker compose up -d --build
```

## Verification commands

```bash
docker ps
docker logs --tail 200 prometheus
docker logs --tail 200 grafana
curl http://localhost:9090/-/healthy
curl http://localhost:3000/api/health
curl http://localhost:8000/metrics
```

## Azure ports to open

- `22` SSH
- `8000` web app (or current `web_port`)
- `3000` Grafana
- `9090` Prometheus

## Grafana setup

1. Open `http://<public-ip>:3000`
2. Login: `admin` / `admin`
3. Add data source:
   - Type: Prometheus
   - URL: `http://prometheus:9090`
   - Access: Server

## Suggested PromQL queries

- CPU VM
  - `100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance))`
- RAM VM
  - `100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))`
- CPU containers
  - `sum by (name) (rate(container_cpu_usage_seconds_total{name!="",image!=""}[5m])) * 100`
- RAM containers
  - `sum by (name) (container_memory_working_set_bytes{name!="",image!=""})`
- Active containers
  - `count(container_last_seen{name!="",image!=""})`
- Request count app
  - `sum(rate(http_requests_total[5m]))`
  - fallback: `sum(rate(http_request_duration_seconds_count[5m]))`

## Manual steps after Terraform changes

```bash
cd infra/terraform
terraform apply
```

Then re-run compose update:

```bash
cd ../../src
docker compose up -d --build
```
