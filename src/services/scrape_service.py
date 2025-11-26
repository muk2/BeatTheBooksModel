import httpx
import csv
from io import StringIO

BASE_URL = "https://www.pro-football-reference.com/teams/{team}/{year}/gamelog.csv"


async def download_team_gamelog(team: str, year: int):
    url = BASE_URL.format(team=team.lower(), year=year)

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        res.raise_for_status()

    # Convert CSV text to a file-like object for csv.DictReader
    csv_content = StringIO(res.text)
    reader = csv.DictReader(csv_content)

    games = []

    for row in reader:
        # Skip future weeks with no points
        if row.get("Pts") == "":
            continue

        game = {
            "team": team.upper(),
            "week": int(row["Week"]),
            "date": row["Date"],
            "opponent": row["Opp"],
            "result": row["Result"],
            "team_points": int(row["Pts"]) if row["Pts"] else None,
            "opp_points": int(row["Pts Allowed"]) if row["Pts Allowed"] else None,
            "team_total_yards": int(row["Tot Yds"]) if row["Tot Yds"] else None,
            "opp_total_yards": int(row["Tot Yds Allowed"]) if row["Tot Yds Allowed"] else None,
            "turnovers": int(row["TO"]) if row["TO"] else None
        }

        games.append(game)

    return games