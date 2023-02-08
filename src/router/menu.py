from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from ..models.vendor import MenuModel,VendorModel,InternalVendorMenuModel,DeliveredOrders,CancelledOrders
from ..database import get_db
from ..schemas.vendor import VendorSchema, MenuSchema,InternalVendorMenuSchema,CancelledOrderInternalVendorSchema,DeliveredOrderInternalVendorSchema
import requests
import json
from datetime import date
from pydantic import BaseModel
import pandas as pd
from io import BytesIO
from databases import Database
import sqlite3
import datetime
time=datetime.datetime.now().time()

con= sqlite3.connect("../students.db")
cur=con.cursor()

database=Database("sqlite:///../students.db")

class ExcelFile(BaseModel):
    file: UploadFile 

router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

@router.post('/upload-excel-for-internalvendor/{email}')
def upload_excel(email:str,file:UploadFile=File(...),db: Session=Depends(get_db)):
  internalvendor=db.query(VendorModel).filter(VendorModel.email == email).first()
  contents=file.file.read()
  exceldata=BytesIO(contents)
  df=pd.read_excel(exceldata)
  print(df)

  items=df['Item']
  prices=df['Price']
  menuIsPresent = db.query(InternalVendorMenuModel).filter(InternalVendorMenuModel.user_id==email).first()
  if menuIsPresent:
    food=''
    Foodprice=''
    for i in range(len(items)) :
        food+=items[i]+'_'
        Foodprice+=str(prices[i])+'_'

    menuIsPresent.menu+=food
    menuIsPresent.price+=Foodprice


  else:
      new_menu = InternalVendorMenuModel()
      data=db.query(VendorModel).filter(email==VendorModel.email).first()
      new_menu.institute=data.institute
      new_menu.mess_name=data.mess_name
      print(data.institute)
      new_menu.user_id=email
      food=''
      Foodprice=''
      

      for i in range(len(items)) :
        food+=items[i]+'_'
        Foodprice+=str(prices[i])+'_'
            
      new_menu.menu=food
      new_menu.price=Foodprice
      
      db.add(new_menu) 

  db.commit()
  print(food)
  return "New Menu Added Successfully!"
  



@router.post('/upload-excell-data/{email_id}')
def create_upload_file(file: UploadFile=File(...),email_id=str, db: Session=Depends(get_db)):
    vendor=db.query(VendorModel).filter(VendorModel.email == email_id).first()
    contents=file.file.read()
    data=BytesIO(contents)
    df=pd.read_excel(data)

    data=df.iloc[0]
    dates=[]
    for i in range(len(data)):
      y=str(data[i])
      x=y.split(' ')[0]
      dates.append(x)
    print(dates)

    for i in range(len(dates)):
      breakfast_items=df.iloc[2:12,i].dropna().values
      lunch_items=df.iloc[13:23,i].dropna().values
      snacks_items=[]
      dinner_items=df.iloc[24:,i].dropna().values
      new_menu = MenuModel()
      # data=db.query(VendorModel).filter(menu.user_id==VendorModel.email).first()
      new_menu.institute=vendor.institute
      new_menu.mess_name=vendor.mess_name
      # print(data.institute)
      new_menu.user_id=email_id
      new_menu.date=dates[i]
      breakfast_food=''
      total_cal=0
      for item in breakfast_items:
        breakfast_food+=item+'_'
        # query = item
        # api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        # response = requests.get(api_url, headers={'X-Api-Key': 'XkZDyixDwhFKHMpODT6I9g==4UK7nf1dFBH3sNK7'})
        # if response.status_code == requests.codes.ok:
        #     total_cal+=(response.json())[0]['calories']
        # else:
        #     print("Error:", response.status_code, response.text)
      # if menu.type == "Breakfast":
      new_menu.breakfast=breakfast_food
      new_menu.calories_breakfast=total_cal

      lunch_food=''
      total_cal=0
      for item in lunch_items:
        lunch_food+=item+'_'
        # query = item
        # api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        # response = requests.get(api_url, headers={'X-Api-Key': 'XkZDyixDwhFKHMpODT6I9g==4UK7nf1dFBH3sNK7'})
        # if response.status_code == requests.codes.ok:
        #     total_cal+=(response.json())[0]['calories']
        # else:
        #     print("Error:", response.status_code, response.text)
      # if menu.type == "Breakfast":
      new_menu.lunch=lunch_food
      new_menu.calories_lunch=total_cal

      dinner_food=''
      total_cal=0
      for item in dinner_items:
        dinner_food+=item+'_'
        # query = item
        # api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        # response = requests.get(api_url, headers={'X-Api-Key': 'XkZDyixDwhFKHMpODT6I9g==4UK7nf1dFBH3sNK7'})
        # if response.status_code == requests.codes.ok:
        #     total_cal+=(response.json())[0]['calories']
        # else:
        #     print("Error:", response.status_code, response.text)
      # if menu.type == "Breakfast":
      new_menu.dinner=dinner_food
      new_menu.calories_dinner=total_cal

      
      db.add(new_menu)

   
    db.commit()
    # print(food)
    # return "New Menu Added Successfully!"
      # print(dinner_items)
    # use the openpyxl library to open the uploaded Excel file
    # wb = openpyxl.load_workbook(file.file[1])
    # do something with the Excel file here
    return {"filename": file.filename}

@router.get('/get-menu-for-vendor/{email}/{date_}')
async def getMenuforVendor(email:str,date_:str, db: Session=Depends(get_db)):
    
    menu = db.query(MenuModel).filter(MenuModel.user_id==email,MenuModel.date==date_).first()
    if menu:
       print(date_,menu.date)
       return menu
    return "No data available"

@router.post('/create-menu-for-vendor')
def createMenuforVendor(menu:MenuSchema, db: Session=Depends(get_db)):
    menuIsPresent = db.query(MenuModel).filter(MenuModel.user_id==menu.user_id,MenuModel.date==menu.date).first()
    
    if menuIsPresent:
        food=''
        total_cal=0
        for item in menu.items:
          food+=item+'_'
          query = item
          api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
          response = requests.get(api_url, headers={'X-Api-Key': 'XkZDyixDwhFKHMpODT6I9g==4UK7nf1dFBH3sNK7'})
          if response.status_code == requests.codes.ok:
              total_cal+=(response.json())[0]['calories']
          else:
              print("Error:", response.status_code, response.text)

        if menu.type == "Breakfast":
          menuIsPresent.breakfast=food
          menuIsPresent.calories_breakfast=total_cal
        elif menu.type == "Lunch":
          menuIsPresent.lunch=food
          menuIsPresent.calories_lunch=total_cal
        elif menu.type == "Snacks":
          menuIsPresent.snacks=food
          menuIsPresent.calories_snacks=total_cal
        elif menu.type == "Dinner":
          menuIsPresent.dinner=food
          menuIsPresent.calories_dinner=total_cal
        print(total_cal)
    
    else:
      new_menu = MenuModel()
      data=db.query(VendorModel).filter(menu.user_id==VendorModel.email).first()
      new_menu.institute=data.institute
      new_menu.mess_name=data.mess_name
      print(data.institute)
      new_menu.user_id=menu.user_id
      new_menu.date=menu.date
      food=''
      total_cal=0
      for item in menu.items:
        food+=item+'_'
        query = item
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'XkZDyixDwhFKHMpODT6I9g==4UK7nf1dFBH3sNK7'})
        if response.status_code == requests.codes.ok:
            total_cal+=(response.json())[0]['calories']
        else:
            print("Error:", response.status_code, response.text)
      if menu.type == "Breakfast":
        new_menu.breakfast=food
        new_menu.calories_breakfast=total_cal
      elif menu.type == "Lunch":
        new_menu.lunch=food
        new_menu.calories_lunch=total_cal
      elif menu.type == "Snacks":
        new_menu.snacks=food
        new_menu.calories_snacks=total_cal
      elif menu.type == "Dinner":
        new_menu.dinner=food
        new_menu.calories_dinner=total_cal
      print(total_cal)
      db.add(new_menu)

   
    db.commit()
    print(food)
    return "New Menu Added Successfully!"


@router.post('/create-menu-for-internalvendor')
def createMenuforInternalVendor(menu:InternalVendorMenuSchema, db: Session=Depends(get_db)):
   menuIsPresent = db.query(InternalVendorMenuModel).filter(InternalVendorMenuModel.user_id==menu.user_id).first()
   if menuIsPresent:
    food=''
    Foodprice=''
    for i in range(len(menu.items)) :
        food+=menu.items[i]+'_'
        Foodprice+=str(menu.prices[i])+'_'

    menuIsPresent.menu+=food
    menuIsPresent.price+=Foodprice


   else:
      new_menu = InternalVendorMenuModel()
      data=db.query(VendorModel).filter(menu.user_id==VendorModel.email).first()
      new_menu.institute=data.institute
      new_menu.mess_name=data.mess_name
      new_menu.status=True
      print(data.institute)
      new_menu.user_id=menu.user_id
      food=''
      Foodprice=''
      

      for i in range(len(menu.items)) :
        food+=menu.items[i]+'_'
        Foodprice+=str(menu.prices[i])+'_'
            
      new_menu.menu=food
      new_menu.price=Foodprice
      
      db.add(new_menu) 

   db.commit()
   print(food)
   return "New Menu Added Successfully!"

@router.get('/get-menu-for-internalvendor/{email}')
def get_menu_for_internal_vendor(email:str,db: Session=Depends(get_db)):
  data={"items":"","prices":""}
  items=db.query(InternalVendorMenuModel).filter(InternalVendorMenuModel.user_id==email).first()
  if items:
   data["items"]=items.menu
   data["prices"]=items.price

  return data

@router.get('/delete-menu-for-internalvendor/{email}')
def get_menu_for_internal_vendor(email:str,db: Session=Depends(get_db)):
  items=db.query(InternalVendorMenuModel).filter(InternalVendorMenuModel.user_id==email).first()
  if items:
   db.query(InternalVendorMenuModel).filter(InternalVendorMenuModel.user_id==email).delete()
  db.commit()

  return "Menu Deleted Successfully"

@router.put('/update-menu-for-vendor')
def updateMenuforVendor(menu:MenuSchema, db: Session=Depends(get_db)):
  menuIsPresent = db.query(MenuModel).filter(MenuModel.user_id==menu.user_id,MenuModel.date==menu.date).first()
  if menuIsPresent:
      food=''
      total_cal=0
      for item in menu.items:
        query = item
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'XkZDyixDwhFKHMpODT6I9g==4UK7nf1dFBH3sNK7'})
        if response.status_code == requests.codes.ok:
            total_cal+=(response.json())[0]['calories']
        else:
            print("Error:", response.status_code, response.text)

        food+=item+'_'
      if menu.type == "Breakfast":
        menuIsPresent.breakfast +=food
      elif menu.type == "Lunch":
        menuIsPresent.lunch +=food
      elif menu.type == "Dinner":
        menuIsPresent.dinner +=food
  
  else:
    new_menu = MenuModel()
    new_menu.user_id=menu.user_id
    new_menu.date=menu.date
    food=''
    for item in menu.items:
      food+=item+'_'
    if menu.type == "Breakfast":
      new_menu.breakfast=food
    elif menu.type == "Lunch":
      new_menu.lunch=food
    elif menu.type == "Dinner":
      new_menu.dinner=food
    db.add(new_menu)

  
  db.commit()
  # print(food)
  return "Menu Updated Successfully!"

@router.get('/get-menu-for-day/{date}/{institute}')
async def getMenuforDay(date:str,institute:str,db: Session=Depends(get_db)):
    

    isApproved = db.query(VendorModel).filter(VendorModel.isApproved == True).all()
    
    
    menuList = []
    if(isApproved):
      for i in range(len(isApproved)):
        if isApproved[i].isApproved == True:
          menu = db.query(MenuModel).filter(MenuModel.institute==institute,MenuModel.date==date,isApproved[i].email==MenuModel.user_id).all()
          menuList.append(menu[0])
          
    print(menuList)
    # return JSONResponse(status_code=200, content={'msg':'menu send sucessfully'})
    return menuList

@router.get('/get-order-list/{date}/{institute}/{email}')
async def get_order_list(date:str, institute:str, email:str,db:Session=Depends(get_db)):
    # query1="SELECT * FROM vendor WHERE isApproved={}".format(True)

    # isApproved = await  database.fetch_all(query=query1)
    # insti="'{}'".format(institute)
    # # print(isApproved[0].email=="dev1@ktms.in")
    orderList = []
    # if(isApproved):
    #   for i in range(len(isApproved)):
    #     if isApproved[i].isApproved == True:
    email="'{}'".format(email)
    date="'{}'".format(date)
    institute="'{}'".format(institute)
    query2="SELECT * FROM studentorders_internalvendor WHERE institute=="+institute+" AND date=="+date
    print(query2)
    menu=cur.execute(query2).fetchall()
      #   print(menu[0][12])
        
    if menu:
     for i in range(len(menu)):
      data={}
      data["name"]=menu[i][1]
      data["address_line_1"]=menu[i][2]
      data["address_line_2"]=menu[i][3]
      data["Phone"]=menu[i][4]
      data["email"]=menu[i][6]
      data["items"]=menu[i][8]
      data["quantities"]=menu[i][9]
      data["prices"]=menu[i][10]
      orderList.append(data)
        
    # print(menu)
    return orderList

@router.get('/internalvendor-status/{email}/{status}')
async def internalvendorStatus(email:str,status:str,db:Session=Depends(get_db)):
  vendor=db.query(VendorModel).filter(VendorModel.email==email).first()
  
  # print(status)
  if status=="True" or status==True or status=='true':
   vendor.status=True
  else:
    vendor.status=False

  db.commit()
  return "Status updated successfully"

@router.get('/get-internalvendor-status/{email}')
async def internalvendorStatus(email:str,db:Session=Depends(get_db)):
  vendor=db.query(VendorModel).filter(VendorModel.email==email).first()
  start=datetime.time(int(vendor.starttime.split(':')[0]),int(vendor.starttime.split(':')[1]),0)
  end=datetime.time(int(vendor.endtime.split(':')[0]),int(vendor.endtime.split(':')[1]),0)
  if(start<=time<=end):
      vendor.status=True
  else:
      vendor.status=False
  db.commit()

  print(vendor.status)
  if start<=time<=end:
   return True
  else:
    return False


@router.post('/post-delivered-order-internalvendor')
async def post_deleted_order(order:DeliveredOrderInternalVendorSchema,db:Session=Depends(get_db)):
  vendor=db.query(VendorModel).filter(VendorModel.email==order.vendor_email).first()
  print(vendor)
  email="'{}'".format(order.email_of_consumer)
  date="'{}'".format(order.date)
  institute="'{}'".format(order.institute)
  query2="DELETE FROM studentorders_internalvendor WHERE institute=="+institute+" AND date=="+date+" AND email=="+email
  cur.execute(query2)
  con.commit()
  data=DeliveredOrders()
  data.email_of_consumer=order.email_of_consumer
  data.name_of_consumer=order.name_of_consumer
  data.vendor_email=order.vendor_email
  data.Address_line_1 = order.Address_line_1
  data.Address_line_2 = order.Address_line_2
  data.Phone = order.Phone
  data.date = order.date
  data.institute= order.institute
  data.items=order.items
  data.quantities=order.quantities
  data.prices=order.price
  data.outlet_name=vendor.mess_name

  db.add(data)
  db.commit()

  return "Data Added successfully"

@router.post('/post-cancelled-order-internalvendor')
async def post_deleted_order(order:CancelledOrderInternalVendorSchema,db:Session=Depends(get_db)):
  vendor=db.query(VendorModel).filter(VendorModel.email==order.vendor_email).first()
  email="'{}'".format(order.email_of_consumer)
  date="'{}'".format(order.date)
  institute="'{}'".format(order.institute)
  query2="DELETE FROM studentorders_internalvendor WHERE institute=="+institute+" AND date=="+date+" AND email=="+email
  cur.execute(query2)
  con.commit()
  # order=db.query(InternalVendorMenuModel)
  data=CancelledOrders()
  data.email_of_consumer=order.email_of_consumer
  data.name_of_consumer=order.name_of_consumer
  data.vendor_email=order.vendor_email
  data.Address_line_1 = order.Address_line_1
  data.Address_line_2 = order.Address_line_2
  data.Phone = order.Phone
  data.date = order.date
  data.institute= order.institute
  data.items=order.items
  data.quantities=order.quantities
  data.prices=order.price
  data.outlet_name=vendor.mess_name

  db.add(data)
  db.commit()

  return "Data Added successfully"


@router.get('/is-item-exists/{item}')
async def is_item_exists(item:str):
  item="'{}'".format(item)
  query2="SELECT * FROM itemstable WHERE item=="+item
  data=cur.execute(query2).fetchone()

  if data:
    return True
  else:
    return False

