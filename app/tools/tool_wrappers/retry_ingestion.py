import time

def retry_with_backoff(func, max_retries=3, backoff=2, *args, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(backoff ** attempt)
    print("All retries failed.")
    return None