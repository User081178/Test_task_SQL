from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import engine, Client, Payment, ClientPaymentRelation

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

class RelationService:
    @staticmethod
    def update_client_payment_relations():
        # Получаем всех клиентов из базы данных
        clients = session.query(Client).all()

        for client in clients:
            # Идентификаторы всех платежей клиента
            payment_ids = [payment.id for payment in client.payments]

            # Идентификаторы существующих связей клиент-платеж
            existing_payment_ids = {relation.payment_id for relation in client.client_payment_relations}
            payment_ids_set = set(payment_ids)

            # Добавляем новые связи
            for payment_id in payment_ids_set - existing_payment_ids:
                new_relation = ClientPaymentRelation(client_id=client.id, payment_id=payment_id)
                session.add(new_relation)

            # Удаляем лишние связи
            for payment_id in existing_payment_ids - payment_ids_set:
                relation_to_delete = session.query(ClientPaymentRelation).filter_by(client_id=client.id, payment_id=payment_id).first()
                session.delete(relation_to_delete)

        session.commit()

class ClientService:
    def create_client(self, name, email):
        # Создаем нового клиента
        new_client = Client(name=name, email=email)
        session.add(new_client)
        session.commit()
        RelationService.update_client_payment_relations()

    def edit_client(self, client_id, new_name, new_email):
        # Изменяем данные клиента
        client = session.query(Client).filter(Client.id == client_id).first()
        if client:
            client.name = new_name
            client.email = new_email
            session.commit()
            RelationService.update_client_payment_relations()

    def delete_client(self, client_id):
        # Удаляем клиента
        client = session.query(Client).filter(Client.id == client_id).first()
        if client:
            session.delete(client)
            session.commit()
            RelationService.update_client_payment_relations()

class PaymentService:
    def create_payment(self, amount, date):
        # Создаем новый платеж
        new_payment = Payment(amount=amount, date=date)
        session.add(new_payment)
        session.commit()
        RelationService.update_client_payment_relations()

    def edit_payment(self, payment_id, new_amount, new_date):
        # Изменяем данные платежа
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            payment.amount = new_amount
            payment.date = new_date
            session.commit()
            RelationService.update_client_payment_relations()

    def delete_payment(self, payment_id):
        # Удаляем платеж
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            session.delete(payment)
            session.commit()
            RelationService.update_client_payment_relations()