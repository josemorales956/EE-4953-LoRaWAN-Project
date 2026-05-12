from payload import encode_snapshot_payload, decode_payload

print("=== CRC Failure Demonstration ===\n")

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

print("Original Payload:")
print(payload.hex().upper())

# Corrupt one byte
corrupted = bytearray(payload)
corrupted[5] ^= 0x01

print("\nCorrupted Payload:")
print(bytes(corrupted).hex().upper())

try:
    decode_payload(bytes(corrupted))
except ValueError as e:
    print("\nCRC Validation Failed:")
    print(e)
