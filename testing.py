import os
import subprocess
import time

def find_mongo_pid():
    """Find MongoDB process ID (PID)."""
    try:
        result = subprocess.run(["pgrep", "mongod"], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def restart_mongo():
    """Kill and restart MongoDB manually."""
    pid = find_mongo_pid()
    
    if pid:
        print(f"MongoDB is running with PID {pid}. Stopping...")
        os.system(f"kill -9 {pid}")
        time.sleep(2)  # Wait for MongoDB to stop

    print("Starting MongoDB...")
    os.system("/usr/bin/mongod --config /etc/mongod.conf --fork")  # Change path if needed

    print("MongoDB restarted successfully.")

restart_mongo()
