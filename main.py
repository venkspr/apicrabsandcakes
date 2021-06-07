import os
from flask import Flask, render_template, request
from flask_cors import CORS

from random import choice
import openai
import json

web_site = Flask(__name__)
CORS(web_site)
prompt_seed = "Q: Fetch unique values of DEPARTMENT from Worker table.\nA: Select distinct DEPARTMENT from Worker;\nQ: Print the first three characters of FIRST_NAME from Worker table.\nA: Select substring(FIRST_NAME,1,3) from Worker;\nQ: Find the position of the alphabet ('a') in the first name column 'Amitabh' from Worker table.\nA: Select INSTR(FIRST_NAME, BINARY'a') from Worker where FIRST_NAME = 'Amitabh';\nQ: Print the FIRST_NAME from Worker table after replacing 'a' with 'A'.\nA: Select CONCAT(FIRST_NAME, ' ', LAST_NAME) AS 'COMPLETE_NAME' from Worker;\nQ: Display the second highest salary from the Worker table.\nA: Select max(Salary) from Worker where Salary not in (Select max(Salary) from Worker);\nQ: Fetch the count of employees working in the department Admin.\nA: SELECT COUNT(*) FROM worker WHERE DEPARTMENT = 'Admin';.\nQ: "
number_list = [
    100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307,
    400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
    416, 417, 418, 421, 422, 423, 424, 425, 426, 429, 431, 444, 450, 451, 500,
    502, 503, 504, 506, 507, 508, 509, 510, 511, 599
]

openai.api_key = os.environ['api_key']


def search(prmp):
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


@web_site.route('/')
def index():
    return render_template('index.html')


@web_site.route('/app/')
# @web_site.route('/app/<username>')
def generate_user():
    question = request.args.get('question')
    # print(search(request.args.get('username')))
    # return render_template('personal_user.html', user=username)
    if not question:
        return 'Invalid request'

    response = web_site.response_class(response=json.dumps(
        (search(request.args.get('question')))),
                                       status=200,
                                       mimetype='application/json')
    return response


@web_site.route('/page')
def random_page():
    return render_template('page.html', code=choice(number_list))


web_site.run(host='0.0.0.0', port=8080)
