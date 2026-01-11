# Prometheus Configuration

Prometheus collects metrics from Proxmox infrastructure for monitoring and alerting.

## Architecture

**Read-only monitoring:**
- Prometheus scrapes metrics from exporters
- No write operations to Proxmox hosts
- No credentials stored in Prometheus config
- All metrics are pulled (not pushed)

## What Prometheus Collects

### From node_exporter (Proxmox Hosts)

Prometheus scrapes node_exporter running on each Proxmox host (port 9100):

**Host Metrics:**
- **CPU**: Usage by mode (user, system, idle, iowait)
- **Memory**: Total, free, cached, buffers, swap usage
- **Disk I/O**: Read/write operations, throughput, I/O wait time
- **Disk Space**: Filesystem sizes and usage per mount point
- **Network**: Bytes sent/received, packet counts, errors per interface
- **System**: Uptime, boot time, load average

**Why this is safe:**
- node_exporter only reads `/proc` and `/sys` filesystems (read-only)
- No authentication required (internal network only)
- No write operations to Proxmox hosts
- Standard Linux metrics (same as any monitoring tool)

### From proxmox-exporter (Monitoring Server)

Prometheus scrapes proxmox-exporter running on monitoring server (port 9221):

**Proxmox Metrics:**
- **VM Status**: Running, stopped, paused per VM
- **VM Resources**: CPU and memory usage per VM
- **Storage**: Pool utilization, disk space per storage pool
- **Cluster**: Node status, cluster health
- **Network**: Bridge information

**Why this is safe:**
- Uses Proxmox API with read-only permissions
- Cannot start, stop, or modify VMs
- Cannot create or delete storage pools
- Cannot modify Proxmox configuration
- API token has minimal permissions

## How Prometheus Scrapes node_exporter

**Scraping Process:**

1. **Prometheus initiates connection** to node_exporter on Proxmox host
2. **node_exporter responds** with metrics in Prometheus format
3. **Prometheus stores** metrics in time-series database
4. **Grafana queries** Prometheus for visualization

**Configuration Example:**
```yaml
scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets:
          - 'proxmox-host-1:9100'
          - 'proxmox-host-2:9100'
```

**Scrape Interval:**
- Default: 15 seconds (configurable)
- Prometheus pulls metrics periodically
- No push from exporters (pull model)

**Data Flow:**
```
Proxmox Host → node_exporter (port 9100) ← Prometheus (scrapes)
```

**Safety:**
- Prometheus pulls data (read-only operation)
- node_exporter exposes metrics (no authentication needed)
- No credentials in scrape configuration
- Network should be isolated to monitoring network

## Configuration

**File**: `prometheus.yml.example`
- Example configuration with placeholders
- Copy to `prometheus.yml` and update with real targets
- No secrets or credentials in configuration

## Scrape Jobs

### node-exporter
- **Port**: 9100
- **Location**: Runs on each Proxmox host
- **Metrics**: CPU, memory, disk I/O, network, system load
- **Safety**: Read-only, no authentication required

### proxmox-exporter
- **Port**: 9221
- **Location**: Runs on monitoring server
- **Metrics**: VM status, storage usage, cluster health
- **Safety**: Read-only API queries, credentials via environment variables

## Setup

1. Copy example configuration:
   ```bash
   cp prometheus.yml.example prometheus.yml
   ```

2. Update targets with real hostnames/IPs

3. Configure credentials via environment variables (not in config file)

4. Start Prometheus with the configuration

## Data Retention

Default retention is 15 days. Adjust `--storage.tsdb.retention.time` flag as needed.

## Security

- No credentials in configuration files
- Use environment variables for sensitive data
- Prometheus runs read-only (scrapes only)
- Network access should be restricted to monitoring network

