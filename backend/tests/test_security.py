from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hash_round_trip():
    hashed = hash_password("correct-horse-battery")
    assert hashed != "correct-horse-battery"
    assert verify_password("correct-horse-battery", hashed)
    assert not verify_password("wrong-password", hashed)

def test_token_round_trip():
    token = create_access_token("tester", "operator")
    payload = decode_access_token(token)
    assert payload["sub"] == "tester"
    assert payload["role"] == "operator"
