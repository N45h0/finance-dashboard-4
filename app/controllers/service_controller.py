from ..models.service import  Service
from app import db

class ServiceController:
    """
        Controlador de `Servicios`.

        Permite realizar las funciones basicas(`borrar,actualizar,crear objetos`) del modelo servicios.
    """

    @staticmethod
    def create_service(name,description,date,category,user_id,price,reamingin_price,account,expiration):
        service                 = Service()
        service.service_name    = name
        service.description     = description
        service.date            = date
        service.category        = category
        service.user_id         = user_id
        service.reamining_price = reamingin_price
        service.price           = price 
        service.account_id      = account
        service.expiration_date = expiration
        db.session.add(service)
        db.session.commit()
        return service
    
    @staticmethod
    def delete_service(service:object):
        db.session.delete(service)
        db.session.commit()
        return  service
    
    @staticmethod
    def update_service(service:object):
        db.session.add(service)
        db.session.commit()