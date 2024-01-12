# MonitoringApplication
The application runs continuously monitoring and storing data related to the hosts in the network.

Collects telemetry data from all the hosts in the network and stores in influx db.
Developed in python, list of host is provided in csv file.
AIOhttp for Asynchronous HTTP Client/Server communication with the hosts.
Time-series Influx DB is used to store the data for all hosts. which can be used to plot and analyse using Grafana.
# Requirement
InfluxDBClient for connecting to Influx DB server.
Grafana to manage and monitor processes.
## Installation




