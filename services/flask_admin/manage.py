from flask.cli import FlaskGroup

from project import app, db
from project.models import User

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

@cli.command("reset_db")
def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="michael@mherman.org"))
    db.session.commit()

if __name__ == "__main__":
    cli()
