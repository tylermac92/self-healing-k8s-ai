import requests
import datetime
import json

LOKI_URL = "http://loki.logging.svc.cluster.local:3100"
QUERY = '{namespace="chaos-demo"}'
LIMIT = 1000

def query_loki():
    now = int(datetime.datetime.now().timestamp() * 1e9)
    start = now - (60 * 5 * 1e9)
    resp = requests.get(
        f"{LOKI_URL}/loki/api/v1/query_range",
        params={
            "query": QUERY,
            "limit": LIMIT,
            "start": int(start),
            "end": int(now),
            "direction": "backward"
        }
    )
    data = resp.json()["data"]["result"]
    logs = [entry for stream in data for entry in stream["values"]]
    return [log[1] for log in logs]

def detect_anomalies(logs):
    suspicious = [line for line in logs if "error" in line.lower() or "fail" in line.lower()]
    return suspicious

if __name__ == "__main__":
    logs = query_loki()
    anomalies = detect_anomalies(logs)
    if anomalies:
        print("Anomalies detected:")
        for a in anomalies:
            print(a)
    else:
        print("No anomalies detected")