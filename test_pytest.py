'''
Tests in Pytest
'''
from app import app


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience

def test_delete_experience():
    '''
    Create a new experience and then delete it.
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/experience',
                                        json=example_experience).json['id']

    response = app.test_client().delete('/resume/experience',json={"id":item_id})
    assert response.status_code == 200
    assert response.json['message'] == "Experience deleted"

def test_put_experience():
    '''
    Add a new experience, update a field in the experience, then get all experiences. 
    
    Check that it returns the updated experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    new_experience = app.test_client().put('/resume/experience/'+str(item_id),
                                           json={"end_date": "October 2023"}).json
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == new_experience


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']
    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == example_education
    app.test_client().delete('/resume/education',json={"id":item_id})
    response_two = app.test_client().get('/resume/education')
    assert len(response_two.get_json()) != len(response.get_json())

def test_put_education():
    '''
    Add a new education, update a field in the education, then get all education resources. 
    
    Check that it returns the updated education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']
    new_education = app.test_client().put('/resume/education/'+str(item_id),
                                           json={"end_date": "October 2023"}).json
    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == new_education


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill
    #tests the delete_skill() function
    app.test_client().delete('/resume/skill',json={"id":item_id})
    response_two = app.test_client().get('/resume/skill')
    assert len(response_two.get_json()) != len(response.get_json())

def test_put_skill():
    '''
    Add a new skill, update a field in the skill, then get all skill resources. 
    
    Check that it returns the updated skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']
    new_skill = app.test_client().put('/resume/skill/'+str(item_id),
                                           json={"proficiency": "10 years"}).json
    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == new_skill



def test_skill_missing_data():
    '''
    Add a new skill with missing data and check that
    it returns a 400 error
    '''
    example_skill = {
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/skill',
                                      json=example_skill)
    assert response.status_code == 400


def test_education_missing_data():
    '''
    Add a new education with missing data and check that
    it returns a 400 error
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/education',
                                      json=example_education)
    assert response.status_code == 400


def test_experience_missing_data():
    '''
    Add a new experience with missing data and check that
    it returns a 400 error
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/experience',
                                      json=example_experience)
    assert response.status_code == 400