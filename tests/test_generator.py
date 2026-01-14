import sys
import os
import secrets
# Add project root to path
sys.path.append(os.getcwd())

from app.services import generator_service

def test_generator():
    print("\n[TEST] Password Generator...")
    
    # Test 1: Length enforcement
    pwd = generator_service.generate_strong_password(length=32)
    print(f"  Generated (32 chars): {pwd}")
    assert len(pwd) == 32
    print("  [PASS] Length correct.")
    
    # Test 2: Complexity
    pwd_complex = generator_service.generate_strong_password(
        length=20,
        include_uppercase=True,
        include_digits=True,
        include_symbols=True
    )
    print(f"  Generated (Complex): {pwd_complex}")
    
    has_upper = any(c.isupper() for c in pwd_complex)
    has_digits = any(c.isdigit() for c in pwd_complex)
    has_symbols = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd_complex)
    
    assert has_upper, "Missing Uppercase"
    assert has_digits, "Missing Digits"
    assert has_symbols, "Missing Symbols"
    
    print("  [PASS] Complexity requirements met.")

if __name__ == "__main__":
    test_generator()
    print("\n[ALL TESTS PASSED] Generator Verified.")
