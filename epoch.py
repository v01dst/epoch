#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime, timezone, timedelta

FORMATS = {
    "iso": "%Y-%m-%dT%H:%M:%S%z",
    "rfc2822": "%a, %d %b %Y %H:%M:%S %z",
    "date": "%Y-%m-%d",
    "time": "%H:%M:%S",
    "datetime": "%Y-%m-%d %H:%M:%S",
}

def parse_input(s):
    s = s.strip()
    try:
        return int(s)
    except ValueError:
        pass
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"]:
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    except ValueError:
        return None

def format_ts(ts, fmt, tz):
    dt = datetime.fromtimestamp(ts, tz=tz)
    if fmt == "iso":
        return dt.strftime("%Y-%m-%dT%H:%M:%S") + dt.strftime("%z")
    if fmt == "rfc2822":
        return dt.strftime("%a, %d %b %Y %H:%M:%S %z")
    if fmt == "relative":
        now = datetime.now(tz=tz)
        diff = now - dt
        secs = int(diff.total_seconds())
        if secs < 0:
            secs = -secs
            suffix = "from now"
        else:
            suffix = "ago"
        if secs < 60:
            return f"{secs}s {suffix}"
        if secs < 3600:
            return f"{secs // 60}m {suffix}"
        if secs < 86400:
            return f"{secs // 3600}h {suffix}"
        if secs < 2592000:
            return f"{secs // 86400}d {suffix}"
        if secs < 31536000:
            return f"{secs // 2592000}mo {suffix}"
        return f"{secs // 31536000}y {suffix}"
    return dt.strftime(FORMATS.get(fmt, "%Y-%m-%d %H:%M:%S"))

def main():
    parser = argparse.ArgumentParser(prog="epoch", description="Work with Unix timestamps.")
    parser.add_argument("input", nargs="?", default=None, help="timestamp or date string")
    parser.add_argument("--format", "-f", choices=["iso", "rfc2822", "date", "time", "datetime", "relative"], default="iso", help="output format")
    parser.add_argument("--tz", default="UTC", help="timezone (UTC or offset like +02:00)")
    parser.add_argument("--now", action="store_true", help="print current timestamp")
    parser.add_argument("--ms", action="store_true", help="input/output in milliseconds")
    args = parser.parse_args()

    if args.tz == "UTC":
        tz = timezone.utc
    else:
        sign = 1 if args.tz[0] == "+" else -1
        parts = args.tz.lstrip("+-").split(":")
        hours = int(parts[0])
        mins = int(parts[1]) if len(parts) > 1 else 0
        tz = timezone(timedelta(hours=sign * hours, minutes=sign * mins))

    if args.now:
        ts = int(datetime.now(tz=timezone.utc).timestamp())
        if args.ms:
            ts *= 1000
        print(ts)
        return

    if args.input is None:
        parser.print_help()
        sys.exit(1)

    ts = parse_input(args.input)
    if ts is None:
        print(f"cannot parse: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.ms:
        ts = ts // 1000

    print(format_ts(ts, args.format, tz))

if __name__ == "__main__":
    main()
