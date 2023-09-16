import json
import random, string
from fastapi import FastAPI, Request, Form,Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import MySQLdb

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'api',
}
conn = MySQLdb.connect(**db_config)

cursor = conn.cursor()
query = "CREATE TABLE IF NOT EXISTS emp( id int NOT NULL  ,name varchar(50),lname varchar(50), email varchar(50), position varchar(50), dept varchar(50),  PRIMARY KEY(id))"
cursor.execute(query)
conn.commit()
class Employee(BaseModel):
    id: int
    name: str
    lname: str
    email: str
    position: str
    dept: str

def get_unique_code():
    code = ''.join(random.choices(string.ascii_uppercase,k=8))
    return code


@app.post("/emp/", response_model=Item)
def create_item(item: Item):
    cursor = conn.cursor()
    query = "INSERT INTO items (name, description) VALUES (%s, %s)"
    cursor.execute(query, (item.name, item.description))
    conn.commit()
    item.id = cursor.lastrowid
    cursor.close()
    return item

@app.get("/get_emp")
async def get_emp():
    with open("data/emp.json", "r") as outfile:
        emp = json.load(outfile)
    return emp

@app.post("/modify_me")
async def modify_me(request: Request):
    data = await request.json()
    data["code"] = get_unique_code()
    with open("data/emp.json", "w") as outfile:
        json.dump(data, outfile)
    return HTMLResponse("<p>done</p>")
    