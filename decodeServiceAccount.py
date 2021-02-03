import base64
import os

base64_message = os.getenv('SERVICE_ACCOUNT')
base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)

with open("service_account.json", 'wb') as file:
    file.write(message_bytes)
