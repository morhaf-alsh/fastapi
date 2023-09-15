import json
import random, string
from fastapi import FastAPI, Request, Form,Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Employee(BaseModel):
    name: str
    lname: str
    email: str
    position:str
    dept:str
    code: str
    def get_dict(self):
        dict ={
        "name": self.name,
        "last name": self.lname,
        "email": self.email,
        "position": self.position,
        "department": self.dept,
        "code": self.get_unique_code()
        }
        return dict

def get_unique_code():
    code = ''.join(random.choices(string.ascii_uppercase,k=8))
    return code

if __name__ == "__main__":
    a= Employee("morhaf","alshoufi","morhaf@fmail.com","it","it")
    print(a.get_dict())

@app.get("/")
async def root(request : Request):
    with open("data/emp.json", "r") as outfile:
        context = json.load(outfile)
    return templates.TemplateResponse('main.html', context = {"request": request, "context" : context })

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
    