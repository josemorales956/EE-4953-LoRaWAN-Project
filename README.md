# EE-4953-LoRaWAN-Project
Project Focusing on LoRaWAN and CRC8 and AES 128

This repository contains supporting code for a secure distributed sensor network architecture that integrates LoRaWAN communication with edge artificial intelligence (AI) processing. The project focuses on secure packet transmission, payload validation, and reliable communication for smart city sensing applications.

The system uses NVIDIA Jetson-based sensor nodes and Wio-E5 LoRa communication modules to collect environmental and activity data, encode structured payloads, and transmit validated packets through a LoRaWAN network.

# Files

## `crc8.py`

Implements a CRC-8 algorithm used for payload integrity validation and error detection.

### Features
- CRC-8-ATM polynomial (`0x07`)
- Detects corrupted payloads
- Used during payload encoding and decoding

## `payload.py`

Implements SNAPSHOT payload encoding and decoding for LoRaWAN communication.

### Supported Features
- Structured binary payload generation
- CRC validation
- Payload parsing
- Snapshot environmental and activity data

## `demo_payload.py`

Demonstrates:
- payload generation
- payload encoding
- payload decoding
- successful CRC validation

### Run

```bash
python demo_payload.py
```

## `demo_crc_failure.py`

Demonstrates CRC-based corruption detection by intentionally modifying payload data and triggering validation failure.

### Run

```bash
python demo_crc_failure.py
```

## `collect_chirpstack_metrics.py`

Demonstrates how communication metrics can be collected from real LoRaWAN uplinks forwarded through a RAK gateway and ChirpStack MQTT broker.

### Features
- subscribes to ChirpStack MQTT uplinks
- decodes payloads
- extracts RSSI values
- estimates packet delivery ratio (PDR)
- tracks missing packets using sequence numbers

## `AT Text`

Contains AT command examples used for configuring and communicating with the Wio-E5 LoRaWAN module.

# Security Features

The project focuses on secure and reliable LoRaWAN communication through:

- AES-128 encryption
- Message Integrity Codes (MIC)
- CRC-8 payload validation
- sequence number tracking
- structured payload formatting

# Performance Metrics

The system evaluates:
- Packet Delivery Ratio (PDR)
- RSSI
- communication reliability
- payload integrity
- object detection accuracy
