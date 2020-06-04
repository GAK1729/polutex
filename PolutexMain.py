import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from createPolutexDB import *
from sqlalchemy import and_, or_
import csv

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS, cross_origin
import requests
import json
import datetime
from datetime import date
from datetime import datetime
from decimal import Decimal
import pandas as pd
import re

import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold



direction_place = {"central": "Thomson", "west": "Lim Chu Kang",
                   "north": "Admirality", "east": "Serangoon", "south": "Holland"}


app = Flask(__name__)


spp = Flask(__name__)
spp.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:qwe@localhost:1234/qwe'


db = SQLAlchemy(spp)

import datetime
from datetime import date
from datetime import datetime
from decimal import Decimal
def checkEarlier(date_string):
    print(date_string)
    print("_________________________________DATE STRING ABOVE_______________________________________________")
    print(type(date_string))
    print("_________________________________TYPE(DATE STRING) ABOVE_______________________________________________")
    return datetime.strptime(date_string, "%Y-%m-%d") <= datetime.today()


# print(checkEarlier("2020-04-16"))

class user_DB(db.Model):
    __tablename__ = "user_DB"
    Username = db.Column(db.String, primary_key=True)
    Password = db.Column(db.String, nullable=False)
    Name = db.Column(db.String, nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.String, nullable=False)
    Nationality = db.Column(db.String, nullable=False)
    Phone_number = db.Column(db.String, nullable=False)
    Emergency_contact_number = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)
    has_disease = db.Column(db.String, nullable=False)

class disease_DB(db.Model):
    __tablename__ = "disease_DB"
    Username = db.Column(db.String, primary_key=True)
    Allergies_to_dust = db.Column(db.String, nullable=True)
    Asthma = db.Column(db.String, nullable=True)
    Bronchitis = db.Column(db.String, nullable=True)
    Lung_cancer = db.Column(db.String, nullable=True)
    Lung_collapse = db.Column(db.String, nullable=True)
    respiratory_Inflammation = db.Column(db.String, nullable=True)
    Pneumonia = db.Column(db.String, nullable=True)

class PSI(db.Model):
    __tablename__ = "PSI"
    Date = db.Column(db.String, primary_key=True)
    north = db.Column(db.String, nullable=False)
    south = db.Column(db.String, nullable=False)
    east = db.Column(db.String, nullable=False)
    west = db.Column(db.String, nullable=False)
    central = db.Column(db.String, nullable=False)


class PM2(db.Model):
    __tablename__ = "PM2"
    Date = db.Column(db.String, primary_key=True)
    north = db.Column(db.String, nullable=False)
    south = db.Column(db.String, nullable=False)
    east = db.Column(db.String, nullable=False)
    west = db.Column(db.String, nullable=False)
    central = db.Column(db.String, nullable=False)



db.create_all()
_PSI_table = PSI
# _PM25_table = PM2
_disease_DB_ = disease_DB

db_string = 'postgres+psycopg2://postgres:qwe@localhost:1234/qwe
'
engine = create_engine(db_string)

db = scoped_session(sessionmaker(bind=engine))

def goCorona(selected_country):
    covid = pd.read_html('https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic')
    covid = covid[4]
    covid.columns = covid.iloc[0]
    data = covid
    data.rename(columns={data.columns[0]:'Country'},inplace= True)
    data.rename(columns={data.columns[1]:'Total Cases'},inplace = True)
    data.rename(columns={data.columns[2]:'Total Deaths'},inplace= True)
    data.rename(columns={data.columns[3]:'Total Recovered Cases'},inplace = True)
    rename_this = list(data.columns)[4]
    data = data.rename({rename_this: 'reco'}, axis=1)  # new method
    total_data = data.iloc[0]
    data['Total Cases'] = data['Total Cases'].str.replace('[[a-z]]','')
    data['Total Cases'] = data['Total Cases'].str.replace('[','')
    data['Country'] = data['Total Cases']
    data['Total Cases'] = data['Total Deaths']
    data['Total Deaths'] = data['Total Recovered Cases']
    data['Total Recovered Cases'] = data['reco']
    total_countries_list = list(data["Country"])
    total_countries_list_END = total_countries_list.index("International conveyances")
    Country_list = total_countries_list[:total_countries_list_END]
    num_affected = len(Country_list)
    Total_Cases_list = list(data["Total Cases"])
    sum = 0
    for i in range(0, len(Total_Cases_list)):
        try:
            val = int(Total_Cases_list[i])
            sum += val
        except ValueError:
            continue
    total_cases_int = sum
    Total_Death_list = list(data["Total Deaths"])
    sum = 0
    for i in range(0, len(Total_Death_list)):
        try:
            val = int(Total_Death_list[i])
            sum += val
        except ValueError:
            continue
    total_deaths_int = sum
    Total_Recovered_Cases_list = list(data["Total Recovered Cases"])
    sum = 0
    for i in range(0, len(Total_Recovered_Cases_list)):
        try:
            val = int(Total_Recovered_Cases_list[i])
            sum += val
        except ValueError:
            continue
    total_recovered_int = sum
    data.drop(data.columns[len(data.columns)-1], axis=1, inplace=True)
    data['Country'] = data['Country'].str.replace('(mainland)','')
    data['Country'] = data['Country'].str.replace('(','')
    data['Country'] = data['Country'].str.replace(')','')
    data['Country'] = data['Country'].str.lower()
    data.index = data['Country']
    data['Total Cases'] = data['Total Cases'].str.replace('–','0')
    data['Total Deaths'] = data['Total Deaths'].str.replace('–','0')
    data['Total Recovered Cases'] = data['Total Recovered Cases'].str.replace('–','0')
    data.dropna(0,inplace=True)
    selected_country = selected_country.lower()
    Country =selected_country
    if Country in list(data.index):
        true = 1
    else:
        true = 0
    if true == 1:
        Total_Cases =  int(data.loc[Country,'Total Cases'])
        Total_Deaths = int(data.loc[Country,'Total Deaths'])
        Total_Recovered_Cases = int(data.loc[Country,'Total Recovered Cases'])
        Total_Active_Cases = Total_Cases - Total_Deaths - Total_Recovered_Cases
    Total_Cases_1 =  int(data.loc['singapore','Total Cases'])
    Total_Deaths_1 = int(data.loc['singapore','Total Deaths'])
    Total_Recovered_Cases_1 = int(data.loc['singapore','Total Recovered Cases'])
    Total_Active_Cases_1 = Total_Cases_1 - Total_Deaths_1 - Total_Recovered_Cases_1
    total_active_int = total_cases_int - total_deaths_int - total_recovered_int
    selected_country = selected_country.capitalize()

    total_cases_int = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % total_cases_int)
    Total_Cases_1 = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Cases_1)
    Total_Cases = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Cases)
    total_deaths_int = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % total_deaths_int)
    Total_Deaths_1 = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Deaths_1)
    Total_Deaths = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Deaths)
    total_active_int = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % total_active_int)
    Total_Active_Cases_1 = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Active_Cases_1)
    Total_Active_Cases = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Active_Cases)
    total_recovered_int = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % total_recovered_int)
    Total_Recovered_Cases_1 = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Recovered_Cases_1)
    Total_Recovered_Cases = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Total_Recovered_Cases)
    Total_Cases_dic = {"The World": total_cases_int, "Singapore": Total_Cases_1, selected_country:Total_Cases}
    Total_Deaths_dic = {"The World": total_deaths_int, "Singapore": Total_Deaths_1, selected_country:Total_Deaths}
    Total_Active_Cases_dic = {"The World": total_active_int, "Singapore": Total_Active_Cases_1, selected_country:Total_Active_Cases}
    Total_Recovered_Cases_dic = {"The World": total_recovered_int, "Singapore": Total_Recovered_Cases_1, selected_country:Total_Recovered_Cases}
    num_affected = num_affected
    return(Total_Cases_dic, Total_Deaths_dic, Total_Active_Cases_dic, Total_Recovered_Cases_dic, num_affected)

def goDiabetes(glucose, bp, skinthickness, insulin, bmi, age):
    f = open("diabetes.csv")
    reader = csv.reader(f)
    diabetes = pd.read_csv('diabetes.csv')
    diabetes = diabetes.drop_duplicates(keep='first')

    diabetes = diabetes.drop(diabetes[diabetes['BMI']==0].index)
    diabetes = diabetes.drop(diabetes[diabetes['BloodPressure']==0].index)
    diabetes = diabetes.drop(diabetes[diabetes['Insulin']==0].index)
    diabetes = diabetes.drop(diabetes[diabetes['Glucose']==0].index)
    diabetes = diabetes.drop(diabetes[diabetes['SkinThickness']==0].index)

    features = list(diabetes.columns)
    features.remove('Outcome')
    features.remove('DiabetesPedigreeFunction')
    features.remove('Pregnancies')

    weight = {1:1.05,0:1}

    log_model = LogisticRegression(class_weight = weight)
    log_model.fit(diabetes[features], diabetes['Outcome'])
    log_model.predict_proba(np.array(diabetes[features].iloc[0]).reshape(1, -1))

    indicator_list = [glucose, bp, skinthickness, insulin, bmi, age]

    predictions = log_model.predict_proba(np.array(indicator_list).reshape(1, -1))

    risk = predictions[0,1]

    print("-"*len("Health Indicator Analysis"))
    print("Health Indicator Analysis")
    print("-"*len("Health Indicator Analysis"))

    if risk < 0.3:
        diabetes_advice = "You are probably in good health, keep it up."
        # print("You are probably in good health, keep it up.")

    elif risk > 0.7:
        diabetes_advice  = "See a doctor as soon as you can and listen to their recommendations. You might be on the way to developing diabetes if you do not change your lifestyle."
        # print("See a doctor as soon as you can and listen to their recommendations. You might be on the way to developing diabetes if you don't change your lifestyle.")

    elif risk > 0.9:
        diabetes_advice = "Go to a hospital right away. Odds are high you have diabetes."
        # print("Go to a hospital right away. Odds are high you have diabetes.")

    else:
        diabetes_advice = "You should be alright for the most part, but take care not to let your health slip."
        # print("You should be alright for the most part, but take care not to let your health slip.")
    risk_percentage = "Your Diabetes Risk Index is {:.2f}%.".format(risk*0.5*100*2)
    return (diabetes_advice, risk_percentage)

    # return print("Your Diabetes Risk Index is {:.2f}/50.".format(risk*0.5*100))

def getRecommendation(pollutant_type, result, user_id):
    number_of_diseases = countDiseases(user_id)
    if(pollutant_type.lower() == 'psi'):
        if(number_of_diseases!=0 and number_of_diseases>1):
            final_result_for_range = (result)*(number_of_diseases)*(0.6)
        elif(number_of_diseases == 1):
            final_result_for_range = (result)*(1.1)
        else:
            final_result_for_range = result

        if(0<=final_result_for_range<=50):
            status = 'Good'
            comments = 'You are safe and can do all normal activities'
        elif(51<=final_result_for_range<=100):
            status = 'Moderate'
            comments = 'You are safe and can do all normal activities'
        elif(101<=final_result_for_range<=200):
            status = 'Unhealthy'
            comments = 'You are at moderate risk. You are requested to REDUCE strenous outdoor and physical exrtion.'
        elif(201<=final_result_for_range<=300):
            status = 'Very unhealthy'
            comments = 'You are at high risk. You are requested to AVOID strenous outdoor and physical exrtion.'
        else:
            status = 'Hazardous'
            comments = 'You at very high risk. You are requested to MINIMISE outdoor activity.'


    elif(pollutant_type.lower() == 'pm25'):

        if(number_of_diseases!=0 and number_of_diseases>1):
            final_result_for_range = (result)*(number_of_diseases)*(0.6)
        elif(number_of_diseases==1):
            final_result_for_range = (result)*(1.1)
        else:
            final_result_for_range = result

        if(final_result_for_range<=55):
            status = 'Normal'
            comments = 'You are safe and can do all normal activities'
        elif(56<=final_result_for_range<=150):
            status = 'Elevated'
            comments = 'You are at moderate risk. You are requested to REDUCE strenous outdoor and physical exertion.'
        elif(151<=final_result_for_range<=250):
            status = 'High'
            comments = 'You are at high risk. You are requested to AVOID strenous outdoor and physical exertion.'
        else:
            status = 'Very high'
            comments = 'You at very high risk. You are requested to MINIMISE outdoor activity.'


    elif(pollutant_type.lower() == 'uv'):

        day = input("Enter the day(morning,afternoon,evening): ")
        pred_uv = calculateUV(day)
        result = statistics.mean(pred_uv)

        if(0<=result<=2.9):
            status = 'Low'
            comments = 'You are safe. You are requested to use sunglass and sunscreen.'
        elif(3<=final_result_for_range<=5.9):
            status = 'Moderate'
            comments = 'You are at moderate risk.You are requested to use sunglass,sunscreen and a hat.'
        elif(6<=final_result_for_range<=7.9):
            status = 'High'
            comments = 'You are at high risk. You are requested to stay home, if necessary please use sunscreen etc.'
        elif(8<=final_result_for_range<=10.9):
            status = 'Very high'
            comments = 'You are at very high risk. You are requested to stay home, if necessary please use sunscreen etc..'
        else:
            status = 'Extreme'
            comments = 'You at extreme risk. You are requested to avoid stepping outdoors.'
    return (result, final_result_for_range, status, comments)

def countDiseases(user_id):
    count = 0
    b = db.query(user_DB).get(user_id)
    if (b.has_disease == "No"):
        return 0
    a = db.query(_disease_DB_).get(user_id)
    if(a.Allergies_to_dust == "Yes"):
        count += 1
    if(a.Asthma == "Yes"):
        count += 1
    if(a.Bronchitis == "Yes"):
        count += 1
    if(a.Lung_cancer == "Yes"):
        count += 1
    if(a.Lung_collapse == "Yes"):
        count += 1
    if(a.respiratory_Inflammation == "Yes"):
        count += 1
    if(a.Pneumonia == "Yes"):
        count += 1
    return count


east = ['Serangoon', 'Punggol', 'Hougang', 'Tampines', 'Pasir Ris', 'Loyang', 'Simei',
            'Kallang', 'Katong', ' East Coast', 'Macpherson', 'Bedok', 'Pulau Ubin', 'Pulau Tekong']
central = ['Thomson', 'Marymount', 'Sin Ming', 'Ang Mo Kio',
               'Bishan', 'Serangoon Gardens', 'MacRitchie', 'Toa Payoh']
north = ['Admirality', 'Kranji', 'Woodlands', 'Sembawang',
             'Yishun', 'Yio Chu Kang', 'Seletar', 'Sengkang']
south = ['Holland', 'Queenstown', 'Bukit Merah', 'Telok Blangah', 'Pasir Panjang',
             'Sentosa', 'Bukit Timah', 'Newton', 'Orchard', 'City', 'Marina South']
west = ['Lim Chu Kang', 'Choa Chu Kang', 'Bukit Panjang', 'Tuas', 'Jurong East', 'Jurong West',
            'Jurong Industrial Estate', 'Bukit Batok', 'Hillview', 'West Coast', 'Clementi']

def whereIsThis(location):
    if (location in east):
         return "east"
    elif (location in west):
         return "west"
    elif (location in north):
         return "north"
    elif (location in south):
         return "south"
    elif (location in central):
         return "central"

def getPredicVal(_date_, location, table):
    east = ['Serangoon', 'Punggol', 'Hougang', 'Tampines', 'Pasir Ris', 'Loyang', 'Simei',
            'Kallang', 'Katong', ' East Coast', 'Macpherson', 'Bedok', 'Pulau Ubin', 'Pulau Tekong']
    central = ['Thomson', 'Marymount', 'Sin Ming', 'Ang Mo Kio',
               'Bishan', 'Serangoon Gardens', 'MacRitchie', 'Toa Payoh']
    north = ['Admirality', 'Kranji', 'Woodlands', 'Sembawang',
             'Yishun', 'Yio Chu Kang', 'Seletar', 'Sengkang']
    south = ['Holland', 'Queenstown', 'Bukit Merah', 'Telok Blangah', 'Pasir Panjang',
             'Sentosa', 'Bukit Timah', 'Newton', 'Orchard', 'City', 'Marina South']
    west = ['Lim Chu Kang', 'Choa Chu Kang', 'Bukit Panjang', 'Tuas', 'Jurong East', 'Jurong West',
            'Jurong Industrial Estate', 'Bukit Batok', 'Hillview', 'West Coast', 'Clementi']
    print("__________________INSIDE getPredicCAL_________________")
    print(table)
    print(type(table))
    print(_date_)
    print(type(_date_))
    a = db.query(table).get(_date_)
    print(a)
    if location in east:
        return (a.east)
    elif location in central:
        return (a.central)
    elif location in north:
        return (a.north)
    elif location in south:
        return (a.south)
    elif location in west:
        return (a.west)


def PSIPredict(date, direction_place, selected_location):
    _date_ = date
    table = _PSI_table
    get_north_mag = getPredicVal(_date_, location=direction_place["north"], table=table)
    get_south_mag = getPredicVal(_date_, location=direction_place["south"], table=table)
    get_east_mag = getPredicVal(_date_, location=direction_place["east"], table=table)
    get_west_mag = getPredicVal(_date_, location=direction_place["west"], table=table)
    get_central_mag = getPredicVal(_date_, location=direction_place["central"], table=table)

    loc_ = whereIsThis(selected_location)
    if (loc_ == "north"):
        result_ = float(get_north_mag)
    elif (loc_ == "south"):
        result_ = float(get_south_mag)
    elif (loc_ == "east"):
        result_ = float(get_east_mag)
    elif (loc_ == "west"):
        result_ = float(get_west_mag)
    elif (loc_ == "central"):
        result_ = float(get_central_mag)
    psi_result, final_result_for_range, status, comments = getRecommendation(pollutant_type="psi", result=int(result_), user_id=cache_user_details["UserName"])
    return render_template("PSI.html", show_alert = 1, selected_location = selected_location,  selected_date=_date_, show_mag = 10, direction_place = direction_place, north_mag = get_north_mag, south_mag = get_south_mag, east_mag = get_east_mag, west_mag = get_west_mag, central_mag = get_central_mag, psi_result=psi_result, final_result_for_range=final_result_for_range, status=status, comments=comments)



def PM2Predict(date, direction_place, selected_location):
    # Datetime has to be in this format YYYY-MM-DDTHH-MM-SS
    # 2019-04-24T10%3A00%3A00
    _date_ = date
    table = PM2
    get_north_mag = getPredicVal(_date_, location=direction_place["north"], table=table)
    get_south_mag = getPredicVal(_date_, location=direction_place["south"], table=table)
    get_east_mag = getPredicVal(_date_, location=direction_place["east"], table=table)
    get_west_mag = getPredicVal(_date_, location=direction_place["west"], table=table)
    get_central_mag = getPredicVal(_date_, location=direction_place["central"], table=table)

    loc_ = whereIsThis(selected_location)
    if (loc_ == "north"):
        result_ = float(get_north_mag)
    elif (loc_ == "south"):
        result_ = float(get_south_mag)
    elif (loc_ == "east"):
        result_ = float(get_east_mag)
    elif (loc_ == "west"):
        result_ = float(get_west_mag)
    elif (loc_ == "central"):
        result_ = float(get_central_mag)
    pm25_result, final_result_for_range, status, comments = getRecommendation(pollutant_type="pm25", result=int(result_), user_id=cache_user_details["UserName"])
    return render_template("PM25.html", show_alert = 1, selected_location = selected_location,  selected_date=_date_, show_mag = 10, direction_place = direction_place, north_mag = get_north_mag, south_mag = get_south_mag, east_mag = get_east_mag, west_mag = get_west_mag, central_mag = get_central_mag, pm25_result=pm25_result, final_result_for_range=final_result_for_range, status=status, comments=comments)
    # return jsonify({"national": 0, "central": getPredicVal(_date_, location=direction_place["central"], table="PM2"), "west": getPredicVal(_date_, location=direction_place["west"], table="PM2"), "north": getPredicVal(
    #     _date_, location=direction_place["north"], table="PM2"), "east": getPredicVal(_date_, location=direction_place["east"], table="PM2"), "south": getPredicVal(_date_, location=direction_place["south"], table="PM2")})


@cross_origin
@app.route('/uv', methods=['POST'])
def check_uv():
    # Datetime has to be in this format YYYY-MM-DDTHH-MM-SS
    # 2019-04-24T10%3A00%3A00
    date = json.loads(request.data)['date']
    if checkEarlier(date):
        url = 'https://api.data.gov.sg/v1/environment/uv-index?date_time=' + str(date).replace(" ", "-")\
            + "T10%3A00%3A00"
        headers = {
            'Accept': 'application/json',
            'Content-Type': "application/json"
        }
        r = requests.get(url, headers=headers)
        result = json.loads(
            r.text)['items'][0]["index"][0]["value"]
        return jsonify(result)
    else:
        return "No Predicted values after this date"


@cross_origin
@app.route('/psi', methods=['POST'])
def check_psi():
    """
    Datetime has to be in this format YYYY-MM-DDTHH-MM-SS
    2019-04-24T10%3A00%3A00
    """
    print("_________________________________ PSI    ENTERED THE FUNCTION_______________________________________________")
    selected_location = request.form.get('selected_location')
    selected_date = request.form.get('selected_date')
    print("_________________________________GOT SOME VALUES_______________________________________________")
    print(selected_location)
    print(type(selected_location))
    print("_________________________________LOCATION ABOVE_______________________________________________")
    print(selected_date)
    print(type(selected_date))
    print("_________________________________DATE ABOVE_______________________________________________")
    # return
    # date = json.loads(request.data)['date']
    # if (1<2):
    if checkEarlier(selected_date):
        print("_________________________________ENTERED IF CONDITION_______________________________________________")
        url = 'https://api.data.gov.sg/v1/environment/psi?date_time=' + str(selected_date) + "T10%3A00%3A00"
        print("_________________________________URL SUCCESS PSI_______________________________________________")
        headers = {
            'Accept': 'application/json',
            'Content-Type': "application/json"
        }
        print("_________________________________headers SUCCESS PSI_______________________________________________")
        r = requests.get(url, headers=headers)
        print("_________________________________get request SUCCESS PSI_______________________________________________")
        result = json.loads(r.text)['items'][0]['readings']["psi_twenty_four_hourly"]
        # result is type dictionary
        print(result)
        #         2020-03-22
        # <class 'str'>
        #      result  = {
        #   "central": 19,
        #   "east": 8,
        #   "north": 13,
        #   "south": 11,
        #   "west": 14
        # }

        print(type(result))
        print("_________________________________result ABOVE_______________________________________________")
        psi_result, final_result_for_range, status, comments = getRecommendation(pollutant_type="psi", result= result[whereIsThis(selected_location)], user_id=cache_user_details["UserName"])
        # return jsonify(result)
        return render_template("PSI.html", show_alert = 1, selected_location = selected_location, selected_date=selected_date, show_mag = 10, north_mag = result['north'], south_mag = result['south'], east_mag = result['east'], west_mag = result['west'], central_mag = result['central'], psi_result=psi_result, final_result_for_range=final_result_for_range, status=status, comments=comments)
    else:
        return PSIPredict(selected_date, direction_place, selected_location = selected_location)

def loginCheck(userName, password):
    un = db.query(user_DB).get(userName)
    if ( None == un ):
        print("Invalid UserName ")
        return (False, 1)
    if( password != un.Password):
        print("Invalid Password ")
        return (False, 2)
    return (True, 3)

north_locations=['Admirality', 'Kranji', 'Woodlands', 'Sembawang', 'Yishun', 'Yio Chu Kang', 'Seletar', 'Sengkang']
south_locations=['Holland', 'Queenstown', 'Bukit Merah', 'Telok Blangah', 'Pasir Panjang', 'Sentosa', 'Bukit Timah', 'Newton', 'Orchard', 'City', 'Marina South']
east_locations=['Serangoon','Punggol','Hougang','Tampines','Pasir Ris','Loyang','Simei','Kallang','Katong',' East Coast','Macpherson', 'Bedok', 'Pulau Ubin', 'Pulau Tekong']
west_locations=['Lim Chu Kang', 'Choa Chu Kang', 'Bukit Panjang', 'Tuas', 'Jurong East', 'Jurong West', 'Jurong Industrial Estate', 'Bukit Batok', 'Hillview', 'West Coast', 'Clementi']
central_locations=['Thomson', 'Marymount', 'Sin Ming', 'Ang Mo Kio', 'Bishan', 'Serangoon Gardens', 'MacRitchie', 'Toa Payoh']

@app.route("/")
def homePage():
    return render_template("HomePage.html")

# @app.route("/")
@app.route("/Login")
def polutexHome():
    return render_template("polutexHome.html", message= "work")


@app.route("/SignUp")
def signUp():
    """Sign Up."""
    return render_template("signUp.html")


signUp_cache = {"user_id":None, "Name":None, "Password":None, "Age":None, "Gender":None, "Nationality":None, "Phone_number":None, "Emergency_contact_number":None, "Email":None, "has_disease":None  }

@app.route("/User", methods=["POST"])
def newPolutexUser():
    """Sign Up."""
    user_id = request.form['username']
    name = request.form['Name']
    password = request.form['password']
    Age = request.form['Age']
    Gender = request.form['Gender']
    Nationality = request.form['Nationality']
    Phone_Number = request.form['Phone Number']
    Emergency_Contact_Number = request.form['Emergency Contact Number']
    Email = request.form['Email']
    has_disease = request.form['disease_Bool']

    if(has_disease == "No"):
        db.add(user_DB(Username=user_id, Password=password, Name=name, Age=Age, Gender=Gender, Nationality=Nationality, Phone_number=Phone_Number, Emergency_contact_number=Emergency_Contact_Number, Email=Email, has_disease = has_disease))
        db.commit()
        return render_template("polutexHome.html")
    elif(has_disease == "Yes"):
        signUp_cache["user_id"] = user_id
        signUp_cache["Name"] = name
        signUp_cache["Password"] = password
        signUp_cache["Age"] = Age
        signUp_cache["Gender"] = Gender
        signUp_cache["Nationality"] = Nationality
        signUp_cache["Phone_number"] = Phone_Number
        signUp_cache["Emergency_contact_number"] = Emergency_Contact_Number
        signUp_cache["Email"] = Email
        signUp_cache["has_disease"] = "Yes"
        return render_template("addDisease.html")
    else:
        return render_template("signUp.html")

@app.route("/addDisease", methods=['GET', 'POST'])
def addDisease():
    """Sign Up."""
    if request.method == 'POST':
        check_box_list  = request.form.getlist('mycheckbox')
        print(check_box_list)
        if(len(check_box_list) == 0):
            return render_template("addDisease.html", message="You have not selected any Disease")
        else:
            db.add(user_DB(Username=signUp_cache["user_id"], Password=signUp_cache["Password"], Name=signUp_cache["Name"] , Age=signUp_cache["Age"], Gender=signUp_cache["Gender"] , Nationality=signUp_cache["Nationality"] , Phone_number=signUp_cache["Phone_number"], Emergency_contact_number=signUp_cache["Emergency_contact_number"], Email=signUp_cache["Email"] , has_disease = signUp_cache["has_disease"]))
            if ('Allergies to dust' in check_box_list):
                Allergies_to_dust_bool = "Yes"
            else:
                Allergies_to_dust_bool = "No"

            if ('Asthma' in check_box_list):
                Asthma_bool = "Yes"
            else:
                Asthma_bool = "No"

            if ('Bronchitis' in check_box_list):
                Bronchitis_bool = "Yes"
            else:
                Bronchitis_bool = "No"

            if ('Lung cancer' in check_box_list):
                Lung_cancer_bool = "Yes"
            else:
                Lung_cancer_bool = "No"

            if ('Lung collapse' in check_box_list):
                Lung_collapse_bool = "Yes"
            else:
                Lung_collapse_bool = "No"

            if ('Respiratory inflammation' in check_box_list):
                respiratory_Inflammation_bool = "Yes"
            else:
                respiratory_Inflammation_bool = "No"

            if ('Pneumonia' in check_box_list):
                Pneumonia_bool = "Yes"
            else:
                Pneumonia_bool = "No"

            db.add(disease_DB(Username=signUp_cache["user_id"], Allergies_to_dust=Allergies_to_dust_bool, Asthma=Asthma_bool, Bronchitis=Bronchitis_bool, Lung_cancer=Lung_cancer_bool, Lung_collapse=Lung_collapse_bool, respiratory_Inflammation=respiratory_Inflammation_bool, Pneumonia=Pneumonia_bool))
            db.commit()
            return render_template("polutexHome.html")


    # db.add(user_DB(Username=user_id, Password=password, Name=name, Age=Age, Gender=Gender, Nationality=Nationality, Phone_number=Phone_Number, Emergency_contact_number=Emergency_Contact_Number, Email=Email, Health_condition=Health_conditionT))
    # db.commit()
    # return render_template("polutexHome.html")

cache_user_details = {"UserName": None, "Password": None, "Name": None, "Age": None, "Gender": None, "Nationality": None, "Phone_Number":None, "Emergency_contact_number": None, "Email": None, "has_disease": None}


@app.route("/loginAttempt/", methods=["POST"])
def loginAttempt():
    """Sign Up."""
    user_id = request.form['username']
    # name = request.form['Name']
    password = request.form['password']
    # return render_template("loggedIn.html", name = user_id)
    sf =  loginCheck(userName = user_id, password = password)
    if(sf[0]):
        # temp = db.query(readerdb).get(user_id)
        # name = temp.name
        # allBooks =db.query(booksdb).all()
        uName = db.query(user_DB).get(user_id)
        usernameT = uName.Username
        passwordT = uName.Password
        nameT = uName.Name
        ageT = uName.Age
        ganderT = uName.Gender
        nationalityT = uName.Nationality
        phone_NumberT = uName.Phone_number
        emergency_Contact_NumberT = uName.Emergency_contact_number
        emailT = uName.Email
        has_diseaseT = uName.has_disease

        cache_user_details["UserName"] = usernameT
        cache_user_details["Password"] = passwordT
        cache_user_details["Name"] = nameT
        cache_user_details["Age"] = ageT
        cache_user_details["Gender"] = ganderT
        cache_user_details["Nationality"] = nationalityT
        cache_user_details["Phone_Number"] = phone_NumberT
        cache_user_details["Emergency_contact_number"] = emergency_Contact_NumberT
        cache_user_details["Email"] = emailT
        cache_user_details["has_disease"] = has_diseaseT



        return render_template("dashboard.html", usernameT=usernameT, passwordT=passwordT, nameT=nameT, ageT=ageT, ganderT=ganderT, nationalityT=nationalityT, phone_NumberT=phone_NumberT, emergency_Contact_NumberT=emergency_Contact_NumberT, emailT=emailT, has_disease=has_diseaseT)
    elif(sf[1] == 1):
        return render_template("polutexHome.html", wrong = "Invalid UserName")
    elif(sf[1] == 2):
        return render_template("polutexHome.html", wrong = "Invalid Password")



@app.route("/heatMap", methods=["POST"])
def heatMap():
    """Heat Map."""
    return render_template("heatMap.html")


@app.route("/guestDashboard", methods=["GET"])
def guestDashboard():
    """dashboard"""
    nameT = cache_user_details["Name"]
    return render_template("guestDashboard.html", nameT=nameT)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """dashboard"""
    return render_template("dashboard.html")

@app.route("/profile/", methods=["GET"])
def userProfile():
    usernameT = cache_user_details["UserName"]
    passwordT = cache_user_details["Password"]
    nameT = cache_user_details["Name"]
    ageT = cache_user_details["Age"]
    ganderT = cache_user_details["Gender"]
    nationalityT = cache_user_details["Nationality"]
    phone_NumberT = cache_user_details["Phone_Number"]
    emergency_Contact_NumberT = cache_user_details["Emergency_contact_number"]
    emailT = cache_user_details["Email"]
    has_diseaseT = cache_user_details["has_disease"]

    if(has_diseaseT == "No"):
        return render_template("loggedIn.html", usernameT=usernameT, passwordT=passwordT, nameT=nameT, ageT=ageT, ganderT=ganderT, nationalityT=nationalityT, phone_NumberT=phone_NumberT, emergency_Contact_NumberT=emergency_Contact_NumberT, emailT=emailT, diseasesT= "None")

    print(usernameT)
    usernameD = db.query(disease_DB).get(usernameT)
    print(usernameD)
    diseases_str = ""
    if("Yes" == usernameD.Allergies_to_dust):
        diseases_str += " Allergies to dust,"

    if("Yes" == usernameD.Asthma):
        diseases_str += " Asthma,"

    if("Yes" == usernameD.Bronchitis):
        diseases_str += " Bronchitis,"

    if("Yes" == usernameD.Lung_cancer):
        diseases_str += " Lung Cancer,"

    if("Yes" == usernameD.Lung_collapse):
        diseases_str += " Lung Collapse,"

    if("Yes" == usernameD.respiratory_Inflammation):
        diseases_str += " Respirator Inflammation,"

    if("Yes" == usernameD.Pneumonia):
        diseases_str += " Pneumonia,"

    diseases_str = diseases_str[:-1]
    print(diseases_str)

    return render_template("loggedIn.html", usernameT=usernameT, passwordT=passwordT, nameT=nameT, ageT=ageT, ganderT=ganderT, nationalityT=nationalityT, phone_NumberT=phone_NumberT, emergency_Contact_NumberT=emergency_Contact_NumberT, emailT=emailT, diseasesT= diseases_str)


@app.route("/settings", methods=["GET"])
def settings():
    """settings"""
    return render_template("settings.html", show_mag = 2)

@app.route("/PSI", methods=["GET"])
def PSI():
    """PSI"""
    selected_location = request.form.get('selected_location')
    selected_date = request.form.get('selected_date')
    print("________________________________________________________________________________")
    print(selected_location)
    print(selected_date)
    return render_template("PSI.html", show_alert = 0, selected_location = "Select Location", selected_date = "Select Date", show_mag = 2, north_mag = 10, south_mag = 10, east_mag = 10, west_mag = 10, central_mag = 10)

@app.route("/PM25", methods=["GET"])
def PM25():
    """PM25"""
    selected_location = request.form.get('selected_location')
    selected_date = request.form.get('selected_date')
    print("________________________________________________________________________________")
    print(selected_location)
    print(selected_date)
    return render_template("PM25.html", show_alert = 0, selected_location = "Select Location", selected_date = "Select Date", show_mag = 2, north_mag = 10, south_mag = 10, east_mag = 10, west_mag = 10, central_mag = 10)

@cross_origin
@app.route('/pm', methods=['POST'])
def check_pm():
    """
    Datetime has to be in this format YYYY-MM-DDTHH-MM-SS
    2019-04-24T10%3A00%3A00
    """
    print("_________________________________ENTERED THE FUNCTION_______________________________________________")
    selected_location = request.form.get('selected_location')
    selected_date = request.form.get('selected_date')
    print("_________________________________GOT SOME VALUES_______________________________________________")
    print(selected_location)
    print(type(selected_location))
    print("_________________________________LOCATION ABOVE_______________________________________________")
    print(selected_date)
    print(type(selected_date))
    print("_________________________________DATE ABOVE_______________________________________________")
    # return
    # date = json.loads(request.data)['date']
    # if (1<2):
    if checkEarlier(selected_date):
        print("_________________________________ENTERED IF CONDITION_______________________________________________")
        url = 'https://api.data.gov.sg/v1/environment/pm25?date_time=' + str(selected_date)\
            + "T10%3A00%3A00"
        print("_________________________________URL SUCCESS_______________________________________________")
        headers = {
            'Accept': 'application/json',
            'Content-Type': "application/json"
        }
        print("_________________________________headers SUCCESS_______________________________________________")
        r = requests.get(url, headers=headers)
        print("_________________________________get request SUCCESS_______________________________________________")
        result = json.loads(r.text)['items'][0]['readings']["pm25_one_hourly"]
        # result is type dictionary
        print(result)


        print(type(result))
        print("_________________________________result ABOVE_______________________________________________")
        # return jsonify(result)
        pm25_result, final_result_for_range, status, comments = getRecommendation(pollutant_type="pm25", result= result[whereIsThis(selected_location)], user_id=cache_user_details["UserName"])
        return render_template("PM25.html", show_alert = 1, selected_location = selected_location, selected_date=selected_date, show_mag = 10, north_mag = result['north'], south_mag = result['south'], east_mag = result['east'], west_mag = result['west'], central_mag = result['central'], pm25_result=pm25_result, final_result_for_range=final_result_for_range, status=status, comments=comments)
    else:
        return PM2Predict(selected_date, direction_place, selected_location = selected_location)

# https://api.data.gov.sg/v1/environment/pm25?date_time=2020-04-10\T10%3A00%3A00


@app.route("/covid19", methods=["GET"])
def covid19():
    """covid19."""
    selected_country = cache_user_details["Nationality"]
    Total_Cases, Total_Deaths, Total_Active_Cases, Total_Recovered_Cases, num_affected = goCorona(selected_country)
    selected_country = selected_country.capitalize()
    return render_template("covid19.html" , selected_country=selected_country, Total_Cases=Total_Cases, Total_Deaths=Total_Deaths, Total_Active_Cases=Total_Active_Cases, Total_Recovered_Cases = Total_Recovered_Cases, num_affected=num_affected)


@app.route("/diabetes", methods=['GET', 'POST'])
def diabetes():
    """diabetes."""
    if request.method == 'POST':
        Glucose = float(request.form.get('Glucose'))
        BloodPressure = float(request.form.get('BloodPressure'))
        SkinThickness = float(request.form.get('SkinThickness'))
        Insulin = float(request.form.get('Insulin'))
        BMI = float(request.form.get('BMI'))
        ageT = int(cache_user_details["Age"])

        print(type(Glucose))
        print(Glucose)

        print(type(BloodPressure))
        print(BloodPressure)

        print(type(SkinThickness))
        print(SkinThickness)

        print(type(Insulin))
        print(Insulin)

        print(type(BMI))
        print(BMI)

        print(type(ageT))
        print(ageT)

        diabetes_advice, risk_percentage = goDiabetes(glucose=Glucose, bp=BloodPressure, skinthickness=SkinThickness, insulin=Insulin, bmi=BMI, age=ageT)
        print("_________________________________diabetes ABOVE_______________________________________________")
        return render_template("diabetes.html", show_alert = 1, diabetes_advice=diabetes_advice, risk_percentage=risk_percentage)
    return render_template("diabetes.html", show_alert = 0)


@app.route("/dengue", methods=["GET"])
def dengue():
    """dengue."""
    return render_template("dengue.html")

@app.route("/", methods=["GET"])
def logOut():
    """logOut."""
    polutexHome()
    return render_template("polutexHome.html", message= "work")
    # render_template("logOut.html")
    # return render_template("logOut.html")



# if __name__ == '__main__':
# 	app.run(debug=True, port=7000)

def diabetes_risk_prediction(glucose, bp, skinthickness, insulin, bmi, age):

    indicator_list = [glucose, bp, skinthickness, insulin, bmi, age]

    predictions = log_model.predict_proba(np.array(indicator_list).reshape(1, -1))

    risk = predictions[0,1]

    print("-"*len("Health Indicator Analysis"))
    print("Health Indicator Analysis")
    print("-"*len("Health Indicator Analysis"))

    if risk < 0.3:
        print("You are probably in good health, keep it up.")

    elif risk > 0.7:
        print("See a doctor as soon as you can and listen to their recommendations. You might be on the way to developing diabetes if you don't change your lifestyle.")

    elif risk > 0.9:
        print("Go to a hospital right away. Odds are high you have diabetes.")

    else:
        print("You should be alright for the most part, but take care not to let your health slip.")

    return print("Your Diabetes Risk is {:.2f}/50.".format(risk*0.5*100))










