from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from faker import Faker
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
#####################
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
#####################
import random
import datetime

db = SQLAlchemy()

# Definiera modeller för användare och roller
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  # Lägg till denna rad
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

# Sätt upp Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)



class Bok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(80), nullable=False)
    forfattare = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    pris = db.Column(db.Float, nullable=False)
    lagerantal = db.Column(db.Integer, nullable=False)
    bestallningsdetaljer = db.relationship('BestallningsDetalj', backref='bok', lazy=True)

class Kund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)
    epost = db.Column(db.String(120), unique=True, nullable=False)
    telefonnummer = db.Column(db.String(20), nullable=False)
    adress = db.Column(db.String(200), nullable=False)
    bestallningar = db.relationship('Bestallning', backref='kund', lazy=True)

class Bestallning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kund_id = db.Column(db.Integer, db.ForeignKey('kund.id'), nullable=False)
    bestallningsdatum = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    leveransstatus = db.Column(db.String(20), nullable=False)
    detaljer = db.relationship('BestallningsDetalj', backref='bestallning', lazy=True)

class BestallningsDetalj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bestallning_id = db.Column(db.Integer, db.ForeignKey('bestallning.id'), nullable=False)
    bok_id = db.Column(db.Integer, db.ForeignKey('bok.id'), nullable=False)
    antal = db.Column(db.Integer, nullable=False)
    pris_per_enhet = db.Column(db.Float, nullable=False)

class Tidningar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(80), nullable=False)
    forfattare = db.Column(db.String(50), nullable=False)
    pris = db.Column(db.Float, nullable=False)
    lagerantal = db.Column(db.Integer, nullable=False)

# Lägg till andra tabeller som Anställda här om det behövs


NR_OF_BOOKS = 100
NR_OF_CUSTOMERS = 300
NR_OF_ORDERS = 600
STARTDATE = datetime.datetime(2022,1,1,0,0,0)

def seed_data(app,db):

    # app.security = Security(app, user_datastore)

    if not Role.query.first():
        user_datastore.create_role(name='Admin')
        user_datastore.create_role(name='User')
        user_datastore.create_role(name='Cashier')
        db.session.commit()

    if not User.query.first():
        user_datastore.create_user(email='test@example.com', password=hash_password('password'), roles=['Admin','User'], confirmed_at=datetime.datetime.now())
        user_datastore.create_user(email='c@c.com', password=hash_password('password'), roles=['User'] ,confirmed_at=datetime.datetime.now())
        user_datastore.create_user(email='d@d.com', password=hash_password('password'), roles=['Admin'], confirmed_at=datetime.datetime.now())
        user_datastore.create_user(email='e@d.com', password=hash_password('password'), roles=['Cashier'],  confirmed_at=datetime.datetime.now())
        db.session.commit()


    fake = Faker()

    nr_of_books = Bok.query.count()

    if nr_of_books < NR_OF_BOOKS:
        for _ in range(NR_OF_BOOKS - nr_of_books):
            title = fake.catch_phrase()
            author = fake.name()
            isbn = fake.isbn13()
            price = random.randint(50, 400)
            inventory = random.randint(0, 10000)

            bok = Bok(titel=title,
                    forfattare=author,
                    isbn=isbn,
                    pris=price,
                    lagerantal=inventory)
            
            db.session.add(bok)
            db.session.commit()


    nr_of_customers = Kund.query.count()

    if nr_of_customers < NR_OF_CUSTOMERS:
        fake2 = Faker('sv_SE')  # Svensk lokaliseringsinställning
        epost_addresser = set()
        
        kunder = []
        while nr_of_customers < NR_OF_CUSTOMERS:
            kund = {
                "namn": fake2.name(),
                "adress": fake2.address(),
                # "epost": fake2.email(),
                "telefonnummer": fake2.phone_number()
            }
            nr_of_customers += 1
            kunder.append(kund)

        total_nr_of_new_customers = len(kunder)
        
        while total_nr_of_new_customers > 0:
            epost = fake2.email()            
            kunden_finns = Kund.query.filter_by(epost=epost).first()
            if kunden_finns or epost in epost_addresser:
                pass
            else:
                epost_addresser.add(epost)
                total_nr_of_new_customers -= 1            


        epost_addresser = list(epost_addresser)
        assert len(kunder) == len(epost_addresser)
        for kund in kunder:
                kund["epost"] = epost_addresser.pop()
                        
        for kund in kunder:
            db.session.add(Kund(**kund))
            db.session.commit()

    nr_of_orders = Bestallning.query.count()
    if nr_of_orders < NR_OF_ORDERS:
        kund_id = [k.id for k in Kund.query.all()]
        for _ in range(NR_OF_ORDERS - nr_of_orders):
            slump_kund = random.choice(kund_id)
            order_datum = fake.date_time_between_dates(STARTDATE)

            if (datetime.datetime.now() - order_datum).days < 8:
                status = 'Ej skickad'
            else:
                status = 'Skickad' if not int(random.gauss(mu=0,sigma=0.5)) else 'Annulerad'

            new_order = Bestallning(kund_id=slump_kund,
                                    bestallningsdatum=order_datum,
                                    leveransstatus=status)
            db.session.add(new_order)
            db.session.commit()

            nr_of_orderdetails = int(random.gauss(mu=3, sigma=1))

            if nr_of_orderdetails < 0: nr_of_orderdetails =1

            bok_id = Bok.query.all()
            for _ in range(nr_of_orderdetails):
                random_bok = random.choice(bok_id)
                orderdetail = BestallningsDetalj(bestallning_id = new_order.id,
                                                bok_id = random_bok.id,
                                                antal = random.randint(1,10),
                                                pris_per_enhet = random_bok.pris)

                db.session.add(orderdetail)
                db.session.commit()

