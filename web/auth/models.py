from flask import request

from web.extensions import db
from web.settings import AUTH_SESSION_COOKIE_NAME


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, unique=True, nullable=False)
    access_token = db.Column(db.String(512), unique=False, nullable=False)
    expires_at = db.Column(db.Integer, unique=False, nullable=False)
    refresh_token = db.Column(db.String(512), unique=False, nullable=False)
    header = db.Column(db.String(512), unique=False, nullable=False)
    payload = db.Column(db.String(512), unique=False, nullable=False)
    signature = db.Column(db.String(512), unique=False, nullable=False)
    name = db.Column(db.String(256), unique=False, nullable=False)
    character_id = db.Column(db.Integer, unique=False, nullable=False)
    corporation_id = db.Column(db.Integer, unique=False, nullable=False)
    alliance_id = db.Column(db.Integer, unique=False, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def is_authenticated(self):
        return self.query.filter_by(session_id=request.cookies.get(AUTH_SESSION_COOKIE_NAME)).first() is not None

    def get_portrait_url(self, size=512):
        if size not in [64, 128, 256, 512]:
            size = 512
        return f'https://images.evetech.net/characters/{self.character_id}/portrait?tenant=tranquility&size={size}'

    def has_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return False
        permissions = Permission.query.filter_by(role_id=role.id).all()
        for permission in permissions:
            if permission.entity_id in [self.character_id, self.corporation_id, self.alliance_id]:
                return True
        else:
            return False

    def get_current_user(self):
        return self.query.filter_by(session_id=request.cookies.get(AUTH_SESSION_COOKIE_NAME)).first()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.String(120), db.ForeignKey('role.id'), nullable=False)
    entity_name = db.Column(db.String(120), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    role = db.relationship('Role', backref=db.backref('entities', lazy='select'))

    def __repr__(self):
        return f'{self.role}:{self.entity_name}'
