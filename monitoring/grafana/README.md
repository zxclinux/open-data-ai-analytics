# Grafana quick start

Grafana runs in Docker on port `3000`.

## Access

- URL: `http://<vm-public-ip>:3000`
- Default username: `admin`
- Default password: `admin`

You will be asked to change the password on first login.

## Prometheus data source

In Grafana, add a Prometheus data source with:

- Name: `Prometheus`
- URL: `http://prometheus:9090`
- Access: `Server`

Then use PromQL queries from project docs/lab instructions to create dashboards.
