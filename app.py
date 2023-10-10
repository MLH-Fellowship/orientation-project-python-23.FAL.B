'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill, Contact

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
    ],
    "contact":
        Contact("Mike Swift",
                "+12129876543",
                "mike@example.com")
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



@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify(data["education"])

    if request.method == 'POST':
        if request.get_json():
            education_data = request.get_json()
            for value in education_data.values():
                if value is None:
                    return jsonify({"message":"Mandatory fields are missing"}), 400
            data['education'].append(Education(**education_data))
            return jsonify({"id":len(data["education"])-1})
        return jsonify({"message":"Invalid data recieved"}), 400
    return jsonify({"message":"Inavlid method"}), 405


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


# Route for Contact GET & PUT retrieves and updates contact information
@app.route('/resume/contact', methods=['GET', 'PUT'])
def contact():
    '''
    Handles Contact requests
    '''
    if request.method == 'GET':
        # GET request that returns the contact information or a message if none is found
        return jsonify(data.get('contact', {"message": "No contact information found"}))

    if request.method == 'PUT':
        # PUT request that updates the contact information and returns the updated information
        content = request.json
        if not content:
            # If the JSON is missing, return a 400 error with a message
            return jsonify({"message": "The JSON is missing"}), 400
        modified = False
        for field, value in content.items():
            # For each field in the JSON, check if it exists and update it if it does
            if hasattr(data['contact'], field) and value:
                setattr(data['contact'], field, value)
                modified = True
        if modified:
            # If the contact information was modified, return the updated information
            return jsonify(data.get('contact', {}))
        # If no modifications were made, return a 400 error with a message
        return jsonify({"message": "Fields were the same or invalid"}), 400
    # If an invalid method is used, return a 405 error with a message
    return jsonify({"message": "Invalid method"}), 405
