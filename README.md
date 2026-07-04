# 💥 Rupture: High-Performance Async API Fuzzer & Load Tester

Rupture is an automated, containerized API load-testing and mutation fuzzing engine designed to uncover performance bottlenecks and catch **silent data corruptions** (mutated data structures or broken API contracts disguised behind successful `200 OK` responses).

Built using `asyncio`, `aiohttp`, `Hypothesis`, and `jsonschema`, Rupture simulates aggressive concurrent traffic using chaotic, property-based payloads, validates JSON structural contracts in real time, and compiles enterprise-ready PDF telemetry reports.

---

## ✨ Features

- ⚡ High-performance asynchronous load testing with `asyncio`
- 🧪 Property-based fuzzing using Hypothesis
- 📜 JSON Schema contract validation
- 🔍 Detects silent API contract corruption hidden behind `200 OK` responses
- 📊 p50 / p95 / p99 latency telemetry
- 📄 Automated PDF reporting
- 🐳 Fully containerized with Docker
- 🧩 Includes a built-in FastAPI sandbox for demonstration

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

# 🚀 Quick Start

Rupture can be used in two ways:

1. **Run the bundled FastAPI sandbox** (recommended for first-time users)
2. **Fuzz any HTTP API endpoint** using the built-in CLI

---

## Prerequisites

- Docker Desktop installed and running

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

# 🎯 Option 1 — Run the Bundled Sandbox Demo

By default, the Docker image launches the included FastAPI sandbox application and automatically fuzzes it. This demonstrates Rupture's ability to detect API contract violations and generate performance telemetry without requiring any external setup.

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

After execution completes, the generated report will be available at

```
out/demo_report.pdf
```

The report contains:

- Latency statistics
- p50 / p95 / p99 metrics
- Contract violations
- Success/failure summary
- Request telemetry

---

# 🌐 Option 2 — Fuzz Your Own API

To target your own API instead of the bundled demo, override the default container entrypoint and invoke the CLI directly.

### Linux/macOS

```bash
docker run --rm \
--entrypoint python \
-v $(pwd)/out:/app/out \
rupture \
-m cli.main \
--url https://your-api.example.com/endpoint \
--users 100
```

### Windows PowerShell

```powershell
docker run --rm `
--entrypoint python `
-v ${PWD}/out:/app/out `
rupture `
-m cli.main `
--url https://your-api.example.com/endpoint `
--users 100
```

### Windows CMD

```cmd
docker run --rm --entrypoint python -v %cd%/out:/app/out rupture -m cli.main --url https://your-api.example.com/endpoint --users 100
```

---

## Using JSON Schema Validation

If you have a JSON Schema describing the expected API response, mount the schema into the container and provide its path using `--schema`.

Example:

```bash
docker run --rm \
--entrypoint python \
-v $(pwd)/out:/app/out \
-v $(pwd)/schema.json:/app/schema.json \
rupture \
-m cli.main \
--url https://your-api.example.com/users \
--users 100 \
--schema /app/schema.json
```

When a schema is supplied, Rupture validates every successful (`200 OK`) response against it and reports any structural contract violations.

---

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `--url` | Target API endpoint |
| `--users` | Number of concurrent workers |
| `--schema` | Optional JSON Schema file for response validation |

All generated reports are written to the mounted `out/` directory.

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