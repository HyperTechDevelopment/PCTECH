from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory,
    make_response,
    after_this_request
)
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import colors
import uuid
import os
from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ITFix.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret-key-1234"

db = SQLAlchemy(app)


class ITFix(db.Model):
    """
     Representa uma correção de TI.

     Atributos:
         id (int): O identificador exclusivo da correção.
         eqp_ti (str): O equipamento de TI.
         modelo_eqp (str): O modelo do equipamento.
         marca_eqp (str): A marca do equipamento.
         serie_eqp (str): O número de série do equipamento.
         data_fix (datetime): A data e hora da correção.
         tecnico (str): O técnico responsável pela correção.
         status (str): O status da correção.
         sr_ticket (str): O número do ticket de solicitação de serviço.
         justificativa (str): A justificativa para a correção.
         data_atualizacao (datetime): A data e hora da atualização.
         data_entrega (datetime): A data e hora da entrega.
         atualizacoes (lista): A lista de atualizações para a correção.
         ID_reparo (str): O identificador exclusivo da correção.
    """

    id = db.Column(db.Integer, primary_key=True)
    eqp_ti = db.Column(db.String(100), nullable=False)
    modelo_eqp = db.Column(db.String(100), nullable=False)
    marca_eqp = db.Column(db.String(100), nullable=False)
    serie_eqp = db.Column(db.String(100), nullable=False)
    data_fix = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tecnico = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    sr_ticket = db.Column(db.String(100), nullable=False)
    justificativa = db.Column(db.Text, nullable=False)
    data_atualizacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime)
    atualizacoes = db.relationship("ReparoAtualizacao", backref="reparo", lazy=True)
    ID_reparo = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
        default=lambda: f"Fix-{uuid.uuid4().int % 10000}",
    )


class ReparoAtualizacao(db.Model):
    """
     Representa uma atualização de reparo.

     Atributos:
         id (int): O identificador exclusivo da atualização.
         reparo_id (int): O ID do conserto associado.
         ID_reparo (str): O identificador exclusivo da atualização.
         eqp_ti (str): O equipamento de TI.
         modelo_eqp (str): O modelo do equipamento.
         marca_eqp (str): A marca do equipamento.
         serie_eqp (str): O número de série do equipamento.
         tecnico (str): O técnico responsável pela atualização.
         status (str): O status da atualização.
         sr_ticket (str): O número do ticket de solicitação de serviço.
         data_fix (datetime): A data e hora da correção.
         justificativa (str): A justificativa para a atualização.
         data_atualizacao (datetime): A data e hora da atualização.
         data_entrega (datetime): A data e hora da entrega.
    """

    id = db.Column(db.Integer, primary_key=True)
    reparo_id = db.Column(db.Integer, db.ForeignKey("it_fix.id"), nullable=False)
    ID_reparo = db.Column(db.String(100), nullable=False)
    eqp_ti = db.Column(db.String(100), nullable=False)
    modelo_eqp = db.Column(db.String(100), nullable=False)
    marca_eqp = db.Column(db.String(100), nullable=False)
    serie_eqp = db.Column(db.String(100), nullable=False)
    tecnico = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    sr_ticket = db.Column(db.String(100), nullable=False)
    data_fix = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    justificativa = db.Column(db.Text, nullable=False)
    data_atualizacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime)


class ITUser(db.Model):
    """
     Representa um usuário de TI.

     Atributos:
         id (int): O identificador exclusivo do usuário.
         nome (str): O nome do usuário.
         it_login (str): O login de TI do usuário.
         password_hash (str): A senha com hash do usuário.
         perfil (str): O perfil do usuário.
    """

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    it_login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(
        db.String(128)
    )  # substituído 'password' por 'password_hash'
    perfil = db.Column(db.String(50), nullable=False)

    @property
    def password(self):
        raise AttributeError("password: campo somente de escrita")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()
    if not ITUser.query.filter_by(it_login="admin").first():
        admin = ITUser(
            nome="Administrador", it_login="admin", password="admin123", perfil="admin"
        )
        db.session.add(admin)
        db.session.commit()


@app.route("/")
def index():
    return redirect(url_for("login"))


def check_login_and_profile():
    """
     Verifica se o usuário está logado e possui um perfil válido.

     Retorna:
         - Caso o usuário não esteja logado, redireciona para a página de login.
         - Se o usuário possuir perfil “admin”, retorna “admin”.
         - Se o usuário possui perfil “técnico”, retorna “técnico”.
         - Caso o usuário tenha um perfil não reconhecido, pisca uma mensagem de erro e redireciona para a página de login.
    """
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user_profile = session.get("profile")
    if user_profile == "admin":
        return "admin"
    elif user_profile == "tecnico":
        return "tecnico"
    else:
        flash("Perfil não reconhecido!")
        return redirect(url_for("login"))

@app.before_request
def before_request():
    @after_this_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    if 'user_id' in session and request.endpoint == 'login':
        return redirect(url_for('dashboard'))
    elif 'user_id' not in session and request.endpoint == 'dashboard':
        return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    """
     Lida com a funcionalidade de login.

     Esta função é responsável por lidar com o processo de login. Ele verifica se o usuário já está logado e caso não esteja, trata do envio do formulário de login. Se o formulário for enviado por meio do método POST, ele recuperará o nome de usuário e a senha dos dados do formulário e os verificará em relação às credenciais de usuário armazenadas. Se as credenciais forem válidas, ele define as variáveis de sessão do usuário e redireciona o usuário para a página do painel. Se as credenciais forem inválidas, uma mensagem de erro será exibida.

     Retorna:
         Se o usuário já estiver logado, ele redireciona para a página do painel.
         Se o formulário for enviado pelo método POST e as credenciais forem válidas, ele redirecionará para a página do painel.
         Se o formulário for enviado pelo método POST e as credenciais forem inválidas, ele exibirá uma mensagem de erro e renderizará a página de login.
         Se ocorrer um erro durante o processo de login, ele exibirá uma mensagem de erro e renderizará a página de login.
    """
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = ITUser.query.filter_by(it_login=username).first()
            if user and user.verify_password(password):
                session["user_id"] = user.id
                session["username"] = user.it_login
                session["nome_tecnico"] = user.nome
                session["profile"] = user.perfil
                return redirect(url_for("dashboard"))
            flash("Credenciais inválidas. Tente novamente.")
        return render_template("login.html")
    except SQLAlchemyError:
        flash("Ocorreu um erro ao tentar fazer login. Por favor, tente novamente.")
        return render_template("login.html")


@app.route("/home")
def home():
    """
     Renderiza a página inicial com base no perfil do usuário.

     Retorna:
         Se o usuário for administrador, ele renderizará o modelo admin_dashboard.html.
         Se o usuário for um técnico, ele recupera todos os objetos ITFix e renderiza o template tech_dashboard.html com a variável 'reparos'.
         Se o usuário não for administrador nem técnico, retorna o valor da variável 'perfil'.
    """
    profile = check_login_and_profile()
    if profile == "admin":
        return render_template("admin_dashboard.html")
    elif profile == "tecnico":
        reparos = ITFix.query.all()
        return render_template("tech_dashboard.html", reparos=reparos)
    else:
        return profile


@app.route("/dashboard")
def dashboard():
    """
     Renderiza o modelo de painel apropriado com base no perfil do usuário.

     Retorna:
         resposta: a resposta HTTP que contém o modelo renderizado.
    """
    profile = check_login_and_profile()
    if profile == "admin":
        response = make_response(render_template("admin_dashboard.html"))
    elif profile == "tecnico":
        reparos = ITFix.query.all()
        response = make_response(
            render_template("tech_dashboard.html", reparos=reparos)
        )
        # Add headers to prevent caching
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    else:
        response = make_response(profile)
    return response


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/usuarios/cadastrar", methods=["GET", "POST"])
def cadastrar_usuario():
    """
     Ver função para registrar um novo usuário.

     Esta função lida com solicitações GET e POST. Se o método de solicitação for POST,
     ele recupera os dados do usuário do formulário de solicitação e tenta criar um novo usuário
     no banco de dados. Se o login já existir, será exibida uma mensagem de erro. Se o
     usuário é criado com sucesso, ele redireciona para a página de lista de usuários. Se o pedido
     método é GET, ele simplesmente renderiza o formulário de registro do usuário.

     Retorna:
         Se o método de solicitação for POST e o usuário for criado com sucesso, ele redireciona
         para a página da lista de usuários. Caso contrário, renderiza o formulário de registro do usuário.

     Levanta:
         SQLAlchemyError: Se ocorrer um erro ao tentar criar o usuário no
         base de dados.

    """
    try:
        if request.method == "POST":
            nome = request.form["nome"]
            login = request.form["login"]
            password = request.form["password"]
            perfil = request.form["perfil"]
            if ITUser.query.filter_by(it_login=login).first():
                flash("Login já existe!")
                return redirect(url_for("cadastrar_usuario"))
            new_user = ITUser(
                nome=nome, it_login=login, password=password, perfil=perfil
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Usuário cadastrado com sucesso!")
            return redirect(url_for("lista_usuarios"))
        return render_template("cadastrar_usuario.html")
    except SQLAlchemyError:
        flash(
            "Ocorreu um erro ao tentar cadastrar o usuário. Por favor, tente novamente."
        )
        return render_template("cadastrar_usuario.html")


@app.route("/usuarios")
def lista_usuarios():
    users = ITUser.query.all()
    return render_template("lista_usuario.html", users=users)


@app.route("/usuarios/editar/<int:user_id>", methods=["GET", "POST"])
def editar_usuario(user_id):
    """
     Edite um usuário com o user_id fornecido.

     Argumentos:
         user_id (int): O ID do usuário a ser editado.

     Retorna:
         Se o método de solicitação for POST:
             - Se o usuário for atualizado com sucesso, ele redireciona para a rota "lista_usuarios".
         Se o método de solicitação for GET:
             - Renderiza o template "editar_usuario.html" com os dados do usuário.

     Levanta:
         SQLAlchemyError: se ocorrer um erro ao atualizar o usuário.

    """
    try:
        user = ITUser.query.get_or_404(user_id)
        if request.method == "POST":
            user.nome = request.form["nome"]
            user.it_login = request.form["login"]
            if request.form["password"]:
                user.password = request.form["password"]
            user.perfil = request.form["perfil"]
            db.session.commit()
            flash("Usuário atualizado com sucesso!")
            return redirect(url_for("lista_usuarios"))
        return render_template("editar_usuario.html", user=user)
    except SQLAlchemyError:
        flash(
            "Ocorreu um erro ao tentar atualizar o usuário. Por favor, tente novamente."
        )
        return render_template("editar_usuario.html", user=user)


@app.route("/usuarios/deletar/<int:user_id>", methods=["POST"])
def deletar_usuario(user_id):
    """
     Exclui um usuário do banco de dados.

     Argumentos:
         user_id (int): O ID do usuário a ser excluído.

     Retorna:
         redirecionamento: Redireciona para a rota "lista_usuarios".

     Levanta:
         SQLAlchemyError: se ocorrer um erro ao excluir o usuário.

    """
    try:
        # Verifique se o user_id corresponde ao do usuário admin
        admin_user = ITUser.query.filter_by(it_login="admin").first()
        if user_id == admin_user.id:
            flash("O usuário admin não pode ser deletado!")
            return redirect(url_for("lista_usuarios"))

        user = ITUser.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("Usuário deletado com sucesso!")
        return redirect(url_for("lista_usuarios"))
    except SQLAlchemyError:
        flash(
            "Ocorreu um erro ao tentar deletar o usuário. Por favor, tente novamente."
        )
        return redirect(url_for("lista_usuarios"))


def create_receipt(reparo, receipt_path):
    """
     Crie um recibo para um reparo.

     Argumentos:
         reparo (Reparo): O objeto de reparo contendo os detalhes do reparo.
         recibo_path (str): O caminho onde o recibo será salvo.

     Retorna:
         tupla: uma tupla contendo o diretório onde o recibo foi salvo e o caminho do arquivo do recibo.

     Levanta:
         Nenhum

    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    directory = os.path.dirname(receipt_path)
    os.makedirs(
        directory, exist_ok=True
    )  # Isso garantirá que o diretório seja criado se não existir
    file_path = os.path.join(
        directory, f"comprovante_{date_str}_{reparo.ID_reparo}.pdf"
    )

    width, height = (
        7.62 * 72,
        5.08 * 72,
    )  # Convertendo as dimensões de polegadas para pontos
    doc = SimpleDocTemplate(
        file_path,
        pagesize=(width, height),
        rightMargin=60,
        leftMargin=30,
        topMargin=60,
        bottomMargin=60,
    )
    story = []
    styles = getSampleStyleSheet()

    # Adiciona o logotipo
    logo = "static/logo_comprovante.png"
    story.append(Image(logo, 40, 40))

    # Personaliza os estilos
    if "Title" not in styles:
        styles.add(ParagraphStyle(name="Title", fontSize=95, textColor=colors.blue))
    if "Normal" not in styles:
        styles.add(ParagraphStyle(name="Normal", fontSize=95, textColor=colors.black))

    # Adiciona os detalhes do reparo ao comprovante
    story.append(Paragraph("Comprovante de Reparo", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Equipamento: {reparo.eqp_ti}", styles["Normal"]))
    story.append(Paragraph(f"Ticket SR: {reparo.sr_ticket}", styles["Normal"]))
    story.append(Paragraph(f"Justificativa: {reparo.justificativa}", styles["Normal"]))
    story.append(Paragraph(f"Modelo: {reparo.modelo_eqp}", styles["Normal"]))
    story.append(Paragraph(f"Série: {reparo.serie_eqp}", styles["Normal"]))
    story.append(Paragraph(f"Marca: {reparo.marca_eqp}", styles["Normal"]))
    story.append(Paragraph(f"Status: {reparo.status}", styles["Normal"]))

    # Adiciona a data de entrega ao comprovante
    data_entrega = (
        "SEM PREVISÃO"
        if reparo.data_entrega is None
        else reparo.data_entrega.strftime("%d/%m/%Y")
    )
    story.append(Paragraph(f"Data de Entrega: {data_entrega}", styles["Normal"]))

    # Adiciona o rodapé
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "COMPROVANTE GERADO PELO SISTEMA PCT - MANUTENÇÃO T.I", styles["Normal"]
        )
    )

    doc.build(story)

    return directory, file_path  # Retornando também o diretório


@app.route("/reparos/cadastrar", methods=["GET", "POST"])
def cadastrar_reparo():
    """
    Ver função para registrar um reparo.

    Esta função lida com solicitações GET e POST. Se o método de solicitação for POST,
    ele recupera os dados do formulário e cria uma nova entrada de reparo no banco de dados. Isso também
    gera um recibo do reparo e o envia como um arquivo para download ao usuário.

    Se o método de solicitação for GET, ele renderizará a página de registro de reparo.

    Retorna:
        Se o método de solicitação for POST, ele retornará o arquivo de recibo gerado como download.
        Se o método de solicitação for GET, ele retornará a página de registro de reparo renderizada.
    """
    if request.method == "POST":
        eqp_ti = request.form["eqp_ti"]
        sr_ticket = request.form["sr_ticket"]
        justificativa = request.form["justificativa"]
        modelo_eqp = request.form["modelo_eqp"]
        serie_eqp = request.form["serie_eqp"]
        marca_eqp = request.form["marca_eqp"]
        status = request.form["status"]
        data_entrega = request.form.get(
            "data_entrega_date"
        )  # Alterado para corresponder ao formulário HTML
        sem_previsao = request.form.get(
            "sem_previsao"
        )  # Novo campo para verificar se a caixa "sem_previsao" está marcada

        # Se "sem_previsao" estiver marcado ou se não houver data, defina data_entrega como None
        if sem_previsao == "on" or not data_entrega:
            data_entrega = None
        else:
            # Caso contrário, tente converter a data para um objeto datetime
            try:
                data_entrega = datetime.strptime(data_entrega, "%Y-%m-%d")
            except ValueError:
                flash("Formato de data inválido. Use o formato AAAA-MM-DD.")
                data_entrega = None
        new_repair = ITFix(
            eqp_ti=eqp_ti,
            tecnico=session["username"],
            sr_ticket=sr_ticket,
            justificativa=justificativa,
            modelo_eqp=modelo_eqp,
            serie_eqp=serie_eqp,
            marca_eqp=marca_eqp,
            status=status,
            data_entrega=data_entrega,
        )
        db.session.add(new_repair)
        db.session.commit()
        flash("Reparo cadastrado com sucesso!")

        # Define o diretório e o caminho do comprovante
        date_str = datetime.now().strftime("%Y-%m-%d")
        directory = os.path.join("comprovantes", date_str)
        os.makedirs(directory, exist_ok=True)
        receipt_path = os.path.join(
            directory, f"comprovante_{date_str}_{new_repair.ID_reparo}.pdf"
        )

        directory, receipt_path = create_receipt(new_repair, receipt_path)

        return send_from_directory(
            directory,
            os.path.basename(receipt_path),
            as_attachment=True,
        )

    # Se o método não for POST (ou seja, GET), renderize a página de cadastro
    return render_template("cadastrar_reparo.html")


@app.route("/reparos")
def reparo_historico():
    """
     Recupera uma lista de objetos ITFix que representam o histórico de reparos e os renderiza em um modelo.

     Retorna:
         Um modelo renderizado contendo o histórico de reparos.
    """
    reparos = ITFix.query.all()
    return render_template("reparo_historico.html", reparos=reparos)


@app.route("/reparos/detalhes/<int:reparo_id>")
def ver_reparo(reparo_id):
    """
     Função de visualização para exibir detalhes de um reparo.

     Parâmetros:
     - reparo_id (int): ID do reparo a ser exibido.

     Retorna:
     - render_template: O modelo renderizado para exibir os detalhes do reparo.
    """
    reparo = ITFix.query.get_or_404(reparo_id)
    historico = (
        ReparoAtualizacao.query.filter_by(reparo_id=reparo_id)
        .order_by(ReparoAtualizacao.data_atualizacao.desc())
        .all()
    )

    # Adicione esta linha para imprimir o histórico no console do servidor
    for atualizacao in historico:
        print(vars(atualizacao))

    return render_template("ver_reparo.html", reparo=reparo, historico=historico)


@app.route("/reparos/reimprimir/<string:reparo_id>")
def reimprimir_comprovante(reparo_id):
    """
    Reimprime o comprovante de um reparo específico.

    Args:
        reparo_id (str): O ID do reparo a ser reimpresso.

    Returns:
        flask.Response: O comprovante reimpresso como um arquivo para download.
    """
    # Busca o reparo pelo ID
    reparo = ITFix.query.filter_by(ID_reparo=reparo_id).first_or_404()

    # Define o diretório e o caminho do comprovante reimpresso
    date_str = datetime.now().strftime("%Y-%m-%d")
    directory = os.path.join("comprovantes_reimpressos", date_str)
    os.makedirs(directory, exist_ok=True)
    receipt_path = os.path.join(
        directory, f"comprovante_{date_str}_{reparo.ID_reparo}.pdf"
    )

    # Recria o comprovante, se necessário
    if not os.path.exists(receipt_path):
        create_receipt(reparo, receipt_path)

    # Envia o comprovante como um arquivo para download
    return send_from_directory(
        directory, os.path.basename(receipt_path), as_attachment=True
    )


@app.route("/atualizar_reparo/<int:reparo_id>", methods=["GET", "POST"])
def atualizar_reparo(reparo_id):
    """
    Atualiza as informações de um reparo no sistema.

    Args:
        reparo_id (int): O ID do reparo a ser atualizado.

    Returns:
        redirect: Redireciona para a página de visualização do reparo atualizado.

    Raises:
        404: Se o reparo com o ID fornecido não for encontrado.

    """
    reparo = ITFix.query.get_or_404(reparo_id)
    if request.method == "POST":

        reparo.eqp_ti = request.form["eqp_ti"]
        reparo.modelo_eqp = request.form["modelo_eqp"]
        reparo.marca_eqp = request.form["marca_eqp"]
        reparo.serie_eqp = request.form["serie_eqp"]
        reparo.status = request.form["status"]
        reparo.justificativa = request.form["justificativa"]

        sem_previsao = "sem_previsao" in request.form
        data_entrega_date = request.form.get("data_entrega_date")
        data_fix = datetime.utcnow()

        if sem_previsao:
            reparo.data_entrega = None
        elif data_entrega_date:
            try:
                reparo.data_entrega = datetime.strptime(data_entrega_date, "%Y-%m-%d")
            except ValueError:
                flash("Formato de data inválido. Use o formato AAAA-MM-DD.", "error")
                return redirect(request.url)

        db.session.commit()

        # Cria um novo registro de histórico com o estado atual do reparo
        historico_atualizacao = ReparoAtualizacao(
            reparo_id=reparo.id,
            ID_reparo=reparo.ID_reparo,
            eqp_ti=reparo.eqp_ti,
            modelo_eqp=reparo.modelo_eqp,
            marca_eqp=reparo.marca_eqp,
            serie_eqp=reparo.serie_eqp,
            tecnico=reparo.tecnico,
            status=reparo.status,
            sr_ticket=reparo.sr_ticket,
            justificativa=reparo.justificativa,
            data_fix=data_fix,
            data_entrega=reparo.data_entrega,
        )
        db.session.add(historico_atualizacao)
        db.session.commit()
        flash("Reparo atualizado com sucesso!", "success")

        return redirect(url_for("ver_reparo", reparo_id=reparo.id))
    else:
        # Formata a data de entrega para o input type="date" antes de renderizar
        if reparo.data_entrega:
            reparo.data_entrega = reparo.data_entrega.strftime("%Y-%m-%d")
        return render_template("atualizar_reparo.html", reparo=reparo)


if __name__ == "__main__":
    app.run(debug=True)
