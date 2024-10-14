import requests
import json
import re

# Notion API details
NOTION_API_KEY = 'your_notion_api_key'
NOTION_DATABASE_ID = 'your_notion_database_id'

# Function to extract poker data using regex
def parse_poker_data(poker_text):
    pattern = re.compile(
        r"Tournament #(?P<tournament_id>\d+), (?P<tournament_name>[\w\s]+) \$(?P<buyin>[\d.]+), Hold'em No Limit\n"
        r"Buy-in: \$(?P<entry_fee>[\d.]+)\+\$(?P<rake>[\d.]+)\+\$(?P<bounty>[\d.]+)\n"
        r"(?P<total_players>\d+) Players\n"
        r"Total Prize Pool: \$(?P<prize_pool>[\d.]+)\n"
        r"Tournament started (?P<start_date>[\d/: ]+)\n"
        r"(?P<finish_position>\d+)(?:st|nd|rd|th) : (?P<player_name>[\w\s]+), \$(?P<winning>[\d.]+)\n"
        r"You finished the tournament in (?P<position>\d+)(?:st|nd|rd|th) place.\n"
        r"You received a total of \$(?P<total_winnings>[\d.]+)."
    )
    match = pattern.match(poker_text.strip())
    if match:
        return match.groupdict()
    return None

# Function to add data to Notion
def add_to_notion(poker_data):
    notion_url = "https://api.notion.com/v1/pages"
    
    # Build the JSON data to send to Notion
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Tournament ID": {"title": [{"text": {"content": poker_data['tournament_id']}}]},
            "Tournament Name": {"rich_text": [{"text": {"content": poker_data['tournament_name']}}]},
            "Buy-in": {"rich_text": [{"text": {"content": poker_data['buyin']}}]},
            "Entry Fee": {"number": float(poker_data['entry_fee'])},
            "Rake": {"number": float(poker_data['rake'])},
            "Bounty": {"number": float(poker_data['bounty'])},
            "Total Players": {"number": int(poker_data['total_players'])},
            "Prize Pool": {"number": float(poker_data['prize_pool'])},
            "Start Date": {"date": {"start": poker_data['start_date']}},
            "Finish Position": {"number": int(poker_data['finish_position'])},
            "Winning": {"number": float(poker_data['winning'])},
            "Total Winnings": {"number": float(poker_data['total_winnings'])},
        }
    }

    # Send request to Notion API
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.post(notion_url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("Data successfully added to Notion")
    else:
        print(f"Failed to add data to Notion: {response.status_code}, {response.text}")

# Example poker data from GGPoker
poker_text = """
Tournament #154678955, Mini SUPER SIX Bounty Turbo $6.60, Hold'em No Limit
Buy-in: $3.07+$0.53+$3
1116 Players
Total Prize Pool: $6,774.12
Tournament started 2024/07/26 01:05:00 
54th : Hero, $20.81
You finished the tournament in 54th place.
You received a total of $20.81.
"""

# Parse the poker data
poker_data = parse_poker_data(poker_text)

if poker_data:
    add_to_notion(poker_data)
else:
    print("Failed to parse poker data")
