"""Download 2025+ race and qualifying results from FastF1.

The Kaggle dataset ends in 2024, so this fills in the newer seasons.
Run from the project root:

    python -m src.fetch_recent

Writes data/recent/results_2025_2026.csv with one row per driver per Grand Prix.
"""

from pathlib import Path

import fastf1
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".fastf1_cache"
OUT = ROOT / "data" / "recent" / "results_2025_2026.csv"
SEASONS = [2025, 2026]


def load_session(year, round_, kind):
    session = fastf1.get_session(year, round_, kind)
    session.load(laps=False, telemetry=False, weather=False, messages=False)
    return session.results


def fetch_race(year, event):
    race = load_session(year, event.RoundNumber, "R")
    if race is None or race.empty or race.Position.isna().all():
        return None

    quali = load_session(year, event.RoundNumber, "Q")
    quali_pos = quali.set_index("Abbreviation")["Position"] if quali is not None else pd.Series(dtype=float)

    # ClassifiedPosition is a number for classified finishers and a letter
    # (R = retired, D = disqualified, ...) otherwise, like Kaggle's `position`.
    position = pd.to_numeric(race.ClassifiedPosition, errors="coerce")

    return pd.DataFrame({
        "year": year,
        "round": event.RoundNumber,
        "date": event.EventDate.date(),
        "race_name": event.EventName,
        "location": event.Location,
        "country": event.Country,
        "driver_number": race.DriverNumber.astype(int),
        "code": race.Abbreviation,
        "first_name": race.FirstName,
        "last_name": race.LastName,
        "team": race.TeamName,
        "quali_position": race.Abbreviation.map(quali_pos),
        "grid": race.GridPosition,
        "position": position,
        "positionOrder": race.Position,
        "points": race.Points,
        "status": race.Status,
    })


def main():
    CACHE.mkdir(exist_ok=True)
    fastf1.Cache.enable_cache(CACHE)
    today = pd.Timestamp.today().normalize()

    frames = []
    for year in SEASONS:
        schedule = fastf1.get_event_schedule(year, include_testing=False)
        for _, event in schedule[schedule.EventDate < today].iterrows():
            try:
                df = fetch_race(year, event)
            except Exception as err:  # results not published yet, API hiccup, etc.
                print(f"  skipped {year} R{event.RoundNumber} {event.EventName}: {err}")
                continue
            if df is None:
                print(f"  skipped {year} R{event.RoundNumber} {event.EventName}: no results")
                continue
            print(f"  {year} R{event.RoundNumber:>2} {event.EventName}: {len(df)} drivers")
            frames.append(df)

    results = pd.concat(frames, ignore_index=True).sort_values(["date", "positionOrder"])
    results.to_csv(OUT, index=False)
    print(f"Saved {len(results):,} rows from {results.groupby(['year', 'round']).ngroups} races to {OUT}")


if __name__ == "__main__":
    main()
