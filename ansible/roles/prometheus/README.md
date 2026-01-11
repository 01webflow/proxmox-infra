# Prometheus Role

Ansible role to install and configure Prometheus on monitoring VMs.

## Purpose

Prometheus collects and stores metrics from exporters:
- Scrapes metrics from node_exporter (on Proxmox hosts)
- Scrapes metrics from proxmox-exporter (on monitoring server)
- Stores time-series data locally
- Provides query API for Grafana

## Safety

**Why this is safe:**
- **Read-only**: Prometheus only scrapes metrics (pulls data)
- **No write operations**: Cannot modify Proxmox hosts or VMs
- **No credentials in config**: Configuration file contains no secrets
- **No remote write**: Does not send data elsewhere (local storage only)
- **No alerting**: Alerting not configured (read-only monitoring)

## Installation

The role installs `prometheus` from system package manager (apt).

**Service:**
- Service name: `prometheus`
- Port: 9090 (default)
- Web UI: `http://prometheus-vm:9090`
- Config: `/etc/prometheus/prometheus.yml`

## Configuration

**Enable the role:**
Set `prometheus_enabled: true` in `ansible/group_vars/vms.yml`

**Default:**
- `prometheus_enabled: false` (disabled by default, safe)

**Configuration file:**
- Deployed from `monitoring/prometheus/prometheus.yml.example`
- Copy to `prometheus.yml` and update with real targets
- No secrets or credentials in configuration

## Usage

The role is integrated into `ansible/playbooks/vm-base.yml` and runs conditionally:

```yaml
roles:
  - role: prometheus
    when: prometheus_enabled | bool
```

## What Prometheus Collects

**From node_exporter (Proxmox hosts):**
- CPU usage and load average
- Memory usage (total, free, cached)
- Disk I/O (read/write operations, throughput)
- Disk space usage (per filesystem)
- Network I/O (bytes sent/received)

**From proxmox-exporter (monitoring server):**
- VM status (running, stopped, paused)
- VM resource usage (CPU, memory per VM)
- Storage pool utilization
- Cluster node status

## Scraping Configuration

Prometheus scrapes exporters every 15 seconds (configurable).

**Example scrape jobs:**
- `node-exporter`: Scrapes from Proxmox hosts (port 9100)
- `proxmox-exporter`: Scrapes from monitoring server (port 9221)

See `monitoring/prometheus/prometheus.yml.example` for configuration.

## Verification

After installation, verify Prometheus is running:

```bash
systemctl status prometheus
curl http://localhost:9090/api/v1/status/config
```

Access web UI:
```bash
# From monitoring network
http://prometheus-vm:9090
```

## Data Retention

Default retention is 15 days. Adjust `--storage.tsdb.retention.time` in systemd service if needed.

## Security

- **No credentials**: Configuration contains no secrets
- **Internal network**: Should only be accessible from monitoring network
- **Read-only**: Prometheus cannot modify monitored systems
- **No remote write**: Data stays local (no external transmission)

## Idempotency

The role is idempotent:
- Safe to run multiple times
- Only installs if not present
- Only starts service if not running
- Configuration updates trigger service restart

