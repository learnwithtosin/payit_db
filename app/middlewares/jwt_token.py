# import base64
# import json

# token = 

# def decode_jwt_str(token_str: str):
#     padding = '=' * (-len(token_str) % 4)

#     return base64.urlsafe_b64decode(token_str + padding)

# def decode_jwt(token: str):
#     header_base64, payload_base64, sig = token.split(".")
#     payload = json.loads(decode_jwt_str(payload_base64))
#     header = json.loads(decode_jwt_str(header_base64))
    
#     return {
#         "header": header,
#         "payload": payload,
#         "sig": sig
#     }