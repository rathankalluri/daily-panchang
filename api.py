# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from panchanga import *
from datetime import datetime
from datetime import timedelta
import sys
import pytz
import json

app = Flask(__name__)

@app.route('/panchang-api/v1.0/')
def login():
    date = request.args.get('date')
    loc = request.args.get('location')

    star_list = ["Ashwini","Bharani","Krittika","Rohini","Mrigashirsha","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Svati","Visakha","Anuradha","Jyeshtha","Mula","Purva ashadha","Uttara ashada","Sravana","Dhanistha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]

    tithi_list = ["Padyami","Vidiya","Thadiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dasami","Ekadasi","Dvadasi","Trayodasi","Chaturdashi","Amavasya","Padyami","Vidiya","Thadiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dasami","Ekadasi","Dvadasi","Trayodasi","Chaturdashi","Pournami"]

    masa_list = ["Chaitra","Vaisakha","Jyeshta","Ashada","Shravana","Bhadrapada","Aswayuja","Kartika","Margasira","Pushya","Magha","Phalguna"]

    vaara_list = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    yoga_list = ["Vishkumbha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma","Dhriti","Shoola","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"]

    karna_list = ["Kintughna","Bava","Baalava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Gara","Taitila","Kaulava","Vanija","Vishti",\
        "Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Shakuni","Chatushpada","Naga"]

    try:
        date = datetime.strptime(date,'%Y-%m-%d')
        date = date.date()
    except IndexError:
        date = datetime.now()

    date = gregorian_to_jd(Date(date.year, date.month, date.day))
    #date = gregorian_to_jd(Date(2019, 4, 11))

    data = {
        'Given Location':loc,
        'Given Date':date
    }
    #print loc
    #print date

    with open("newcities.json") as fp:
        cities = json.load(fp)
        #only_cities = cities.keys()
    if loc not in cities:
        return jsonify({'Error':'City Not found'})

    lat = float(cities[loc]["latitude"])
    lon = float(cities[loc]["longitude"])
    tz = cities[loc]["timezone"]
    #timez = pytz.timezone(tz)

    #dt = datetime.utcnow()
    #offset_seconds = timez.utcoffset(dt).seconds
    #offset_hours = offset_seconds / 3600.0
    #tz = "{:+d}:{:02d}".format(int(offset_hours), int((offset_hours % 1) * 60))
    #tz = int(tz)

    dt = datetime.now()
    #print (dt)
    tz_now = pytz.timezone(tz)
    tz = tz_now.utcoffset(dt).total_seconds()/60/60

    location = Place(lat, lon, tz)
    #print location

    MR = moonrise(date, location)
    MR = "{0}:{1}:{2}".format(MR[0],MR[1],MR[2])
    MS = moonset(date, location)
    MS = "{0}:{1}:{2}".format(MS[0],MS[1],MS[2])
    SR = sunrise(date, location)[1]
    SR = "{0}:{1}:{2}".format(SR[0],SR[1],SR[2])
    SS = sunset(date, location)[1]
    SS = "{0}:{1}:{2}".format(SS[0],SS[1],SS[2])
    Vaara = vaara(date)
    Karna = karana(date, location)
    Tithi = tithi(date, location)
    Nakshatra = nakshatra(date,location)
    Yoga = yoga(date,location)
    Masa = masa(date, location)
    Ritu = ritu(Masa[0])

    #print("Moon Rise :{0}".format(MR))
    #print("Moon Set :{0}".format(MS))
    #print("Sun Rise :{0}".format(SR))
    #print("Sun Set :{0}".format(SS))
    if Karna:
        karna = karna_list[Karna[0]-1]
    if Vaara:
        day_name = vaara_list[Vaara]
    #print("Vaara :{0}".format(day_name))
    #print("Karana :{0}".format(Karna))

    Tithi1 = tithi_list[Tithi[0]-1]
    Tithi1_time = timedelta(hours=Tithi[1][0],minutes=Tithi[1][1], seconds=Tithi[1][2])
    Tithi1_time = str(Tithi1_time)
    if '1 day' in Tithi1_time:
        Tithi1_time = Tithi1_time.replace('1 day', 'Next day')
    Thithi = "{0} till {1}".format(Tithi1, Tithi1_time)
    
    if len(Tithi)>2:
        Tithi2 = tithi_list[Tithi[2]-1]
        Tithi2_time = Tithi[3]
        Tithi2_time = timedelta(hours=Tithi[3][0],minutes=Tithi[3][1], seconds=Tithi[3][2])
        Tithi2_time = str(Tithi2_time)
        if '1 day' in str(Tithi2_time):
            Tithi2_time = Tithi2_time.replace('1 day', 'Next day')
        Thithi = "{0} till {1}, Tithi {2} till {3}".format(Tithi1, Tithi1_time, Tithi2, Tithi2_time)

    if Nakshatra:
        star = star_list[Nakshatra[0]-1]
        star_time = timedelta(hours=Nakshatra[1][0],minutes=Nakshatra[1][1], seconds=Nakshatra[1][2])
        star_time = str(star_time)

    if '1 day' in star_time:
        star_time = star_time.replace('1 day', 'Next day')
    #print("Nakshatra :{0} , Till {1}".format(star,star_time))
    Nakshatram = "{0} , Till {1}".format(star,star_time)
    
    if Yoga:
        yogam = yoga_list[Yoga[0]-1]
        yoga_time = timedelta(hours=Yoga[1][0],minutes=Yoga[1][1], seconds=Yoga[1][2])
        yoga_time = str(yoga_time)
        Yogam = "{0} , Till {1}".format(yogam,yoga_time)

    if Masa:
        masam = masa_list[Masa[0]-1]
        if Masa[1]:
            masam = "Adhika "+masam
    #print("Masa :{0}".format(masam))

    data2 = {
        'MoonRise': MR,
        'MoonSet': MS,
        'SunRise': SR,
        'SunSet': SS,
        'Vaaram': day_name,
        'Karna': karna,
        'Tithi': Thithi,
        'Maasa': masam,
        'Ritu': Ritu,
        'Nakshatra': Nakshatram,
        'Yoga':Yogam
    }
    return jsonify(data2)

if __name__ == '__main__':
    app.run(debug=True)