# Credential Input UI Stub

This markdown shows a minimal pseudo-form for capturing portal login information. In a real application these values would be sent to a backend and stored temporarily in Redis via [`app/storage/redis.py`](../../app/storage/redis.py).

```html
<form>
  <label for="portal">Portal Name</label>
  <input id="portal" type="text" placeholder="e.g. Portal A" />

  <label for="username">Username</label>
  <input id="username" type="text" />

  <label for="password">Password</label>
  <input id="password" type="password" placeholder="••••••" />

  <button type="submit">Submit</button>
</form>
```

Upon clicking **Submit**, the UI would call a function such as:

```python
from app.storage import redis

redis.set_key(f"cred:{portal}", username + ":" + password, expire=600)
```

This demonstrates how credentials could be temporarily stored. The full implementation would route these values through the backend and handle encryption when integrating with real portals.
