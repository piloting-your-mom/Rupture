import asyncio
import time
import aiohttp

from fuzz.validator import validate_response_schema


async def worker(
    session: aiohttp.ClientSession,
    url: str,
    payload: dict,
    schema: dict | None,
    semaphore: asyncio.Semaphore,
    results: list,
):
    """
    Executes a single fuzzed request and validates the response.
    """
    async with semaphore:
        start_time = time.perf_counter()

        try:
            async with session.post(url, json=payload) as response:
                latency = time.perf_counter() - start_time

                is_valid = True
                validation_error = None

                if response.status == 200:
                    try:
                        response_json = await response.json()

                        if schema:
                            is_valid, validation_error = validate_response_schema(
                                response_json,
                                schema,
                            )

                    except Exception:
                        is_valid = False
                        validation_error = "Response body was not valid JSON"

                failure_type = None

                if response.status >= 400:
                    failure_type = f"HTTP Error {response.status}"

                elif not is_valid:
                    failure_type = f"Schema Failure ({validation_error})"

                results.append(
                    {
                        "payload": payload,
                        "status": response.status,
                        "latency": latency,
                        "error": failure_type,
                    }
                )

        except Exception as e:
            latency = time.perf_counter() - start_time

            results.append(
                {
                    "payload": payload,
                    "status": 0,
                    "latency": latency,
                    "error": f"Connection Error ({type(e).__name__})",
                }
            )


async def run_engine(
    url: str,
    payloads: list[dict],
    concurrency: int,
    schema: dict | None = None,
):
    """
    Runs the asynchronous fuzzing engine using pre-generated payloads.

    Parameters
    ----------
    url : str
        Target API endpoint.

    payloads : list[dict]
        Pre-generated fuzz payloads.

    concurrency : int
        Maximum number of simultaneous requests.

    schema : dict | None
        Optional JSON schema for response validation.
    """

    results = []

    semaphore = asyncio.Semaphore(concurrency)

    connector = aiohttp.TCPConnector(
        limit=concurrency,
        limit_per_host=concurrency,
        ttl_dns_cache=300,
        enable_cleanup_closed=True,
    )

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
    ) as session:

        tasks = [
            asyncio.create_task(
                worker(
                    session=session,
                    url=url,
                    payload=payload,
                    schema=schema,
                    semaphore=semaphore,
                    results=results,
                )
            )
            for payload in payloads
        ]

        await asyncio.gather(*tasks)

    return results