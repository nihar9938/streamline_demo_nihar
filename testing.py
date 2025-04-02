import subprocess

def restart_mongodb():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "mongod"], check=True)
        print("MongoDB restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting MongoDB: {e}")

restart_mongodb()
