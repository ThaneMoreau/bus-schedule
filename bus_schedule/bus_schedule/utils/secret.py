import os

from django.core.management.utils import get_random_secret_key


def generate_secret_key(path, filename):
    from django.core.management.utils import get_random_secret_key
    secret = f"SECRET_KEY = \'{get_random_secret_key()}\'"
    full_path = os.path.join(path, filename)
    with open(full_path, 'w') as f:
        f.write(secret)
