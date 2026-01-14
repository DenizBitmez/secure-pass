import hashlib
import httpx

async def check_pwned_password(password: str) -> int:
    """
    Checks if password has been exposed in data breaches using Have I Been Pwned API via k-Anonymity.
    Returns the count of times it was seen. 0 means safe (so far).
    """
    # 1. SHA-1 hash the password
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1password[:5]
    suffix = sha1password[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
            return 0 # Fail safe or raise error depending on requirements
    
    # 3. Check if suffix is in response
    # Response format: SUFFIX:COUNT
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    
    return 0
