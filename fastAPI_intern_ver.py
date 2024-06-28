from fastapi import FastAPI, HTTPException, Path, Request
from pydantic import BaseModel, Field
from starlette import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import re

app = FastAPI()

class Users:
    name: str
    email: str

    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRequest(BaseModel):
    name: str
    email: str

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


class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    if request.method == "DELETE":
        return JSONResponse(status_code=500, content={"message": f"DELETE operation failed: {exc.message}"})
    else:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {exc.message}"})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = {"msg": "Wrong input parameters."})


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
        raise HTTPException(status_code=400, detail = 'Wrong user id type.')

@app.post("/user", status_code = status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    msg = {}
    new_user = Users(**user_request.model_dump())

    if (len(new_user.name) != 0) and (len(new_user.email) != 0):
        if checkMail(new_user.email):
            if checkExist(new_user.name, new_user.email):
                idxN = list(user)[-1] + 1
                buff = {"name": new_user.name, "email": new_user.email, "activate": True}
                user[idxN] = buff
                msg = {"msg": "Add new user succeed.", "user_id": idxN}
                return msg
            else:
                raise HTTPException(status_code=409, detail = 'User/mail already exists.')
        else:
            raise HTTPException(status_code=400, detail = 'Wrong input email')
    else:
        raise HTTPException(status_code=400, detail = 'Wrong input parameters.')

@app.put("/user/{user_id}", status_code = status.HTTP_200_OK)
async def update_user(update_user: UserRequest, user_id: int):
    msg = {}    
    existFlag = (user_id in user) and (user[user_id]["activate"] == True)

    if existFlag:
        if len(update_user.name) != 0:
            user[user_id]["name"] = update_user.name
        if len(update_user.email) != 0:
            if checkMail(update_user.email):
                user[user_id]["email"] = update_user.email
            else:
               raise HTTPException(status_code = 400, detail = 'Wrong email foramt.')

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
        raise HTTPException(status_code = 404, detail = 'User not exist.')
