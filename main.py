from fastapi import FastAPI,HTTPException,status,Path
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter
from issues import router as router
from timer import log_request_time

app = FastAPI()
app.include_router(router)
app.middleware("http")(log_request_time)

users ={
    1:{
        "name":"ahmad",
        "website":"www.ahmad.com",
        "age":28,
        "role":"developer"
    },
    2:{
        "name":"khaled",
        "website":"www.khaled.com",
        "age":21,
        "role":"Manager"
    }
}

#Base PyDantic Model
class User(BaseModel):
    name:str
    website:str
    age:int
    role:str

class UpdateUser(BaseModel):
    name:Optional[str] = None
    website:Optional[str] = None
    age:Optional[int] = None
    role:Optional[str] = None

#EndPoint
@app.get("/")
def root():
    return{"message":"Welcome to FastAPI"}

#Get All Users
@app.get("/users")
def get_user():
    return users

#Get Users
@app.get("/users/{user_id}")
def get_user(user_id:int = Path(...,description="The ID you want get",gt=0,lt=100)):
    if user_id not in users:
        raise HTTPException(status_code=404,detail="User Not Found")
    return users[user_id]

#Create Users
@app.post("/users/{user_id}",status_code=status.HTTP_201_CREATED)
def created_user(user_id:int,user:User):
    if user_id in users:
        raise HTTPException(status_code=400,detail="User Already Existed")
    users[user_id]=user.model_dump()
    return users[user_id]

#Update a User
@app.put("/users/{user_id}")
def update_user(user_id:int,user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User Not Found")
    current_user = users[user_id]
    if user.name is not None:
        current_user["name"]=user.name
    if user.website is not None:
        current_user["website"]=user.website
    if user.age is not None:
        current_user["age"]=user.age
    if user.role is not None:
        current_user["role"]=user.role
    return users[user_id]

#Delete a User
@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User Not Found")
    deleted_user = users.pop(user_id)
    return {"message":"user has been deleted","deleted_user":deleted_user}

#Search a User
@app.get("/users/search/")
def search_user(user_name: Optional[str] = None):
    if not user_name :
        return {"message":"name is required parameter."}
    for u in users.values():
        if u["name"]==user_name:
            return u
    raise HTTPException(status_code=404,detail="User Not Found")

