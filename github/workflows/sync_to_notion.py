import requests
import os

# Replace with your Notion API token and database ID
NOTION_API_TOKEN = os.getenv('secret_TnaDfufN1h09vCjl4qeLP7Je3qgugiwJXggKhtdKe1E')
NOTION_DATABASE_ID = os.getenv('1cbdcc7a064e4674bd2943e1e0ac6019‎')

# Function to fetch GitHub repositories
def fetch_github_repositories():
    url = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to fetch starred repositories
def fetch_starred_repositories():
    url = 'https://api.github.com/user/starred'
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to sync data to Notion
def sync_to_notion():
    github_repos = fetch_github_repositories()
    starred_repos = fetch_starred_repositories()

    # Example logic to sync data to Notion
    # Replace with your actual Notion API integration code
    notion_data = {
        "database_id": NOTION_DATABASE_ID,
        "properties": {
            "Name": {"title": [{"text": {"content": "Example Repository"}}]},
            # Add more properties as needed
        }
    }

    # Example request to Notion API
    notion_url = 'https://api.notion.com/v1/pages'
    headers = {
        'Authorization': f'Bearer {NOTION_API_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-05-13'
    }
    response = requests.post(notion_url, headers=headers, json=notion_data)

    # Check response status
    if response.status_code == 200:
        print('Data synced successfully to Notion!')
    else:
        print(f'Failed to sync data to Notion. Status code: {response.status_code}')

if __name__ == "__main__":
    sync_to_notion()
