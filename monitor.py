"""
Simple Python monitor for the HF Space `healthz` endpoint.
Usage: python scripts/monitor.py --url https://your-space.hf.space/healthz --interval 10
"""
import time
import argparse
import requests


def main(url: str, interval: int):
    print(f"Starting monitor for {url} (interval {interval}s)")
    while True:
        try:
            r = requests.get(url, timeout=10)
            print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} Status: {r.status_code} Content: {r.text}")
        except Exception as e:
            print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} ERROR: {e}")
        time.sleep(interval)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--url', default='https://DS22F2001348-llm-quiz-solver.hf.space/healthz')
    p.add_argument('--interval', type=int, default=10)
    args = p.parse_args()
    main(args.url, args.interval)
