
import requests
import os
from getpass import getpass

API_KEY = os.getenv("RIOT_API_KEY") or getpass("Enter Riot API key: ")

game_name = input("Enter Riot ID name: ")
tag_line = input("Enter Riot ID tag (without #): ")

# Get account information
account_url = (
    f"https://americas.api.riotgames.com/riot/account/v1/"
    f"accounts/by-riot-id/{game_name}/{tag_line}"
)

headers = {"X-Riot-Token": API_KEY}

account_response = requests.get(account_url, headers=headers)
account_response.raise_for_status()
account = account_response.json()

puuid = account["puuid"]

# Get ranked statistics for the North American server
summoner_url = (
    f"https://na1.api.riotgames.com/lol/summoner/v4/"
    f"summoners/by-puuid/{puuid}"
)

summoner_response = requests.get(summoner_url, headers=headers)
summoner_response.raise_for_status()

ranked_url = (
    f"https://na1.api.riotgames.com/lol/league/v4/"
    f"entries/by-puuid/{puuid}"
)

ranked_response = requests.get(ranked_url, headers=headers)
ranked_response.raise_for_status()
ranked_data = ranked_response.json()

# Find Solo/Duo statistics
solo_queue = next(
    (queue for queue in ranked_data
     if queue["queueType"] == "RANKED_SOLO_5x5"),
    None
)
if solo_queue:
    wins = solo_queue["wins"]
    losses = solo_queue["losses"]
    total_games = wins + losses
    win_rate = wins / total_games * 100

    print(f"\nPlayer: {game_name}#{tag_line}")
    print(f"Rank: {solo_queue['tier']} {solo_queue['rank']}")
    print(f"League Points: {solo_queue['leaguePoints']}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Total games: {total_games}")
    print(f"Win rate: {win_rate:.2f}%")
else:
    print("No ranked Solo/Duo statistics found.")
