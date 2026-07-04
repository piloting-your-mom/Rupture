import click
import asyncio
import json
import os
from engine.core import run_engine
from report.aggregator import calculate_metrics, generate_pdf_report

@click.command()
@click.option('--url', required=True, type=str, help='The target API endpoint URL.')
@click.option('--users', default=5, type=int, help='Number of concurrent logical users.')
@click.option('--schema', type=click.Path(exists=True), help='Path to the user-supplied jsonschema definition.')
@click.option('--output', default='./out/report.pdf', type=str, help='Path where the PDF report should be saved.')
def main(url, users, schema, output):
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
    
    # 1. Process Telemetry Analytics
    click.echo("🧮 Calculating performance metrics and percentiles...")
    metrics = calculate_metrics(results)
    
    # 2. Print Aggregated Terminal Summary
    click.echo("\n📊 --- AGGREGATED METRICS SUMMARY ---")
    click.echo(f"  Total Requests: {metrics['total_requests']}")
    click.echo(f"  Success Rate:   {metrics['success_count']} requests passed")
    click.echo(f"  Error Rate:     {metrics['error_rate']}%")
    click.echo(f"  p50 Latency:    {metrics['p50']}s")
    click.echo(f"  p95 Latency:    {metrics['p95']}s")
    click.echo(f"  p99 Latency:    {metrics['p99']}s")
    
    if metrics['error_distribution']:
        click.echo("\n🚨 Error Breakdown:")
        for err, count in metrics['error_distribution'].items():
            click.echo(f"  - {err}: {count} occurrences")

    # 3. Compile PDF Artifact
    click.echo("\n🖨️  Generating PDF Report...")
    try:
        generate_pdf_report(metrics, output)
        click.echo(f"✅ Report successfully generated at: {output}")
    except Exception as e:
        click.echo(f"❌ PDF Generation Failed: {e}")
        click.echo("💡 Tip: Ensure WeasyPrint system dependencies (Cairo/Pango) are installed or switch to Docker execution.")

if __name__ == '__main__':
    main()