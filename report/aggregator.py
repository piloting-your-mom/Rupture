import math

def calculate_metrics(results: list) -> dict:
    """
    Computes p50, p95, p99 latencies, throughput, and error tracking 
    from raw engine worker runs.
    """
    if not results:
        return {}

    # Extract latencies for successful requests to avoid skewing performance metrics
    latencies = sorted([r["latency"] for r in results if r["status"] == 200])
    total_requests = len(results)
    
    # Error classification distribution
    error_counts = {}
    success_count = 0
    
    for r in results:
        if r["error"]:
            error_counts[r["error"]] = error_counts.get(r["error"], 0) + 1
        else:
            success_count += 1

    error_rate = ((total_requests - success_count) / total_requests) * 100

    # Fallbacks if 100% of requests failed or timed out
    def get_percentile(p):
        if not latencies:
            return 0.0
        idx = max(0, min(len(latencies) - 1, math.ceil((p / 100.0) * len(latencies)) - 1))
        return latencies[idx]

    return {
        "total_requests": total_requests,
        "success_count": success_count,
        "error_rate": round(error_rate, 2),
        "error_distribution": error_counts,
        "p50": round(get_percentile(50), 4),
        "p95": round(get_percentile(95), 4),
        "p99": round(get_percentile(99), 4),
    }
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def generate_pdf_report(metrics: dict, output_pdf_path: str):
    """
    Renders telemetry metrics into an HTML layout via Jinja2,
    then compiles it into an immutable PDF report using WeasyPrint.
    """
    # Create the output directory path if it doesn't exist yet
    output_dir = os.path.dirname(output_pdf_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Locate the template layout relative to this file's position
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, "templates")
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.html")
    
    # Inject metrics payload into HTML string
    rendered_html_string = template.render(metrics=metrics)
    
    # Compile the final document
    print(f"📄 Compiling stakeholder report target to: {output_pdf_path}")
    HTML(string=rendered_html_string).write_pdf(output_pdf_path)