import secrets
import string

def generate_strong_password(
    length: int = 16,
    include_uppercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True
) -> str:
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    alphabet = string.ascii_lowercase
    required_chars = []

    if include_uppercase:
        alphabet += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    
    if include_digits:
        alphabet += string.digits
        required_chars.append(secrets.choice(string.digits))
        
    if include_symbols:
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        alphabet += symbols
        required_chars.append(secrets.choice(symbols))
        
    # Fill the rest
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(alphabet) for _ in range(remaining_length)]
    
    secrets.SystemRandom().shuffle(password_chars)
    
    return ''.join(password_chars)
