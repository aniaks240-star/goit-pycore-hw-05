from collections import Counter
from datetime import datetime
import sys


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(maxsplit=3)
    if len(parts) != 4:
        raise ValueError("Expected date, time, level and message.")
    date, time, level, message = parts
    datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    level = level.upper()
    if level not in ("INFO", "ERROR", "DEBUG", "WARNING"):
        raise ValueError(f"Unknown logging level: {level}.")
    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> list:
    logs = []
    with open(file_path, encoding="utf-8-sig") as file:
        for number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                raise ValueError(f"Invalid log at line {number}: {error}") from error
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log["level"] == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<17}| Кількість")
    print("-" * 17 + "|" + "-" * 10)
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python task_3.py <logfile> [level]")
        return 1
    level = sys.argv[2].upper() if len(sys.argv) == 3 else None
    if level and level not in ("INFO", "ERROR", "DEBUG", "WARNING"):
        print("Unknown logging level.")
        return 1
    try:
        logs = load_logs(sys.argv[1])
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Cannot load logs: {error}")
        return 1
    display_log_counts(count_logs_by_level(logs))
    if level:
        print(f"\nДеталі логів для рівня '{level}':")
        for log in filter_logs_by_level(logs, level):
            print(f"{log['date']} {log['time']} - {log['message']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
