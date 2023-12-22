from fastapi import FastAPI
from redis_om import get_redis_connection
from fastapi import CORSMiddleware

app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

# connecting to redis database

redis = get_redis_connection(
    host="redis-17977.c267.us-east-1-4.ec2.cloud.redislabs.com:",
    port=17977,
    password = "Nalian@2020",
    decode_responses=True
)

# creating a database model
class User(redis.Model):
    name: str
    password: str
    
    
    database = redis
    

@app.get("/")

async def root():
    return {"message": "Hello World"}

@app.get('/use')
async def all():
    return User.all()