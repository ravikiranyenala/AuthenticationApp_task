from django.shortcuts import render
import mysql.connector
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
from django.conf import settings
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    if request.method =="POST":
        return render(request,'index.html')
    else:
        return render(request,'index.html')
def home_page(request):
    if request.method == "POST":
        entered_user_name = request.POST["userName"]
        entered_password = request.POST["User_password"]
        try:
            db_connection = mysql.connector.connect(host="localhost",user="root", passwd="", database="auth_db")
            get_connection = db_connection.cursor()
            get_connection.execute("SELECT * FROM `admin_login`;")
            for each_line in get_connection:                
                db_username = each_line[1]
                db_password = each_line[2]  
                if (entered_user_name == db_username and entered_password == db_password):
                    return render(request,'home_page.html')
                else:
                    return HttpResponse('<h1>Wrong credentials</h1>')
            
        except:
            print("error")
            return render(request,'index.html')
    else:
        return render(request,'index.html')
        
def show_jsonData(request):
    try:
        db_connection = mysql.connector.connect(host="localhost",user="root", passwd="", database="auth_db")
        get_connection = db_connection.cursor()
        get_connection.execute("SELECT * FROM `json_data`;")

        row_headers=[x[0] for x in get_connection.description] 
        rv = get_connection.fetchall()
        log_data_table=[]
        for result in rv:
            log_data_table.append(dict(zip(row_headers,result)))
        print("json data : ",log_data_table)
        return render(request,'show_json_data.html',{'json_data_list':log_data_table})        

    except:
        print("error")
        return render(request,'index.html')

def file_uploaded(request):
    if (request.method=="POST"):
        uploaded_file = request.FILES['file']
        if (uploaded_file.name).endswith('.json'):
            print ('File is a json')        
            file_save = FileSystemStorage()
            file_save.save(uploaded_file.name, uploaded_file)
            
            db_connection = mysql.connector.connect(host="localhost",user="root", passwd="", database="auth_db")
            get_connection = db_connection.cursor()
                    
            media_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

            file_read = open(media_path,'r')
            json_read = json.load(file_read)

            for each_element in json_read:
                #each_element.strip()
                #each_element.split(",")
                userID = each_element["userId"]
                ID = each_element["id"]
                title = str(each_element["title"])
                body = str(each_element["body"])
                insert_query = """INSERT INTO `json_data` values(null,%s,%s,%s,%s)"""
                column_values = (userID, ID, title, body)
                get_connection.execute(insert_query, column_values)
                db_connection.commit()
            print("data storing is done")
            return HttpResponse('<h1>Successfully uploaded json file</h1>')
        else:
            return HttpResponse('<h1>Please upload .json file only</h1>')

    else:
        return render(request, 'home_page.html')
            

