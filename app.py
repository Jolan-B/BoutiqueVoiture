#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

from flask import session, g
import pymysql.cursors


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host='localhost',  # serveurhost
            user='root',  # jbertin4
            password='Jfast88!04',  # mdp
            database='Sujet4',  # BDD_jbertin4
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exeption):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ########################################################### Sujet  4

# ACCUEIL

@app.route('/')
def show_accueil():
    return render_template('layout.html')


# ACCUEIL


# CATÉGORIE

@app.route('/categorie/show')
def show_categorie():
    mycursor = get_db().cursor()

    sqlCategorie = '''
    SELECT 
        Categorie.idCategorie AS id,
        Categorie.nomCategorie AS nom,
        Categorie.catalogueCategorie AS catalogue,
        Categorie.photoCategorie AS photo
    FROM Categorie
    ORDER BY Categorie.idCategorie
    '''

    mycursor.execute(sqlCategorie)
    Categories = mycursor.fetchall()

    return render_template('categorie/show_categorie.html', Categories=Categories)


@app.route('/categorie/add', methods=['GET'])
def add_categorie():
    return render_template('categorie/add_categorie.html')


@app.route('/categorie/add', methods=['POST'])
def valid_add_categorie():
    nom = request.form.get('libelleCategorie', '')
    catalogue = int(request.form.get('catalogue', ''))
    photo = request.form.get('logo', '')

    mycursor = get_db().cursor()
    tuple_param = (nom, catalogue, photo)

    print(tuple_param)

    sql = '''
    INSERT INTO Categorie(idCategorie,nomCategorie,catalogueCategorie,photoCategorie)
    VALUES(NULL,%s,%s,%s)
    '''

    mycursor.execute(sql, tuple_param)
    get_db().commit()

    # print(u' Catégorie ajoutée , libellé :', nom,'---- catalogue' , catalogue , '- logo',photo)
    # message = u'Catégorie ajoutée , libellé : '+nom+',     catalogue : ' + catalogue + ',     logo : '+photo
    # flash(message, 'alert-success')

    return redirect('/categorie/show')


@app.route('/categorie/confirm_delete')
def confirm_delete_categorie():
    id = int(request.args.get('id'))
    print(id)

    mycursor = get_db().cursor()
    sqlCategorie = '''
    SELECT
        Categorie.idCategorie AS id,
        Categorie.nomCategorie AS nom
    FROM Categorie
    WHERE idCategorie=%s
    '''

    mycursor.execute(sqlCategorie, id)
    Categorie = mycursor.fetchone()

    mycursor = get_db().cursor()
    sqlVoitures = '''
    SELECT 
        Voiture.idVoiture AS id,
        Voiture.nomVoiture AS nom
    FROM Voiture
    WHERE Voiture.id_categorie=%s
    ORDER BY Voiture.idVoiture;
    '''
    mycursor.execute(sqlVoitures, id)
    Voitures = mycursor.fetchall()
    print("LES VOITURES AFFECTÉES SONT : ", Voitures)

    return render_template('categorie/delete_categorie.html', Voitures=Voitures, Categorie=Categorie, id=id)


@app.route('/categorie/delete', methods=['GET'])
def delete_categorie():
    id = request.args.get('id')
    print(type(id))
    print(id)

    mycursor = get_db().cursor()
    sqlDeleteCascade = '''
    DELETE
    FROM Voiture
    WHERE Voiture.id_categorie=%s;
    '''

    mycursor.execute(sqlDeleteCascade, id)
    get_db().commit()

    mycursor = get_db().cursor()
    sqlDeleteCategori = '''
    DELETE 
    FROM Categorie
    WHERE idCategorie=%s;
    '''

    mycursor.execute(sqlDeleteCategori, id)
    get_db().commit()

    # print ("une catégorie supprimée, categorie_id :",categorie_id)
    # message=u'Catégorie supprimée, id : ' + categorie_id
    # flash(message, 'alert-warning')
    return redirect('/categorie/show')


@app.route('/categorie/edit', methods=['GET'])
def edit_categorie():
    id = request.args.get('id')

    print(id)

    mycursor = get_db().cursor()
    sqlBase = '''
    SELECT 
        Categorie.idCategorie AS id,
        Categorie.nomCategorie AS nom,
        Categorie.catalogueCategorie AS catalogue,
        Categorie.photoCategorie AS photo
    FROM Categorie
    WHERE Categorie.idCategorie=%s;
    '''
    mycursor.execute(sqlBase, id)
    Base = mycursor.fetchone()

    print(Base)

    return render_template('categorie/edit_categorie.html', Base=Base)


@app.route('/categorie/edit', methods=['POST'])
def valid_edit_categorie():
    id = int(request.form.get('id'))
    nom = request.form.get('nom')
    catalogue = int(request.form.get('catalogue'))
    photo = request.form.get('photo')

    tuple_param = (nom, catalogue, photo, id)

    mycursor = get_db().cursor()
    sql = '''
    UPDATE Categorie
    SET nomCategorie=%s,catalogueCategorie=%s,photoCategorie=%s
    WHERE Categorie.idCategorie=%s;
    '''

    mycursor.execute(sql, tuple_param)
    get_db().commit()

    # print(u'catégorie modifiée, categorie_id: ',categorie_id, " libelleCategorie :", libelleCategorie ,'---- catalogue' , catalogue , '- logo',logo)
    # message=u'Catégorie modifiée, id : ' + categorie_id + ",     libelle : " + libelleCategorie +',     catalogue : ' + catalogue + ',     logo : '+logo
    # flash(message, 'alert-success')
    return redirect('/categorie/show')


# CATÉGORIE


# VOITURE

@app.route('/voiture/show', methods=['GET'])
def show_voiture():
    mycursor = get_db().cursor()

    sqlVoiture = '''
    SELECT 
        Voiture.idVoiture as id,
        Voiture.nomVoiture as nom,
        Voiture.dateLancementVoiture as date,
        Voiture.prixVoiture as prix,
        Voiture.puissanceVoiture as puissance,
        Voiture.photoVoiture as photo,
        Categorie.nomCategorie as categorie
        
    FROM Voiture
    INNER JOIN 
        Categorie ON Voiture.id_categorie = Categorie.idCategorie
    ORDER BY 
        Voiture.idVoiture;
    '''

    mycursor.execute(sqlVoiture)
    Voitures = mycursor.fetchall()

    return render_template('voiture/show_voiture.html', Voitures=Voitures)


@app.route('/voiture/add', methods=['GET'])
def add_voiture():
    mycursor = get_db().cursor()

    sqlCategorie = '''
    SELECT 
        Categorie.idCategorie AS id,
        Categorie.nomCategorie AS nom
    FROM Categorie
    ORDER BY 
        Categorie.idCategorie;
    '''
    mycursor.execute(sqlCategorie)
    Categories = mycursor.fetchall()

    print(Categories)

    return render_template('voiture/add_voiture.html', Categories=Categories)


@app.route('/voiture/add', methods=['POST'])
def valid_add_voiture():
    nom = request.form.get('nomVoiture', '')
    date = request.form.get('dateLancement', '')
    idCategorie = request.form.get('categorie_id', '')
    prix = int(request.form.get('prixVoiture', ''))
    puissance = int(request.form.get('puissance', ''))
    photo = request.form.get('photo', '')

    mycursor = get_db().cursor()
    tuple_param = (nom, date, prix, puissance, photo, idCategorie)
    print(tuple_param)

    sql = '''
    INSERT INTO Voiture(idVoiture,nomVoiture,dateLancementVoiture,prixVoiture,puissanceVoiture,photoVoiture,id_categorie)
    VALUES (NULL,%s,%s,%s,%s,%s,%s)
    '''

    mycursor.execute(sql, tuple_param)
    get_db().commit()

    # message = u'Voiture ajoutée , nom: ',nom ,  ',     dateLancement : ',date, ',     categorie_id : ' , str(idCategorie) , ',     prixVoiture: ' , prix ,  '€,     puissance: ', puissance , 'CV,    photo: ' , photo
    # print(message)
    # flash(message, 'alert-success')

    return redirect('/voiture/show')


@app.route('/voiture/delete', methods=['GET'])
def delete_voiture():
    id = int(request.args.get('id'))

    mycursor = get_db().cursor()
    sqlDelete = '''
    DELETE
    FROM Voiture
    WHERE idVoiture=%s;
    '''
    mycursor.execute(sqlDelete, id)
    get_db().commit()

    # id = request.args.get('id', '')
    # message=u'Voiture supprimée, id : ' + id
    # flash(message, 'alert-warning')
    return redirect('/voiture/show')


@app.route('/voiture/edit', methods=['GET'])
def edit_voiture():
    id = int(request.args.get('id'))
    print("L ID EST ", id)

    mycursor = get_db().cursor()
    sqlBase = '''
    SELECT 
        Voiture.idVoiture as id,
        Voiture.nomVoiture as nom,
        Voiture.dateLancementVoiture as date,
        Voiture.prixVoiture as prix,
        Voiture.puissanceVoiture as puissance,
        Voiture.photoVoiture as photo,
        Categorie.idCategorie as idCategorie,
        Categorie.nomCategorie as categorie
    FROM Voiture
    INNER JOIN Categorie ON Voiture.id_categorie = Categorie.idCategorie
    WHERE Voiture.idVoiture = %s;    
    '''

    mycursor.execute(sqlBase, id)
    Base = mycursor.fetchone()
    print("LES VALEURS DE BASE SONT : ", Base)

    mycursor = get_db().cursor()

    sqlCategories = '''
    SELECT 
        Categorie.idCategorie AS id,
        Categorie.nomCategorie as nom
    FROM Categorie;
    '''

    mycursor.execute(sqlCategories)
    Categories = mycursor.fetchall()
    print("LES VAEURS DISPO SONT : ", Categories)

    return render_template('voiture/edit_voiture.html', Base=Base, Categories=Categories)


@app.route('/voiture/edit', methods=['POST'])
def valid_edit_voiture():
    id = int(request.form.get('id'))
    nom = request.form.get('nomVoiture')
    date = request.form.get('dateLancement')
    categorie = int(request.form.get('categorie_id'))
    prix = float(request.form.get('prixVoiture'))
    puissance = int(request.form.get('puissance'))
    photo = request.form.get('photo')

    tuple_param = (nom, date, categorie, prix, puissance, photo, id)

    mycursor = get_db().cursor()
    sqlVoiture = '''
    UPDATE Voiture 
    SET nomVoiture=%s,
        dateLancementVoiture=%s,
        id_categorie=%s,
        prixVoiture=%s,
        puissanceVoiture=%s,
        photoVoiture=%s
    WHERE 
        idVoiture=%s;
    '''

    mycursor.execute(sqlVoiture, tuple_param)
    get_db().commit()

    return redirect('/voiture/show')


# VOITURE


# ETAT

@app.route('/etat/show')
def show_etat():
    mycursor = get_db().cursor()
    sqlAll = '''
    SELECT 
        SUM(Voiture.prixVoiture) as prix,
        COUNT(Voiture.idVoiture) as nbModele
    FROM Voiture;
    '''
    mycursor.execute(sqlAll)
    EtatCategorie = mycursor.fetchone()

    mycursor = get_db().cursor()
    sqlEtat = '''
    SELECT
        DISTINCT Categorie.idCategorie AS id,
        Categorie.nomCategorie AS nom,
        COUNT(Voiture.idVoiture) AS nbModele,
        SUM(Voiture.prixVoiture) as prix

    FROM 
        Categorie
    LEFT JOIN Voiture ON Voiture.id_categorie=Categorie.idCategorie
    GROUP BY Categorie.idCategorie;
    '''
    mycursor.execute(sqlEtat)
    Categories = mycursor.fetchall()
    # print(Categories)

    mycursor = get_db().cursor()
    sqlPuissance = '''
    SELECT 
    Voiture.puissanceVoiture as puissance,
    COUNT(Voiture.puissanceVoiture) as nbModele,
    ROUND(SUM(Voiture.prixVoiture)/(Voiture.puissanceVoiture*COUNT(Voiture.puissanceVoiture)),2) as prixCV
    FROM Voiture
    GROUP BY Voiture.puissanceVoiture
    ORDER BY ROUND(SUM(Voiture.prixVoiture)/(Voiture.puissanceVoiture*COUNT(Voiture.puissanceVoiture)),2);
    '''
    mycursor.execute(sqlPuissance)
    EtatPuissance = mycursor.fetchall()
    # print(EtatPuissance)

    mycursor = get_db().cursor()
    sqlPuissanceTot = '''
    SELECT 
        SUM(Voiture.puissanceVoiture) as nbCV,
        ROUND(SUM(Voiture.prixVoiture)/(SUM(Voiture.puissanceVoiture)),2) as prixMoyenCV
    FROM Voiture
    '''
    mycursor.execute(sqlPuissanceTot)
    PuissanceTot = mycursor.fetchone()
    # print("PUISSANCE TOT EST : ", PuissanceTot)

    tranchePrix = [0, 25000, 50000, 75000, 100000]
    mycursor = get_db().cursor()
    sqlPrix = '''
    SELECT
        COUNT(Voiture.idVoiture) as nbModele,
        ROUND(SUM(Voiture.puissanceVoiture)/(COUNT(Voiture.idVoiture)),2) as cvMoyen,
        ROUND(SUM(Voiture.prixVoiture)/(COUNT(Voiture.idVoiture)),2) as prixMoyen
    FROM Voiture
    WHERE Voiture.prixVoiture <= 25000;
    '''
    mycursor.execute(sqlPrix)
    Prix = mycursor.fetchall()
    Prix[0]['prixInf'] = tranchePrix[0]
    Prix[0]['prixSup'] = tranchePrix[1]

    mycursor = get_db().cursor()
    sqlPrix = '''
    SELECT
        COUNT(Voiture.idVoiture) as nbModele,
        ROUND(SUM(Voiture.puissanceVoiture)/(COUNT(Voiture.idVoiture)),2) as cvMoyen,
        ROUND(SUM(Voiture.prixVoiture)/(COUNT(Voiture.idVoiture)),2) as prixMoyen
    FROM Voiture
    WHERE Voiture.prixVoiture < 50000 && Voiture.prixVoiture > 25000;
    '''
    mycursor.execute(sqlPrix)
    Prix += mycursor.fetchall()
    Prix[1]['prixInf'] = tranchePrix[1]
    Prix[1]['prixSup'] = tranchePrix[2]

    mycursor = get_db().cursor()
    sqlPrix = '''
    SELECT
        COUNT(Voiture.idVoiture) as nbModele,
        ROUND(SUM(Voiture.puissanceVoiture)/(COUNT(Voiture.idVoiture)),2) as cvMoyen,
        ROUND(SUM(Voiture.prixVoiture)/(COUNT(Voiture.idVoiture)),2) as prixMoyen
    FROM Voiture
    WHERE Voiture.prixVoiture < 75000 && Voiture.prixVoiture > 50000;
    '''
    mycursor.execute(sqlPrix)
    Prix += mycursor.fetchall()
    Prix[2]['prixInf'] = tranchePrix[2]
    Prix[2]['prixSup'] = tranchePrix[3]

    mycursor = get_db().cursor()
    sqlPrix = '''
    SELECT
        COUNT(Voiture.idVoiture) as nbModele,
        ROUND(SUM(Voiture.puissanceVoiture)/(COUNT(Voiture.idVoiture)),2) as cvMoyen,
        ROUND(SUM(Voiture.prixVoiture)/(COUNT(Voiture.idVoiture)),2) as prixMoyen
    FROM Voiture
    WHERE Voiture.prixVoiture >= 100000;
    '''
    mycursor.execute(sqlPrix)
    Prix += mycursor.fetchall()
    Prix[3]['prixInf'] = tranchePrix[3]
    Prix[3]['prixSup'] = tranchePrix[4]
    # print("REPARTITION DES PRIX ", Prix)

    mycursor = get_db().cursor()
    sqlEtatPrix = '''
    SELECT
        ROUND(SUM(Voiture.prixVoiture)/(COUNT(Voiture.idVoiture)),2) as prixMoyen
    FROM Voiture;
    '''
    mycursor.execute(sqlEtatPrix)
    EtatPrix = mycursor.fetchone()
    # print(EtatPrix)

    return render_template('/etat/show_etat.html', EtatCategorie=EtatCategorie, Categories=Categories,
                           Puissances=EtatPuissance, EtatPuissance=PuissanceTot, Prix=Prix, EtatPrix=EtatPrix)


# ETAT


# FILTRE

@app.route('/voiture/filtre', methods=['GET', 'POST'])
def show_filtre():
    mycursor = get_db().cursor()

    sqlCategorie = '''
    SELECT 
        Categorie.idCategorie AS id,
        Categorie.nomCategorie AS nom
    FROM Categorie
    ORDER BY 
        Categorie.idCategorie;
    '''
    mycursor.execute(sqlCategorie)
    Categories = mycursor.fetchall()

    nomVoiture = request.form.get('nomVoiture', '')
    print("LE MODÈLE RECHERCHÉ EST : ", nomVoiture)
    prixMin = (request.form.get('prixMin', ""))
    prixMax = (request.form.get('prixMax', ""))
    print("LE PRIX MIN EST : ", prixMin)
    print("LE PRIX MAX EST : ", prixMax)
    categorie = request.form.getlist('categorie', None)
    print("LA LISTE DE CATÉGORIES EST : ", categorie)

    session['categorie'] = []

    if (nomVoiture and nomVoiture != ""):
        session['nomVoiture'] = nomVoiture

    if (prixMin or prixMax):
        if (prixMin != ""):
            session['prixMin'] = prixMin

        if (prixMax != ""):
            session['prixMax'] = prixMax

    if (categorie and categorie != []):
        for i in categorie:
            session['categorie'].append(int(i))

    print("LA SESSION EST : ", session)

    mycursor = get_db().cursor()
    sqlVoiture = '''
    SELECT 
        Voiture.nomVoiture as nom,
        Voiture.prixVoiture as prix,
        Voiture.puissanceVoiture as puissance,
        Voiture.photoVoiture as photo,
        Categorie.nomCategorie as categorie
    FROM Voiture
    INNER JOIN 
        Categorie ON Voiture.id_categorie = Categorie.idCategorie
    WHERE 1 = 1
'''

    if 'nomVoiture' in session:
        sqlVoiture += f" AND Voiture.nomVoiture LIKE '%{session['nomVoiture']}%' "

    if (session.get('prixMin')):
        sqlVoiture += f" AND Voiture.prixVoiture >= {session['prixMin']} "

    if (session.get('prixMax')):
        sqlVoiture += f" AND Voiture.prixVoiture <= {session['prixMax']} "

    if (session.get('categorie')):
        print(session['categorie'][0])
        sqlVoiture += f" AND ( Voiture.id_categorie = {session['categorie'][0]}"
        for id in session['categorie']:
            sqlVoiture += f" OR Voiture.id_categorie = {id} "
        sqlVoiture += f")"

    sqlVoiture += f";"

    mycursor.execute(sqlVoiture)
    Voitures = mycursor.fetchall()

    # print(Voitures)

    return render_template('/voiture/front_voiture_filtre_show.html', Categories=Categories, Voitures=Voitures)


@app.route('/voiture/delete_filtre', methods=['GET', 'POST'])
def delete_filtre():
    session.pop('nomVoiture', None)
    session.pop('prixMin', None)
    session.pop('prixMax', None)
    session.pop('categorie', None)
    print("LA SESSION DEL : ", session)
    return redirect('/voiture/filtre')


# FILTRE


if __name__ == '__main__':
    app.run(debug=True, port=5000)
