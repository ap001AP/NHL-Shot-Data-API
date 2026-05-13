import requests
import pandas as pd
import time
import os

NHL_API = "https://api-web.nhle.com/v1"

def get_play_by_play(game_id: int) -> list[dict]:
    url = f"{NHL_API}/gamecenter/{game_id}/play-by-play"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return []
    return r.json().get("plays", [])

def extract_shots(plays: list[dict], game_id: int) -> list[dict]:
    shots = []
    for play in plays:
        if play.get("typeDescKey") not in ("shot-on-goal", "goal"):
            continue

        details = play.get("details", {})
        x = details.get("xCoord")
        y = details.get("yCoord")
        shot_type = details.get("shotType", "unknown")
        situation = play.get("situationCode", "1551")  # 1551 = 5v5

        if x is None or y is None:
            continue

        # Distance and angle from goal (goal is at x=89)
        dist = ((abs(x) - 89) ** 2 + y ** 2) ** 0.5
        import math
        angle = abs(math.degrees(math.atan2(abs(y), abs(abs(x) - 89))))

        shots.append({
            "game_id": game_id,
            "is_goal": int(play["typeDescKey"] == "goal"),
            "x_coord": x,
            "y_coord": y,
            "distance": round(dist, 2),
            "angle": round(angle, 2),
            "shot_type": shot_type,
            "situation_code": situation,
            "period": play.get("periodDescriptor", {}).get("number", 0),
        })
    return shots

def download_season(season: str = "20232024", max_games: int = 500):
    """
    NHL game IDs: {season}{type}{number}
    season = 20232024, type = 02 (regular), games 0001–1312
    """
    print(f"Pulling up to {max_games} games from {season} season...")
    all_shots = []
    failed = 0

    for i in range(1, max_games + 1):
        game_id = int(f"{season[:4]}02{i:04d}")
        plays = get_play_by_play(game_id)

        if not plays:
            failed += 1
            if failed > 20:  # stop if too many misses in a row
                break
            continue

        shots = extract_shots(plays, game_id)
        all_shots.extend(shots)
        failed = 0  # reset on success

        if i % 50 == 0:
            print(f"  Game {i}: {len(all_shots):,} shots so far...")

        time.sleep(0.3)  

    df = pd.DataFrame(all_shots)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/shots_combined.csv", index=False)
    print(f"\nDone. {len(df):,} shots saved to data/shots_combined.csv")
    print(f"Goal rate: {df['is_goal'].mean():.1%}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(df.head())
    return df

if __name__ == "__main__":
    download_season("20232024", max_games=500)