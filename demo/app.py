from fastapi import FastAPI, Request, Response, status
import random

app = FastAPI(title="Rupture Intentional Target Demo")

@app.post("/api/v1/process")
async def healthy_endpoint(request: Request):
    """
    An ideal, compliant endpoint. It echo-returns the 
    received payload wrapped inside a predictable contract.
    """
    body = await request.json()
    return {
        "status": "success",
        "processed_payload": body
    }

@app.post("/api/v1/flaky")
async def unstable_endpoint(request: Request, response: Response):
    """
    An intentionally broken endpoint simulating silent structural corruption.
    50% of the time under high pressure, it mutates data types or 
    completely drops structural payload requirements.
    """
    body = await request.json()
    
    # Introduce chaos: Simulating an internal server state race condition
    if random.choice([True, False]):
        # Mutation: Wrap the data incorrectly or return a flat message string
        return {
            "status": "success",
            "processed_payload": "CRITICAL_ERROR: Data string serialization corrupted" 
        }
    
    return {
        "status": "success",
        "processed_payload": body
    }