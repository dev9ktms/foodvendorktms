from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship,Mapped
from ..database import Base

class VendorModel(Base):
    __tablename__ = "vendor"

    name = Column(String)
    Phone = Column(Integer)
    institute=Column(String)
    email = Column(String,nullable=False,primary_key=True)
    Address_line_1=Column(String)
    Address_line_2=Column(String)
    City=Column(String)
    State=Column(String)
    Pincode=Column(Integer)
    Country=Column(String)
    mess_name=Column(String)
    isApproved = Column(Boolean)
    type= Column(String)
    status=Column(Boolean)
    starttime=Column(String)
    endtime=Column(String)
    menu: Mapped[list["MenuModel"]] = relationship("MenuModel",back_populates="vendor")



class DeletedVendorModel(Base):
    __tablename__ = "deleted_vendors"

    name = Column(String)
    Phone = Column(Integer)
    institute=Column(String)
    email = Column(String,nullable=False,primary_key=True)
    Address_line_1=Column(String)
    Address_line_2=Column(String)
    City=Column(String)
    State=Column(String)
    Pincode=Column(Integer)
    Country=Column(String)
    mess_name=Column(String)
    isApproved = Column(Boolean)

class MenuModel(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("vendor.email",ondelete="CASCADE"),nullable=False) 
    breakfast = Column(String)
    lunch = Column(String)
    snacks = Column(String)
    dinner = Column(Integer)
    date = Column(String)
    institute=Column(String)
    calories_breakfast=Column(String)
    calories_lunch=Column(String)
    calories_snacks=Column(String)
    calories_dinner=Column(String)
    mess_name=Column(String)

    vendor: Mapped["VendorModel"] = relationship("VendorModel",back_populates="menu")

class InternalVendorMenuModel(Base):
    __tablename__ = "internalvendormenu"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("vendor.email",ondelete="CASCADE"),nullable=False) 
    menu=Column(String)
    price=Column(String)
    institute=Column(String)
    mess_name=Column(String)
    
    
    

class SessionModel(Base):
    __tablename__="session"
    
    sessionId = Column(String, primary_key=True)
    email = Column(String)

class CancelledOrders(Base):
    __tablename__="cancelled_orders"
    id = Column(Integer,index=True, primary_key=True)
    email_of_consumer=Column(String)
    name_of_consumer=Column(String)
    vendor_email=Column(String)
    Address_line_1 = Column(String)
    Address_line_2 = Column(String)
    Phone = Column(Integer)
    date = Column(String)
    institute= Column(String)
    items=Column(String)
    quantities=Column(String)
    prices=Column(String)
    outlet_name=Column(String)

class DeliveredOrders(Base):
    __tablename__="delivered_orders"
    id = Column(Integer,index=True, primary_key=True)
    email_of_consumer=Column(String)
    name_of_consumer=Column(String)
    vendor_email=Column(String)
    Address_line_1 = Column(String)
    Address_line_2 = Column(String)
    Phone = Column(Integer)
    date = Column(String)
    institute= Column(String)
    items=Column(String)
    quantities=Column(String)
    prices=Column(String)
    outlet_name=Column(String)

class CalorieTracker(Base):
    __tablename__="calorie_info"
    id = Column(Integer,index=True, primary_key=True)
    items=Column(String)
    calories=Column(String) 



