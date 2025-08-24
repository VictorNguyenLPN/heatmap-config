import os
import sys
import subprocess
from datetime import datetime, timedelta

# Pattern 2/9 (7 hàng, 16 cột)
pattern_1 = [
    "##### . . . ##### . . ...# . ##### . #...# . #####",
    "....# . . . #...# . . ..## . #...# . #...# . #....",
    "....# . . . #...# . . .#.# . #...# . #...# . #....",
    "##### . . . ##### . . ...# . ##### . ##### . #####",
    "#.... . . . ....# . . ...# . ....# . ....# . ....#",
    "#.... . . . ....# . . ...# . ....# . ....# . ....#",
    "##### . # . ##### . # ...# . ##### . ....# . #####",
]

pattern = [row.replace(" ", "") for row in pattern_1]

CENTER = True
TOTAL_WEEKS = 53
COMMITS_PER_DAY = 3

if len(sys.argv) < 2:
    print("Enter start date follow this format YYYY-MM-DD. Example: ")
    print("   python3 main.py 2023-07-16")
    sys.exit(1)

try:
    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
except ValueError:
    print("start_date must in this format YYYY-MM-DD")
    sys.exit(1)

if start_date.weekday() != 6:
    print("start_date is not Sunday")

if CENTER:
    margin = (TOTAL_WEEKS - len(pattern[0])) // 2
    pattern = [("." * margin) + row + ("." * margin) for row in pattern]

open("log.txt", "w").close()

def commit_on(date_str):
    for i in range(COMMITS_PER_DAY):
        with open("log.txt", "a") as f:
            f.write(f"{date_str} - commit {i}\n")
        subprocess.run(["git", "add", "log.txt"])
        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = date_str + " 12:00:00"
        subprocess.run(
            ["git", "commit", "--date", date_str + " 12:00:00", "-m", f"pixel {date_str}"],
            env=env
        )
    print(f"Commit {COMMITS_PER_DAY} save into {date_str}")

for col in range(len(pattern[0])):
    for row in range(len(pattern)):
        if pattern[row][col] == "#":
            commit_day = start_date + timedelta(weeks=col, days=row)
            commit_on(commit_day.strftime("%Y-%m-%d"))
