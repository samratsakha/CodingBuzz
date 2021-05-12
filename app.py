# Required Libraries
from flask import Flask, render_template, request, make_response
import jsonify
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

from requests.sessions import Request

# Googlesheets Authentication
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('codingbuzz_credentials.json',scope)
client = gspread.authorize(credentials)
sheet = client.open("codingbuzz_login_database").sheet1

app = Flask(__name__)


# compiler-API
# Recieve output from API
def recieve_raw_output(url,pass_data):
    try:
        r = requests.post(url, data=pass_data)
        string = r.content
        string = str(string)
        string = string.split("<br>")
        output = string[len(string)-1]
        return output
    except:
        return '---ERROR----'

# Select language and API configuration
def compiler(language,code,std_input):
    url = 'https://tpcg1.tutorialspoint.com/tpcg.php'

    if language=='cpp':
        data = {
            'lang': 'cpp',
            'device':'' ,
            'code': code,
            'stdinput': std_input,
            'ext': 'cpp',
            'compile': 'g++ -o main *.cpp',
            'execute': 'main',
            'mainfile': 'main.cpp',
            'uid': '9745043'
        }
        output = recieve_raw_output(url,data)
        output = output[0:-1]
        return output 
    
    if language=='python':
        data = {
            'lang': 'python3',
            'device':'' ,
            'code': code,
            'stdinput': std_input,
            'ext': 'py',
            'compile': '0',
            'execute': 'python3 main.py',
            'mainfile': 'main.py',
            'uid': '9745043'
        }
        output = recieve_raw_output(url,data)
        output = output[0:-1]
        return output 

    if language=='java':
        data = {
            'lang': 'java',
            'device':'' ,
            'code': code,
            'stdinput': std_input,
            'ext': 'java',
            'compile': 'javac',
            'execute': 'java -Xmx128M -Xms16M',
            'mainfile': 'HelloWorld.java',
            'uid': '9745043'
        }
        output = recieve_raw_output(url,data)
        output = output[0:-1]
        return output 

    if language=='c':
        data = {
            'lang': 'c',
            'device':'' ,
            'code': code,
            'stdinput': std_input,
            'ext': 'c',
            'compile': 'gcc -o main *.c',
            'execute': 'main',
            'mainfile': 'main.c',
            'uid': '9745043'
        }
        output = recieve_raw_output(url,data)
        output = output[0:-1]
        return output


# Templates
# Home page
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


# Register Page
@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        return render_template('register.html')
    else:
        return render_template('index.html')


# Direct login to dashboard
@app.route("/login_dashboard", methods=['POST'])
def login():
    if request.method == 'POST':

        email = [item for item in sheet.col_values(1) if item]
        password = [item for item in sheet.col_values(2) if item]

        email_recieve = request.form['email_id']
        password_recieve = request.form['pwd_id']
        email_recieve = email_recieve.replace(" ","")
        password_recieve = password_recieve.replace(" ","")

        flag = 0
        for i in range(1,len(email)):
            if email_recieve==email[i]:
                if password_recieve==password[i]:
                    flag = 1
                    return render_template('dashboard.html',email_pass=email_recieve)
                else:
                    flag = 1
                    return render_template('index.html',incorrect_pwd="YES",email_pass=email_recieve)
        
        if flag ==0:
            return render_template('index.html',incorrect_pwd="YES_REGISTER",email_pass=email_recieve)

    else:
        return render_template('index.html')


# Register to dashboard
@app.route("/dashboard", methods=['POST'])
def dashboard():
    if request.method == 'POST':

        email = [item for item in sheet.col_values(1) if item]
        password = [item for item in sheet.col_values(2) if item]

        email_recieve = request.form['email_id']
        password_recieve = request.form['pwd_id']
        email_recieve = email_recieve.replace(" ","")
        password_recieve = password_recieve.replace(" ","")

        flag = 0
        for i in range(1,len(email)):
            if email[i]==email_recieve:
                sheet.update_cell(i+1,2,password_recieve)
                flag = 1

        len_row = len(email)
        if flag ==0:
            sheet.update_cell(len_row+1,1,email_recieve)
            sheet.update_cell(len_row+1,2,password_recieve)


        return render_template('dashboard.html',email_pass=email_recieve)
    else:
        return render_template('index.html')


# Programs
# -------------------------------------------------------- Program 1 ---------------------------------------------------------
@app.route("/program_1", methods=['POST'])
def program_1():
    if request.method == 'POST':

        email = [item for item in sheet.col_values(1) if item]
        email_receive = request.form['email_1']

        code = ""
        for i in range(1,len(email)):
            if email_receive==email[i]:
                code = sheet.cell(i+1,3).value

        return render_template('program_1.html',email_pass=email_receive,pass_code=code)
    else:
        return render_template('index.html')

#Evaluate Programs
#Program 1 Run
@app.route("/program_1/evaluate_program_1", methods=['POST'])
def evaluate_program_1():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    stdinp = "2 15"

    output = compiler(receive_lang,receive_code,stdinp)
    output = output.replace("\\n","<br>")
    
    x = {"output": output}
    y = json.dumps(x)

    return y


#Program 1 Test Cases
@app.route("/program_1/evaluate_program_1/test_cases", methods=['POST'])
def evaluate_program_1_test():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    input_cases = ["2 15","89 125","1 10","999990 1000000"]
    output_cases = ["3 5 7 9 11 13 ","91 93 95 97 99 101 103 105 107 109 111 113 115 117 119 121 123 ",
    "3 5 7 9 ","999991 999993 999995 999997 999999 "]

    flag = 0
    for i in range(len(input_cases)):
        output = compiler(receive_lang,receive_code,input_cases[i])
        if output!=output_cases[i]:
            flag = 1
            break

    outs = ""
    if flag==1:
        outs = "TEST CASES FAILED"
    else:
        outs = "TEST CASES PASSED"
    
    output = compiler(receive_lang,receive_code,input_cases[0])
    output = output.replace("\\n","<br>")
    
    x = {"output": output,"status":outs}
    y = json.dumps(x)

    return y


#Program 1 Submission 
@app.route("/submit_program_1", methods=['POST'])
def submit_program_1():
    if request.method == 'POST':

        email = [item for item in sheet.col_values(1) if item]

        final_output = request.form['final_output']
        email_receive = request.form['email']

        for i in range(1,len(email)):
            if email_receive==email[i]:
                sheet.update_cell(i+1,3,final_output)


        return render_template('dashboard.html',email_pass=email_receive)
    else:
        return render_template('index.html')




# -------------------------------------------------------- Program 2 ---------------------------------------------------------
@app.route("/program_2", methods=['POST'])
def program_2():
    if request.method == 'POST':
        email = [item for item in sheet.col_values(1) if item]
        email_receive = request.form['email_2']

        code = ""
        for i in range(1,len(email)):
            if email_receive==email[i]:
                code = sheet.cell(i+1,4).value

        return render_template('program_2.html',email_pass=email_receive,pass_code=code)
    else:
        return render_template('index.html')

#Evaluate Programs
#Program 2 Run
@app.route("/program_2/evaluate_program_2", methods=['POST'])
def evaluate_program_2():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    stdinp = "908657"

    output = compiler(receive_lang,receive_code,stdinp)
    output = output.replace("\\n","<br>")
    
    x = {"output": output}
    y = json.dumps(x)

    return y


#Program 2 Test Cases
@app.route("/program_2/evaluate_program_2/test_cases", methods=['POST'])
def evaluate_program_2_test():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    input_cases = ["15698","908657","1","1234567","101"]
    output_cases = ["89651","756809","1","7654321","101"]

    flag = 0
    for i in range(len(input_cases)):
        output = compiler(receive_lang,receive_code,input_cases[i])
        output = output.replace("\\n","")
        if output!=output_cases[i]:
            flag = 1
            break

    outs = ""
    if flag==1:
        outs = "TEST CASES FAILED"
    else:
        outs = "TEST CASES PASSED"
    
    output = compiler(receive_lang,receive_code,input_cases[1])
    output = output.replace("\\n","<br>")
    
    x = {"output": output,"status":outs}
    y = json.dumps(x)

    return y


#Program 2 Submission 
@app.route("/submit_program_2", methods=['POST'])
def submit_program_2():
    if request.method == 'POST':

        email = [item for item in sheet.col_values(1) if item]

        final_output = request.form['final_output']
        email_receive = request.form['email']

        for i in range(1,len(email)):
            if email_receive==email[i]:
                sheet.update_cell(i+1,4,final_output)


        return render_template('dashboard.html',email_pass=email_receive)
    else:
        return render_template('index.html')





# -------------------------------------------------------- Program 3 ---------------------------------------------------------
@app.route("/program_3", methods=['POST'])
def program_3():
    if request.method == 'POST':
        email = [item for item in sheet.col_values(1) if item]
        email_receive = request.form['email_3']

        code = ""
        for i in range(1,len(email)):
            if email_receive==email[i]:
                code = sheet.cell(i+1,5).value

        return render_template('program_3.html',email_pass=email_receive,pass_code=code)
    else:
        return render_template('index.html')

#Evaluate Programs
#Program 3 Run
@app.route("/program_3/evaluate_program_3", methods=['POST'])
def evaluate_program_3():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    stdinp = "cOdinGbUzz"

    output = compiler(receive_lang,receive_code,stdinp)
    output = output.replace("\\n","<br>")
    
    x = {"output": output}
    y = json.dumps(x)

    return y


#Program 3 Test Cases
@app.route("/program_3/evaluate_program_3/test_cases", methods=['POST'])
def evaluate_program_3_test():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    input_cases = ["cOdinGbUzz","helloWORLD","APPLE","aZzA","PROgram"]
    output_cases = ["CoDINgBuZZ","HELLOworld","apple","AzZa","proGRAM"]

    flag = 0
    for i in range(len(input_cases)):
        output = compiler(receive_lang,receive_code,input_cases[i])
        output = output.replace("\\n","")
        if output!=output_cases[i]:
            flag = 1
            break

    outs = ""
    if flag==1:
        outs = "TEST CASES FAILED"
    else:
        outs = "TEST CASES PASSED"
    
    output = compiler(receive_lang,receive_code,input_cases[0])
    output = output.replace("\\n","<br>")
    
    x = {"output": output,"status":outs}
    y = json.dumps(x)

    return y


#Program 3 Submission 
@app.route("/submit_program_3", methods=['POST'])
def submit_program_3():
    if request.method == 'POST':

        email = [item for item in sheet.col_values(1) if item]

        final_output = request.form['final_output']
        email_receive = request.form['email']

        for i in range(1,len(email)):
            if email_receive==email[i]:
                sheet.update_cell(i+1,5,final_output)


        return render_template('dashboard.html',email_pass=email_receive)
    else:
        return render_template('index.html')





# -------------------------------------------------------- Program 4 ---------------------------------------------------------
@app.route("/program_4", methods=['POST'])
def program_4():
    if request.method == 'POST':
        email = [item for item in sheet.col_values(1) if item]
        email_receive = request.form['email_4']

        code = ""
        for i in range(1,len(email)):
            if email_receive==email[i]:
                code = sheet.cell(i+6,3).value

        return render_template('program_4.html',email_pass=email_receive,pass_code=code)
    else:
        return render_template('index.html')

#Evaluate Programs
#Program 4 Run
@app.route("/program_4/evaluate_program_4", methods=['POST'])
def evaluate_program_4():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    stdinp = "6\n7 3 2 0 4 1"

    output = compiler(receive_lang,receive_code,stdinp)
    output = output.replace("\\n","<br>")
    
    x = {"output": output}
    y = json.dumps(x)

    return y


#Program 4 Test Cases
@app.route("/program_4/evaluate_program_4/test_cases", methods=['POST'])
def evaluate_program_4_test():

    req = request.get_json()
    receive_lang = req['language']
    receive_code = req['program']
    
    input_cases = ["6\n7 3 2 0 4 1","10\n78 98 24 17 98 81 42 58 65 24",
    "5\n1 0 1 2 1","7\n 99999 55555 44444 55555 77777 11111 22222"]
    output_cases = ["4","81","1","77777"]

    flag = 0
    for i in range(len(input_cases)):
        output = compiler(receive_lang,receive_code,input_cases[i])
        output = output.replace("\\n","")
        if output!=output_cases[i]:
            flag = 1
            break

    outs = ""
    if flag==1:
        outs = "TEST CASES FAILED"
    else:
        outs = "TEST CASES PASSED"
    
    output = compiler(receive_lang,receive_code,input_cases[1])
    output = output.replace("\\n","<br>")
    
    x = {"output": output,"status":outs}
    y = json.dumps(x)

    return y


#Program 4 Submission 
@app.route("/submit_program_4", methods=['POST'])
def submit_program_4():
    if request.method == 'POST':

        email = [item for item in sheet.col_values(1) if item]

        final_output = request.form['final_output']
        email_receive = request.form['email']

        for i in range(1,len(email)):
            if email_receive==email[i]:
                sheet.update_cell(i+1,6,final_output)


        return render_template('dashboard.html',email_pass=email_receive)
    else:
        return render_template('index.html')




if __name__=="__main__":
    app.run(debug=True)

