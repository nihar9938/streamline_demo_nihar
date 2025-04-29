import pandas as pd
import requests
import asyncio
import aiohttp  # For potentially more efficient asynchronous HTTP

async def get_oauth_access_token():
    # ... (same as before)

async def fetch_project_ids(session, base_url, job, headers):
    try:
        async with session.get(f'{base_url}/api/v4/search?scope=blobs&search="{job.split(\' \')[0]}"', headers=headers) as res:
            res.raise_for_status()
            data = await res.json()
            ids = [i['project_id'] for i in data]
            return job, list(set(ids))
    except aiohttp.ClientError as e:
        print(f"Error fetching for job {job}: {e}")
        return job, []

async def search_project_files():
    access_token = await get_oauth_access_token()
    if not access_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    base_url = 'https://automation.gitlab.aws.site.gs.com'
    results = {}

    try:
        df = pd.read_excel('ETO_jobs.xlsx')
        jobs = df['Autosys_Key'].dropna().tolist()

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_project_ids(session, base_url, job, headers) for job in jobs]
            for future in asyncio.as_completed(tasks):
                job, project_ids = await future
                results[job] = project_ids

        df1 = pd.DataFrame(list(results.items()), columns=['Jobs', 'project_ids'])
        df1.to_excel('Autosys_job.xlsx', index=False)
        print('Success')

    except FileNotFoundError:
        print("Error: ETO_jobs.xlsx not found.")
    except KeyError:
        print("Error: 'Autosys_Key' column not found in ETO_jobs.xlsx")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def main():
    await search_project_files()

if __name__ == "__main__":
    asyncio.run(main())
