from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel

connection_string = "Connection string"

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Post(BaseModel):
    text : str
    color : str
    author : str

def get_database():

    client = MongoClient(connection_string)

    return client['comm_it_db']

dbname = get_database()

def bubble_sort(array):

    for i in range(len(array)):
        for j in range(len(array) - 1 - i):
            if array[j]["likes"] < array[j + 1]["likes"]:
                buffer = array[j]
                array[j] = array[j + 1]
                array[j + 1] = buffer

@app.get("/")
def index():

    comm_it_post_data = dbname['comm_it_post_data']
    posts_data = comm_it_post_data.find()
    posts_data_array = []

    for id in posts_data:
        posts_data_array.append({"text": id["text"], "color": id["color"],
                                 "likes" : id["likes"], "author" : id["author"]})

    bubble_sort(posts_data_array)

    return posts_data_array

@app.post("/new_post")
def post(post : Post):

    new_post = {"text" : post.text, "color" : post.color,
                "likes" : 0, "author" : post.author}

    comm_it_post_data = dbname['comm_it_post_data']

    dbname.comm_it_post_data.insert_one(new_post)

    return 0
