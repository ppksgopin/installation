from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import re


class MyException(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id


app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)




class Users:
    name: str
    email: str

    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRequest(BaseModel):
    name: str = Field(min_length = 1)
    email: str = Field(min_length = 1)

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'Add user name',
                'email': 'Add user email'
            }
        }

user = {
    1:{"name": "Wanyu_Lee", "email": "Wanyu_Lee@pegatroncorp.com", "activate": True},
    2:{"name": "Sandy1_Zeng", "email": "Sandy1_Zeng@pegatroncorp.com", "activate": True}
}

def checkMail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
    	return True
    else:
        return False

def checkExist(name, mail):
    checkFlag = False
    for i in user:
        if (user[i]["name"] == name) or (user[i]["email"] == mail):
            checkFlag = True
            break

    return not checkFlag



@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


@app.get("/user/{user_id}", status_code = status.HTTP_200_OK)
async def inspect_user_by_id(user_id):
    digitFlag = str.isdigit(user_id) and int(user_id) != 0

    if digitFlag:
        user_id = int(user_id)
        existFlag = (user_id in user) and (user[user_id]["activate"] == True)

        if digitFlag:
            if existFlag:
                return user[user_id]
            else:
                raise HTTPException(status_code = 404, detail = 'User not exist.')
    else:
        raise HTTPException(status_code=400, detail='Wrong user id type.')

@app.post("/user", status_code = status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    print("Code processing.")

    msg = {}
    new_user = Users(**user_request.model_dump())


    '''


    formatFlag = checkMail(new_user.email)
    existFlag = checkExist(new_user.name, new_user.email)

    if not existFlag:
        raise HTTPException(status_code = 409, detail = 'User already exists.')

    if formatFlag:
        idxN = list(user)[-1] + 1
        buff = {"name": new_user.name, "email": new_user.email, "activate": True}
        user[idxN] = buff
        msg = {"msg": "Add new user succeed.", "user_id": idxN}
        print(msg)
        return msg
    else:
        raise HTTPException(status_code = 400, detail = 'Wrong input parameters.')
    '''

@app.put("/user/{user_id}", status_code = status.HTTP_200_OK)
async def update_user(update_user: UserRequest, user_id: int):
    msg = {}
    existFlag = (user_id in user) and (user[user_id]["activate"] == True)
    if existFlag:
        user[user_id]["name"] = update_user.name
        user[user_id]["email"] = update_user.email
        msg = {"msg": "Update user " + str(user_id) + " data succeed."}
        return msg
    else:
        raise HTTPException(status_code = 404, detail='User not exist.')


@app.delete("/user/{user_id}", status_code = status.HTTP_200_OK)
async def delete_user(user_id: int = Path(gt = 0) ):
    existFlag = (user_id in user) and (user[user_id]["activate"] == True)
    msg = {}

    if existFlag:
        user[user_id]["activate"] = False
        msg = {"msg": "Delete user " + str(user_id) + " succeed."}
        return msg
    else:
        raise HTTPException(status_code = 404, detail='User not exist.')