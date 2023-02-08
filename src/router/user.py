from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from ..models.vendor import VendorModel, SessionModel, DeletedVendorModel, CalorieTracker
from ..schemas.vendor import VendorSchema,UpdateVendorSchema,CalorieInfoInput
from ..database import get_db
import requests
import json
import datetime
time=datetime.datetime.now().time()
 

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth')
async def auth(request: Request, db: Session=Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user=db.query(VendorModel).filter(VendorModel.email==token.get('userinfo')['email']).first()
        if user is None:
            userinfo = token.get('userinfo')
            newUser = VendorModel()
            newUser.name = userinfo['name']
            newUser.email = userinfo['email']
            db.add(newUser)
            db.commit()
        loginSession = SessionModel()
        loginSession.sessionId = token.get('access_token')
        loginSession.email = token.get('userinfo')['email']
        db.add(loginSession)
        db.commit()
        response = RedirectResponse(url="http://localhost:3000/authredirect/vendor?token="+str(token.get('access_token')))
        return response
    except ValueError:
        raise HTTPException(status_code=498, detail=ValueError)

@router.get('/getuser')
async def auth(request: Request, db: Session=Depends(get_db)):
    token = request.headers["Authorization"]
    userResponse = db.query(SessionModel).filter(SessionModel.sessionId==token).first()
    email = userResponse.email
    if email:
        userInfo =db.query(VendorModel).filter(VendorModel.email==email).first()
        response = {
            "user": {
                'name':userInfo.name,
                'email':userInfo.email,
                'institute':userInfo.institute,
                'typeofvendor':userInfo.type
            }
        }
        print(response)
        return JSONResponse(status_code=200, content=response) 
    else:
        raise HTTPException(status_code=498, detail={'msg': 'Invalid Token'})

def convert(date_time):
    format ="%I:%M"
    date_time_str=datetime.datetime.strptime(date_time, format)
    return date_time_str

@router.post('/create')
def create_user(user: VendorSchema, db: Session=Depends(get_db)):
    
    user_model=db.query(VendorModel).filter(VendorModel.email==user.email).first()
    user_model.isApproved=False
    user_model.Phone=user.Phone
    user_model.institute=user.institute
    user_model.name=user.name
    user_model.Address_line_1=user.Address_line_1
    user_model.Address_line_2=user.Address_line_2
    user_model.City=user.City
    user_model.State=user.State
    user_model.Pincode=user.Pincode
    user_model.Country=user.Country
    user_model.mess_name=user.mess_name
    user_model.type=user.type
    user_model.starttime=user.starttime
    user_model.endtime=user.endtime
    start=datetime.time(int(user.starttime.split(':')[0]),int(user.starttime.split(':')[1]),0)
    end=datetime.time(int(user.endtime.split(':')[0]),int(user.endtime.split(':')[1]),0)
    if(start<=time<=end):
        user_model.status=True
    else:
        user_model.status=False
    print(user_model.status)
          
       

    db.add(user_model)
    db.commit()

    return user



@router.get("/isNewUser/{email_id}")
def isNewUser(email_id,db:Session=Depends(get_db)):

    user_model=db.query(VendorModel).filter(VendorModel.email==email_id).first()

    if user_model.Phone is None:
        return True
    return False


@router.get("/getVendorInfo/{email_id}")
def getVendorInfo(email_id,db:Session=Depends(get_db)):

    user_model=db.query(VendorModel).filter(VendorModel.email==email_id).first()
    print(user_model)
    return user_model
    


@router.get("/logout/{email_id}")
async def logout(email_id,db:Session=Depends(get_db)): 
    db.query(SessionModel).filter(SessionModel.email==email_id).delete()

    db.commit()

    return "user logged out successfully"

@router.get('/get-user-list')
def read_api(db: Session=Depends(get_db)):
    return db.query(VendorModel).filter(VendorModel.isApproved==False).all()

@router.get('/get-approved-user')
def read_api(db: Session=Depends(get_db)):
    return db.query(VendorModel).filter(VendorModel.isApproved==True).all()

@router.get('/approve/{email_id}')
def approve_user(email_id,db: Session=Depends(get_db)):
    user_model=db.query(VendorModel).filter(VendorModel.email==email_id).first()
    user_model.isApproved=True

    db.add(user_model)
    db.commit()
    # print(user_model)
    return user_model


@router.post("/updateVendorInfo")
async def update_user( user:UpdateVendorSchema,db:Session=Depends(get_db)):
    user_model=db.query(VendorModel).filter(VendorModel.email==user.email).first()

    if user_model is None:
        raise  HTTPException(
            status_code=404,
            detail=f"ID {user.email} : Does Not Exist"
        )


    # user_model.password = user.password
    
    user_model.Address_line_1=user.Address_line_1
    user_model.Address_line_2=user.Address_line_2
    user_model.City=user.City
    user_model.State=user.State
    user_model.Pincode=user.Pincode 
    user_model.mess_name=user.mess_name
    user_model.starttime=user.starttime
    user_model.endtime=user.endtime
  

    
    db.commit()

    return user







@router.get("/disapprove/{email_id}")
def dissaprove_user(email_id,db: Session=Depends(get_db)):
    user_model=db.query(VendorModel).filter(VendorModel.email==email_id).first()
    

    deleted_user=DeletedVendorModel()

    deleted_user.name=user_model.name
    deleted_user.Phone=user_model.Phone
    deleted_user.Pincode=user_model.Pincode
    deleted_user.mess_name=user_model.mess_name
    deleted_user.isApproved=False
    deleted_user.institute=user_model.institute
    deleted_user.email=user_model.email
    deleted_user.Country=user_model.Country
    deleted_user.City=user_model.City
    deleted_user.State=user_model.State
    deleted_user.Address_line_1=user_model.Address_line_1
    deleted_user.Address_line_2=user_model.Address_line_2

    db.add(deleted_user)  
    db.query(VendorModel).filter(VendorModel.email==email_id).delete()  
    db.commit()

    return "user dissaproved successfully"

@router.post("/calorietracker")
async def create_calorie_info(data : list [CalorieInfoInput], db: Session = Depends(get_db)):
    for item in data:
        items = item.items
        calories = item.calories
        db_record = CalorieTracker(items=items, calories=calories)
        db.add(db_record)
    db.commit()
    return {"item": items, "calorie": calories}

