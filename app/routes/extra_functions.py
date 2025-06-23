"""
 Funciones extra
"""


#modulos externos
from flask                                import Blueprint,redirect,flash,render_template,jsonify,request
from flask_login                          import current_user,login_required,logout_user
from werkzeug.security                    import generate_password_hash

#modulos propios
from ..extra_functions.token              import confirm_token,genera_token
from ..extra_functions.notification_funct import send_gmail_confirmation,send_changepassword_request,send_changeemail_request
from ..extra_functions.email_decorator    import email_validation
from ..models.importaciones               import User,Account,Income,Loan,Service,Scheduled_income
from ..controllers.importaciones          import UserController,LoanController,ServiceController,AccountController,IncomeController,ScheduledIncomeController
from app.forms.importaciones              import FormularioCambiarContraseña,FormularioCambiarGmail

extra_functions_bp = Blueprint("extra_functions",__name__)


@extra_functions_bp.route('/') 
@extra_functions_bp.route('/index') 
def index(): 
    if current_user.is_authenticated:
        if current_user.email_conf is False:
            return render_template("extra_functions/confirmation.html")
        else:    
            return redirect('/home')
    else:
        return redirect("/iniciar")

@extra_functions_bp.route("/cerrar_sesion")
@login_required
@email_validation
def cerrar():
    logout_user()
    return redirect("/")

#-------------------------Funciones para confirmar correo------------------------

@extra_functions_bp.route("/conf_email/<token>")
@login_required
def confirm_email(token):
    if current_user.email_conf:
        return redirect("/index")
    email = confirm_token(token)
    user = User().get_by_id(current_user.id)
    if user.email == email:
        user.email_conf= True
        UserController().update_user(user)
        flash("Cuenta confirmada")
        return redirect("/index")
    else:
        flash("Token invalido")
        #aqui añadir que muestre token vencido
        return render_template("extra_functions/confirmation.html", error="Token inválido o vencido")

@extra_functions_bp.route("/reenviartoken")
@login_required
def reenviar_token():
    user  = User().get_by_id(current_user.id)
    token = genera_token(user.email)
    send_gmail_confirmation(token)
    return redirect("https://mail.google.com/")

#----------------Estas funciones permiten el acceso a informacion del usuario para que se carge en los formularios de actualizacion----------
@extra_functions_bp.route("/informacion_cuenta/<int:id>")
@login_required
@email_validation
def info_cuenta(id):
    account = Account().get_by_id(id)
    account_data = {
        'card':account.card,
        'account_name':account.account_name,
    }
    return jsonify(account_data)

@extra_functions_bp.route("/informacion_ingreso/<int:id>")
@login_required
@email_validation
def info_ingreso(id):
    income = Income().get_by_id(id)
    income_data = {
        'income_name':income.income_name,
        'income_date':income.income_date,
        'description':income.description,
        'category':income.category,
        'amount':income.amount
    }
    return jsonify(income_data)

@extra_functions_bp.route("/informacion_prestamo/<int:id>")
@login_required
@email_validation
def info_prestamo(id):
    loan = Loan().get_by_id(id)
    loan_data = {
        "name":loan.loan_name,
        "holder":loan.holder,
        "price":loan.price,
        "quota":loan.quota,
        "tea":loan.tea,
        "expiration_date":loan.expiration_date
    }
    return jsonify(loan_data)

@extra_functions_bp.route("/informacion_servicio/<int:id>")
@login_required
@email_validation
def info_servicio(id):
    service = Service().get_by_id(id)
    service_data = {
        "name":service.service_name,
        "description":service.description,
        "category":service.category,
        "price":service.price,
        "expiration_date":service.expiration_date
    }
    return jsonify(service_data)

@extra_functions_bp.route("/informacion_ingreso_programado/<int:id>")
@login_required
@email_validation
def info_ingreso_programado(id):
    income = Scheduled_income().get_by_id(id)
    income_data = {
        "name":income.income_name,
        "description":income.description,
        "category":income.category,
        "amount":income.amount,
        "next_income":income.next_income
    }
    return jsonify(income_data)

#---------------------CAMBIO DE CLAVE Y EMAIL-----------------------

@extra_functions_bp.route("/solicitud_cambio_clave", methods=["GET", "POST"])
def solicitud_cambio_clave():
    """
    Permite a cualquier usuario solicitar recuperación de contraseña ingresando su email.
    """
    if request.method == "POST":
        email = request.form.get("email")
        user = User().get_by_email(email)
        if user:
            token = genera_token(user.email)
            # Enviar correo de recuperación
            send_changepassword_request(token, user)
        # Mostrar mensaje genérico por seguridad
        flash("Si el correo existe, se ha enviado un mensaje para restablecer la contraseña.")
        return render_template("extra_functions/change_password/solicitud_cambio_clave.html", enviado=True)
    return render_template("extra_functions/change_password/solicitud_cambio_clave.html", enviado=False)

@extra_functions_bp.route("/cambio_clave/<token>",methods=["GET","POST"])
def cambiar_clave(token):
    """
        Recibimos el token, verificamos que sea el email correcto y evaluamos el tipo de método get (formulario para cambiar contraseña)
        post (verificamos que la información esté bien y actualizamos la contraseña del usuario)
    """
    email = confirm_token(token)
    user = User().get_by_email(email)
    if user:
        form = FormularioCambiarContraseña()
        if request.method == "GET":
            return render_template("extra_functions/change_password/cambio_pass.html", form=form)
        if request.method == "POST":
            form = FormularioCambiarContraseña()
            if form.validate_on_submit():
                nueva_contraseña = form.clave.data
                user.password_hash = generate_password_hash(nueva_contraseña)
                UserController().update_user(user)
                flash("Contraseña cambiada exitosamente. Por favor, inicia sesión de nuevo.")
                return redirect("/iniciar")
    return "Error"

@extra_functions_bp.route("/solicitud_cambio_email")
@login_required
@email_validation
def solicitud_cambio_email():
    """
        Enviamos el mensaje de solicitud de cambio de correo, al email con el token para verificar que es su correo
    """
    token = genera_token(current_user.email)
    send_changeemail_request(token)
    return render_template("extra_functions/change_email/solicitud_cambio_email.html")

@extra_functions_bp.route("/cambio_email/<token>",methods=["GET","POST"])
@login_required
@email_validation
def cambiar_email(token):
    """
        Recibimos el token verificamos que sea el email correcto y evaluamos el tipo de metodo get(formulario para cambiar correo)
        post(verificamos que la informacion este bien y actualizamos el correo del usuario)
    """
    token = token
    email = confirm_token(token)
    if current_user.email == email:
        form = FormularioCambiarGmail()
        if request.method == "GET":
            return render_template("extra_functions/change_email/cambio_email.html",form=form)
        if request.method == "POST":
            form = FormularioCambiarGmail()
            if form.validate_on_submit():
                user = User().get_by_id(current_user.id)
                nuevo_email = form.email.data
                user.email  = nuevo_email
                user.email_conf = 0
                new_email_tk = genera_token(nuevo_email)
                send_gmail_confirmation(new_email_tk)
                UserController().update_user(user)
                return render_template("extra_functions/confirmation.html")
    else:
        return "Error"

#-------------Funciones de eliminacion-----------

@extra_functions_bp.route("/borrar_prestamo/<int:id>",methods=["POST"])
@login_required
@email_validation
def borrar_prestamo(id:int):
    loan = Loan().get_by_id(id)
    if loan is None:
        return render_template("extra_functions/error-message/no_exist_error.html",objeto="prestamo")
    else:
        if loan.user_id == current_user.id:
            LoanController().delete_loan(loan)
            return redirect("/verprestamos")
        else:
            return render_template("extra_functions/error-message/eliminated_error.html",objeto="prestamo")

@extra_functions_bp.route("/borrar_servicio/<int:id>",methods=["POST"])
@login_required
@email_validation
def borrar_servicio(id:int):
    service = Service().get_by_id(id)
    if service is None:
        return render_template("extra_functions/error-message/no_exist_error.html",objeto="servicio")
    else:
        if service.user_id == current_user.id:
            ServiceController().delete_service(service)
            return redirect("/verservicios")
        else:
            return render_template("extra_functions/error-message/eliminated_error.html",objeto="servicio")

@extra_functions_bp.route("/borrar_cuenta/<int:id>",methods=["POST"])
@login_required
@email_validation
def borrar_cuenta(id:int):
    account = Account().get_by_id(id)
    if account is None:
        return render_template("extra_functions/error-message/no_exist_error.html",objeto="cuenta")
    else:
        if account.user_id == current_user.id:
            AccountController().delete_account(account)
            return redirect("/vercuentas")
        else:
            return render_template("extra_functions/error-message/eliminated_error.html",objeto="cuenta")

@extra_functions_bp.route("/ingreso/<int:id>",methods=["POST"])
@login_required
@email_validation
def borrar_ingreso(id:int):
    income = Income().get_by_id(id)
    if income is None:
        return render_template("extra_functions/error-message/no_exist_error.html",objeto="ingreso")
    else:
        if income.user_id == current_user.id:
            IncomeController().delete_income(income)
            return redirect("/veringresos")
        else:
            return render_template("extra_functions/error-message/eliminated_error.html",objeto="ingreso")

@extra_functions_bp.route("/ingresoprogramado/<int:id>",methods=["POST"])
@login_required
@email_validation
def borrar_ingresoprogramado(id:int):
    income = Scheduled_income().get_by_id(id)
    if income is None:
        return render_template("extra_functions/error-message/no_exist_error.html",objeto="ingreso programado")
    else:
        if income.user_id == current_user.id:
            ScheduledIncomeController().delete_income(income)
            return redirect("/veringresosprogramados")
        else:
            return render_template("extra_functions/error-message/eliminated_error.html",objeto="ingreso programado")
