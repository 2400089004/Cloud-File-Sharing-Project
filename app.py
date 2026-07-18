import os
from flask import Flask, render_template, request,send_from_directory,session,redirect, url_for
import pymysql
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import boto3

load_dotenv("cloud.env")
print("AWS_ACCESS_KEY_ID =", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_REGION =", os.getenv("AWS_REGION"))
print("BUCKET =", os.getenv("BUCKET_NAME"))

app=Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
s3=boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
bucket_name=os.getenv("BUCKET_NAME")
conn = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)
cursor=conn.cursor()
@app.route('/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users(username,email,password) VALUES(%s,%s,%s)", (username,email,hashed_password))
        conn.commit()
        return "user registration succcessfully"
    return render_template('registration.html')
@app.route('/login',methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            username=user[1]
            session["username"] = username

            cursor.execute(
                "select filename from files where username=%s",
                (session["username"],)
            )
            rows=cursor.fetchall()

            files = []

            for row in rows:
                files.append(row[0])


            return render_template(
                "dashboard.html",
                username=session["username"],
                files=files
            )

        else:
            return "Invalid Email or Password"

    return render_template("login.html")
@app.route('/upload',methods=['POST'])
def upload():
    file=request.files['file']
    if file:
        s3.upload_fileobj(file,bucket_name,file.filename)
        cursor.execute("insert into files(username,filename) values(%s,%s)",(session["username"],file.filename))
        conn.commit()
        cursor.execute(
            "select filename from files where username=%s",
            (session["username"],)
        )
        rows=cursor.fetchall()
        files=[]
        for row in rows:
            files.append(row[0])
        return render_template(
            "dashboard.html",
            username=session["username"],
            files=files
        )
    return "NO file selected"
@app.route('/download/<filename>')
def download(filename):

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    s3.download_file(
        bucket_name,
        filename,
        os.path.join("uploads", filename)
    )

    return send_from_directory(
        "uploads",
        filename,
        as_attachment=True
    )
@app.route('/delete/<filename>')
def delete(filename):

    s3.delete_object(
        Bucket=bucket_name,
        Key=filename
    )

    cursor.execute(
        "delete from files where username=%s and filename=%s",
        (session["username"],filename)
    )
    conn.commit()
    cursor.execute(
        "select filename from files where username=%s",
        (session["username"],)
    )
    rows=cursor.fetchall()
    files=[]
    for row in rows:
        files.append(row[0])

    return render_template(
        "dashboard.html",
        username=session.get("username","guest"),
        files=files
    
    )
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
if __name__ ==  '__main__':
    app.run(debug=True)