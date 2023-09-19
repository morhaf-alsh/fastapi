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
query = "CREATE TABLE IF NOT EXISTS emp( id int NOT NULL AUTO_INCREMENT ,name varchar(50),lname varchar(50), email varchar(50), position varchar(50), dept varchar(50),  PRIMARY KEY(id))"
cursor.execute(query)
conn.commit()
class Employee(BaseModel):
    id: int
    name: str
    lname: str
    email: str
    position: str
    dept: str



@app.post("/emp/", response_model=Employee)
def create_item(emp: Employee):
    cursor = conn.cursor()
    query = "INSERT INTO emp (name, lname, email, position, dept) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (emp.name, emp.lname, emp.email, emp.position, emp.dept))
    conn.commit()
    emp.id = cursor.lastrowid
    cursor.close()
    return emp

# @app.get("/get_emp")
# async def get_emp():
#     with open("data/emp.json", "r") as outfile:
#         emp = json.load(outfile)
#     return emp

# @app.post("/modify_me")
# async def modify_me(request: Request):
#     data = await request.json()
#     data["code"] = get_unique_code()
#     with open("data/emp.json", "w") as outfile:
#         json.dump(data, outfile)
#     return HTMLResponse("<p>done</p>")
    