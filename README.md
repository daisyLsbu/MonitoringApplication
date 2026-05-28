# MonitoringApplication
The application runs continuously monitoring and storing data related to the hosts in the network.
implements: influx write, influx read, aiohttp
Collects telemetry data from all the hosts in the network and stores in influx db.
Developed in python, list of host is provided in csv file.
AIOhttp for Asynchronous HTTP Client/Server communication with the hosts.
Time-series Influx DB is used to store the data for all hosts. which can be used to plot and analyse using Grafana.

### Part 3 — Monitoring Application

**Repository:** [`monitoringapplication`](https://github.com/daisyLsbu/monitoringapplication)

The **central data aggregation and storage layer**. This application runs continuously, polling the Telemetry Application on each host and persisting all metrics into a time-series database. The stored data feeds both the reactive migration logic and the LSTM model training/inference.

**What it does:**
- Reads a CSV file listing all hosts in the network
- Asynchronously polls each host's Telemetry App endpoint using `aiohttp`
- Writes all incoming data to InfluxDB (time-series format)
- Exposes data for visualisation via Grafana dashboards

**Key technologies:**
- Python
- `aiohttp` — asynchronous HTTP client for concurrent host polling
- InfluxDB — time-series storage
- Grafana — visualisation and dashboarding (optional but recommended)

**Configuration:** provide a `hosts.csv` file listing the IP/hostname of every node to monitor.

---

# Requirement
InfluxDBClient for connecting to Influx DB server.
Grafana to manage and monitor processes.
## Installation
Run the setup.sh (after uncommenting the text - for the first time)
run build.sh
update host.csv file with the hosts to be monitored in the network
## Test
To check if everything is working fine, you can use collectDisplayTable.py file and follow instruction
update the influx DB credential in influcDBsuite.py
execute run.sh
This will display the collected data on your terminal. If Grafana is running then it should reflect there
as well.
Note: The code assumes that the user has access to a local instance of InfluxDB
and Grafana. Please make sure to install and configure them properly before using this software.</s>

use test_data.json file for sample data


