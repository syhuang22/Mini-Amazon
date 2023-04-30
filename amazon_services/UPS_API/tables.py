from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db_url = "postgresql://postgres:passw0rd@127.0.0.1:5432/amazon2"

class Commodity(Base):
    __tablename__ = 'amazon_commodity'
    commodity_id = Column(Integer, primary_key=True)
    description = Column(Text)
    count = Column(Integer)

class Product(Base):
    __tablename__ = 'amazon_product'
    product_id = Column(Integer, primary_key=True)
    description = Column(Text)

class Warehouse(Base):
    __tablename__ = 'amazon_warehouse'
    warehouse_id = Column(Integer, primary_key=True)
    location_x = Column(Integer)
    location_y = Column(Integer)
    
class Package(Base):
    __tablename__ = 'amazon_package'
    package_id = Column(Integer, primary_key=True)
    destination_x = Column(Integer)
    destination_y = Column(Integer)
    user_id = Column(Integer, nullable=True)
    status = Column(Text, default='purchase')
    truck_id = Column(Integer, default=0)
'''
class Order(Base):
    __tablename__ = 'amazon_order'
    order_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('amazon_product.product_id'))
    quantity = Column(Integer)
    warehouse_id = Column(Integer, ForeignKey('amazon_warehouse.warehouse_id'))
    package_id = Column(Integer, ForeignKey('amazon_package.package_id'))
'''

class Order(Base):
    __tablename__ = 'amazon_order'
    order_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('amazon_product.product_id'))
    product = relationship('Product')
    quantity = Column(Integer)
    warehouse_id = Column(Integer, ForeignKey('amazon_warehouse.warehouse_id'))
    warehouse = relationship('Warehouse')
    package_id = Column(Integer, ForeignKey('amazon_package.package_id'))
    package = relationship('Package')

class Request(Base):
    __tablename__ = 'amazon_request'
    request_id = Column(Integer, primary_key=True)
    type = Column(Text, default='purchase')
    status = Column(Text, default='open')
    pk_id = Column(Integer, ForeignKey('amazon_package.package_id'))
    package = relationship('Package')

    