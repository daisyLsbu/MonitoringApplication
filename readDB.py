from influxdb_client_3 import InfluxDBClient3
from influxdb_client_3 import InfluxDBClient3, Point


client = InfluxDBClient3(
    token="apiv3_qtEShFmAk4ssjjJ5o8d8xfD0qmN1NmK6xKwOuehgbpB0AI-OWvLtfs2k8bUmt6mFvmxVdQPkui-BVYx6ETRTHg",
    host="http://localhost:8181",
    database="monitoring"
)

table = client.query("SHOW TABLES")
df = table.to_pandas()
print(df[df['table_schema'] == 'iox'])

table = client.query('SELECT * FROM "Device" LIMIT 20')
print(table.to_pandas())
