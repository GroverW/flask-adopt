from flask import Flask, redirect, render_template
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm
import requests
from secrets import bearer_token

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
    petfinder = get_petfinder_pet()

    return render_template('index.html', pets=pets, petfinder=petfinder)


@app.route('/<int:petid>', methods=['GET', 'POST'])
def show_pet_page(petid):
    """Page where people can view and edit pet"""
    pet = Pet.query.get(petid)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data or None
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        return redirect('/')

    return render_template('pet_details.html', pet=pet, form=form)


@app.route('/add', methods=['GET', 'POST'])
def show_add_pet_form():
    """Page shows add pet form, and validates submissions."""
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


def get_petfinder_pet():
    response = requests.get('https://api.petfinder.com/v2/animals?sort=random&limit=1',
                            headers={'Authorization': f'Bearer {bearer_token}'})

    json_animal = response.json()
    animal = json_animal['animals'][0]

    animal_atts = {'name': animal['name'],
                   'species': animal['species'],
                   'age': animal['age'],
                   'description': animal['description'],
                   'photourl': animal['photos'][0]['medium'],
                   'status': animal['status']}

    return animal_atts


