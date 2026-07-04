# 💥 Rupture: High-Performance Async API Fuzzer & Load Tester

Rupture is an automated, containerized API load-testing and mutation fuzzing engine designed to uncover performance bottlenecks and catch **silent data corruptions** (mutated data structures or broken API contracts disguised behind successful `200 OK` responses).

Built using `asyncio`, `aiohttp`, `Hypothesis`, and `jsonschema`, Rupture simulates aggressive concurrent traffic using chaotic, property-based payloads, validates JSON structural contracts in real time, and compiles enterprise-ready PDF telemetry reports.

---

# 🏗️ System Architecture

Rupture operates on an orchestrated, non-blocking asynchronous pipeline that cleanly separates payload generation, network execution, validation, and reporting.

```text
                        +------------------+
                        |   User CLI Input |
                        +---------+--------+
                                  |
                                  v
                      +------------------------+
                      |   Hypothesis Engine    |
                      | Generates Chaotic Data |
                      +-----------+------------+
                                  |
                                  v
                     +--------------------------+
                     | asyncio Worker Pool      |
                     | aiohttp Concurrent I/O   |
                     +-----------+--------------+
                                 |
                                 v
                  +-------------------------------+
                  | JSON Schema Contract Validator |
                  +---------------+---------------+
                                  |
                                  v
                    +-----------------------------+
                    | Telemetry Aggregator        |
                    | Latency + Errors + Metrics  |
                    +---------------+-------------+
                                    |
                                    v
                      +---------------------------+
                      | PDF Report Generator      |
                      | Jinja2 + WeasyPrint       |
                      +---------------------------+
```

## Pipeline Overview

### 1. CLI Layer (`click`)
Collects:

- Target API endpoint
- HTTP method
- Concurrency level
- Number of requests
- JSON schema (optional)

---

### 2. Fuzzing Layer (`Hypothesis`)

Automatically generates recursive payloads including:

- Deeply nested objects
- Missing fields
- Null values
- Oversized integers
- Unicode edge cases
- Randomized arrays
- Invalid data types

---

### 3. Execution Core (`asyncio` + `aiohttp`)

Distributes fuzz payloads across a configurable asynchronous worker pool using a protective semaphore for efficient concurrency.

Features include:

- High-throughput asynchronous requests
- Connection pooling
- Low-overhead scheduling
- Configurable concurrency limits

---

### 4. Validation Layer (`jsonschema`)

Each API response is validated against a predefined JSON schema.

This allows Rupture to detect:

- Incorrect field types
- Missing required fields
- Additional unexpected fields
- Nested contract violations

These issues are detected even when the server incorrectly responds with:

```
HTTP/1.1 200 OK
```

---

### 5. Reporting Layer (`Jinja2` + `WeasyPrint`)

After execution completes, Rupture aggregates telemetry and generates a polished PDF report containing:

- Success rate
- Failure rate
- Contract violations
- Latency distributions
- Percentile metrics
- Response statistics

---

# 🚀 Quick Start (Local Sandbox Demo)

Rupture includes a fully containerized FastAPI sandbox that intentionally introduces contract violations, allowing the engine to demonstrate its detection capabilities without requiring any external API.

---

## Prerequisites

- Docker Desktop installed
- Docker daemon running

---

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rupture.git
cd rupture
```

---

## 2. Build the Docker Image

```bash
docker build -t rupture .
```

---

## 3. Run the Automated Demo

The following command executes the complete sandbox test suite and mounts the generated reports onto your local machine.

### Linux/macOS

```bash
docker run --rm \
-v $(pwd)/out:/app/out \
rupture
```

### Windows PowerShell

```powershell
docker run --rm `
-v ${PWD}/out:/app/out `
rupture
```

### Windows CMD

```cmd
docker run --rm -v %cd%/out:/app/out rupture
```

---

## 4. View the Report

After execution completes:

```
./out/demo_report.pdf
```

will contain:

- Latency graphs
- Request statistics
- Schema validation failures
- Percentile metrics
- Contract violation summary

---

# 📊 Sample Runtime Output

```text
=========================================
Rupture Async Fuzzer Started
=========================================

Workers:              50
Total Requests:       500
Target Endpoint:      http://sandbox:8000/test

Running...

✔ Completed

Processed Samples:    500

Successful Responses: 48
Contract Violations:  452

Success Rate:         9.6%
Violation Rate:       90.4%

Latency

p50: 0.0204 s
p95: 0.0268 s
p99: 0.0281 s

PDF report generated:

out/demo_report.pdf
```

---

# 📈 Example Report Metrics

| Metric | Value |
|---------|------:|
| Total Requests | 500 |
| Successful Contracts | 48 |
| Failed Contracts | 452 |
| Success Rate | 9.6% |
| Failure Rate | 90.4% |
| Median Latency (p50) | 20.4 ms |
| 95th Percentile | 26.8 ms |
| 99th Percentile | 28.1 ms |

---

# 🛠 Technology Stack

## Language

- Python 3.12

---

## CLI

- click

---

## Asynchronous Networking

- asyncio
- aiohttp

---

## Property-Based Testing

- Hypothesis

---

## Schema Validation

- jsonschema

---

## Reporting

- Jinja2
- WeasyPrint

---

## Testing

- pytest
- allure-pytest

---

## Containerization

- Docker
- Docker Compose

---

## Example Project Structure

```text
rupture/
│
├── app/
│   ├── cli.py
│   ├── worker.py
│   ├── fuzz.py
│   ├── validator.py
│   ├── telemetry.py
│   ├── report.py
│   └── templates/
│
├── sandbox/
│   ├── main.py
│   └── Dockerfile
│
├── tests/
│
├── out/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🎯 Primary Capabilities

- High-performance asynchronous load testing
- Property-based payload mutation
- Recursive JSON fuzz generation
- JSON Schema validation
- Silent contract corruption detection
- Configurable concurrency
- Dockerized execution
- Automated PDF reporting
- Real-time telemetry
- Percentile latency analysis

---

# 🔍 Detects Problems That Traditional Load Testers Miss

Unlike traditional benchmarking tools that only evaluate HTTP status codes, Rupture validates the structure of every response.

Example:

**Request**

```json
{
  "id": 12
}
```

Expected Response

```json
{
  "id": 12,
  "name": "Alice",
  "active": true
}
```

Server Returns

```json
{
  "id": "12",
  "name": null,
  "active": "yes"
}
```

HTTP Status

```text
200 OK
```

Traditional load testers:

✅ Request Passed

Rupture:

❌ Contract Violation Detected

This enables teams to identify subtle API regressions that would otherwise remain unnoticed in production.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Built as a high-performance asynchronous API fuzzing engine for detecting hidden API contract violations, stress-testing distributed services, and producing enterprise-grade telemetry reports.