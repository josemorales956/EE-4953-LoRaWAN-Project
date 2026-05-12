from payload import encode_snapshot_payload, decode_payload

# Create payload
payload = encode_snapshot_payload(
    node_id=1,
    seq=1,
    temp_c=30.5,
    humidity_pct=48.2,
    battery_mv=5100,
    event_code=1,
    people=3,
    vehicles=2,
    bikes=0,
    confidence=0.91,
    dwell_s=45,
    status_flags=0
)

print("Encoded Payload:")
print(payload.hex().upper())

# Decode payload
decoded = decode_payload(payload)

print("\nDecoded Payload:")
for key, value in decoded.items():
    print(f"{key}: {value}")
