# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, DateTime, Column


db = SQLAlchemy()
Base = db.Model


class Order(Base):
    __tablename__ = 't_order'
    __table_args__ = {'schema': 'core'}

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    cost = Column(Integer)
    shipping_date = Column(DateTime)
    amount = Column(Integer)

