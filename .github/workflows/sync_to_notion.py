import os
import requests
import time
from github import Github

# Authenticate with GitHub and Notion
GITHUB_TOKEN = os.getenv('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')
NOTION_TOKEN = os.getenv('secret_TnaDfufN1h09vCjl4qeLP7Je3qgugiwJXggKhtdKe1E')
NOTION_DATABASE_ID = os.getenv('1cbdcc7a064e4674bd2943e1e0ac6019‎')

g = Github(GITHUB_TOKEN)

# Function to handle rate limiting
def handle_rate_limiting():
    rate_limit = g.get_rate_limit().core
    remaining = rate_limit.remaining
    reset_time = rate_limit.reset.timestamp()
    current_time = time.time()
    if remaining == 0:
        sleep_time = max(0, reset_time - current_time)
        print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)

# Function to send data to Notion
def send_to_notion(repo_name, repo_url, interaction_type):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": repo_name
                        }
                    }
                ]
            },
            "URL": {
                "url": repo_url
            },
            "Type": {
                "select": {
                    "name": interaction_type
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Failed to add {repo_name} to Notion: {response.text}")

# Fetch Starred Repositories
user = g.get_user()
try:
    starred_repos = user.get_starred()
except Exception as e:
    print(f"Error fetching starred repositories: {e}")
    starred_repos = []

# Send Data to Notion
for repo in starred_repos:
    repo_name = repo.full_name
    repo_url = repo.html_url
    interaction_type = "Star"
    send_to_notion(repo_name, repo_url, interaction_type)
    handle_rate_limiting()

print("Data has been sent to Notion")
