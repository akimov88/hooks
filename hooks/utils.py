import hashlib
import json
import random
import time

from rest_framework.exceptions import ValidationError


def send_data(data: dict, attempt: int = 5) -> dict:
    try:
        time.sleep(random.random())
        result = random.randint(0, 50)
        hash_data = hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
        if result <= 10:
            raise ValueError('send_data_error')
        return {'number': result, 'md5': hash_data}
    except ValueError:
        attempt -= 1
        if attempt == 0:
            raise ValidationError('send_data_error')
        send_data(data, attempt)
