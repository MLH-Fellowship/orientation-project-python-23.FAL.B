'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        index = request.args.get('id')
        if index and index.isdigit():
            index = int(index)
            if 0 <= index < len(data["experience"]):
                return jsonify(data["experience"][index])
            return jsonify({"message": "Invalid id"}), 400
        return jsonify(data["experience"])

    if request.method == 'POST':
        content = request.get_json()
        required_fields = ["title", "company", "start_date", "end_date", "description", "logo"]
        if not content or any(field not in content for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400
        data["experience"].append(Experience(**content))
        return jsonify({"id": len(data["experience"]) - 1}), 201

    return jsonify({"message": "Invalid method"}), 405


@app.route('/resume/education', methods=['GET'])
def get_education():
    '''
    Handles education GET requests
    '''
    index = request.args.get("id")
    if index:
        if index.isdigit() and 0 <= int(index) < len(data["education"]):
            return jsonify(data["education"][int(index)])
        return jsonify({"message": "Invalid index"}), 400
    return jsonify(data["education"])


@app.route('/resume/education', methods=['POST'])
def post_education():
    '''
    Handles education POST requests
    '''
    if request.get_json():
        education_data = request.get_json()
        for value in education_data.values():
            if value is None:
                return jsonify({"message":"Mandatory fields are missing"}), 400
        data['education'].append(Education(**education_data))
        return jsonify({"id":len(data["education"])-1})
    return jsonify({"message":"Invalid data recieved"}), 400


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify(data.get('skill', []))

    if request.method == 'POST':
        required_fields = ['name', 'proficiency', 'logo']
        if not request.json:
            return jsonify({"message": "Request body must be JSON"}), 400
        for field in required_fields:
            if field not in request.json:
                return jsonify({"message": f"Your request is missing {field}."}), 400

        new_skill = Skill(request.json['name'],
                            request.json['proficiency'],
                            request.json['logo'])
        data['skill'].append(new_skill)
        return jsonify({"id": len(data['skill']) - 1})

    return jsonify({"message": "This Route only supports GET & POST"}), 405
