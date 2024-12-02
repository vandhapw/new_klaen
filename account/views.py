from django.shortcuts import render, redirect
from .forms import *
from django.forms.models import model_to_dict
from .models import AppUsers, UserLog, UserGroup
from datetime import timedelta, datetime
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login 
from django.contrib import messages
# from production.utils import get_database_client, MONGO_DB
from production.utils import dbLocation
from pymongo import MongoClient, DESCENDING
import pytz
from django.utils import timezone
import logging
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests
from rest_framework import status
from django.conf import settings

client = MongoClient(dbLocation)
db = client.server_db
buildthing_data_collection = db.klaen_buildthing
sensor_data_collection = db.klaen_arduino_sensor
weather_data_collection = db.weather_api
plalion_data_collection = db.plalion_klaen_sensor
plalion_company_data_collection = db.plalion_company_sensor

jungrok_url = "http://54.180.153.12:3000/plalion/"




# client, ssh_tunnel = get_database_client()

def login_page(request):
    if 'user' in request.session:
    #     appid = request.session.get('appid')
    #     user = request.session.get('user')
    # context = {'appid':appid, 'user':user}
    # print(context)
        return dashboard_page(request)
    # user = request.session.get('user')
    # appid = request.session.get('appid')
    # if user is not None:
    #     return redirect('/dashboard/')
    return render(request,'login-form-17.html')

@login_required
def check_page(request):
    return render(request,'check.html')

def dashboard_page(request):
    context = {}
    if 'user' in request.session:
        appid = request.session.get('appid')
        user = request.session.get('user')
    context = {'appid':appid, 'user':user}
    print('context', context)
    return render(request,'dashboard/dashboard_sensor.html', context) #default dashboard.html
        
def admin_page(request):
    context = {}
    if 'user' in request.session:
        appid = request.session.get('appid')
        user = request.session.get('user')
    context = {'appid':appid, 'user':user}
    print('context', context)
    return render(request,'dashboard/admin-dashboard.html', context) #default dashboard.html
      

@csrf_exempt
def login_api_(request):
    if request.method == 'POST':
        # Get username/email and password from POST request
        username = request.POST.get('username')  # Can be username or email
        password = request.POST.get('password')
     # Authenticate by username or email
        try:
            user = AppUsers.objects.get(username=username)
        except AppUsers.DoesNotExist:
            user = AppUsers.objects.filter(username=username).first()

        if user:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                # return redirect('home')  # Replace 'home' with your desired redirect
                return JsonResponse('success loggen in', safe=False)
            else:
                # messages.error(request, 'Invalid credentials.')
                return JsonResponse({'message':'Failed', 'user':user}, safe=False)
        else:
            messages.error(request, 'User does not exist.')
        # return redirect('login')  # Redirect back to the login page
            return JsonResponse({'message':'Failed', 'user':user}, safe=False)
    else:
            # Render the login page for GET request
        # return render(request, 'login.html')
        return JsonResponse('lgin html', safe=False)

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
       
        data = json.loads(request.body)
       
        username = data.get('username')
        password = data.get('password')
        
        seoul_tz = pytz.timezone(settings.TIME_ZONE)

        
        try:
            user = AppUsers.objects.get(username=username)
        except:
            return HttpResponse('incorrect id')

        try:
            userinfo = UserLog.objects.get(username=user.id)
            userinfo_dict = model_to_dict(userinfo)
        except UserLog.DoesNotExist:
            userinfo = UserLog.objects.create(
            id = user.id,    
            username=user.id,  # Pass the User instance
            visitcount=0,
            login_at=datetime.utcnow(),
            logout_at=datetime.utcnow()
        )
            # return JsonResponse({'message': 'UserLog does not exist for this user'}, status=400)
        # request.session['appid'] = user.appid
       
        if check_password(password, user.password):
            if userinfo.visitcount == None:
                cnt = 1
            else:
                cnt = userinfo.visitcount + 1
            userinfo.visitcount = cnt            
            userinfo.login_at = datetime.now(seoul_tz)
            userinfo.save()
            request.session['user'] = username
            request.session['appid'] = user.appid
            return JsonResponse({'message': 'Login successful','time':userinfo_dict})
        else:
            return JsonResponse({'message': 'Username and password are required'}, status=400)
       
        # if request.content_type != 'application/json':
        #     return JsonResponse({'message': 'Invalid Content-Type, expected application/json'}, status=415)
        # try:
        #     data = json.loads(request.body)
        #     username = data.get('username')
        #     password = data.get('password')

        #     if not username or not password:
        #         return JsonResponse({'message': 'Username and password are required'}, status=400)
        #     db = client[MONGO_DB]
        #     user_collection = db['user']
        #     user = user_collection.find_one({'username': username})
        #     print('user', user)
            
        #     session_data = {key: value for key, value in request.session.items()}
        #     logger.debug(f'Session data: {session_data}')

        #     if user and check_password(password, user['password']):
        #         request.session['user'] = username
        #         request.session['appid'] = user.get('appid')  # Default appid if not present
        #         session_data = {"user_session":request.session['user'], "appid_session":request.session['appid']}
        #         print('session_data', session_data)
        #         return JsonResponse({'message': 'Login successful'})
        #     return JsonResponse({'message': 'Incorrect username or password'}, status=401)
        # except json.JSONDecodeError:
        #     return JsonResponse({'message': 'Invalid JSON'}, status=400)
        # except Exception as e:
        #     logger.error(e, exc_info=True)
        #     print(logger.error())
        #     return JsonResponse({'message': 'An error occurred during login'}, status=500)
        
@csrf_exempt
def logout_api(request):
    if request.method == 'POST':
        username = request.session.get('user')
        if username:
            try:
                userinfo = UserLog.objects.get(username__username=username)
                userinfo.logout_at = timezone.now()
                userinfo.save()
            except UserLog.DoesNotExist:
                pass  # Handle the case where the UserLog does not exist
            logout(request)
        return JsonResponse({'message': 'Logout successful', 'redirect_url':'/'})
        
    
    
@csrf_exempt
def register_api(request):
    
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        re_password = data['re_password']
        email = data['email']
        
        res_data = {}
        
        if not (username and password and re_password and email):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            hash_password = make_password(password)
           
            data = {
                'username': username,
                'password': hash_password,
                'email': email,
                'registered_at': datetime.datetime.now()
            }
            
            # Connect to MongoDB (adjust connection details accordingly)
            db = client[MONGO_DB]  # Use your actual MongoDB database name
            users_collection = db['app_users']  # Use your actual collection name for users

            # Find user by username
            user = users_collection.insert_one(data)
        
        if user:
            return JsonResponse({'message': 'Register successful! Please Login', 'redirect_url':'/'})
        else:
            return JsonResponse({'error': 'Incorrect password'}, status=401)
    else:
        return JsonResponse({'error': 'User not found'}, status=404)
    
#================================================================================================
# New Code # 2024 November

def monitoring_page(request):
    context = {}
    return render(request,'dashboard/dashboard_sensor.html', context)

def apps_page(request):
    context = {}
    return render(request,'apps-page.html', context)

def get_unique_serial_numbers(request):
    # Use the distinct method to get unique serial numbers
    unique_serial_numbers = plalion_company_data_collection.distinct("serial_number")

    latest_values = []

    for serial_number in unique_serial_numbers:
        # Find the latest document for each unique serial number
        latest_document = plalion_company_data_collection.find_one(
            {"serial_number": serial_number},
            sort=[("timestamp", DESCENDING)]  # Assuming 'timestamp' is the field to sort by
        )
        if latest_document:
            # Convert ObjectId to string for JSON serialization
            latest_document["_id"] = str(latest_document["_id"])
            latest_values.append(latest_document)

    return JsonResponse (latest_values, safe=False)

def device_management(request):
    return render(request, 'dashboard/admin-device_management.html')

def device_management_2(request):
    return render(request, 'dashboard/admin-device_management_2.html')

def get_latest_sensor_mqtt(request):
    # serial_numbers = [8545872, 2581352, 2581292, 2581308, 4200100]
    serial_numbers = [7229092, 7225848, 7229064]
    titles = [
        "1BAY 공장 실내 공기질 모니터링 현황",
        "2BAY 공장 실내 공기질 모니터링 현황",
        "3BAY 공장 실내 공기질 모니터링 현황",
    ]
    REST_API = jungrok_url + 'status/get'
    headers = {
        "Content-Type": "application/json"
    }
    
    results = []
    ozone_sum = 0
    co2_sum = 0
    voc_sum = 0
    temperature_sum = 0
    humidity_sum = 0
    particulate_matter_sum = 0
    count = 0
    latest_timestamp = None

    for i, serial_num in enumerate(serial_numbers):
        data = {
            "serial_num": [serial_num],
        }
        
        response = requests.post(REST_API, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            rows = response_data.get("rows", [])
            
            if rows:
                row = rows[0]
                row["title"] = titles[i] if i < len(titles) else f"Title for serial number {serial_num}"
                row["voc_val"] = round((row.get("voc_val") / 1000), 3)
                results.append(row)
                
                # Accumulate values
                ozone_sum += row.get("ozone_val", 0)
                co2_sum += row.get("co2_val", 0)
                voc_sum += row.get("voc_val", 0)
                temperature_sum += row.get("temp_val", 0)
                humidity_sum += row.get("humi_val", 0)
                particulate_matter_sum += row.get("dust_val", 0)
                count += 1
                
                # Update latest timestamp
                latest_timestamp = row.get("last_time", latest_timestamp)
            else:
                results.append({"serial_num": serial_num, "error": "No data from the REST API"})
        else:
            results.append({"serial_num": serial_num, "error": "Failed to fetch data from the REST API"})
    
    if count > 0:
        averages = {
            "title": "1공장 실내 공기질 모니터링 현황",
            "ozone_val": round(ozone_sum / count, 3),
            "co2_val": round(co2_sum / count, 3),
            "voc_val": round(voc_sum / count, 3),
            "temp_val": round(temperature_sum / count, 3),
            "humi_val": round(humidity_sum / count, 3),
            "dust_val": round(particulate_matter_sum / count, 3),
            "last_time": latest_timestamp
        }
        results.insert(0, averages)
    
    response_data = {
        "results": results,
        "latest_timestamp": latest_timestamp
    }
    
    return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)

            
# Create your views here.
