import requests
import json
from datetime import datetime, timedelta
from calendar import monthrange

def sum_month_day(rang):
    data =rang['month']['data']['skillSummaries'][4]
    print json.dumps(data, indent=4, sort_keys=True)
    
    for i in range(1,len(rang['month']['data']['skillSummaries'])):
        rang['month']['data']['skillSummaries'][i]['contactsOutOfSLA'] = str(float(rang['month']['data']['skillSummaries'][i]['contactsOutOfSLA']) + float(rang['today']['data']['skillSummaries'][i]['contactsOutOfSLA']))
        
        rang['month']['data']['skillSummaries'][i]['contactsWithinSLA'] = str(float(rang['month']['data']['skillSummaries'][i]['contactsWithinSLA']) + float(rang['today']['data']['skillSummaries'][i]['contactsWithinSLA']))
        
        rang['month']['data']['skillSummaries'][i]['abandonCount'] = str(float(rang['month']['data']['skillSummaries'][i]['abandonCount']) + float(rang['today']['data']['skillSummaries'][i]['abandonCount']))
        
        if ((float(rang['month']['data']['skillSummaries'][i]['contactsOutOfSLA'])+float(rang['month']['data']['skillSummaries'][i]['contactsWithinSLA']))):
            rang['month']['data']['skillSummaries'][i]['serviceLevel']  = str(100*float(rang['month']['data']['skillSummaries'][i]['contactsWithinSLA']) / (float(rang['month']['data']['skillSummaries'][i]['contactsOutOfSLA'])+float(rang['month']['data']['skillSummaries'][i]['contactsWithinSLA'])))
        
    data =rang['month']['data']['skillSummaries'][4]
        

def put_data(rang):
    headers = {'kf-api-key': '8fcec0536acace78fd91d895fe78878c3f3c3a3d'}
    url = 'https://app.klipfolio.com/api/1/datasource-instances/'+rang['datasource']+'/data'
    r = requests.put(url,headers=headers, data=json.dumps(rang['data']))

def get_data(token):
    current_date = datetime.now()
    today = str(current_date)[:10]
    tomorrow = str(current_date+timedelta(days=1))[:10]
    this_week_start = str(current_date-timedelta(days=current_date.weekday()))[:10]
    month_beginning = str(current_date-timedelta(days=current_date.timetuple().tm_mday-1))[:10]
    
    #handle API date range limit of 30 days
    eom = monthrange(current_date.year,current_date.month)[1]
    if eom > 30:
        eom = 30 
    month_end = str(current_date.year)+'-'+str(current_date.month)+'-'+str(eom)
    
    headers = {'Authorization' : 'bearer '+token}
    ranges = {'today': {'data' : '', 'params': [today,tomorrow], 'datasource': '2e01d07f1efa0ab0409e7d1897f27c59'}, 
            'week': {'data' : '', 'params': [this_week_start,tomorrow], 'datasource': 'ecaf2b9852d7d1c113bd4dc3712bb937'},
            'month': {'data' : '', 'params': [month_beginning,month_end], 'datasource': '60244b8045174c52e5aabd7914931ab9'}}
    for key,value in ranges.iteritems():
        url = 'https://api-c19.incontact.com/inContactAPI/services/v8.0/skills/summary?startDate='+value['params'][0]+'&endDate='+value['params'][1]
        ranges[key]['data'] = requests.get(url, headers=headers).json()
        ranges[key] 
        print key
        if (key == 'month' and eom > 30):
            sum_month_day(ranges)       
        put_data(ranges[key])

def get_token():
    token_url = 'https://api.incontact.com/InContactAuthorizationServer/Token'
    headers = {'Content-Type':'application/json','Authorization':'basic {KEY}'}
    payload = {'grant_type' : 'password','username' : '{USERNAME}','password' : '{PASSWORD}','scope' : ''}

    r = requests.post(token_url, headers=headers, data=json.dumps(payload))
    access_token = r.json()['access_token']
    get_data(access_token)

get_token()
