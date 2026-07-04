import click
import asyncio
import json
import os
from engine.core import run_engine

@click.command()
@click.option('--url', required=True, type=str, help='The target API endpoint URL.')
@click.option('--users', default=5, type=int, help='Number of concurrent logical users.')
@click.option('--schema', type=click.Path(exists=True), help='Path to the user-supplied jsonschema definition.')
def main(url, users, schema):
    """Rupture: Automated API Load Testing & Fuzzing CLI."""
    click.echo(f"🚀 Initializing Rupture Fuzz Engine...")
    click.echo(f"🎯 Target URL: {url}")
    click.echo(f"👥 Concurrent Users: {users}")
    
    # Load schema file if passed
    schema_data = None
    if schema:
        click.echo(f"📜 Loading Schema Contract: {schema}")
        with open(schema, 'r') as f:
            schema_data = json.load(f)

    click.echo("⏳ Spawning worker pool with chaotic payloads...")
    results = asyncio.run(run_engine(url, users, schema=schema_data))
    
    click.echo("\n📊 --- FUZZ & SCHEMA LIVE RESULTS ---")
    for idx, res in enumerate(results, 1):
        click.echo(f"\n👉 Request {idx}:")
        click.echo(f"  [Payload Sent]: {res['payload']}")
        if res["error"]:
            # Flags structural corruptions even on 200 OK!
            click.echo(f"  ❌ Result: FAILED | {res['error']} | Latency: {res['latency']:.4f}s")
        else:
            click.echo(f"  ✅ Result: PASSED | Status {res['status']} | Latency: {res['latency']:.4f}s")
            
    click.echo(f"\n✅ Finished processing {len(results)} fuzz targets.")

if __name__ == '__main__':
    main()