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



import pandas as pd
import asyncio
import aiohttp
import random
import os

async def get_oauth_access_token():
    client_id = 'your_client_id'  # Replace with your actual client ID
    client_secret = 'your_client_secret'  # Replace with your actual client secret
    data = {
        'grant_type': 'client_credentials'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://id.web.gs.com/as/token.oauth2', data=data, auth=(client_id, client_secret)) as response:
                response.raise_for_status()
                json_response = await response.json()
                return json_response['access_token']
    except aiohttp.ClientError as e:
        print(f"Error getting access token: {e}")
        return None

async def safe_api_call_async(session, url, headers, max_retries=5, initial_delay=1):
    retries = 0
    while retries < max_retries:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            if response is not None and response.status == 429:
                delay = initial_delay * (2 ** retries) + random.uniform(0, 0.1)
                print(f"Rate limit encountered for {url}. Retrying in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
                retries += 1
            else:
                print(f"API error for {url}: {e}")
                break
        await asyncio.sleep(0.1)
    print(f"Failed to get response after {max_retries} retries for {url}")
    return None

async def process_batch_async(session, access_token, batch_jobs, batch_number, all_results):
    headers = {"Authorization": f"Bearer {access_token}"}
    base_url = 'https://automation.gitlab.aws.site.gs.com'
    print(f"Processing batch {batch_number} with {len(batch_jobs)} entries...")
    tasks = []
    for job in batch_jobs:
        url = f'{base_url}/api/v4/search?scope=blobs&search="{job.split(\' \')[0]}"'
        async def fetch(job_url, current_job):
            data = await safe_api_call_async(session, job_url, headers)
            if data:
                ids = [item['project_id'] for item in data]
                all_results[current_job] = list(set(ids))
            else:
                all_results[current_job] = []
            await asyncio.sleep(0.05) # Small delay between individual requests within a batch
        tasks.append(asyncio.create_task(fetch(url, job)))
    await asyncio.gather(*tasks)
    print(f"Batch {batch_number} processed.")

async def search_project_files_batchwise_async():
    access_token = await get_oauth_access_token()
    if not access_token:
        return

    batch_size = 1500
    output_dir = 'output_batches_async'
    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_excel('ETO_jobs.xlsx')
        all_jobs = df['Autosys_Key'].dropna().tolist()
        num_batches = (len(all_jobs) + batch_size - 1) // batch_size
        all_results = {}

        async with aiohttp.ClientSession() as session:
            for i in range(num_batches):
                start_index = i * batch_size
                end_index = min((i + 1) * batch_size, len(all_jobs))
                batch_jobs = all_jobs[start_index:end_index]
                batch_number = i + 1

                await process_batch_async(session, access_token, batch_jobs, batch_number, all_results)

                df_batch = pd.DataFrame(list(all_results.items()), columns=['Jobs', 'project_ids'])
                output_filename = os.path.join(output_dir, f'autosys_job_batch_{batch_number}.xlsx')
                df_batch.to_excel(output_filename, index=False)
                all_results = {} # Clear results for the next batch
                print(f"Output for batch {batch_number} saved to '{output_filename}'")
                await asyncio.sleep(1) # Add a delay between processing batches to avoid overwhelming the API

        print('All batches processed and saved.')

    except FileNotFoundError:
        print("Error: ETO_jobs.xlsx not found.")
    except KeyError:
        print("Error: 'Autosys_Key' column not found in ETO_jobs.xlsx")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def main():
    await search_project_files_batchwise_async()

if __name__ == "__main__":
    asyncio.run(main())
