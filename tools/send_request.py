from langchain_core.tools import tool
from shared_store import BASE64_STORE, url_time
import time
import os
import requests
import json
from collections import defaultdict
from typing import Any, Dict, Optional
from urllib.parse import urljoin

cache = defaultdict(int)
retry_limit = 4

@tool
def post_request(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
    """
    Send an HTTP POST request to the given URL with the provided payload.
    """
    # FIXED: Skip webhook.site (causes network errors)
    if "webhook.site" in url:
        print(f"⚠️ Skipping webhook.site call: {url}")
        return {"skipped": True, "reason": "webhook.site not accessible in HF Spaces"}

    # Handling if the answer is a BASE64
    ans = payload.get("answer")
    if isinstance(ans, str) and ans.startswith("BASE64_KEY:"):
        key = ans.split(":", 1)[1]
        payload["answer"] = BASE64_STORE[key]

    headers = headers or {"Content-Type": "application/json"}

    try:
        cur_url = os.getenv("url")
        cache[cur_url] += 1
        sending = payload
        if isinstance(payload.get("answer"), str):
            sending = {
                "answer": payload.get("answer", "")[:100],
                "email": payload.get("email", ""),
                "url": payload.get("url", "")
            }
        print(f"\nSending Answer \n{json.dumps(sending, indent=4)}\n to url: {url}")
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        response.raise_for_status()

        data = response.json()
        print("Got the response: \n", json.dumps(data, indent=4), '\n')

        delay = time.time() - url_time.get(cur_url, time.time())
        print(delay)
        next_url = data.get("url")
        # Canonicalize relative URLs returned by the server against the current URL
        if next_url and not next_url.lower().startswith(("http://", "https://")):
            base = cur_url or payload.get("url") or ""
            try:
                resolved = urljoin(base, next_url)
                print(f"Resolved relative next_url '{next_url}' -> '{resolved}'")
                next_url = resolved
                data["url"] = next_url
            except Exception:
                print(f"Could not resolve next_url: {next_url}")
        if not next_url:
            return "Tasks completed"
        if next_url not in url_time:
            url_time[next_url] = time.time()

        correct = data.get("correct")
        if not correct:
            cur_time = time.time()
            prev = url_time.get(next_url, time.time())
            if cache[cur_url] >= retry_limit or delay >= 175:
                print("Not retrying, moving on to the next question")
                data = {"url": data.get("url", "")}
            else:
                os.environ["offset"] = str(url_time.get(next_url, time.time()))
                print("Retrying..")
                data["url"] = cur_url
                data["message"] = "Retry Again!"
        print("Formatted: \n", json.dumps(data, indent=4), '\n')
        forward_url = data.get("url", "")
        os.environ["url"] = forward_url
        if forward_url == next_url:
            os.environ["offset"] = "0"

        return data
    except requests.HTTPError as e:
        err_resp = e.response
        try:
            err_data = err_resp.json()
        except ValueError:
            err_data = err_resp.text
        print("HTTP Error Response:\n", err_data)
        return err_data

    except requests.ConnectionError as e:
        print("Connection error:", e)
        return {"error": "Network unreachable", "details": str(e)}

    except Exception as e:
        print("Unexpected error:", e)
        return str(e)
