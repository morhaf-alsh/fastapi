import uvicorn
import json
import random, string
from fastapi import FastAPI, Request, Form,Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import MySQLdb
import os
from typing import Optional

app = FastAPI()

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'api',
}
conn = MySQLdb.connect(**db_config)

cursor = conn.cursor()
query = "CREATE TABLE IF NOT EXISTS emp( id int AUTO_INCREMENT ,name varchar(50),lname varchar(50), email varchar(50), position varchar(50), dept varchar(50),  PRIMARY KEY(id))"
cursor.execute(query)
conn.commit()
class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    lname: str
    email: str
    position: str
    dept: str
    lists: Optional[list] = None



@app.post("/emp/", response_model=Employee)
def create_emp(emp: Employee):
    cursor = conn.cursor()
    query = "INSERT INTO emp (name, lname, email, position, dept) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (emp.name, emp.lname, emp.email, emp.position, emp.dept))
    conn.commit()
    emp.id = cursor.lastrowid
    cursor.close()
    return emp

@app.get("/emp/list/")
def list_emps():
    cursor = conn.cursor()
    query = "SELECT * FROM emp"
    cursor.execute(query)
    emps = cursor.fetchall()
    print(emps)
    emps_all =[]
    for row in emps:
        item = {}
        item["id"] = row[0]
        item["name"] = row[1]
        item["lname"] = row[2]
        item["email"] = row[3]
        item["position"] = row[4]
        item["dept"] = row[5]
        emps_all.append(item)
    cursor.close()
    return emps_all

@app.delete("/emp/{emp_id}")
def delete_emp(emp_id: int):
    cursor = conn.cursor()
    query = "DELETE FROM emp WHERE id=%s"
    cursor.execute(query, (emp_id,))
    conn.commit()
    cursor.close()
    return {"id": emp_id}

@app.put("/emp/{emp_id}", response_model=Employee)
def modify_item(emp_id: int, emp: Employee):
    cursor = conn.cursor()
    query = "UPDATE emp SET name=%s, lname=%s, email=%s, position=%s, dept=%s WHERE id=%s"
    cursor.execute(query, (emp.name, emp.lname, emp.email, emp.position, emp.dept, emp_id))
    conn.commit()
    cursor.close()
    emp.id = emp_id 
    return emp



if __name__ == '__main__':
    uvicorn.run("hello:app", port=8000, host="0.0.0.0")