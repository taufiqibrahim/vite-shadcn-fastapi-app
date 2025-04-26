import secrets
import string

def generate_unique_id(prefix='org', random_length=16):
    alphabet = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(random_length))
    return f"{prefix}-{random_part}"

# Example usage
unique_id = generate_unique_id()
print(unique_id)