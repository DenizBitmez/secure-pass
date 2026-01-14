from zxcvbn import zxcvbn

def check_password_strength(password: str) -> dict:
    """
    Calculates password strength using zxcvbn.
    Returns a dictionary with score (0-4) and feedback.
    """
    result = zxcvbn(password)
    return {
        "score": result["score"],
        "feedback": [result["feedback"]["warning"]] if result["feedback"]["warning"] else result["feedback"]["suggestions"]
    }
