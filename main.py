import json

from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from graphene import ObjectType, String, Int, Field, List, Enum, Schema, Argument

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)


class PersonModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    address_number = db.Column(db.Integer, nullable=False)
    address_street = db.Column(db.String(120), nullable=False)
    address_city = db.Column(db.String(120), nullable=False)
    address_state = db.Column(db.String(2), nullable=False)


class StateEnum(Enum):
    CA = "CA"
    NY = "NY"
    TX = "TX"
    FL = "FL"
    # more states here


class Address(ObjectType):
    number = Int(required=True)
    street = String(required=True)
    city = String(required=True)
    state = StateEnum(required=True)


class Person(ObjectType):
    email = String(required=True)
    name = String(required=True)
    address = Field(Address)


class Query(ObjectType):
    people = List(Person)
    person = Field(Person, email=Argument(String, required=True))

    def resolve_people(root, info):
        people = PersonModel.query.all()
        return [convert_person(person) for person in people]


def convert_person(person):
    return {
        'email': person.email,
        'name': person.name,
        'address': {
            'number': person.address_number,
            'street': person.address_street,
            'city': person.address_city,
            'state': person.address_state,
        }
    }


schema = Schema(query=Query)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


def load_data_to_db():
    # Clear the table
    PersonModel.query.delete()

    with open('data.json') as f:
        data = json.load(f)
    for person_data in data:
        address = person_data['address']
        person = PersonModel(email=person_data['email'], name=person_data['name'],
                             address_number=address['number'], address_street=address['street'],
                             address_city=address['city'], address_state=address['state'])
        db.session.add(person)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        load_data_to_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
