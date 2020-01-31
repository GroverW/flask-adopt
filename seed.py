from models import db, Pet
from app import app

db.drop_all()
db.create_all()

parsley = Pet(
            name="Parsley",
            species="Cat",
            photo_url=None,
            age=2,
            notes="",
            available=False)
pimento = Pet(
            name="Pimento",
            species="Cat",
            photo_url=None,
            age=2,
            notes="",
            available=True)
cheddar = Pet(
            name="Cheddar",
            species="Cat",
            photo_url=None,
            age=2,
            notes="",
            available=True)

db.session.add_all([parsley, pimento, cheddar])

db.session.commit()