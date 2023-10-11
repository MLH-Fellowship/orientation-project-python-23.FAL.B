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

experience_required_fields = set(["title", "company", "start_date",
                                  "end_date", "description", "logo"])

education_required_fields = set(["course", "school", "start_date",
                                 "end_date", "grade", "logo"])

skill_required_fields = set(["name", "proficiency", "logo"])

# Function to dynamically check required fields and build
# a response with all the missing required fields
def check_fields(data, required_fields):
    '''
    Check if all the required fields are present in the given data dictionary.
    '''
    # missing_fields is grounded on required_fields
    missing_fields = required_fields - set(data.keys())
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {missing_fields}"}), 400
    return None

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
        bad_fields = check_fields(content, experience_required_fields)
        if bad_fields:
            return bad_fields
        data["experience"].append(Experience(**content))
        return jsonify({"id": len(data["experience"]) - 1}), 201
    return jsonify({"message": "Invalid method"}), 405

@app.route('/resume/experience/<index>', methods=['PUT'])
def put_experience(index):
    '''
    Handle experience PUT requests
    Returns the updated experience resource
    '''
    # Check that a valid index was provided
    if not index.isdigit() or int(index) < 0 or int(index) >= len(data["experience"]):
        return jsonify({"message": "Invalid id"}), 400

    index = int(index)
    content = request.get_json()

    # Check that a valid body was provided
    if not request.json:
        return jsonify({"message": "Request body must be JSON"}), 400

    # Update each field for the experience at the given index
    for field in content.keys():
        if content[field]:
            setattr(data["experience"][index], field, content[field])
    return jsonify(data["experience"][index]), 200

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

@app.route('/resume/education', methods=['DELETE'])
def delete_education():
    """
    Handles education DELETE requests
    """
    if request.get_json():
        id_data = request.get_json()
        index = id_data["id"]
        if -1 < index < len(data["education"]):
            del data["education"][index]
        else:
            return jsonify({"message":"Index is out of bounds"}), 400
    return jsonify({"message":"Inavlid method"}), 405
@app.route('/resume/education', methods=['POST'])
def post_education():
    '''
    Handles education POST requests
    '''
    if request.get_json():
        education_data = request.get_json()
        bad_fields = check_fields(education_data, education_required_fields)
        if bad_fields:
            return bad_fields
        for value in education_data.values():
            if value is None:
                return jsonify({"message":"Mandatory fields are missing"}), 400
        data['education'].append(Education(**education_data))
        return jsonify({"id":len(data["education"])-1})
    return jsonify({"message":"Invalid data recieved"}), 400



@app.route('/resume/education/<index>', methods=['PUT'])
def put_education(index):
    '''
    Handle education PUT requests
    Returns the updated education resource
    '''
    # Check that a valid index was provided
    if not index.isdigit() or int(index) < 0 or int(index) >= len(data["education"]):
        return jsonify({"message": "Invalid id"}), 400

    index = int(index)
    content = request.get_json()

    # Check that a valid body was provided
    if not request.json:
        return jsonify({"message": "Request body must be JSON"}), 400

    # Update each field for the education at the given index
    for field in content.keys():
        if content[field]:
            setattr(data["education"][index], field, content[field])

    return jsonify(data["education"][index]), 200

@app.route('/resume/skill', methods=['GET'])
def get_skill():
    '''
    Handles GET skill requests
    '''
    index = request.args.get("id")
    if index:
        if index.isdigit() and 0 <= int(index) < len(data["skill"]):
            return jsonify(data["skill"][int(index)])
        return jsonify({"message": "Invalid index"}), 400
    return jsonify(data.get('skill', []))

@app.route('/resume/skill', methods=['POST'])
def post_skill():
    '''
    Handles POST skill requests
    '''
    if not request.json:
        return jsonify({"message": "Request body must be JSON"}), 400
    
    bad_fields = check_fields(request.json, skill_required_fields)
    if bad_fields:
        return bad_fields

    new_skill = Skill(request.json['name'],
                        request.json['proficiency'],
                        request.json['logo'])
    data['skill'].append(new_skill)
    return jsonify({"id": len(data['skill']) - 1})

@app.route('/resume/skill/<index>', methods=['PUT'])
def put_skill(index):
    '''
    Handle skill PUT requests
    Returns the updated skill resource
    '''
    # Check that a valid index was provided
    if not index.isdigit() or int(index) < 0 or int(index) >= len(data["skill"]):
        return jsonify({"message": "Invalid id"}), 400

    index = int(index)
    content = request.get_json()

    # Check that a valid body was provided
    if not request.json:
        return jsonify({"message": "Request body must be JSON"}), 400

    # Update each field for the skill at the given index
    for field in content.keys():
        if content[field]:
            setattr(data["skill"][index], field, content[field])

    return jsonify(data["skill"][index]), 200
