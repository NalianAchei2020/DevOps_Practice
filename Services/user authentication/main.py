"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Configure Redis connection
redis_host = "redis-17977.c267.us-east-1-4.ec2.cloud.redislabs.com"
redis_port = 17977
redis_password = "Nalian@2020"
redis_db = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Define User model
class User(BaseModel):
    name: str
    email: str
    password: str


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get('/users')
async def read_users():
    user_data = redis_db.hgetall("users")
    users = []
    for user_dict in user_data.values():
        user_json = user_dict  # No need for decoding in this case
        user = User.parse_raw(user_json)  # Parse JSON string to User object
        users.append(user)
    return users

@app.post('/users')
async def create_user(user: User):
    redis_db.hset("users", user.name, user.json())
    return {"message": "User created successfully"}
    """
    
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Configure Redis connection
redis_host = "redis-17977.c267.us-east-1-4.ec2.cloud.redislabs.com"
redis_port = 17977
redis_password = "Nalian@2020"
redis = get_redis_connection(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)

# Define User model
class User(HashModel):
    name: str
    password: str
    
    # Define Redis-specific fields
    name = "user"  # Name of the Redis hash
    database = redis

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get('/users', methods=['GET'])
async def read_users():
    return User.all()

@app.post('/users', methods=['POST'])
async def create_user(user: User):
    return user.save()