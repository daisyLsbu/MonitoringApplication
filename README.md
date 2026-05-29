# MonitoringApplication

> A self-contained Python service for continuous, asynchronous telemetry collection from a distributed network of hosts — storing time-series data in InfluxDB and surfacing it through Grafana. Designed as an independent building block that can be dropped into any observability or orchestration pipeline.

---

## Overview

**MonitoringApplication** is the central data aggregation layer for a distributed monitoring system. It runs continuously on a single node, reading a CSV file of host definitions, polling each host's telemetry endpoint concurrently using asynchronous HTTP, and writing all incoming metrics — both host-level and container-level — into a time-series InfluxDB database.

Because the collector, the database client, and the display utility are cleanly separated into independent modules, the application can be adapted to different data sources, storage backends, or polling frequencies without restructuring the codebase.

---

## Features

- **Asynchronous multi-host polling** — uses `aiohttp` and `asyncio` to concurrently fetch data from all nodes in the network at each polling interval, with no blocking between hosts
- **Host and container metrics** — stores device-level resource metrics (CPU, memory, storage, network) and per-container metrics (CPU %, memory %, network %) as separate InfluxDB measurements
- **CSV-driven host configuration** — add or remove nodes by editing `data/nodes.csv`; no code changes required
- **Configurable polling interval** — set the collection frequency in seconds at startup
- **InfluxDB write and read** — `influxdbsuite.py` provides both write (for the collector) and read (for downstream consumers and testing) operations against the database
- **Terminal display mode** — `collectDisplaytable.py` lets you verify collected data directly on the console without needing Grafana
- **Grafana-ready** — data is written in a format ready for Grafana dashboards out of the box
- **Sample data included** — `test_data.json` provides a representative data payload for testing the write pipeline without live hosts

---

## How It Works

```
data/nodes.csv
      │
      │  read host list (ip, port, api endpoint)
      ▼
collectorAsync.py
      │
      │  concurrent aiohttp GET requests (one per host per interval)
      ▼
Telemetry endpoints on each host
      │
      │  JSON response (device stats + container stats)
      ▼
influxdbsuite.py
      │
      │  write to InfluxDB (Device measurement + Container measurement)
      ▼
InfluxDB  ──────►  Grafana (optional dashboards)
```

At each polling cycle, `collectorAsync.py` builds a coroutine for every host URL in `nodes.csv`, gathers all responses concurrently with `asyncio.gather`, and passes the full result set to `influxdbsuite.writeToDBCombinedTest`, which writes each device and its containers as tagged InfluxDB points.

---

## InfluxDB Data Model

Two measurements are written per polling cycle:

**`Device`** — one point per host, tagged with `host` (IP address):

| Field | Description |
|---|---|
| `cpu_used` | CPU usage percentage |
| `cpu_free` | CPU free percentage |
| `cpu_percent` | Combined CPU utilisation |
| `storage_used` | Storage used (bytes) |
| `storage_free` | Storage available (bytes) |
| `storage_percent` | Storage utilisation % |
| `vm_used` | Virtual memory used (bytes) |
| `vm_free` | Virtual memory free (bytes) |
| `vm_percent` | Virtual memory utilisation % |
| `network_drop` | Network packet drops |

**`Container`** — one point per container per host, tagged with `host` and `id`:

| Field | Description |
|---|---|
| `cpu_percent` | Container CPU utilisation % |
| `cpu_usage` | Raw container CPU usage |
| `mem_percent` | Container memory utilisation % |
| `memory_usage` | Container memory usage (bytes) |
| `nw_percent` | Container network utilisation % |
| `nw_usage` | Container network usage (bytes) |

---

## Getting Started

### Prerequisites

- Python 3.8+
- A running [InfluxDB](https://docs.influxdata.com/influxdb/) instance (local or remote)
- [Grafana](https://grafana.com/docs/grafana/latest/) *(optional, for dashboards)*
- [TelemetryApplication](https://github.com/daisyLsbu/TelemetryApplication) running on each host you want to monitor

### Installation

```bash
git clone https://github.com/daisyLsbu/MonitoringApplication.git
cd MonitoringApplication
```

Run the setup script (uncomment lines on first use), then build:

```bash
bash scripts/setup.sh
bash scripts/build.sh
```

Or install dependencies directly:

```bash
pip install -r requirement.txt
```

### Configuration

**1. Host list** — edit `data/nodes.csv` to list every host you want to monitor:

```csv
ip,port,api
192.168.1.10,5000,combined
192.168.1.11,5000,combined
192.168.1.12,5000,combined
```

Each row defines a host IP, the port the Telemetry Application is running on, and the API endpoint to call (`combined` returns both device and container metrics).

**2. InfluxDB credentials** — update the connection settings in `influxdbsuite.py`:

```python
token = "<your-influxdb-token>"
org   = "<your-org>"
url   = "http://localhost:8086"
```

### Running the collector

```bash
bash scripts/run.sh
```

Or run directly with Python:

```bash
python collectorAsync.py
```

The default polling interval is 1 second. To change it, edit the `asyncio.run(storeData(interval=1))` call at the bottom of `collectorAsync.py`.

### Verifying without Grafana

Use the terminal display utility to confirm data is being collected and stored correctly:

```bash
python collectDisplaytable.py
```

This prints collected metrics in a formatted table to the console. If Grafana is running and connected to the same InfluxDB instance, it will update automatically at the same time.

### Testing with sample data

To test the InfluxDB write pipeline without live hosts, run `influxdbsuite.py` directly:

```bash
python influxdbsuite.py
```

This writes the payload defined in `test_data.json` (or the inline test data at the bottom of the file) to the `telemetrydata` bucket, letting you verify your InfluxDB connection and data model before deploying to a live network.

---

## Use as a Building Block

MonitoringApplication is designed to be **reused as the data aggregation and persistence layer** in any project that needs to collect time-series metrics from multiple HTTP-accessible hosts. You can:

- **Swap the data source** — the host list and endpoint are entirely config-driven; point `nodes.csv` at any HTTP API that returns JSON and adjust the write logic in `influxdbsuite.py` accordingly
- **Change the polling interval** — a single parameter controls the collection frequency; reduce it for near-real-time monitoring or increase it to reduce write load
- **Extend the schema** — add new fields to the `Point` writes in `influxdbsuite.py` to capture additional metrics without touching the collector or host configuration
- **Replace InfluxDB** — `influxdbsuite.py` is the only module that knows about the storage backend; swap it out for any other time-series or relational database by reimplementing its write interface
- **Feed any downstream consumer** — because data lands in InfluxDB, any tool that can query InfluxDB (Grafana, custom ML pipelines, alert systems) can consume it without any changes to the collector

---

## Used In

This application has been used as **Part 2 — the central data aggregation and storage layer** in the following project in this account:

### [reactiveAndPredictiveMigration](https://github.com/daisyLsbu/reactiveAndPredictiveMigration)


## Dependencies

| Library | Purpose |
|---|---|
| `aiohttp` | Asynchronous HTTP client for concurrent host polling |
| `asyncio` | Python async event loop |
| `influxdb-client` | InfluxDB Python client for write and query operations |
| `pandas` | CSV parsing for the host list |

Install all dependencies:

```bash
pip install -r requirement.txt
```

> **Note:** This application assumes a locally accessible InfluxDB instance. Install and configure InfluxDB before running the collector. Grafana is optional but recommended for visualising the collected time-series data.

---

## License

Licensed under the [GNU General Public License v3.0](LICENSE).
