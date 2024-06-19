from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import engine, Client, Payment, ClientPaymentRelation

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

class RelationService:
    @staticmethod
    def update_client_payment_relations(session):
        # Получаем всех клиентов из базы данных
        clients = session.query(Client).all()

        for client in clients:
            try:
                # Идентификаторы существующих связей клиент-платеж для данного клиента
                existing_payment_ids = {relation.payment_id for relation in client.client_payment_relations}
                print(f"Existing Payment IDs for Client ID {client.id}: {existing_payment_ids}")

                # Обновляем связи
                for payment in client.payments:
                    payment_id = payment.id
                    # Добавляем связь, если она отсутствует
                    if payment_id not in existing_payment_ids:
                        new_relation = ClientPaymentRelation(client_id=client.id, payment_id=payment_id)
                        session.add(new_relation)

                # Удаляем связи, если payment_id не найден
                for relation in client.client_payment_relations.copy():
                    if relation.payment_id not in [payment.id for payment in client.payments]:
                        session.delete(relation)

            except AttributeError:
                print(f"У клиента с ID {client.id} пока нет платежей, связи не требуют обновления.")

        session.commit()


class ClientService:
    def create_client(self):
        name = input("Введите имя клиента: ")
        email = input("Введите email клиента: ")

        new_client = Client(name=name, email=email)
        session.add(new_client)
        session.commit()
        RelationService.update_client_payment_relations()

    def edit_client(self):
        client_id = input("Введите ID клиента для редактирования: ")
        client = session.query(Client).filter(Client.id == client_id).first()
        if client:
            new_name = input("Введите новое имя клиента: ")
            new_email = input("Введите новый email клиента: ")

            client.name = new_name
            client.email = new_email
            session.commit()
            RelationService.update_client_payment_relations()
        else:
            print(f"Клиент с ID {client_id} не найден.")

    def delete_client(self):
        client_id = input("Введите ID клиента для удаления: ")
        client = session.query(Client).filter(Client.id == client_id).first()
        if client:
            session.delete(client)
            session.commit()
            RelationService.update_client_payment_relations()
            print(f"Клиент с ID {client_id} успешно удален.")
        else:
            print(f"Клиент с ID {client_id} не найден.")


# Пример использования
service = ClientService()
service.create_client()
service.edit_client()
service.delete_client()

class PaymentService:
    def create_payment(self):
        amount = float(input("Введите сумму платежа: "))
        date = input("Введите дату платежа (гггг-мм-дд): ")

        # Создаем новый платеж
        new_payment = Payment(amount=amount, date=date)
        session.add(new_payment)
        session.commit()
        RelationService.update_client_payment_relations()

    def edit_payment(self):
        payment_id = int(input("Введите ID платежа для редактирования: "))
        new_amount = float(input("Введите новую сумму платежа: "))
        new_date = input("Введите новую дату платежа (гггг-мм-дд): ")

        # Изменяем данные платежа
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            payment.amount = new_amount
            payment.date = new_date
            session.commit()
            RelationService.update_client_payment_relations()

    def delete_payment(self):
        payment_id = int(input("Введите ID платежа для удаления: "))

        # Удаляем платеж
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            session.delete(payment)
            session.commit()
            RelationService.update_client_payment_relations()
            
# Пример использования
service = PaymentService()
service.create_payment()
service.edit_payment()
service.delete_payment()
