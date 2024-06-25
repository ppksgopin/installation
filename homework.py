from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

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
    1:{"name": "Wanyu_Lee", "email": "Wanyu_Lee@pegatroncorp.com"},
    2:{"name": "Sandy1_Zeng", "email": "Sandy1_Zeng@pegatroncorp.com"}
}


@app.get("/getuser/{user_id}", status_code = status.HTTP_200_OK)
async def inspect_user_by_id(user_id: int = Path(gt = 0)):
    info_get = False
    for i in user:
        if i == user_id:
            return user[user_id]
            info_get = True
            break
    if not info_get:
        raise HTTPException(status_code = 404, detail = 'User not exist.')
    else:
        raise HTTPException(status_code = 400, detail = 'Please input user id.')

@app.post("/createuser", status_code = status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    new_user = Users(**user_request.model_dump())
    user[list(user)[-1] + 1] = new_user


@app.put("/updateuser/{user_id}", status_code = status.HTTP_200_OK)
async def update_user(update_user: UserRequest, user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code = 400, detail = 'Wrong input parameters.')
    else:
        info_changed = False
        for i in user:
            if i == user_id:
                user[i] = update_user
                info_changed = True
                break
        if not info_changed:
            raise HTTPException(status_code = 404, detail = 'User not exist.')


@app.delete("/deluser/{user_id}", status_code = status.HTTP_200_OK)
async def delete_user(user_id: int = Path(gt = 0) ):
    user_deleted = False
    for i in user:
        if i == user_id:
            del user[user_id]
            user_deleted = True
            break
    if not user_deleted:
        raise HTTPException(status_code = 404, detail = 'User not exist.')


