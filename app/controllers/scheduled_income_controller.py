from ..models.scheduled_incomes import Scheduled_income 
from app import db

class ScheduledIncomeController:
    """
        Controlador de `Ingresos programados`.

        Permite realizar las funciones basicas(`borrar,actualizar,crear objetos`) del modelo ingresos programados.
    """

    @staticmethod
    def create_income(name,date,amount,user_id,description,next_income,categoria,account_id,received_amount:0,pending_amount:0):
        income                = Scheduled_income()
        income.income_name    = name
        income.income_date    = date
        income.amount         = amount
        income.description    = description
        income.next_income    = next_income
        income.pending_amount = pending_amount
        income.received_amount= received_amount
        income.category       = categoria
        income.user_id        = user_id
        income.account_id     = account_id
        db.session.add(income)
        db.session.commit()
        return income
    
    @staticmethod
    def delete_income(income:object):
        db.session.delete(income)
        db.session.commit()
        return  income
    
    @staticmethod
    def update_income(income:object):
        db.session.add(income)
        db.session.commit()

        