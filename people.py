# -*- coding: utf-8 -*-

from flask import (
    make_response,
    abort
)

from config import db
from models import (
    Person,
    PersonSchema
)


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:    json string of list of people
    """
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()

    person_schema = PersonSchema(many=True)
    return person_schema.dump(people).data


def read_one(person_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:        person matching id
    """
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is not None:
        person_schema = PersonSchema()
        return person_schema.dump(person).data

    else:
        abort(404, 'Person not found for Id {person_id}'.format(
            person_id=person_id))


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data

    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    lname = person.get('lname')
    fname = person.get('fname')

    existing_person = Person.query \
        .filter(Person.fname == fname) \
        .filter(Person.lname == lname) \
        .one_or_none()

    if existing_person is None:

        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        db.session.add(new_person)
        db.session.commit()

        return schema.dump(new_person).data, 201

    else:
        abort(409, f'Person {fname} {lname} exists already')


def update(person_id, person):
    """
    This function updates an existing person in the people structure

    :param person_id:   Id of the person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    update_person = Person.query \
        .filter(Person.person_id == person_id) \
        .one_or_none()

    if update_person is not None:

        schema = PersonSchema()
        update = schema.load(person, session=db.session).data

        update.id = update_person.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_person).data

        return data, 200

    else:
        abort(404, 'Person not found for Id: {person_id}'.format(
            person_id=person_id))


def delete(person_id):
    """
    This function deletes a person from the people structure

    :param person_id:   Id of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response('Person {person_id} deleted'.format(
            person_id=person_id), 200)

    else:
        abort(404, 'Person not found for Id: {person_id}'
              .format(person_id=person_id))
