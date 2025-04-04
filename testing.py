import os
import subprocess
import time

def find_mongo_pid():
    """Find MongoDB process ID (PID) using `ps` instead of `pgrep`."""
    try:
        # Get all running processes and search for 'mongod'
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        
        for line in lines:
            if "mongod" in line and "--config" in line:  # Ensures we target the main MongoDB process
                parts = line.split()
                return parts[1]  # PID is the second column
        
    except subprocess.CalledProcessError:
        return None

def restart_mongo():
    """Kill and restart MongoDB manually."""
    pid = find_mongo_pid()
    
    if pid:
        print(f"MongoDB is running with PID {pid}. Stopping...")
        os.system(f"kill -9 {pid}")
        time.sleep(2)  # Wait for MongoDB to fully stop

    print("Starting MongoDB...")
    os.system("/usr/bin/mongod --config /etc/mongod.conf --fork")  # Change path if needed

    print("MongoDB restarted successfully.")

restart_mongo()



https://chatgpt.com/share/67ef8914-f05c-8012-85c0-28e33654b77f
