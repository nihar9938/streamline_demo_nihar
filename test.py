import pandas as pd
import requests
import os

def get_oauth_access_token():
    client_id = 'your_client_id'  # Replace with your actual client ID
    client_secret = 'your_client_secret'  # Replace with your actual client secret
    data = {
        'grant_type': 'client_credentials'
    }
    try:
        response = requests.post('https://id.web.gs.com/as/token.oauth2', data=data, auth=(client_id, client_secret))
        response.raise_for_status()
        json_response = response.json()
        return json_response['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token: {e}")
        return None

def process_batch_synchronous(access_token, batch_jobs, batch_number):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    base_url = 'https://automation.gitlab.aws.site.gs.com'
    batch_results = {}
    print(f"Processing batch {batch_number} with {len(batch_jobs)} entries...")
    for job in batch_jobs:
        try:
            res = requests.get(f'{base_url}/api/v4/search?scope=blobs&search="{job.split(\' \')[0]}"', headers=headers)
            res.raise_for_status()
            data = res.json()
            ids = [item['project_id'] for item in data]
            batch_results[job] = list(set(ids))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching for job '{job}' in batch {batch_number}: {e}")
            batch_results[job] = []
    print(f"Batch {batch_number} processed.")
    return batch_results

def search_project_files_batchwise_synchronous():
    access_token = get_oauth_access_token()
    if not access_token:
        return

    batch_size = 1500
    output_dir = 'output_batches'
    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_excel('ETO_jobs.xlsx')
        all_jobs = df['Autosys_Key'].dropna().tolist()
        num_batches = (len(all_jobs) + batch_size - 1) // batch_size

        for i in range(num_batches):
            start_index = i * batch_size
            end_index = min((i + 1) * batch_size, len(all_jobs))
            batch_jobs = all_jobs[start_index:end_index]
            batch_number = i + 1

            batch_results = process_batch_synchronous(access_token, batch_jobs, batch_number)

            df_batch = pd.DataFrame(list(batch_results.items()), columns=['Jobs', 'project_ids'])
            output_filename = os.path.join(output_dir, f'autosys_job_batch_{batch_number}.xlsx')
            df_batch.to_excel(output_filename, index=False)
            print(f"Output for batch {batch_number} saved to '{output_filename}'")

        print('All batches processed and saved.')

    except FileNotFoundError:
        print("Error: ETO_jobs.xlsx not found.")
    except KeyError:
        print("Error: 'Autosys_Key' column not found in ETO_jobs.xlsx")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    search_project_files_batchwise_synchronous()
