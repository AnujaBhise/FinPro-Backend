
# utils/auth.py - Authentication utilities (JWT and password hashing)

from datetime import datetime, timedelta
import bcrypt as _bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext

# JWT Configuration
JWT_SECRET = 'your_jwt_secret_key'
ALGORITHM = "HS256"
TOKEN_EXPIRES = 24  # hours

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return _bcrypt.hashpw(password_bytes, _bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode("utf-8")[:72]
    return _bcrypt.checkpw(plain_bytes, hashed_password.encode("utf-8"))


def create_token(user_id: int) -> str:
    """Create a JWT token for a user"""

    expire = datetime.utcnow() + timedelta(
        hours=TOKEN_EXPIRES
    )

    to_encode = {
        "id": user_id,
        "exp": expire
    }

    return jwt.encode(
        to_encode,
        JWT_SECRET,
        algorithm=ALGORITHM
    )


def decode_token(token: str) -> dict:
    """Decode a JWT token and return the payload"""

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None

