from app.database import db


class Language(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<Language {self.name}>"

    @classmethod
    def create(cls, name):
        language = cls(name=name)
        db.session.add(language)
        db.session.commit()
        return language

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        language = cls.query.get(id)
        if language:
            for key, value in kwargs.items():
                setattr(language, key, value)
            db.session.commit()
        return language

    @classmethod
    def delete(cls, id):
        language = cls.query.get(id)
        if language:
            db.session.delete(language)
            db.session.commit()
        return language

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
