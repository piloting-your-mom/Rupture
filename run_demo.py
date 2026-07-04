import subprocess
import time
import sys
import os

def main():
    print("🛸 [Rupture Orchestrator] Booting local FastAPI demo target...")
    
    # 1. Start the FastAPI demo app in the background using uvicorn
    # We force it to run on port 8080 inside the host/container
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "demo.app:app", "--host", "0.0.0.0", "--port", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Give the FastAPI server 2 seconds to bind to the port and warm up
    time.sleep(2)
    
    try:
        print("🎯 [Rupture Orchestrator] Target alive. Launching Rupture Fuzz Engine...")
        
        # 2. Execute our Rupture CLI targeting our own local "flaky" endpoint!
        # We pass the demo_schema path we created to watch it catch failures.
        cmd = [
            "python", "-m", "cli.main",
            "--url", "http://127.0.0.1:8080/api/v1/flaky",
            "--users", "10",
            "--schema", "./schemas/demo_schema.json",
            "--output", "./out/demo_report.pdf"
        ]
        
        # Run it synchronously and let it print straight to the console
        subprocess.run(cmd, check=True)
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")
    finally:
        # 3. Clean up: Safely kill the background FastAPI server so port 8080 is freed
        print("🛑 [Rupture Orchestrator] Shutting down background demo target...")
        api_process.terminate()
        api_process.wait()
        print("✨ Done.")

if __name__ == "__main__":
    main()