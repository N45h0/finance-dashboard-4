from app import db 

class Loan(db.Model):
    """
        Objeto que representa el modelo `Prestamo`.

        Tiene las columnas con todos 
        datos necesarios que necesita
        el modelo: `id,precio,nombre,titular....`
    """
    
    __tablename__   = "loans"

    #columnas
    id              = db.Column(db.Integer,primary_key=True)
    loan_name       = db.Column(db.String(50),nullable=False)
    holder          = db.Column(db.String(50),nullable=False)
    price           = db.Column(db.Integer,nullable=False)
    description    = db.Column(db.String(160),nullable=True)
    date            = db.Column(db.Date(),nullable=False)
    quota           = db.Column(db.Integer,nullable=True)
    tea             = db.Column(db.Float,nullable=True)
    reamining_price = db.Column(db.Integer,nullable=False)
    user_id         = db.Column(db.Integer,db.ForeignKey("users.id",ondelete="CASCADE"))
    account_id      = db.Column(db.Integer,db.ForeignKey("accounts.id",ondelete="CASCADE"))
    expiration_date = db.Column(db.Date(),nullable=False)
    #relaciones
    loan_payments   = db.relationship("Loan_payment",back_populates="loan") 
    user            = db.relationship("User",back_populates="loans")     
    account         = db.relationship("Account",back_populates="accounts_loan")            

    #Funciones para obtener datos del modelo prestamo

    @staticmethod
    def get_all_by_userid(id:int):
        """
        Retorna todos los objetos del modelo Loan en una lista, relacionados con el `usuario activo actualmente `\n
        :Ejemplo:
        ```
            return [loan_object_1,loan_object_2]
        ```
        :Parametros: id
        :id: = identificador unico de usuario
        """


        all_loans = db.session.execute(db.select(Loan)).scalars()
        all_loans_list =[]
        for loan in all_loans:
            if loan.user_id ==id:
                all_loans_list.append(loan)
        return all_loans_list
    
    @staticmethod
    def get_all_amount_payment(id:int):
        """
        Retorna el pago en general realizado con los prestamos, relacionados con el `usuario activo actualmente`. \n
        :Ejemplo:
        ```
            return 345800
        ```
        :Parametros: id
        :id: = identificador unico de usuario
        """

        all_loans =db.session.execute(db.select(Loan)).scalars()
        all_loans_list =[]

        for loan in all_loans:
            if loan.user_id == id:
                all_loans_list.append(loan.price-loan.reamining_price)
        return sum(all_loans_list)

    @staticmethod
    def get_all_for_payment(id:int):
        """
        Retorna todos los prestamos disponibles para pagar relacionados con el `usuario activo actualmente`. \n
        :Ejemplo:
        ```
            return [loan_object_1,loan_object_2]
        ```
        :Parametros: id
        :id: = identificador unico de usuario
        """


        all_loans =db.session.execute(db.select(Loan)).scalars()
        all_loans_list =[]
        for loan in all_loans:
            if loan.user_id == id and loan.reamining_price>0:
                all_loans_list.append(loan)
        return all_loans_list
    
    @staticmethod 
    def get_full_amount():
        all_loans = db.session.execute(db.select(Loan)).scalars()
        amount = 0
        for loan in all_loans:
            amount+= loan.price
        return amount
    
    @staticmethod 
    def get_full_reamining_amount():
        all_loans = db.session.execute(db.select(Loan)).scalars()
        amount = 0
        for loan in all_loans:
            amount += loan.reamining_price
        return amount
    
    @staticmethod
    def get_by_id(id):
        """
        Retorna el objeto del modelo `prestamo` que coincida con el `id` proporcionado. \n
        :Ejemplo:
        ```
            return loan_object_22
        ```
        :Parametros: id
        :id: = identificador unico de prestamo
        """


        loan =Loan.query.filter_by(id=id).first()
        return loan
    
    
    @staticmethod
    def get_all_for_account(id:int,account_list:list):
        """   
        Retorna los objetos del modelo `prestamos` dividido en las distintas `cuentas`. \n
        :Ejemplo:
        ```
            return [
                [loan_object_1,loan_object_5],
                [loan_object_2,loan_object_12],
                [loan_object_4]
            ]
            #Cada fila de la matriz representa una cuenta y dentro de las distintas filas,estan los prestamos relacionados con esa cuenta.
        ```
        :Parametros: id,account_list
        :id: = identificador unico de usuario.
        :account_list: = lista de cuentas que tiene el usuario.
        """


        all_loans = Loan().get_all_by_userid(id)
        all_accounts = [[] for account in account_list]
        for loan in all_loans:
            for account in account_list:
                print(account.id)
                if loan.account_id == account.id:
                    all_accounts[account_list.index(account)].append(loan)
        return all_accounts
       
    @staticmethod
    def get_loan_summary(id):
        """
        Retorna un resumen financiero de todos los prestamos relacionados con el `usuario activo actualmente` y lo retorna en un diccionario.\n

        :Ejemplo:
        ```
            return {"monto_total":500000,"monto_pagado":10000,"monto_restante":490000,"progreso":2}
            #progreso=porcentaje
        ```
        :Parametros: id
        :id: = identificador unico de usuario
        """


        all_loans        = db.session.execute(db.select(Loan)).scalars()
        all_amount       = 0
        payment_amount   = 0
        reamining_amount = 0
        progress         = 0
        print(all_loans)    
        for loan in all_loans:
            if loan.user_id ==id:
                all_amount += loan.price
                reamining_amount += loan.reamining_price
        if all_amount==0:
            return {"monto_total":0,"monto_pagado":0,"monto_restante":0,"progreso":0}
        else:
            payment_amount = all_amount - reamining_amount
            progress = (payment_amount*100)/all_amount
            return {"monto_total":all_amount,"monto_pagado":payment_amount,"monto_restante":reamining_amount,"progreso":progress}
