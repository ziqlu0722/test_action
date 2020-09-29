from app import db
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import generate_password_hash, check_password_hash
import re
import uuid

# this is to create UUID for sqlite
from sqlalchemy.types import TypeDecorator, CHAR

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

class User(db.Model):
#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    id = db.Column(GUID(), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(128))
    account_created = db.Column(db.DateTime())
    account_updated = db.Column(db.DateTime())

    def __init__(self, email_address, first_name, last_name):
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User {}>'.format(self.email_address)

    # enforce strong password: 1. more than 8 chars, 2. no single char pwd 3. has at least 1 symbol 4. has at least a digit
    @classmethod
    def valid_passord(cls, password):
        length = len(password) > 8
        unique = len(set(password)) > 4
        symbol = bool(re.search(r"\W", password))
        digit = bool(re.search(r"\d", password))
        return length and unique and symbol and digit

    @classmethod
    def valid_email(cls, email):
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return bool(re.search(email_regex, email))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, str(password))
