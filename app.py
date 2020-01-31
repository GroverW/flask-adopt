from flask import Flask, redirect, render_template, request
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'alskdjf094r'

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


@app.route('/')
def home_page():
    pets = Pet.query.all()

    return render_template('index.html', pets=pets)


@app.route('/<int:petid>', methods=['GET', 'POST'])
def pet_page(petid):
    pet = Pet.query.get(petid)
    form = EditPetForm()

    print("********************pet", pet, "form", form)

    return render_template('pet_details.html', pet=pet, form=form)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data or None
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(
                    name=name,
                    species=species,
                    photo_url=photo_url,
                    age=age,
                    notes=notes)

        db.session.add(new_pet)
        db.session.commit()

        return redirect('/')

    return render_template('add_pet.html', form=form)
