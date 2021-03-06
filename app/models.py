from datetime import datetime
import random
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import login_manager
from barcode_gen import generate_barcode
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Permission:
    VIEW = 0x01
    ADD = 0x02
    EDIT = 0x04
    REMOVE = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.VIEW |
                     Permission.ADD |
                     Permission.EDIT, True),
            'Moderator': (Permission.VIEW |
                          Permission.ADD |
                          Permission.EDIT |
                          Permission.REMOVE, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', backref='author', lazy='dynamic')

    @staticmethod
    def generate_fake(count=15):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_moderator(self):
        return self.can(Permission.EDIT) and self.can(Permission.REMOVE)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(24), unique=True)
    name = db.Column(db.String(24))
    count = db.Column(db.Integer)
    price = db.Column(db.Float)
    sn = db.Column(db.String(24), unique=True)
    barcode = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=50):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            bc_value = str(random.randrange(11111111, 99999999))
            u = User.query.offset(randint(0, user_count - 1)).first()
            it = Item(number=forgery_py.address.phone(),
                      name=forgery_py.lorem_ipsum.word(),
                      count=1,
                      price=10,
                      description=forgery_py.lorem_ipsum.sentence(),
                      timestamp=forgery_py.date.date(),
                      barcode=bc_value,
                      author_id=u.id)
            db.session.add(it)
            db.session.commit()
            generate_barcode(bc_value)

    def __repr__(self):
        return '<Item %r' % self.name

    @staticmethod
    def get_count():
        return Item.query.count()

    @staticmethod
    def get_items_id_list():
        items = Item.get_count()
        item_list = []
        for item in items:
            item_list.append(item.id)
        return item_list

    @staticmethod
    def get_items():
        return Item.query.all()


class Stocktake(db.Model):
    __tablename__ = 'stocktakes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    end_date = db.Column(db.DateTime, index=True)
    is_ended = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Stocktake %r' % self.name

    @staticmethod
    def generate_fake():
        from random import seed
        import forgery_py

        seed()
        st = Stocktake(name=forgery_py.lorem_ipsum.word(),
                       start_date=forgery_py.date.date())
        db.session.add(st)
        db.session.commit()


class StItem(db.Model):
    __tablename__ = 'stitems'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(24))
    name = db.Column(db.String(24))
    count = db.Column(db.Integer)
    price = db.Column(db.Float)
    sn = db.Column(db.String(24))
    barcode = db.Column(db.String(64))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    is_scanned = db.Column(db.Boolean, default=False)
    stocktake = db.Column(db.Integer, db.ForeignKey('stocktakes.id'))

    def __repr__(self):
        return '<StItem %r' % self.name
