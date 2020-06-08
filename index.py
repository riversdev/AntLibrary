# IMPORTACION DE LIBRERIAS NECESARIAS
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_mysqldb import MySQL
from datetime import datetime, date, time, timedelta
import calendar
import time
from flask_socketio import SocketIO, send, emit
import json
import os

# INICIALIZACION DE LA VARIABLE NAME EN app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# CONFIGURACION DE APP PARA LA CONEXION A LA BASE DE DATOS
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'antLibrary'
mysql = MySQL(app)

# SESION INICIAL
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


# RAIZ #############################################################
@app.route("/")
def login():
    session.pop('user', None)
    return render_template('login.html')

# FUNCION PARA EL LOGIN DE USUARIO
@app.route("/logging_user", methods=['POST'])
def logging_user():
    if request.method == 'POST':
        session.pop('user', None)

        name = request.form['txtName']
        passwd = request.form['txtPass']
        confPasswd = request.form['txtConfPass']

        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM users WHERE fullname = %s and password = %s and password = %s', (name, passwd, confPasswd))
        data = cur.fetchone()

        if data is None:
            flash(u'Intentalo nuevamente !!!', 'error')
            return redirect(url_for('login'))
        else:
            session['user'] = name
            flash(u'Todo está listo !!!', 'success')
            return redirect(url_for('home'))


# HOME #############################################################
@app.route("/home")
def home():
    if g.user:
        return render_template('home.html')
    else:
        flash(u'Inicia nuevamente !!!', 'error')
        return redirect(url_for('login'))


# INVENTORY ########################################################
@app.route("/inventory") # creacion de la ruta para la funcion
def inventory(): # creacion de la funcion
    if g.user: # en caso de existir una sesion iniciada de ejecutan las siguientes lineas
        cur = mysql.connection.cursor() # se establece una conexion a la base de datos en 'cur'
        cur.execute('SELECT * FROM books') # ejecucion de la consulta select en la tabla libros
        dataBooks = cur.fetchall() # almacenamiento del retorno de la consulta en la variable dataBooks
        cur.execute('SELECT * FROM audiovisualRoom')#ejecucion de la consulta select en la tabla audiovisual
        dataAudiovisual = cur.fetchall() # almacenamiento del retorno en la variable dataBooks
        cur.execute('SELECT * FROM library') # ejecucion de la consulta select en la tabla biblioteca
        dataLibrary = cur.fetchall() # almacenamiento del retorno de la consulta en la variable dataLibrary
        cur.execute('SELECT * FROM projectors') # ejecucion de la consulta select en la tabla proyectores
        dataProjectors = cur.fetchall() # almacenamiento del retorno en la variable dataProjectors
        import datetime # se importa datetime en la presente funcion
        import time # se importa time en la presente funcion
        hoy = datetime.date.today().strftime("%Y-%m-%d") # se guarda la fecha actual en la variable 'hoy'
        enTres = datetime.date.today().strftime(
            "%Y-%m-" + str(int(datetime.date.today().strftime("%d")) + 3)) # se guarda la fecha dentro de 3 dias en la variable 'enTres'
        hour = time.strftime("%H:%M") # se guarda la hora actual en la variable 'hour'
        return render_template('inventory.html', books=dataBooks, audiovisualRoom=dataAudiovisual, library=dataLibrary, projectors=dataProjectors, fechaActual=hoy, fechaEntrega=enTres, hora=hour)
        # se retorna a la vista de inventario con todos los registros de todos los tipos de inventario
    else: #en caso de no existir una sesion iniciada se ejecutan las siguientes lineas
        flash(u'Inicia nuevamente !!!', 'error') # se manda una alerta a la siguiente vista
        return redirect(url_for('login')) # redireccionamiento a la vista de inicio de sesion
    
# FUNCION PARA AGREGAR LIBRO
@app.route("/addBook", methods=['POST']) # creacion de la ruta para la funcion, haciendo uso de post
def addBook(): # creacion de la funcion en la ruta
    if request.method == 'POST': # en caso de que request reciba un metodo post continua
        code = request.form['codeBook'] # guardar el valor del input 'codeBook' en code
        name = request.form['nameBook'] # guardar el valor del input 'nameBook' en name
        author = request.form['authorBook'] # guardar el valor del input 'authorBook' en author
        editorial = request.form['editorialBook'] # guardar el valor del input 'editorialBook' en editorial
        yearEdition = request.form['yearEdition'] # guardar el valor del input 'yearEdition' en yearEdition
        unidadMed = request.form['unidadMedida'] # guardar el valor del input 'unidadMedida' en unidadMed
        materia = request.form['materia'] # guardar el valor del input 'materia' en materia
        campoConocim = request.form['campoConocim']#guardar el valor del input 'campoConocim'en campoConocim
        estadoFisico = request.form['estadoFisico']#guardar el valor del input 'estadoFisico'en estadoFisico
        dateInput = request.form['dateInput'] # guardar el valor del input 'dateInput' en dateInput
        responsable = request.form['responsable'] # guardar el valor del input 'responsable' en responsable
        observations = request.form['observations']#guardar el valor del input 'observations'en observations
        cur = mysql.connection.cursor() # se crea una conexion a la base dedatos y se guarda en 'cur'
        cur.execute(
            "INSERT INTO books (code, tittle, author, editorial, yearEdition, unidadMedida, materia, campoConocimiento, estadoFisico, dateInput, responsable, observations, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (code, name, author, editorial, yearEdition, unidadMed, materia, campoConocim, estadoFisico, dateInput, responsable, observations, 'A'))
            # se crea la insercion de datos a la base de datos con los datos en las variables anteriores
        mysql.connection.commit() # se ejecuta la consulta
        flash(u'Libro agregado exitosamente', 'success') # envio de un mensaje de flash a la vista HTML
        return redirect(url_for('inventory')) # redireccionamiento llamando a la funcion de inventario l-72

# FUNCION PARA AGREGAR ELEMENTO DE AUDIOVISUAL
@app.route("/addAudiovisual", methods=['POST'])
def addAudiovisual():
    code = request.form['codeAudio']
    description = request.form['descriptionAudio']
    serie = request.form['serieAudio']
    marca = request.form['marcaAudio']
    model = request.form['modelAudio']
    propiedad = request.form['propertyAudio']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO audiovisualRoom (code, description, serie, marca, model, property) VALUES (%s, %s, %s, %s, %s, %s) ",
                (code, description, serie, marca, model, propiedad))
    mysql.connection.commit()
    flash(u'Elemento agregado exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA AGREGAR PROYECTOR
@app.route("/addProjector", methods=['POST'])
def addProjector():
    code = request.form['codeProjector']
    description = request.form['descriptionProjector']
    serie = request.form['serieProjector']
    marca = request.form['marcaProjector']
    model = request.form['modelProjector']
    propiedad = request.form['propertyProjector']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO projectors (code, description, serie, marca, model, property, status) VALUES (%s, %s, %s, %s, %s, %s, %s) ",
                (code, description, serie, marca, model, propiedad, 'A'))
    mysql.connection.commit()
    flash(u'Proyector agregado exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA AGREGAR ELEMENTO DE BIBLIOTECA
@app.route("/addLibrary", methods=['POST'])
def addLibrary():
    code = request.form['codeLibrary']
    description = request.form['descriptionLibrary']
    serie = request.form['serieLibrary']
    marca = request.form['marcaLibrary']
    model = request.form['modelLibrary']
    propiedad = request.form['propertyLibrary']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO library (code, description, serie, marca, model, property, status) VALUES (%s, %s, %s, %s, %s, %s, %s) ",
                (code, description, serie, marca, model, propiedad, 'A'))
    mysql.connection.commit()
    flash(u'Elemento agregado exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA ACTUALIZAR LIBRO
@app.route("/updateBook/<string:id>", methods=['POST'])
def updateBook(id):
    if request.method == 'POST':
        name = request.form['nameBook']
        author = request.form['authorBook']
        editorial = request.form['editorialBook']
        yearEdition = request.form['yearEdition']
        unidadMed = request.form['unidadMedida']
        materia = request.form['materia']
        campoConocim = request.form['campoConocim']
        estadoFisico = request.form['estadoFisico']
        dateInput = request.form['dateInput']
        responsable = request.form['responsable']
        observations = request.form['observations']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE books
                SET tittle = %s,
                author = %s,
                editorial = %s,
                yearEdition = %s,
                unidadMedida = %s,
                materia = %s,
                campoConocimiento = %s,
                estadoFisico = %s,
                dateInput = %s,
                responsable = %s,
                observations = %s
            WHERE code = %s
        """, (name, author, editorial, yearEdition, unidadMed, materia, campoConocim, estadoFisico, dateInput, responsable, observations, id))
        mysql.connection.commit()
        flash(u'Libro actualizado exitosamente', 'success')
        return redirect(url_for('inventory'))

# FUNCION PARA ACTUALIZAR ELEMENTO DE AUDIOVISUAL
@app.route("/updateAudiovisual/<string:id>", methods=['POST'])
def updateAudiovisual(id):
    if request.method == 'POST':
        description = request.form['descriptionAudio']
        serie = request.form['serieAudio']
        marca = request.form['marcaAudio']
        model = request.form['modelAudio']
        propiedad = request.form['propertyAudio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE audiovisualRoom
                SET description = %s,
                serie = %s,
                marca = %s,
                model = %s,
                property = %s
            WHERE code = %s
        """, (description, serie, marca, model, propiedad, id))
    mysql.connection.commit()
    flash(u'Elemento actualizado exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA ACTUALIZAR ELEMENTO DE BILIOTECA
@app.route("/updateLibrary/<string:id>", methods=['POST'])
def updateLibrary(id):
    if request.method == 'POST':
        description = request.form['descriptionLibrary']
        serie = request.form['serieLibrary']
        marca = request.form['marcaLibrary']
        model = request.form['modelLibrary']
        propiedad = request.form['propertyLibrary']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE library
                SET description = %s,
                serie = %s,
                marca = %s,
                model = %s,
                property = %s
            WHERE code = %s
        """, (description, serie, marca, model, propiedad, id))
    mysql.connection.commit()
    flash(u'Elemento actualizado exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA ACTUALIZAR PROYECTOR
@app.route("/updateProjector/<string:id>", methods=['POST'])
def updateProjector(id):
    if request.method == 'POST':
        description = request.form['descriptionProjector']
        serie = request.form['serieProjector']
        marca = request.form['marcaProjector']
        model = request.form['modelProjector']
        propiedad = request.form['propertyProjector']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE projectors
                SET description = %s,
                serie = %s,
                marca = %s,
                model = %s,
                property = %s
            WHERE code = %s
        """, (description, serie, marca, model, propiedad, id))
    mysql.connection.commit()
    flash(u'Proyector actualizado exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA ELIMINAR LIBRO
@app.route("/deleteInv/<id>")
def deleteInv(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE code = %s", [id])
    mysql.connection.commit()
    flash(u'Libro removido exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA ELIMINAR ELEMENTO DE AUDIOVISUAL
@app.route("/deleteAudiovisual/<id>")
def deleteAudio(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM audiovisualRoom WHERE code = %s", [id])
    mysql.connection.commit()
    flash(u'Elemento removido exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA ELIMINAR ELEMENTO DE BIBLIOTECA
@app.route("/deleteLibrary/<id>")
def deleteLibrary(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM library WHERE code = %s", [id])
    mysql.connection.commit()
    flash(u'Elemento removido exitosamente', 'success')
    return redirect(url_for('inventory'))

# FUNCION PARA ELIMINAR PROYECTOR
@app.route("/deleteProjector/<id>")
def deleteProjector(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM projectors WHERE code = %s", [id])
    mysql.connection.commit()
    flash(u'Proyector removido exitosamente', 'success')
    return redirect(url_for('inventory'))


# VISITS ########################################################
@app.route("/visits")
def visits():
    if g.user:
        import datetime
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM visitors")
        data = cur.fetchall()
        return render_template('visits.html', visitors=data, fechaActual=hoy)
    else:
        flash(u'Inicia nuevamente !!!', 'error')
        return redirect(url_for('login'))

# FUNCION PARA AGREGAR VISITAS
@app.route("/addVisitor", methods=['POST'])
def addVisitor():
    date = request.form['dateInput']
    grade = request.form['grade']
    group = request.form['group']
    name = request.form['name']
    asunto = request.form['asunto']
    matricula = request.form['matricula']
    carrera = request.form['carrera']
    sexo = request.form['sexo']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO visitors (date, grade, grupo, name, asunto, matricula, carrera, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (date, grade, group, name, asunto, matricula, carrera, sexo))
    mysql.connection.commit()
    flash(u'Visita agregada exitosamente', 'success')
    return redirect(url_for('visits'))

# FUNCION PARA EDITAR VISITAS
@app.route("/editVisitor/<id>", methods=['POST'])
def editVisitor(id):
    date = request.form['dateInput']
    grade = request.form['grade']
    grupo = request.form['group']
    name = request.form['name']
    asunto = request.form['asunto']
    matricula = request.form['matricula']
    carrera = request.form['carrera']
    sexo = request.form['sexo']
    cur = mysql.connection.cursor()
    cur.execute(
        """UPDATE visitors
            SET date = %s,
                grade = %s,
                grupo = %s,
                name = %s,
                asunto = %s,
                matricula = %s,
                carrera = %s,
                sexo = %s
            WHERE id = %s
        """, (date, grade, grupo, name, asunto, matricula, carrera, sexo, id))
    mysql.connection.commit()
    flash(u'Visita actualizada exitosamente', 'success')
    return redirect(url_for('visits'))

# FUNCION PARA ELIMINAR VISITAS
@app.route("/deleteVisitor/<id>")
def deleteVisitor(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM visitors WHERE id = %s", [id])
    mysql.connection.commit()
    flash(u'Visita removida exitosamente', 'success')
    return redirect(url_for('visits'))

# CARDS ########################################################
@app.route("/cards")
def cards():
    if g.user:
        import datetime
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tableTempCardTable")
        dataMobiliario = cur.fetchall()
        return render_template('cards.html', fechaActual=hoy, prestamo=dataMobiliario)
    else:
        flash(u'Inicia nuevamente !!!', 'error')
        return redirect(url_for('login'))


@app.route("/addTableTemp", methods=['POST'])
def addTableTemp():
    cant = request.form['cantidad']
    description = request.form['description']
    code = request.form['code']
    marca = request.form['marca']
    import datetime
    dateLoan = datetime.date.today().strftime("%Y-%m-%d")
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tableTempCardTable (cant, description, code, marca, dateLoan) VALUES(%s, %s, %s, %s, %s)",
                (cant, description, code, marca, dateLoan))
    mysql.connection.commit()
    flash(u'Añadido exitosamente !!!', 'success')
    return redirect(url_for('cards'))

# FUNCION PARA AGREGAR DATOS DE UNA TARJETA DE PRESTAMO DE LIBRO A ALUMNOS
@app.route("/addCardBookAlumn", methods=['POST'])
def addCardBookAlumn():
    name = request.form['nameAlumn']
    materia = request.form['matterAlumn']
    carrera = request.form['areaAlumn']
    semestre = request.form['grade']
    grupo = request.form['group']
    codeBook = request.form['codeBook']
    tittleBook = request.form['nameBook']
    authorBook = request.form['authorBook']
    dateLoan = request.form['dateLoan']
    dateDelivery = request.form['dateDelivery']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cardBookAlumn (name, materia, carrera, semestre, grupo, codeBook, tittleBook, authorBook, dateLoan, dateDelivery, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (name, materia, carrera, semestre, grupo, codeBook, tittleBook, authorBook, dateLoan, dateDelivery, 'D'))
    cur.execute("""
            UPDATE books
                SET status = %s
            WHERE code = %s
            """, ('D', codeBook))

    mysql.connection.commit()

    data = ['', name, materia, carrera, semestre, grupo,
            codeBook, tittleBook, authorBook, dateLoan, dateDelivery]
    flash(u'Tarjeta creada exitosamente', 'success')
    return render_template('cardBookAlumn.html', data=data)

# FUNCION PARA AGREGAR DATOS DE UNA TARJETA DE PRESTAMO DE LIBRO A PERSONAL DOCENTE O ADMINISTRATIVO
@app.route("/addCardBookTeacher", methods=['POST'])
def addCardBooTeacher():
    name = request.form['nameTeacher']
    codeBook = request.form['codeBook']
    tittleBook = request.form['nameBook']
    authorBook = request.form['authorBook']
    genderBook = request.form['genderBook']
    dateLoan = request.form['dateLoan']
    dateDelivery = request.form['dateDelivery']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cardBookTeacher (name, codeBook, tittleBook, authorBook, genderBook, dateLoan, dateDelivery, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, codeBook, tittleBook, authorBook, genderBook, dateLoan, dateDelivery, 'D'))
    cur.execute("""
            UPDATE books
                SET status = %s
            WHERE code = %s
            """, ('D', codeBook))
    mysql.connection.commit()
    data = ['', name, codeBook, tittleBook,
            authorBook, genderBook, dateLoan, dateDelivery]
    flash(u'Tarjeta creada exitosamente', 'success')
    return render_template('cardBookTeacher.html', data=data)

# FUNCION PARA AGREGAR DATOS DE UNA TARJETA DE PRESTAMO DE PROYECTOR
@app.route("/addCardProjector", methods=['POST'])
def addCardProjector():
    code = request.form['code']
    projectorInfo = request.form['projectorInfo']
    cargoSolic = request.form['cargoSolic']
    nameSolic = request.form['nameSolic']
    mattAct = request.form['mattAct']
    grade = request.form['grade']
    group = request.form['group']
    aula = request.form['aula']
    dateLoan = request.form['dateLoan']
    hourLoan = request.form['hourLoan']
    hourDelivery = request.form['hourDelivery']
    noProjector = request.form['noProjector']

    try:
        check1 = request.form['check1']
    except:
        check1 = ""

    try:
        check2 = request.form['check2']
    except:
        check2 = ""

    try:
        check3 = request.form['check3']
    except:
        check3 = ""

    try:
        check4 = request.form['check4']
    except:
        check4 = ""

    try:
        check5 = request.form['check5']
    except:
        check5 = ""

    try:
        check6 = request.form['check6']
    except:
        check6 = ""

    try:
        check7 = request.form['check7']
    except:
        check7 = ""

    try:
        check8 = request.form['check8']
    except:
        check8 = ""

    try:
        check9 = request.form['check9']
    except:
        check9 = ""

    description = ""

    cheks = [check1, check2, check3, check4,
             check5, check6, check7, check8, check9]

    for check in cheks:
        if check != "":
            description = check + ", " + description

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cardProjector (descripcion, cargo, nombre, matAct, semestre, grupo, aula, fecha, horarioPrestamo, horarioEntrega, numero, componentes, status, code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (projectorInfo, cargoSolic, nameSolic, mattAct, grade, group, aula, dateLoan, hourLoan, hourDelivery, noProjector, description, 'D', code))

    cur.execute("""
            UPDATE projectors
                SET status = %s
            WHERE code = %s""", ('D', code))

    mysql.connection.commit()
    data = ['', projectorInfo, cargoSolic, nameSolic, mattAct, grade, group,
            aula, dateLoan, hourLoan, hourDelivery, noProjector, description, 'D', code]

    flash(u'Tarjeta creada exitosamente', 'success')
    return render_template('cardProjectors.html', data=data)

# ESCUCHADOR DE EVENTOS socketIO ---------------------------------
# @socketio.on('message')
# def handleMessage(msg, msg2, msg3, msg4, msg5):
#     print("Message: " + msg + msg2 + msg3 + msg4 + msg5)
#     send((msg, msg2, msg3, msg4, msg5), broadcast=True)


@app.route("/getmethod/<jsdata>")
def get_javascript_data(jsdata):
    values = jsdata.split(",")
    codes = []
    newCodes = []
    for data in values:
        print("|"+data+"|-"+str(len(data)))
        code = []
        for C in data:
            if C != " ":
                code.append(C)
        codes.append(code)
        code = []

    print("--- CODES ---")
    for code in codes:
        print(code)
        cadena = "".join(code)
        newCodes.append(cadena)

    print("--- NEW CODES ---")
    for code in newCodes:
        print(code)

    registros = []
    cur = mysql.connection.cursor()
    i = 0
    for code in newCodes:
        cur.execute("SELECT * FROM library WHERE code = '"+newCodes[i]+"';")
        registro = cur.fetchone()
        registros.append(registro)
        i = i + 1

    print("--- REGISTROS ---")
    for record in registros:
        print(record)

    import datetime
    dateLoan = datetime.date.today().strftime("%Y-%m-%d")

    for registro in registros:
        cur.execute("INSERT INTO tableTempCardTable (cant, description, code, marca, dateLoan) VALUES (%s, %s, %s, %s, %s)",
                    ("1", registro[1], registro[0], registro[3], dateLoan))
        mysql.connection.commit()
        flash(u'Elemento agregado exitosamente', 'success')

    return render_template('cards.html', pedido=registros)


@app.route("/deleteRecordTCM/<id>")
def deleteRecordTCM(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tableTempCardTable WHERE code = %s", [id])
    mysql.connection.commit()
    flash(u'Registro removido', 'success')
    return redirect(url_for('cards'))


@app.route("/addCardMobiliario", methods=['POST'])
def addCardMobiliario():
    responsable = request.form['nameResponsable']
    area = request.form['areaResponsable']
    ubication = request.form['DF']

    import datetime
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    dateHour = datetime.datetime.now()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tableTempCardTable")
    records = cur.fetchall()

    for dat in records:
        cur.execute("""UPDATE library
                        SET status = 'D'
                        WHERE code = %s""", [dat[2]])

    cur.execute(
        "INSERT INTO cardMobiliario(marcador, cant, description, code, marca, dateLoan, ubication, nameResponsable, areaResponsable) SELECT %s, cant, description, code, marca, dateLoan, %s, %s, %s FROM tableTempCardTable", [dateHour, ubication, responsable, area])

    cur.execute("INSERT INTO idCardMobiliario(marcador, dateLoan, nameResponsable, status, areaResponsable) VALUES (%s, %s, %s, %s, %s)", [
                dateHour, hoy, responsable, 'D', area])

    cur.execute("DELETE FROM tableTempCardTable WHERE cant = %s", ("1"))
    mysql.connection.commit()

    flash(u'Tarjeta creada exitosamente', 'success')
    return redirect(url_for('record'))


@app.route("/updateCardMobiliarioTemp/<id>", methods=['POST'])
def updateCardMobiliarioTemp(id):
    cant = request.form['cantidad']
    description = request.form['descriptionTempM']
    marca = request.form['marca']
    import datetime
    dateLoan = datetime.date.today().strftime("%Y-%m-%d")
    cur = mysql.connection.cursor()
    cur.execute(
        """UPDATE tableTempCardTable
            SET cant = %s,
                description = %s,
                marca = %s,
                dateLoan = %s
            WHERE code = %s
        """, (cant, description, marca, dateLoan, id))
    mysql.connection.commit()
    flash(u'Registro actualizado exitosamente', 'success')
    return redirect(url_for('cards'))

# RESERVATIONS #########################################################
@app.route("/reservations")
def reservations():
    if g.user:
        import datetime
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cardAudiovisual")
        dataEvents = cur.fetchall()

        data = []

        for result in dataEvents:
            hourStart = ""
            hourEnd = ""

            if str(result[2])[2] == ":":
                hourStart = str(result[2])
            else:
                hourStart = "0" + str(result[2])

            if str(result[4])[2] == ":":
                hourEnd = str(result[4])
            else:
                hourEnd = "0" + str(result[4])

            data.append({
                'code': result[0],
                'title': result[8],
                'start': str(result[1])+"T"+hourStart,
                'end': str(result[3])+"T"+hourEnd,
                'hourStart': hourStart,
                'hourEnd': hourEnd,
                'name': result[5],
                'department': result[6],
                'conditions': result[7],
                'color': result[9]
            })

        with open("static/json/events.json", "w") as file:
            json.dump(data, file, indent=4)
        return render_template('reservations.html', fechaActual=hoy)
    else:
        flash(u'Inicia nuevamente !!!', 'error')
        return redirect(url_for('login'))


@app.route("/data")
def return_data():
    with open("static/json/events.json", "r") as input_data:
        return input_data.read()


@app.route("/addReservation", methods=['POST'])
def addReservation():
    dateLoan = request.form['dateLoan']
    hourLoan = request.form['hourLoan']
    dateDelivery = request.form['dateDelivery']
    hourDelivery = request.form['hourDelivery']
    name = request.form['name']
    department = request.form['department']
    conditionsInput = request.form['conditionsInput']
    activities = request.form['activities']
    color = request.form['inputColor']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cardAudiovisual (dateLoan, hourLoan, dateDelivery, hourDelivery, name, department, conditionsInput, activities, color, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (dateLoan, hourLoan, dateDelivery, hourDelivery, name, department, conditionsInput, activities, color, 'A'))
    mysql.connection.commit()
    flash(u'Evento agregado', 'success')
    return redirect(url_for('reservations'))


@app.route("/updateReservation/<id>", methods=['POST'])
def updateReservation(id):
    dateLoan = request.form['dateLoan']
    hourLoan = request.form['hourLoan']
    dateDelivery = request.form['dateDelivery']
    hourDelivery = request.form['hourDelivery']
    name = request.form['name']
    department = request.form['department']
    conditionsInput = request.form['conditionsInput']
    activities = request.form['activities']
    color = request.form['inputColor']
    cur = mysql.connection.cursor()
    cur.execute(
        """UPDATE cardAudiovisual
            SET dateLoan = %s,
                hourLoan = %s,
                dateDelivery = %s,
                hourDelivery = %s,
                name = %s,
                department = %s,
                conditionsInput = %s,
                activities = %s,
                color = %s
            WHERE id = %s""",
        (dateLoan, hourLoan, dateDelivery, hourDelivery, name, department, conditionsInput, activities, color, id))
    mysql.connection.commit()
    flash(u'Evento actualizado', 'success')
    return redirect(url_for('reservations'))


@app.route("/deleteReservation/<id>", methods=['POST'])
def deleteReservation(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cardAudiovisual WHERE code = %s", [id])
    mysql.connection.commit()
    flash(u'Evento removido exitosamente', 'success')
    return redirect(url_for('reservations'))

# GRAPH #########################################################
@app.route("/newGraph", methods=['POST', 'GET'])
def newGraph():
    if g.user:
        import datetime

        primerAnio = 0
        ultimoAnio = int(datetime.date.today().strftime("%Y"))

        primerMes = 0
        ultimoMes = int(datetime.date.today().strftime("%m"))

        primerMes = ultimoMes - 6
        primerAnio = ultimoAnio
        if primerMes <= 0:
            primerMes = 13 + primerMes
            primerAnio = ultimoAnio - 1

        Pmes = str(primerMes)
        Umes = str(ultimoMes)

        if len(Pmes) < 2:
            Pmes = "0" + Pmes
        else:
            Pmes = Pmes

        if len(Umes) < 2:
            Umes = "0" + Umes
        else:
            Umes = Umes

        print(">>> Primer Mes: " + Pmes)
        print(">>> Ultimo Mes: " + Umes)

        meses = []

        fechas = {}
        fechas['inicio'] = []
        fechas['fin'] = []

        if primerMes < ultimoMes:
            primerMes = primerMes + 1
            while primerMes <= ultimoMes:
                if primerMes == 1:
                    meses.append("Enero")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-01-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-01-32")
                if primerMes == 2:
                    meses.append("Febrero")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-02-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-02-32")
                if primerMes == 3:
                    meses.append("Marzo")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-03-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-03-32")
                if primerMes == 4:
                    meses.append("Abril")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-04-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-04-32")
                if primerMes == 5:
                    meses.append("Mayo")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-05-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-05-32")
                if primerMes == 6:
                    meses.append("Junio")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-06-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-06-32")
                if primerMes == 7:
                    meses.append("Julio")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-07-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-07-32")
                if primerMes == 8:
                    meses.append("Agosto")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-08-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-08-32")
                if primerMes == 9:
                    meses.append("Septiembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-09-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-09-32")
                if primerMes == 10:
                    meses.append("Octubre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-10-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-10-32")
                if primerMes == 11:
                    meses.append("Noviembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-11-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-11-32")
                if primerMes == 12:
                    meses.append("Diciembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-12-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-12-32")
                primerMes = primerMes + 1
        else:
            while primerMes < 13:
                if primerMes == 1:
                    meses.append("Enero")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-01-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-01-32")
                if primerMes == 2:
                    meses.append("Febrero")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-02-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-02-32")
                if primerMes == 3:
                    meses.append("Marzo")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-03-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-03-32")
                if primerMes == 4:
                    meses.append("Abril")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-04-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-04-32")
                if primerMes == 5:
                    meses.append("Mayo")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-05-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-05-32")
                if primerMes == 6:
                    meses.append("Junio")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-06-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-06-32")
                if primerMes == 7:
                    meses.append("Julio")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-07-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-07-32")
                if primerMes == 8:
                    meses.append("Agosto")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-08-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-08-32")
                if primerMes == 9:
                    meses.append("Septiembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-09-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-09-32")
                if primerMes == 10:
                    meses.append("Octubre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-10-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-10-32")
                if primerMes == 11:
                    meses.append("Noviembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-11-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-11-32")
                if primerMes == 12:
                    meses.append("Diciembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-12-01")
                    fechas["fin"].append(
                        datetime.date.today().strftime("%Y")+"-12-32")
                primerMes = primerMes + 1
            primerMes = 0
            while primerMes <= ultimoMes:
                if primerMes == 1:
                    meses.append("Enero")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-01-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-01-32")
                if primerMes == 2:
                    meses.append("Febrero")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-02-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-02-32")
                if primerMes == 3:
                    meses.append("Marzo")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-03-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-03-32")
                if primerMes == 4:
                    meses.append("Abril")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-04-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-04-32")
                if primerMes == 5:
                    meses.append("Mayo")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-05-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-05-32")
                if primerMes == 6:
                    meses.append("Junio")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-06-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-06-32")
                if primerMes == 7:
                    meses.append("Julio")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-07-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-07-32")
                if primerMes == 8:
                    meses.append("Agosto")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-08-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-08-32")
                if primerMes == 9:
                    meses.append("Septiembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-09-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-09-32")
                if primerMes == 10:
                    meses.append("Octubre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-10-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-10-32")
                if primerMes == 11:
                    meses.append("Noviembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-11-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-11-32")
                if primerMes == 12:
                    meses.append("Diciembre")
                    fechas["inicio"].append(
                        datetime.date.today().strftime("%Y")+"-12-01")
                    fechas["fin"].append(
                        str(int(datetime.date.today().strftime("%Y"))-1)+"-12-32")
                primerMes = primerMes + 1

        primerFecha = str(primerAnio) + "-" + Pmes + "-01"
        ultimaFecha = datetime.date.today().strftime("%Y-%m-%d")
        print(">>> Primera Fecha: " + primerFecha)
        print(">>> Ultimoa Fecha: " + ultimaFecha)

        print("---MESES---")
        for months in meses:
            print(months)

        print("---FECHAS---")
        for i in fechas:
            print(fechas[i])

        # LLENAR ARCHIVOS JSON CON CATEGORIAS Y SERIES
        lista = []
        for mes in meses:
            lista.append(mes)

        with open("static/json/categories.json", "w") as file:
            json.dump(lista, file, indent=4)

        try:
            parametro1 = request.form['param1']
        except:
            return redirect(url_for('graph'))

        try:
            parametro2 = request.form['param2']
        except:
            return redirect(url_for('graph'))

        Lparam1 = parametro1.split(",")
        Lparam2 = parametro2.split(",")

        cadClave1 = Lparam1[0]
        valor1 = Lparam1[1]
        cadClave2 = Lparam2[0]
        valor2 = Lparam2[1]

        print("VVVVALORESSSSSSSS")
        print(cadClave1)
        print(valor1)
        print(cadClave2)
        print(valor2)

        clave1 = ''
        clave2 = ''
        lista1 = []
        lista2 = []

        asuntos = ['Sala de lectura', 'PC', 'Taller', 'Actividad externa']
        semestres = [1, 2, 3, 4, 5, 6]
        carreras = ['Programacion', 'Soporte',
                    'Alimentos', 'Electricidad', 'Procesos']
        grupos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        sexos = ['Hombre', 'Mujer']

        if cadClave1 == 'Asunto':
            clave1 = 'asunto'
            lista1.extend(asuntos)
        if cadClave1 == 'Semestre':
            clave1 = 'grade'
            lista1.extend(semestres)
        if cadClave1 == 'Carrera':
            clave1 = 'carrera'
            lista1.extend(carreras)
        if cadClave1 == 'Grupo':
            clave1 = 'grupo'
            lista1.extend(grupos)
        if cadClave1 == 'Sexo':
            clave1 = 'sexo'
            lista1.extend(sexos)

        if cadClave2 == 'Asunto':
            clave2 = 'asunto'
            lista2.extend(asuntos)
        if cadClave2 == 'Semestre':
            clave2 = 'grade'
            lista2.extend(semestres)
        if cadClave2 == 'Carrera':
            clave2 = 'carrera'
            lista2.extend(carreras)
        if cadClave2 == 'Grupo':
            clave2 = 'grupo'
            lista2.extend(grupos)
        if cadClave2 == 'Sexo':
            clave2 = 'sexo'
            lista2.extend(sexos)

        print("---DATOS INICIALES---")
        print(clave1)
        print(clave2)
        print(lista1)
        print(lista2)

        cur = mysql.connection.cursor()
        values = [[], [], [], [], [], [], [], [], [], [], [], []]

        u = len(lista1)
        v = 0

        while v < u:
            x = 0
            while x < 6:
                cur.execute('SELECT count(*) FROM visitors WHERE date BETWEEN %s AND %s AND '+clave1 +
                            ' = %s AND '+clave2+' = %s', (fechas['inicio'][x], fechas['fin'][x], lista1[v], valor2))
                dataRecord = cur.fetchone()
                values[v].append(dataRecord[0])
                x = x + 1
            v = v + 1

        print(",,,,,VALUES,,,,,")
        for value in values:
            print(value)

        data = []
        z = len(lista1)
        w = 0

        while w < z:
            data.append({
                'name': lista1[w],
                'data': values[w]
            })
            w = w + 1

        with open("static/json/series.json", "w") as file:
            json.dump(data, file, indent=4)

        cadenaInfo = 'Mostrando todas las visitas de todos los tipos de ('+cadClave1 + \
            ') donde ('+cadClave2 + ' = '+valor2+') en los últimos 6 meses'
        return render_template('graph.html', information=cadenaInfo)
    else:
        flash(u'Inicia nuevamente !!!', 'error')
        return redirect(url_for('login'))


@app.route("/graph")
def graph():
    if g.user:
        return render_template('graph.html')
    else:
        flash(u'Inicia nuevamente !!!', 'error')
        return redirect(url_for('login'))


@app.route("/series1")
def series1():
    with open("static/json/series1.json", "r") as input_data:
        return input_data.read()


@app.route("/series2")
def series2():
    with open("static/json/series2.json", "r") as input_data:
        return input_data.read()


@app.route("/categories")
def categories():
    with open("static/json/categories.json", "r") as input_data:
        return input_data.read()


@app.route("/series")
def series():
    with open("static/json/series.json", "r") as input_data:
        return input_data.read()

# RECORD ########################################################
@app.route("/record")
def record():
    if g.user:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cardBookAlumn')
        dataCardBookAlumn = cur.fetchall()
        cur.execute('SELECT * FROM cardBookTeacher')
        dataCardBookTeacher = cur.fetchall()
        cur.execute('SELECT * FROM idCardMobiliario')
        dataCardMobiliario = cur.fetchall()
        cur.execute('SELECT * FROM cardProjector')
        dataCardProjector = cur.fetchall()
        cur.execute('SELECT * FROM cardAudiovisual')
        dataCardAudiovisual = cur.fetchall()
        return render_template('record.html', cardBookAlumn=dataCardBookAlumn, cardBookTeacher=dataCardBookTeacher, cardMobiliario=dataCardMobiliario, cardProjector=dataCardProjector, cardAudiovisual=dataCardAudiovisual)
    else:
        flash(u'Inicia nuevamente !!!', 'error')
        return redirect(url_for('login'))

# GENERATOR CARDS ########################################################
@app.route("/generatingStudentBookCard/<id>")
def generatingStudentBookCard(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cardBookAlumn WHERE id = "' + id + '"')
    data = cur.fetchone()
    return render_template('cardBookAlumn.html', data=data)


@app.route("/deliveryAlumnBook/<codeBook>/<codeRecord>")
def deliveryAlumnBook(codeBook, codeRecord):
    cur = mysql.connection.cursor()
    cur.execute("""
            UPDATE books
                SET status = %s
            WHERE code = %s
            """, ('A', codeBook))
    cur.execute("""
            UPDATE cardBookAlumn
                SET status = %s
            WHERE id = %s
            """, ('A', codeRecord))
    mysql.connection.commit()
    flash(u'Liberación de libro exitosa', 'success')
    return redirect(url_for('record'))


@app.route("/generatingTeacherBookCard/<id>")
def generatingTeacherBookCard(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cardBookTeacher WHERE id = "' + id + '"')
    data = cur.fetchone()
    return render_template('cardBookTeacher.html', data=data)


@app.route("/deliveryTeacherBook/<codeBook>/<codeRecord>")
def deliveryTeacherBook(codeBook, codeRecord):
    cur = mysql.connection.cursor()
    cur.execute("""
            UPDATE books
                SET status = %s
            WHERE code = %s
            """, ('A', codeBook))
    cur.execute("""
            UPDATE cardBookTeacher
                SET status = %s
            WHERE id = %s
            """, ('A', codeRecord))
    mysql.connection.commit()
    flash(u'Liberación de libro exitosa', 'success')
    return redirect(url_for('record'))


@app.route("/generatingMobiliarioCard/<marcador>")
def generatingMobiliarioCard(marcador):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM cardMobiliario WHERE marcador = %s', [marcador])
    data = cur.fetchall()
    return render_template('cardMobiliario.html', data=data)


@app.route("/deliveryMobiliario/<marcador>")
def deliveryMobiliario(marcador):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM cardMobiliario WHERE marcador = %s", [marcador])
    data = cur.fetchall()
    for dat in data:
        cur.execute("""
                UPDATE library
                    SET status = %s
                WHERE code = %s""", ['A', dat[4]])

    cur.execute("""
            UPDATE idCardMobiliario
                SET status = %s
            WHERE marcador = %s
            """, ('A', marcador))

    mysql.connection.commit()
    flash(u'Liberación de mobiliario exitosa', 'success')
    return redirect(url_for('record'))


@app.route("/generatingProjectorCard/<id>")
def generatingProjectorCard(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cardProjector WHERE id = "' + id + '"')
    data = cur.fetchone()
    return render_template('cardProjectors.html', data=data)


@app.route("/deliveryProjector/<codeProjector>/<codeRecord>")
def deliveryProjector(codeProjector, codeRecord):
    cur = mysql.connection.cursor()
    cur.execute("""
            UPDATE projectors
                SET status = %s
            WHERE code = %s
            """, ('A', codeProjector))
    cur.execute("""
            UPDATE cardProjector
                SET status = %s
            WHERE id = %s
            """, ('A', codeRecord))
    mysql.connection.commit()
    flash(u'Liberación exitosa', 'success')
    return redirect(url_for('record'))


@app.route("/generatingAudiovisualCard/<id>")
def generatingAudiovisualCard(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cardAudiovisual WHERE id = "' + id + '"')
    data = cur.fetchone()
    import datetime
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    return render_template('cardAudiovisual.html', data=data, fechaActual=hoy)


@app.route("/deliveryAudiovisual/<code>")
def deliveryAudiovisual(code):
    cur = mysql.connection.cursor()
    cur.execute("""
            UPDATE cardAudiovisual
                SET status = %s
            WHERE id = %s""", ('A', code))
    mysql.connection.commit()
    flash(u'Liberación exitosa', 'success')
    return redirect(url_for('record'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    # socketio.run(app, debug=True)
