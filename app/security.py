import hashlib, hmac, json
from .config import SECRET
def sign(data, controller_id):
    key = f"{SECRET}:{controller_id}".encode()
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(key, raw, hashlib.sha256).hexdigest()
def verify(data, controller_id, signature):
    return hmac.compare_digest(sign(data, controller_id), signature)
