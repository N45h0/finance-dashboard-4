from ..models.account import  Account
from app import db

class AccountController:
    """
        Controlador de `Cuentas`.

        Permite realizar las funciones basicas(`borrar,actualizar,crear objetos`) del modelo cuentas.
    """
    
    @staticmethod
    def create_account(name,card,user_id,saldo):
        account              = Account()
        account.account_name = name
        account.card         = card
        account.user_id      = user_id
        account.balance      = saldo
        db.session.add(account)
        db.session.commit()
        return account
    
    @staticmethod
    def delete_account(account:object):
        db.session.delete(account)
        db.session.commit()
        return  account
    
    @staticmethod
    def update_account(account:object):
        db.session.add(account)
        db.session.commit()

        
