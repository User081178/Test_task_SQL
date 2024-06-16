import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = sqlalchemy.orm.declarative_base()


# Класс для описания таблицы клиентов
class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


# Класс для описания таблицы платежей
class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    date = Column(Date)


# Класс для описания промежуточной таблицы для связи клиентов и платежей
class ClientPaymentRelation(Base):
    __tablename__ = 'client_payment_relations'

    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
    payment_id = Column(Integer, ForeignKey('payments.id'), primary_key=True)

    client = relationship("Client")
    payment = relationship("Payment")


# Создание соединения с базой данных MySQL
 engine = create_engine('mysql://Sokov:Base081178@localhost/testdb')
 Base.metadata.create_all(engine)
