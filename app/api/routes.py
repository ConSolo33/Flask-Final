
from flask import Blueprint, request, jsonify
from models import db, User, Prompt, Prompt_schema, Prompts_schema
from flask_login import current_user
from helpers import id_required

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/prompts', methods = ['POST'])
@id_required
def create_prompt(current_user_id):
    title = request.json['title']
    date = request.json['date']
    idea = request.json['idea']
    user_id = current_user_id.user_id

    prompt = Prompt(title, date, idea, user_id = user_id)

    db.session.add(prompt)
    db.session.commit()

    response = Prompt_schema.dump(prompt)
    return jsonify(response)

@api.route('/prompts', methods = ['GET'])
@id_required
def get_all_prompts(current_user_id):
    a_user = current_user_id.user_id
    prompts = Prompt.query.filter_by(user_id = a_user).all()
    response = Prompts_schema.dump(prompts)
    return jsonify(response)

@api.route('/prompts/<id>', methods = ['GET'])
@id_required
def get_single_prompt(current_user_id, id):
    prompt = Prompt.query.get(id)
    response = Prompt_schema.dump(prompt)
    return jsonify(response)

@api.route('/prompts/<id>', methods = ['POST', 'PUT'])
@id_required
def update_prompt(current_user_id, id):
    prompt = Prompt.query.get(id)
    prompt.title = request.json['title']
    prompt.date = request.json['date']
    prompt.idea = request.json['idea']
    prompt.user_id = current_user_id.user_id

    db.session.commit()
    response = Prompt_schema.dump(prompt)
    return jsonify(response)

@api.route('/prompts/<id>', methods = ['DELETE'])
@id_required
def delete_prompt(current_user_id, id):
    prompt = Prompt.query.get(id)
    db.session.delete(prompt)
    db.session.commit()
    response = Prompt_schema.dump(prompt)
    return jsonify(response)