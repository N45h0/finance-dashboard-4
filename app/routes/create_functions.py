"""
Funciones de creacion
"""



#modulos externos
from flask                                import Blueprint,render_template,redirect,request,flash
from flask_login                          import current_user,login_required
from datetime import datetime
#modulos propios
from app.forms.importaciones              import FormularioCrearPrestamos,FormularioCrearPagoServicio,FormularioCrearPagoPrestamo,FormularioCrearServicio,FormularioCrearCuenta,FormularioCrearIngresoProgamado,FormularioCrearIngreso
from app.controllers.importaciones        import AccountController,IncomeController,UserController,ServiceController,LoanController,LoanPaymentController,ServicePaymentController,ScheduledIncomeController
from app.models.importaciones             import Account,User,Service,Loan,Loan_payment
from ..extra_functions.email_decorator    import email_validation
from ..extra_functions.calcular_tem       import calcular_tem

create_functions_bp = Blueprint('create_functions', __name__)


@create_functions_bp.route("/crearcuenta",methods=["GET","POST"])
@login_required
@email_validation
def crear_cuenta():
    if request.method =="GET":
        form = FormularioCrearCuenta()
        return render_template("create_functions/crear_cuenta.html",form=form)
    
    if request.method == "POST":
        form = FormularioCrearCuenta()
        if form.validate_on_submit():
            #despues de validar creamos el objeto cuenta para bd
            nombre  = form.nombre.data
            tarjeta = form.tarjeta.data
            saldo   = form.saldo.data

            #actualizamos saldo del usuario 
            user = User().get_by_id(current_user.id)
            user.balance = (user.balance or 0) + saldo

            AccountController().create_account(nombre,tarjeta,current_user.id,saldo)
            flash("¡Cuenta creada exitosamente!", "success")
            return redirect("/vercuentas")
        else:
            return "false"
    flash("Ocurrió un error al crear la cuenta. Intenta nuevamente.")
    return redirect(request.url)

@create_functions_bp.route("/crearingreso",methods=["GET","POST"])
@login_required
@email_validation
def crear_ingreso():
    if request.method =="GET":
        form = FormularioCrearIngreso()
        return render_template("create_functions/crear_ingreso.html",form=form)
    
    if request.method == "POST":
        form = FormularioCrearIngreso()
        if form.validate_on_submit():

            #despues de validar creamos el objeto ingreso para bd
            nombre          = form.nombre.data
            fecha           = form.fecha_pago.data
            descripcion     = form.descripcion.data
            categoria       = form.categoria.data
            monto           = form.monto.data
            cuenta_valor    = request.form.get("cuenta")
            if cuenta_valor is None:
                flash("Debes seleccionar una cuenta para el ingreso.", "error")
                return redirect(request.url)
            try:
                account_id = int(cuenta_valor)
            except ValueError:
                flash("Cuenta inválida.", "error")
                return redirect(request.url)
            IncomeController().create_income(nombre,fecha,monto,current_user.id,descripcion,categoria,account_id)

            #actualizamos el saldo total del usuario
            usuario         = User().get_by_id(current_user.id)
            usuario.balance = (usuario.balance or 0) + monto
            UserController().update_user(usuario)
            #actualizamos el saldo de la cuenta 
            account         = Account().get_by_id(account_id)
            account.balance = (account.balance or 0) + monto
            AccountController().update_account(account)
            flash("¡Ingreso registrado exitosamente!", "success")
            return redirect("/veringresos")
        else:
            flash("Ocurrió un error al validar el formulario.", "error")
            return redirect(request.url)
    flash("Ocurrió un error al crear el ingreso. Intenta nuevamente.")
    return redirect(request.url)


@create_functions_bp.route("/crearingresoprogramado",methods=["GET","POST"])
@login_required
@email_validation
def crear_ingreso_programado():
    if request.method =="GET":
        form = FormularioCrearIngresoProgamado()
        return render_template("create_functions/crear_ingreso_programado.html",form=form)
    
    if request.method == "POST":
        form = FormularioCrearIngresoProgamado()
        if form.validate_on_submit():
            #despues de validar creamos el objeto ingreso programado para bd
            nombre          = form.nombre.data
            fecha           = datetime.now()
            descripcion     = form.descripcion.data
            categoria       = form.categoria.data
            proximo_pago    = form.proximo_pago.data
            monto           = form.monto.data
            account_id      = int(request.form.get("cuenta"))
            ScheduledIncomeController().create_income(nombre,fecha,monto,current_user.id,descripcion,categoria=categoria,next_income=proximo_pago,received_amount=0,pending_amount=monto,account_id=account_id)
            flash("¡Ingreso programado creado exitosamente!", "success")
            return redirect("/veringresosprogramados")
        

@create_functions_bp.route("/crearservicio",methods=["GET","POST"])
@login_required
@email_validation
def crear_servicio():
    if request.method == "GET":
        form = FormularioCrearServicio()
        accounts = Account().get_all_by_userid(current_user.id)#es para la relacion una a muchos entre(cuenta y servicios)
        return render_template("create_functions/crear_servicio.html",form=form,accounts=accounts)
    
    if request.method == "POST":
        form = FormularioCrearServicio()
        if form.validate_on_submit():

            #despues de validar creamos el objeto servicio para bd
            nombre      = form.nombre.data
            descripcion = form.descripcion.data
            fecha       = datetime.now()
            vencimiento = form.fecha_vencimiento.data
            categoria   = form.categoria.data
            precio      = form.precio.data
            cuenta      = int(request.form.get("cuenta"))
            ServiceController().create_service(nombre,descripcion,fecha,categoria,current_user.id,precio,precio,cuenta,vencimiento)
            flash("¡Servicio creado exitosamente!", "success")
            return redirect("/verservicios")
        else:
            return render_template("auth/verservicios.html",form=form)


@create_functions_bp.route("/crearprestamo",methods=["GET","POST"])
@login_required
@email_validation
def crear_prestamo():
    if request.method == "POST":
        form = FormularioCrearPrestamos()
        print(f'nombre:{form.nombre.data},titular:{form.titular.data},precio:{form.precio.data},cuota:{form.cuota.data},tea:{form.tea.data},descripcion:{form.descripcion.data},vencimiento:{form.fecha_vencimiento.data}')
        if form.validate_on_submit():
            #despues de validar creamos el objeto prestamo para bd
            nombre      = form.nombre.data
            titular     = form.titular.data 
            precio      = form.precio.data
            cuota       = form.cuota.data
            tea         = form.tea.data
            descripcion = form.descripcion.data
            fecha       = datetime.now()
            vencimiento = form.fecha_vencimiento.data
            cuenta      = int(request.form.get("cuenta"))
            LoanController().create_loan(nombre,titular,precio,cuota,current_user.id,cuenta,precio,fecha,vencimiento,descripcion,tea)
            flash("¡Préstamo creado exitosamente!", "success")
            return redirect("/verprestamos")
        else:
            print("error")
            return render_template("create_functions/crear_prestamo.html",form=form)
        
@create_functions_bp.route("/pagoprestamo",methods=["GET","POST"])
@login_required
@email_validation
def pago_prestamo():
    if request.method =="GET":
        form  = FormularioCrearPagoPrestamo()
        loans = Loan().get_all_for_payment(current_user.id)#es para la relacion una a muchos entre(prestamos y prestamos pagados)
        return render_template("create_functions/crear_pago_prestamo.html",form=form,loans=loans)
    
    if request.method =="POST":
        form = FormularioCrearPagoPrestamo()
        if form.validate_on_submit:
            loan = Loan().get_by_id(request.form.get("prestamo"))
            #una vez validamos el formulario, evaluamos que el usuario tenga monto suficiente
            account = Account().get_by_id(loan.account_id)
            if account.balance < form.monto.data:
                flash("Monto insuficiente","error")
                return redirect("/pagoprestamo")
            else:
                prestamo_id = int(request.form.get("prestamo"))
                monto       = form.monto.data
                prestamo = Loan().get_by_id(prestamo_id)
                
                #Evaluamos si el usuario pago mas de lo que cuesta 
                if monto > prestamo.reamining_price:
                    monto = prestamo.reamining_price
                    account.balance = (account.balance or 0) - monto
                else:
                    monto  = form.monto.data
                    account.balance = (account.balance or 0) - monto
                
                ultimos_pagos = Loan_payment().get_all_by_loan(prestamo.id)
                ultimo_pago = monto
                if len(ultimos_pagos)>0:
                    ultimo_pago = ultimos_pagos[-1].amount
                    print("entro len")
                fecha_pago =form.fecha.data  
                tea = float(prestamo.tea)
                if tea >0:
                    print("tiene tea")
                    if fecha_pago > prestamo.expiration_date:
                        print("es tarde para pagar")
                        monto =float(monto+calcular_tem(prestamo.tea,prestamo.quota)*ultimo_pago) 
                        account.balance = (account.balance or 0) - monto
                        print(ultimo_pago)
                print(f"monto:{monto}")
                descrip = form.descripcion.data
                user_id = current_user.id
                #creamos el objeto prestamo_pagado para bd
                LoanPaymentController().create_loan_payment(monto,fecha_pago,descrip,prestamo_id,user_id)

                #actualizamos el monto restante para pagar el prestamo
                prestamo.reamining_price = prestamo.reamining_price -monto
                LoanController().update_loan(prestamo)
                #actualizamos el saldo de la cuenta de usuario

                user = User().get_by_id(current_user.id)
                user.balance = (user.balance or 0) - monto
                UserController().update_user(user)
                return redirect("/verprestamos")
        else:
            return "error"

@create_functions_bp.route("/pagoservicio",methods=["GET","POST"])
@login_required
@email_validation
def pago_servicio():
    if request.method == "GET":
        form     = FormularioCrearPagoServicio()
        services = Service().get_all_for_payment(current_user.id)#es para la relacion una a muchos entre(Servicio y pago de servicios)
        return render_template("create_functions/crear_pago_servicio.html",form=form,services=services)
    
    if request.method == "POST":
        form = FormularioCrearPagoServicio()
        if form.validate_on_submit():
            #una vez validamos el formulario, evaluamos que el usuario tenga monto suficiente
            user = User().get_by_id(current_user.id)
            if user.balance < form.monto.data:
                flash("Monto insuficiente","error")
                return redirect("/pagoservicio")
            else:
                servicio_id    = int(request.form.get("servicio"))
                monto          = form.monto.data
                servicio = Service().get_by_id(servicio_id)

                #Evaluamos si el usuario pago mas de lo que cuesta 
                if monto > servicio.reamining_price:
                    monto = servicio.reamining_price
                else:
                    monto  = form.monto.data
                fecha       = form.fecha.data
                descripcion = form.descripcion.data
                user_id     = current_user.id
                #creamos el objeto servicio_pagado para bd
                ServicePaymentController().create_service_payment(monto,fecha,descripcion,servicio_id,user_id)

                #actualizamos el monto restante para pagar el servicio
                servicio.reamining_price = servicio.reamining_price-monto
                ServiceController().update_service(servicio)

                #actualizamos el monto de la cuenta usuario
                user = User().get_by_id(current_user.id)
                user.balance = (user.balance or 0) - monto
                UserController().update_user(user)
                return redirect("/verservicios")
        else:
            return "error"