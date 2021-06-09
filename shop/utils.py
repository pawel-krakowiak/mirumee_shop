import jwt
from datetime import datetime
from graphql_jwt.settings import jwt_settings
    
## JWT payload for Hasura
def jwt_payload(user, context=None):
    jwt_datetime = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
    jwt_expires = int(jwt_datetime.timestamp())
    payload = {}
    payload['email'] = str(user.email) # For library compatibility
    payload['sub'] = str(user.id)
    payload['sub_fname'] = user.first_name
    payload['sub_lname'] = user.last_name
    payload['sub_email'] = user.email
    payload['sub_active'] = user.is_active
    payload['sub_staff'] = user.is_staff
    payload['sub_superuser'] = user.is_superuser
    payload['exp'] = jwt_expires
    payload['https://hasura.io/jwt/claims'] = {}
    payload['https://hasura.io/jwt/claims']['x-hasura-user-id'] = str(user.id)
    return payload