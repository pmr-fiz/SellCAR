from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, DECIMAL,
    UniqueConstraint, TIMESTAMP, create_engine
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
import os

engine = create_engine('sqlite:///car_marketplace.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    phone = Column(String, nullable=False)
    avatar_url = Column(String)

    cars = relationship("Car", back_populates="user")
    sales_sold = relationship("Sale", foreign_keys="Sale.seller_id", back_populates="seller")
    sales_bought = relationship("Sale", foreign_keys="Sale.buyer_id", back_populates="buyer")


class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    country = Column(String)

    models = relationship("Model", back_populates="brand")
    cars = relationship("Car", back_populates="brand")


class Model(Base):
    __tablename__ = 'models'

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    name = Column(String, nullable=False)
    year_start = Column(Integer)
    year_end = Column(Integer)

    brand = relationship("Brand", back_populates="models")
    cars = relationship("Car", back_populates="model")


class Car(Base):
    __tablename__ = 'cars'

    car_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    model_id = Column(Integer, ForeignKey("models.model_id"))

    description = Column(Text)
    body_type = Column(String, nullable=False)
    color = Column(String, nullable=False)
    engine_displacement = Column(DECIMAL, nullable=False)
    engine_power = Column(DECIMAL, nullable=False)
    fuel_type = Column(String, nullable=False)
    mileage = Column(Integer, nullable=False)
    numberofDoors = Column(Integer)
    year = Column(Integer, nullable=False)
    vehicle_transmission = Column(String, nullable=False)
    owners = Column(Integer, nullable=False)
    drive_trains = Column(String, nullable=False)
    wheel = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    acceleration = Column(DECIMAL, nullable=False)
    fuel_rate = Column(DECIMAL, nullable=False)
    vin = Column(String, unique=True)
    state_number = Column(String)

    user = relationship("User", back_populates="cars")
    brand = relationship("Brand", back_populates="cars")
    model = relationship("Model", back_populates="cars")
    sale = relationship("Sale", back_populates="car", uselist=False)
    photos = relationship("Photo", back_populates="car")


class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("users.user_id"))
    buyer_id = Column(Integer, ForeignKey("users.user_id"))
    car_id = Column(Integer, ForeignKey("cars.car_id"), unique=True)
    sale_price = Column(DECIMAL)
    sale_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    seller = relationship("User", foreign_keys=[seller_id], back_populates="sales_sold")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="sales_bought")
    car = relationship("Car", back_populates="sale")


class Photo(Base):
    __tablename__ = 'photos'

    photo_id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("cars.car_id"))
    photo_url = Column(String, nullable=False)

    car = relationship("Car", back_populates="photos")


if __name__ == "__main__":
    current_dir = os.getcwd()
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы!")
    db_file = 'car_marketplace.db'
    if os.path.exists(db_file):
        file_size = os.path.getsize(db_file)
        print(f"Файл базы данных создан: {db_file}")
        print(f"Размер файла: {file_size} байт")
    else:
        print("Файл базы данных НЕ создан!")
    session.close()