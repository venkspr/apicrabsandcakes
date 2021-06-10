import os
from flask import Flask, render_template, request
from flask_cors import CORS
import openai
import json

web_site = Flask(__name__)
CORS(web_site)
prompt_seed = "Q: Fetch unique values of DEPARTMENT from Worker table.\nA: Select distinct DEPARTMENT from worker;\nQ: Print the first three characters of FIRST_NAME from worker table.\nA: Select substring(first_name,1,3) from worker;\nQ: Find the position of the alphabet ('a') in the first name column 'Amitabh' from Worker table.\nA: select instr(first_name, BINARY'a') from worker where first_name = 'Amitabh';\nQ: Print the FIRST_NAME from worker table after replacing 'a' with 'A'.\nA: Select concat(first_name, ' ', last_name) AS 'complete_name' from worker;\nQ: Display the second highest salary from the Worker table.\nA: select max(salary) from worker where salary not in (select max(salary) from worker);\nQ: Fetch the count of employees working in the department Admin.\nQ: A: select count(*) FROM worker where department = 'ADMIN';.\nQ: Tell me the details of employees who makes highest salary. \nA: select * from worker where salary = ( select    max(salary) from worker ); \nQ: List details of unshipped orders. \nA: select * from orders where status!='shipped'; \nQ: List details of shipped orders to london. \nA: select * from orders where status = 'shipped' and ucase(city)='LONDON'; \nQ:List all the orders shipped to london which were classic cars. \nA: select * from orders where status = 'shipped' and ucase(city) = 'LONDON' and ucase(product_category) = ucase('classic car'); \nQ: list all worker who are male/ \nA: select * from worker where gender = 'M'; \nQ: "

prompt_react = "Q: Generate primary button.\nA: <button type='button' class='btn btn-primary'>Primary</button>\nQ: Generate a form with input username, password, checkbox and submit button. \A: <form> <div class='form-group'> <label for='email'>Email address</label> <input type='email' class='form-control' id='email' aria-describedby='emailHelp' placeholder='Enter email'> <small id='emailHelp' class='form-text text-muted'>We'll never share your email with anyone else.</small> </div> <div class='form-group'> <label for='password'>Password</label> <input type='password' class='form-control' id='password' placeholder='Password'> </div> <div class='form-check'> <input type='checkbox' class='form-check-input' id='checkbox'> <label class='form-check-label' for='chehckbox'>Check me out</label> </div> <button type='submit' class='btn btn-primary'>Submit</button> </form> \nQ: "
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
                                        max_tokens=200,
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
