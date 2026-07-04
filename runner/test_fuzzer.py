import pytest
import asyncio
import allure
from engine.core import run_engine

# We pull target settings from global execution state or environment variables
# For now, we will define defaults that can be overriden
TARGET_URL = "https://httpbin.org/post"
CONCURRENCY = 3
SCHEMA = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "url": { "type": "string" },
    "json": { "type": ["object", "array", "string", "number", "boolean", "null"] }
  },
  "required": ["url", "json"]
}

def test_api_fuzz_and_load():
    """
    Executes the Rupture engine inside a Pytest lifecycle context.
    """
    # Run our async engine synchronously inside the test
    results = asyncio.run(run_engine(TARGET_URL, CONCURRENCY, schema=SCHEMA))
    
    # Iterate through the async worker results and create explicit steps/assertions
    for idx, res in enumerate(results, 1):
        with allure.step(f"Evaluating Worker Request #{idx}"):
            # Attach the payload sent to Allure for historical debugging
            allure.attach(
                str(res["payload"]), 
                name=f"Payload Request #{idx}", 
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Latency: {res['latency']:.4f}s\nStatus Code: {res['status']}", 
                name=f"Metadata Request #{idx}", 
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Assert that the engine found no errors (HTTP, Schema corruption, or Timeout)
            if res["error"]:
                pytest.fail(f"Fuzz failure captured on worker {idx}: {res['error']}")