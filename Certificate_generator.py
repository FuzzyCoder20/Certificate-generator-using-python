import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import sqlite3 as sql
import os
import csv
from sqlite3 import Error
from pil import Image, ImageFont, ImageDraw
import pandas as pd
import numpy
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import sqlite3


def database_stuff():
    conn = sqlite3.connect('db3')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS members(NAME TEXT, EMAIL_ID TEXT)")
    conn.commit()
    '''print ("******membersTable Data*******")
    c = conn.cursor()
    c.execute("SELECT * FROM members")
    rows = c.fetchall()
    for row in rows:
      print(row)'''
    conn.close()



#TKINTER stufffffffffff
main_menu = tk.Tk()

name_label = Label(main_menu, text="NAME")
name_label.pack()
name_entry = tk.StringVar()
name_entry_entry = Entry(main_menu, textvariable=name_entry)
name_entry_entry.pack()


email_label = Label(main_menu, text="EMAIL")
email_label.pack()
email_entry = tk.StringVar()
email_entry_entry = Entry(main_menu, textvariable=email_entry)
email_entry_entry.pack()


def savedata ():
    print(dir(name_entry))
    conn = sqlite3.connect('db3')
    c = conn.cursor()
    c.execute('INSERT INTO members (NAME,EMAIL_ID) VALUES (?,?)', (name_entry.get(), email_entry.get()))
    conn.commit()
    print("OK")

u_ent_btn = Button(text="Enter",command=savedata)
u_ent_btn.pack()

database_stuff()
main_menu.mainloop()


#certificate generator part

def createCertificate(names):
        
        text_y_position = 592
        image_source = Image.open('sample_certificate.jpg', mode='r') #SAMPLE CERTIFICATE TEMPLATE
        #extra test
        image_width = image_source.width
        image_height = image_source.height
        draw = ImageDraw.Draw(image_source)
        font = ImageFont.truetype("DejaVuSerif-Bold.ttf", 100)
        text_width, _ = draw.textsize(name, font = font) 
        draw.text( 
                ( 
                # this calculation is done  
                # to centre the image 
                    (image_width - text_width) / 2, 
                    text_y_position 
                ), 
                name, fill="#000000",
                font = font        ) 
    #draw.text((559,577), name, fill=FONT_COLOR, font=font,align="center")
    #draw.text((WIDTH-w/4,600), name, fill=FONT_COLOR, font=font)
        image_source.save("D:\py programs\certificate_gen\Cert_&_emails_python\\" + "Participation_cert"".jpg")
        print('printing certificate of: '+name)
    
def sendMail(name,email):
    fromaddr = "XXX@gmail.com"  #ENTER YOUR EMAIL HERE
    toaddr = email
    msg = MIMEMultipart()  
    msg['From'] = fromaddr 
    msg['To'] = toaddr  
    msg['Subject'] = "Certificate of Participation"
    body = """\
    <html>
    <body>
        <p>Thank you for attending our <b> abc</b> organised by <b>xyz committee</b> </p>
    </body>
    </html>
    """ 
    msg.attach(MIMEText(body, 'html'))  
    filename = "Participation_cert.jpg"
    #add your path
    attachment = open("\py programs\certificate_gen\Cert_&_emails_python\Participation_cert.jpg", "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, "xxxxx") #ENTER YOUR PASSWORD HERE
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
    s.quit() 



con = sqlite3.connect('db3')
df = pd.read_sql_query("SELECT * from members", con)
con.close()
for i in range(len(df)):
    name = df.iloc[i,0]
    email = df.iloc[i,1]
    createCertificate(name)
    sendMail(name, email)