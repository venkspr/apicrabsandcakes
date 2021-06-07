import os
from flask import Flask, render_template, request
from flask_cors import CORS
from random import choice
import openai
import json

web_site = Flask(__name__)
CORS(web_site)
prompt_seed = "Q: Fetch unique values of DEPARTMENT from Worker table.\nA: Select distinct DEPARTMENT from Worker;\nQ: Print the first three characters of FIRST_NAME from Worker table.\nA: Select substring(FIRST_NAME,1,3) from Worker;\nQ: Find the position of the alphabet ('a') in the first name column 'Amitabh' from Worker table.\nA: Select INSTR(FIRST_NAME, BINARY'a') from Worker where FIRST_NAME = 'Amitabh';\nQ: Print the FIRST_NAME from Worker table after replacing 'a' with 'A'.\nA: Select CONCAT(FIRST_NAME, ' ', LAST_NAME) AS 'COMPLETE_NAME' from Worker;\nQ: Display the second highest salary from the Worker table.\nA: Select max(Salary) from Worker where Salary not in (Select max(Salary) from Worker);\nQ: Fetch the count of employees working in the department Admin.\nA: SELECT COUNT(*) FROM worker WHERE DEPARTMENT = 'Admin';.\nQ: "

prompt_react = "Q: Fetch unique values of DEPARTMENT from Worker table.\nA: Select distinct DEPARTMENT from Worker;\nQ: Print the first three characters of FIRST_NAME from Worker table.\nA: Select substring(FIRST_NAME,1,3) from Worker;\nQ: Find the position of the alphabet ('a') in the first name column 'Amitabh' from Worker table.\nA: Select INSTR(FIRST_NAME, BINARY'a') from Worker where FIRST_NAME = 'Amitabh';\nQ: Print the FIRST_NAME from Worker table after replacing 'a' with 'A'.\nA: Select CONCAT(FIRST_NAME, ' ', LAST_NAME) AS 'COMPLETE_NAME' from Worker;\nQ: Display the second highest salary from the Worker table.\nA: Select max(Salary) from Worker where Salary not in (Select max(Salary) from Worker);\nQ: Fetch the count of employees working in the department Admin.\nA: SELECT COUNT(*) FROM worker WHERE DEPARTMENT = 'Admin';.\nQ: "
openai.api_key = os.environ['api_key']


def sql(prmp):
    response = openai.Completion.create(engine="davinci",
                                        prompt=prompt_seed + prmp + ". \nA:",
                                        temperature=0.5,
                                        max_tokens=100,
                                        top_p=1.0,
                                        frequency_penalty=0.2,
                                        presence_penalty=0.0,
                                        stop=["\n"])
    # print(response)
    return response

def react_response(prmp):
    response = openai.Completion.create(engine="davinci",
                                        prompt=prompt_react + prmp + ". \nA:",
                                        temperature=0.5,
                                        max_tokens=100,
                                        top_p=1.0,
                                        frequency_penalty=0.2,
                                        presence_penalty=0.0,
                                        stop=["\n"])
    # print(response)
    return response

@web_site.route('/')
def index():
    return render_template('index.html')


@web_site.route('/app/')
# @web_site.route('/app/<username>')
def app():
    question = request.args.get('question')
    # print(search(request.args.get('username')))
    # return render_template('personal_user.html', user=username)
    if not question:
        return 'Invalid request'

    response = web_site.response_class(response=json.dumps(
        (sql(request.args.get('question')))),
                                       status=200,
                                       mimetype='application/json')
    return response

@web_site.route('/react/')
# @web_site.route('/app/<username>')
def react():
    question = request.args.get('question')
    # print(search(request.args.get('username')))
    # return render_template('personal_user.html', user=username)
    if not question:
        return 'Invalid request'

    response = web_site.response_class(response=json.dumps(
        (react_response(request.args.get('question')))),
                                       status=200,
                                       mimetype='application/json')
    return response
web_site.run(host='0.0.0.0', port=8080)
