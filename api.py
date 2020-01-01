# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from panchanga import *
from datetime import datetime
from datetime import timedelta
import sys
import pytz
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/panchang-api/*": {"origins": "*"}})

@app.route('/panchang-api/v1.0/')
def login():
    date = request.args.get('date')
    loc = request.args.get('location')

    #PARAMETERS LISTS

    star_list = ["Ashwini","Bharani","Krittika","Rohini","Mrigashirsha","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Svati","Visakha","Anuradha","Jyeshtha","Mula","Purva ashadha","Uttara ashada","Sravana","Dhanistha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]

    tithi_list = ["Padyami","Vidiya","Thadiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dasami","Ekadasi","Dvadasi","Trayodasi","Chaturdashi","Amavasya","Padyami","Vidiya","Thadiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dasami","Ekadasi","Dvadasi","Trayodasi","Chaturdashi","Pournami"]

    masa_list = ["Chaitra","Vaisakha","Jyeshta","Ashada","Shravana","Bhadrapada","Aswayuja","Kartika","Margasira","Pushya","Magha","Phalguna"]

    vaara_list = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    yoga_list = ["Vishkumbha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma","Dhriti","Shoola","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"]

    karna_list = ["Kintughna","Bava","Baalava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Gara","Taitila","Kaulava","Vanija","Vishti",\
        "Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti","Shakuni","Chatushpada","Naga"]

    ritu_list = ["Vasant - Spring","Grishma - Summer","Varsha - Monsoon","Sharad - Autumn","Hemant - Pre-winter","Shishir - Winter"]

    star_start_time = [16.8,19.2,21.6,20.8,15.2,14,21.6,17.6,22.4,21.6,17.6,16.8,18,17.6,15.2,15.2,13.6,15.2,17.6,19.2,17.6,13.6,13.6,16.8,16,19.2,21.6]

    varjam_start_time = [20,9.6,12,16,5.6,8.4,12,8,12.8,12,8,12.8,12,8,7.2,8.4,8,5.6,5.6,4,5.6,[8,22.4],9.6,8,4,4,7.2,6.4,9.6,12]

        
    # Variables for Rahu, Yama, Gulika and durmuhurtha calculations
    rahu_kala_cal = [0.875,0.125,0.75,0.5,0.625,0.375,0.25]
    yama_kala_cal = [0.5,0.375,0.25,0.125,1,0.75,0.625]
    gulika_kala_cal = [0.75,0.625,0.5,0.375,0.25,0.125,1]
    durmu_cal = [0.14,[6.4,8.8],[2.4,4.8],5.6,[4,8.8],[2.4,6.4],1.6]


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
    MR1 = moonrise(date, location)
    MR = "{0}:{1}:{2}".format(MR[0],MR[1],MR[2])
    MS = moonset(date, location)
    MS1 = moonset(date, location)
    MS = "{0}:{1}:{2}".format(MS[0],MS[1],MS[2])

    SRA = sunrise(date, location)[1]
    #SR1 = sunrise(date, location)[0]
    #SRO = timedelta(hours=SRA[0],minutes=SRA[1],seconds=SRA[2])
    SR = "{0}:{1}:{2}".format(SRA[0],SRA[1],SRA[2])

    SSA = sunset(date, location)[1]
    #SS1 = sunset(date, location)[0]
    SS = "{0}:{1}:{2}".format(SSA[0],SSA[1],SSA[2])
    Vaara = vaara(date)
    Karna = karana(date, location)
    Tithi = tithi(date, location)
    Nakshatra = nakshatra(date,location)
    Yoga = yoga(date,location)
    Masa = masa(date, location)
    Ritu = ritu(Masa[0])

    #Day Duration for Rahu, Yamganda kalas
    day_dura = day_duration(date, location)
    day_dura_formated = "{0}:{1}:{2}".format(day_dura[1][0],day_dura[1][1],day_dura[1][2])

    def delta_to_dec(timedel):
        hours, remainder = divmod(timedel.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        m = int(minutes) * 1/60
        s = int(seconds) * 1/3600
        h = int(hours)
        dura = h + m + s
        return dura, hours, minutes, seconds
    
    def get_night_duration(MR, MS):
        MRT = timedelta(hours=MR1[0],minutes=MR1[1],seconds=MR1[2])
        MST = timedelta(hours=MS1[0],minutes=MS1[1],seconds=MS1[2])

        night_diff = MST-MRT
        night_dura, hours, minutes, seconds = delta_to_dec(night_diff)

        night_dura_formated = "{0}:{1}:{2}".format(hours,minutes,seconds)
        #night_dura = timedelta(hours=hours,minutes=minutes,seconds=seconds)
        return night_dura, night_dura_formated

    if Karna is not None:
        karna = karna_list[Karna[0]-1]
    else:
        karna = ''
    if Vaara is not None:
        day_name = vaara_list[Vaara]
    else:
        day_name = ''

    #Tithi Conversion 
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
    
    #Nakshatra Calcuation
    if Nakshatra:
        star = star_list[Nakshatra[0]-1]
        star_time1 = timedelta(hours=Nakshatra[1][0],minutes=Nakshatra[1][1], seconds=Nakshatra[1][2])
        star_time = str(star_time1)

    if '1 day' in star_time:
        star_time = star_time.replace('1 day', 'Next day')
    #print("Nakshatra :{0} , Till {1}".format(star,star_time))
    Nakshatram = "{0} , Till {1}".format(star,star_time)
    
    #Yogam
    #Add pros and cons of Yogas
    if Yoga:
        yogam = yoga_list[Yoga[0]-1]
        yoga_time = timedelta(hours=Yoga[1][0],minutes=Yoga[1][1], seconds=Yoga[1][2])
        yoga_time = str(yoga_time)
        if '1 day' in yoga_time:
            yoga_time = yoga_time.replace('1 day', 'Next day')
        Yogam = "{0} , Till {1}".format(yogam,yoga_time)
    
    #Masa Calcuation
    if Masa:
        masam = masa_list[Masa[0]-1]
        if Masa[1]:
            masam = "Adhika "+masam

    if Ritu is not None:
        Ritu = ritu_list[Ritu]

    def to_dt(decimal_time):
        m = int((decimal_time * 60) % 60)
        s = int((decimal_time * 3600) % 60)
        h = int(decimal_time)
        formated_time = "{0}:{1}:{2}".format(h,m,s)
        return (formated_time)

    def decimal_SR(SRA):
        m = int(SRA[1]) * 1/60
        s = int(SRA[2]) * 1/3600
        h = int(SRA[0])
        decimal_SR = h + m + s
        return decimal_SR

    def rahu_kalam(Vaara,day_dura,rahu_kala_cal,SRA):
        rahu_kal_start = decimal_SR(SRA)+day_dura[0]*rahu_kala_cal[Vaara]
        rahu_kal_end = rahu_kal_start+day_dura[0]*0.125

        rahu_kal_start = to_dt(rahu_kal_start)
        rahu_kal_end = to_dt(rahu_kal_end)

        return ("Start: {0} , End: {1}".format(rahu_kal_start, rahu_kal_end))

    def yamaganda_kalam(Vaara,day_dura,yama_kala_cal,SRA):
        yama_kal_start = decimal_SR(SRA)+day_dura[0]*yama_kala_cal[Vaara]
        yama_kal_end = yama_kal_start+day_dura[0]*0.125

        yama_kal_start = to_dt(yama_kal_start)
        yama_kal_end = to_dt(yama_kal_end)

        return ("Start: {0} , End: {1}".format(yama_kal_start, yama_kal_end))

    def gulika(Vaara,day_dura,gulika_kala_cal,SRA):
        gulika_kal_start = decimal_SR(SRA)+day_dura[0]*gulika_kala_cal[Vaara]
        gulika_kal_end = gulika_kal_start+day_dura[0]*0.125

        gulika_kal_start = to_dt(gulika_kal_start)
        gulika_kal_end = to_dt(gulika_kal_end)

        return ("Start: {0} , End: {1}".format(gulika_kal_start, gulika_kal_end))

    night_dura, night_dura_formated = get_night_duration(MR, MS)

    def durmuhurtham(Vaara,day_dura,SRA,SSA,durmu_cal,night_dura):

        if Vaara in [1,2,4,5]:
            if Vaara == 2:
                durmu1 = decimal_SR(SRA)+day_dura[0]*(durmu_cal[Vaara][0]/12)
                durmu2 = decimal_SR(SSA)+night_dura*(durmu_cal[Vaara][1]/12)
                return durmu1, durmu2, day_dura[0]*(0.8/12)
            else:
                durmu1 = decimal_SR(SRA)+day_dura[0]*(durmu_cal[Vaara][0]/12)
                durmu2 = decimal_SR(SRA)+day_dura[0]*(durmu_cal[Vaara][1]/12)
                return durmu1, durmu2, day_dura[0]*(0.8/12)
        elif Vaara in [0,3,6]:
            durmu1 = decimal_SR(SRA)+day_dura[0]*(durmu_cal[Vaara]/12)
            return durmu1, None, day_dura[0]*(0.8/12)

    rahu_kalam = rahu_kalam(Vaara,day_dura,rahu_kala_cal,SRA)
    yama_kalam = yamaganda_kalam(Vaara,day_dura,yama_kala_cal,SRA)
    gulika_kalam = gulika(Vaara,day_dura,gulika_kala_cal,SRA)
    durmu1, durmu2, day_durat = durmuhurtham(Vaara,day_dura,SRA,SSA,durmu_cal,night_dura) 

    if durmu2==None:
        till = durmu1+day_durat
        durmu_today = "{0} till {1}".format(to_dt(durmu1), to_dt(till))
        #print (durmu_today)
    else:
        till1 = durmu1+day_durat
        till2 = durmu2+day_durat
        durmu_today = "{0} till {1}, and again from {2} till {3}".format(to_dt(durmu1), to_dt(till1), to_dt(durmu2), to_dt(till2))
        #print (durmu_today)

    def amrita_gadiyas(star_time1, Nakshatra, star_start_time):
        #amrita starts after x hours of starting time of nakshatra
        #stime of amrita/varj = start time of Nakshatra * x/24(duration of nakshatra)
        stime_of_star = delta_to_dec(star_time1)
        #print(star_time)
        #print(stime_of_star)
        #print (star_start_time[Nakshatra[0]-1])

        #duration of amrita/varj = duration of nakshatra * 1.6/24
        return True
    
    def varjam():
        return True 

    amrita_gadiyas(star_time1, Nakshatra, star_start_time)

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
        'Yoga':Yogam,
        'Day Duration': day_dura_formated,
        'Night Duration': night_dura_formated,
        'Rahu Kalam': rahu_kalam,
        'Yama Kalam': yama_kalam,
        'Gulika Kalam': gulika_kalam,
        'Durmuhurtam': durmu_today
    }
    return jsonify(data2)

if __name__ == '__main__':
    app.run(debug=True)
