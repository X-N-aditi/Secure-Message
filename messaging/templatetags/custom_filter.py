from django import template
from cryptography.fernet import Fernet

register = template.Library()

# Store your key securely; this is just an example.
# In production, retrieve it from a secure location.
KEY = b'your_symmetric_key_here'  # Replace with your actual key

@register.filter
def decrypt_message(encrypted_content):
    f = Fernet(KEY)
    try:
        decrypted_message = f.decrypt(encrypted_content.encode()).decode()
    except Exception as e:
        return "Decryption failed"  # Handle decryption errors appropriately
    return decrypted_message
