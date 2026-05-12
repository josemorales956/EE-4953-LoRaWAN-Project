import json
import base64
import time
from collections import defaultdict

import paho.mqtt.client as mqtt
from payload import decode_payload

MQTT_HOST = "localhost"
MQTT_PORT = 1883
TOPIC = "application/+/device/+/event/up"

node_stats = defaultdict(lambda: {
    "received": 0,
    "last_seq": None,
    "missing": 0,
    "rssi_values": [],
    "latency_values_ms": [],
})

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        uplink = json.loads(msg.payload.decode())

        # ChirpStack sends payload data as base64
        raw_payload = base64.b64decode(uplink["data"])

        decoded = decode_payload(raw_payload)

        node_id = decoded["node_id"]
        seq = decoded["seq"]

        stats = node_stats[node_id]
        stats["received"] += 1

        # Estimate missing packets using sequence numbers
        if stats["last_seq"] is not None:
            expected = (stats["last_seq"] + 1) & 0xFF
            if seq != expected:
                missed = (seq - expected) % 256
                stats["missing"] += missed

        stats["last_seq"] = seq

        # RSSI from gateway metadata
        if "rxInfo" in uplink and len(uplink["rxInfo"]) > 0:
            rssi = uplink["rxInfo"][0].get("rssi")
            if rssi is not None:
                stats["rssi_values"].append(rssi)

        # Optional latency estimate if timestamp exists
        rx_time = time.time()
        stats["latency_values_ms"].append(0)  # placeholder unless send timestamp is included

        print(f"Received from Node {node_id}: {decoded}")

    except Exception as e:
        print("Error processing uplink:", e)

def print_summary():
    print("\n=== System Performance Summary ===")
    print("Node ID | PDR (%) | Avg RSSI (dBm) | Packets Received | Missing Packets")
    print("-" * 75)

    for node_id, stats in node_stats.items():
        received = stats["received"]
        missing = stats["missing"]
        total_estimated = received + missing

        pdr = (received / total_estimated) * 100 if total_estimated > 0 else 0

        avg_rssi = (
            sum(stats["rssi_values"]) / len(stats["rssi_values"])
            if stats["rssi_values"]
            else 0
        )

        print(
            f"Node {node_id} | "
            f"{pdr:.1f} | "
            f"{avg_rssi:.1f} | "
            f"{received} | "
            f"{missing}"
        )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)

try:
    print("Listening for ChirpStack uplinks...")
    client.loop_forever()
except KeyboardInterrupt:
    print_summary()
