#!/usr/bin/env python3
import sys, json, datetime, os

HOME = os.path.expanduser("~")
LOG_BASE = os.path.join(HOME, "logs", "rpi-home")

def log_message(level: str, message: str, file_name: str):
    LOG_FILE = os.path.join(LOG_BASE, file_name)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "level": level,
        "message": message
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    if len(sys.argv) < 4:
        print("Usage: logcli.py <level> <message> <file name>")
        sys.exit(1)

    level = sys.argv[1]
    file_name = sys.argv[-1]
    message = " ".join(sys.argv[2:-1])
    log_message(level, message, file_name)


if __name__ == "__main__":
    main()
