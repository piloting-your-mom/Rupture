import asyncio
import time
import aiohttp
from fuzz.validator import validate_response_schema

async def worker(session: aiohttp.ClientSession, url: str, payload: dict, schema: dict | None, semaphore: asyncio.Semaphore, results: list):
    """
    A single worker loop that fires a fuzzed payload and checks its schema contract.
    """
    async with semaphore:
        start_time = time.perf_counter()
        try:
            # Send the fuzzed payload via POST
            async with session.post(url, json=payload, timeout=10) as response:
                latency = time.perf_counter() - start_time
                
                # Default values
                response_json = None
                is_valid = True
                validation_error = None
                
                # Attempt to parse body as JSON if status is 200
                if response.status == 200:
                    try:
                        response_json = await response.json()
                        # If a schema is provided, validate it!
                        if schema:
                            is_valid, validation_error = validate_response_schema(response_json, schema)
                    except Exception:
                        is_valid = False
                        validation_error = "Response body was not valid JSON"

                # Classify the failure based on the plan's 3 buckets
                failure_type = None
                if response.status >= 400:
                    failure_type = f"HTTP Error {response.status}"
                elif not is_valid:
                    failure_type = f"Schema Failure ({validation_error})"

                results.append({
                    "payload": payload,
                    "status": response.status,
                    "latency": latency,
                    "error": failure_type
                })
        except Exception as e:
            latency = time.perf_counter() - start_time
            results.append({
                "payload": payload,
                "status": 0,
                "latency": latency,
                "error": f"Connection Error ({type(e).__name__})"
            })

async def run_engine(url: str, concurrency: int, schema: dict | None = None):
    """
    Orchestrates fuzz payload generation and routes concurrent workers.
    """
    from fuzz.strategies import generate_fuzzed_payloads
    
    # Generate one chaotic payload per concurrent user
    payloads = generate_fuzzed_payloads(concurrency)
    results = []
    
    semaphore = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(limit=concurrency)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        # Pass an individual fuzzed payload to each worker task
        tasks = [
            asyncio.create_task(worker(session, url, payloads[i], schema, semaphore, results))
            for i in range(concurrency)
        ]
        await asyncio.gather(*tasks)
        
    return results