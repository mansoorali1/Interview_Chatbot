from flask import Flask, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
#from werkzeug import secure_filename
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import Email, InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import numpy as np
import MySQLdb
import pandas as pd
from datetime import datetime
import re
#from flask_mail import Mail, Message

#deadline='28-Sep-2021'

question_bank = pd.read_excel("Question bank.xlsx")
question_bank['Unique_Question_ID'] = question_bank['Unique_Question_ID'].apply(lambda x: int(x))
question_bank['Difficulty level'] = question_bank['Difficulty level'].apply(lambda x: int(x))
question_bank['MaxMarks'] = question_bank['MaxMarks'].apply(lambda x: int(x))

question_bank['Answer_2'] = question_bank['Answer_2'].apply(lambda x:x if x is not np.nan else "")
question_bank['Answer_3'] = question_bank['Answer_3'].apply(lambda x:x if x is not np.nan else "")
df = question_bank.copy()
# print(df.Category[0].lower() == 'svm')
# print(question_bank.head())
# print(df.head())
# print(question_bank['Difficulty level'])

app = Flask(__name__)
#mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['UPLOAD_FOLDER'] = '/uploads_interviewbot/'
#app.config['MAX_CONTENT_PATH'] = '1000000'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# configuration of mail
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'testing.interviewbot@gmail.com'
# app.config['MAIL_PASSWORD'] = 'pass*123'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

# Configuration for MySQL database for storing aspirant data:
hostName = 'db4free.net'      
userName = 'udreedbczu'          
passWord = 'ezcb9vazqz'           
dbName =  userName                
DBConn= MySQLdb.connect(hostName,userName,passWord,dbName)

login_provided_by_aspirant=''
user_topics = ''

def runCMD (DDL):
    
    """

    MySQL function for CUD of CRUD

    """

    DBConn= MySQLdb.connect(hostName,userName,passWord,dbName)
    myCursor = DBConn.cursor()
    retcode = myCursor.execute(DDL) 
    print(retcode)
    DBConn.commit()
    DBConn.close()

def runSELECT (CMD):
    
    """

    MySQL function for R of CRUD

    """

    DBConn= MySQLdb.connect(hostName,userName,passWord,dbName)
    df_mysql = pd.read_sql(CMD, con=DBConn)    
    DBConn.close()
    return df_mysql

def runRoute(msg):
    
    """

    This function automatically routes all SQL operations to runCMD or runSELECT automatically
    
    """
    
    if msg[0:6]=="SELECT" or msg[0:6]=="select":
        return runSELECT(msg)
    else:
        runCMD(msg)


@app.before_first_request
def create_tables():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db = SQLAlchemy(app)  #not required here
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    signIn_count = db.Column(db.Integer, nullable=False)  # Shah

class RegisterForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(), Length(min=0, max=100)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=4, max=100)])
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists."
            )

class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(), Length(min=0, max=100)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=4, max=100)])
    submit = SubmitField("Log In")

@app.route("/")
def home():
    return render_template('home.html')


#################### STORING USER ANSWER WITH QUESTION ################

# Creating user question answer table
# runCMD("DROP TABLE IF EXISTS userQA;")
# runCMD("CREATE TABLE userQA ( \
#   sno INT KEY NOT NULL, \
#   question varchar(225) NOT NULL, \
#   answer varchar(225), \
#   saved_date varchar(100), \
#   userid varchar(30), \
#   primary key (sno) \
#   );")


@app.route("/answer2db",methods=["GET","POST"])
@login_required
def answer2db():
    global login_provided_by_aspirant
    la = login_provided_by_aspirant
    save_datetime = datetime.utcnow()
    if request.method == "POST":
        quesNans = request.json[0]
        ques = quesNans['question']
        answ = quesNans['answer']
        ques = str(ques)
        answ = str(answ)
        # TODO:  Remove quotes from ques and answ

        # Removing Bad characters from string before sending to database.
        BAD_SYMBOLS_RE = re.compile("""[/$%{}^'"#\\\\|\-`~_]""")
        QBAD_SYMBOLS_RE = re.compile("""[/^'"#\\\\|\-`~_]""")

        ques = re.sub(pattern=QBAD_SYMBOLS_RE,repl='', string = ques)
        answ = re.sub(pattern=BAD_SYMBOLS_RE,repl='', string = answ)

        runCMD('INSERT INTO userQA (question, answer,saved_date,userid) VALUES ("{}","{}","{}","{}");'.format(ques,answ,save_datetime,la))

    return 'kkkk'     # Uncaught (in promise) SyntaxError: Unexpected token k in JSON at position 0. Currently ignored
    

@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    #Interview instructions
    return render_template('dashboard.html')

@app.route("/interview", methods=["GET","POST"])
@login_required
def interview():
    global user_topics, login_provided_by_aspirant   

    def test_topic(topics):

        la = login_provided_by_aspirant
        save_datetime = datetime.utcnow()

        topicAndQuesDict_list= []
        i = 0
        for topic in topics:
            q = df[df.Category.apply(lambda x:x.lower())==topic.lower()][['Unique_Question_ID','Question',
                                                                          'Difficulty level','Answer',
                                                                          'Answer_2','Answer_3',"MaxMarks"]]

            no_questions_per_diff_level_dict= {1:3, 2:2, 3:1 } # TODO Can be taken from client
            difficulty_levels = q['Difficulty level'].nunique()
            question_dict = {'topic':topic}

            for level in range(1,difficulty_levels+1):  # For each difficulty level
                q_level = q[q['Difficulty level'].apply(lambda x:int(x))==int(level)]
                ques_choices = q_level.Unique_Question_ID.tolist()
                no_questions_per_diff_level=  no_questions_per_diff_level_dict[level]

                for chance in range(no_questions_per_diff_level):  # Ask three questions
                    choiceq = int(np.random.choice(ques_choices))  # select a question randomly
                    ques = q.Question[choiceq]

                    # No. of words required and marks

                    marks = str(q.MaxMarks[choiceq])

                    word_limit = "Word limit for answer: "
                    
                    a1 = len(str(q.Answer[choiceq]).split(" "))
                    a2 = len(str(q.Answer_2[choiceq]).split(" "))
                    a3 = len(str(q.Answer_3[choiceq]).split(" "))
                    # print(a1, a2, a3)

                    actual_answers_len_max = max(a1,a2,a3)

                    if actual_answers_len_max == 1:
                        word_limit += 'One word answer'
                    else:      
                        word_limit += f'{int(actual_answers_len_max*0.8)}-{actual_answers_len_max}'
                    
                    ques_choices.remove(int(choiceq))
                    question_dict[i] = [ques, word_limit,marks]

                    QBAD_SYMBOLS_RE = re.compile("""[/^'"#\\\\|\-`~_]""")
                    ques2 = ques
                    ques2 = re.sub(pattern=QBAD_SYMBOLS_RE,repl='', string = ques2)
                    runCMD('INSERT INTO userQA (question, answer,saved_date,userid) VALUES ("{}","{}","{}","{}");'.format(ques2,' ',save_datetime,la))
                    i += 1

            topicAndQuesDict_list.append(question_dict)
        return topicAndQuesDict_list   
    data = test_topic(user_topics) # Generating Topic with Question Data

    if request.method =='POST':
        return render_template('successt.html')
    display_topic = ", ".join(i for i in user_topics)
    return render_template("interview.html", uname=login_provided_by_aspirant, topics=display_topic, data = data)


@app.route("/login", methods=["GET","POST"])
def login():    
    form = LoginForm()
    if form.validate_on_submit():        
        user = User.query.filter_by(username=form.username.data.lower()).first() ## Shah

        if user:
            user.username = user.username.lower() #Shah
            if user.signIn_count == 0:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    
                    global login_provided_by_aspirant
                    global user_topics  
                    login_provided_by_aspirant = user.username # Shah


                    user_topics = runRoute(f"select topics from aspirant_topics where login='{login_provided_by_aspirant}'").iloc[0,0].split(',')
                    user_topics = [i.strip(" ") for i in user_topics]
                    
                    login_user(user)  # Don't comment out this.
                    

                    user.signIn_count += 1  #SHah
                    db.session.commit() #Shah

                    return redirect((url_for('dashboard')))
            else: #Shah
                return render_template("successt.html")
        else:
            return redirect(url_for("register"))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed_password, signIn_count=0)
        new_user.username = new_user.username.lower()  #Shah
        existing_user = User.query.filter_by(username=new_user.username).first()

        if existing_user:
            existing_user = existing_user.username   #Shah
            
        if existing_user !=  new_user.username: #Shah 

            try:  
                registered_user = runRoute(f"select login from aspirant_topics where login='{new_user.username}'").iloc[0,0]
            except:
                return redirect(url_for('register'))
            else:
                db.session.add(new_user)
                db.session.commit()
        return redirect(url_for('login'))


    return render_template('register.html', form=form) 



@app.route("/successt")
@login_required
def successt():
    return render_template("successt.html")

@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)

