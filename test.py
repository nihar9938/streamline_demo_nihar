import requests

def hit_api(url, num_requests=100):
    success_count = 0
    failure_count = 0
    
    for i in range(num_requests):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                success_count += 1
            else:
                failure_count += 1
            print(f"Request {i+1}: Status Code - {response.status_code}")
        except requests.exceptions.RequestException as e:
            failure_count += 1
            print(f"Request {i+1}: Failed - {e}")
    
    print(f"\nSummary: {success_count} successes, {failure_count} failures")

if __name__ == "__main__":
    api_url = "https://your-api-endpoint.com"  # Replace with the actual API URL
    hit_api(api_url)
