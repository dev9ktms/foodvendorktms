from pydantic import BaseModel, Field

class VendorSchema(BaseModel):
    institute: str = Field()
    Phone: int = Field()
    email: str = Field(min_length=1)
    name: str = Field()
    Address_line_1: str = Field()
    Address_line_2: str = Field()
    City: str = Field()
    State: str = Field()
    Pincode: int = Field() 
    Country: str = Field()
    mess_name: str = Field()
    type:str=Field()
    starttime: str = Field()
    endtime: str = Field()


class MenuSchema(BaseModel):
    user_id: str = Field()
    date: str= Field(min_length=1)
    type: str= Field(min_length=1)
    items: list= Field()
    # institute: str= Field()

class UpdateVendorSchema(BaseModel):
    email: str = Field(min_length=1)
    mess_name:str=Field()
    Address_line_1: str = Field()
    Address_line_2: str = Field()
    City: str = Field()
    State: str = Field()
    Pincode: int = Field()
    starttime:str = Field()
    endtime:str = Field()
    
class InternalVendorMenuSchema(BaseModel):
    user_id: str = Field()
    items: list= Field()
    prices:list=Field()

class DeliveredOrderInternalVendorSchema(BaseModel):
    email_of_consumer: str = Field()
    name_of_consumer: str = Field()
    vendor_email: str = Field()
    Address_line_1 : str = Field()
    Address_line_2: str = Field()
    Phone : int = Field()
    date  : str = Field()
    institute: str = Field()
    items:str=Field()
    quantities:str=Field()
    price:str=Field()
 

class CancelledOrderInternalVendorSchema(BaseModel):
    email_of_consumer: str = Field()
    name_of_consumer: str = Field()
    vendor_email: str = Field()
    Address_line_1 : str = Field()
    Address_line_2: str = Field()
    Phone : int = Field()
    date  : str = Field()
    institute: str = Field()
    items:str=Field()
    quantities:str=Field()
    price:str=Field()
 
class CalorieInfoInput(BaseModel):
    items:str=Field()
    calories:str=Field()   



