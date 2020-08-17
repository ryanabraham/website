from flask import Flask, render_template,url_for,request,redirect
import csv
import email, smtplib, ssl,time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)


def email():
  subject = "Someone has sent you a message on your website"
  body = "Please reply to this message on your website."
  sender_email = "mytesttest17@gmail.com"
  receiver_email = "ryan.ryanabraham@gmail.com"
  password = 'tester360'


  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = subject
  message["Bcc"] = receiver_email  

  
  message.attach(MIMEText(body, "plain"))

  filename = "database.csv"  # In same directory as script

  # Open PDF file in binary mode
  with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
      zac = MIMEBase("application", "octet-stream")
      zac.set_payload(attachment.read())

  # Encode file in ASCII characters to send by email    
  encoders.encode_base64(zac)

# Add header as key/value pair to attachment part
  wow = "database.txt"
  zac.add_header(
      "Content-Disposition",
      f"attachment; filename= {wow}",
  )

  # Add attachment to message and convert message to string
  message.attach(zac)
    # Open PDF file in binary mode
  with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())

  # Encode file in ASCII characters to send by email    
  encoders.encode_base64(part)

# Add header as key/value pair to attachment part
  part.add_header(
      "Content-Disposition",
      f"attachment; filename= {filename}",
  )

  # Add attachment to message and convert message to string
  message.attach(part)
  text = message.as_string()

  # Log in to server using secure context and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, text)
  print('Succesfully sent ')


@app.route('/')
def home():
  return render_template('index.html')
def writer(cats):
  with open('database.txt', mode='w') as wow:
    wow.write(f'{cats}')
def write(data):
  with open('database.txt',mode='a') as database:
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    file = database.write(f'\n {email},{subject},{message}')
def writecsv(data):
  with open('database.csv',mode='w') as database2:
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    csv_writer = csv.writer(database2 ,delimiter=",",quotechar='"',quoting = csv.QUOTE_MINIMAL )
    csv_writer.writerow([email,subject,message])

@app.route('/<string:page_name>')
def html_page(page_name):
   try:
     return render_template(page_name)
   except:
     return render_template('indexer.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
      data = request.form.to_dict()
      writecsv(data)
      email()
      return redirect('/thankyou.html')
    else:
      return 'something went wrong'

@app.route('/submit', methods=['POST', 'GET'])
def submit():
  if request.method == 'POST':
    passw = request.form.to_dict()
  else:
    return 'There was a error' 
  if passw == {'message': 'password'}:
   return redirect('/rename.html')
  else:
    writer(passw)
    return redirect('/index.html') 

app.run(host='0.0.0.0', port=8080 ,debug=True)