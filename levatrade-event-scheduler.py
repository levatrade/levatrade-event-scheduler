import datetime
import requests
import boto3
import json

from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
daily_settings_table = dynamodb.Table('daily_settings')

sched = BlockingScheduler()

def levatrade_trade_setups():
    td_auth_endpoint = 'http://54.174.182.208:5000/auth'
    data = {
        'username':'dockingunited',
        'account_number':'686214464',
        'password':'Michaelwiggum1',
        'client_id':'BOBBYRITHM'
    }
    headers = {
        'ContentType': 'application/json'
    }
    td_auth_data = requests.post(td_auth_endpoint, data=json.dumps(data), headers=headers)
    daily_settings_table.put_item(Item={
                    'key': 'td_auth',
                    'value': td_auth_data.text
                })

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10)
def start_trading():
    tz = timezone('EST')
    current_date = datetime.now(tz).strftime("%Y-%m-%d")
    sched.add_job(levatrade_trade_setups, 'interval', mins=5, start_date='{} 10:00:00'.format(current_date), end_date='{} 10:00:00'.format(current_date), id='levatrade_trade_setups')
    print('This job is run every weekday at 5pm.')

# at 8:00am EST time we will re auth TD to store new access token for the day
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=8)
def levatrade_auth_td():
    td_auth_endpoint = 'http://54.174.182.208:5000/auth'
    data = {
        'username':'dockingunited',
        'account_number':'686214464',
        'password':'Michaelwiggum1',
        'client_id':'BOBBYRITHM'
    }
    requests.post(td_auth_endpoint, data=data)

    print('This job is run every weekday at 5pm.')

#sched.start()

td_auth_endpoint = 'http://54.174.182.208:5000/auth'
data = {
    'username':'dockingunited',
    'account_number':'686214464',
    'password':'Michaelwiggum1',
    'client_id':'BOBBYRITHM'
}
headers = {
    'ContentType': 'application/json'
}
td_auth_data = requests.post(td_auth_endpoint, data=json.dumps(data), headers=headers)
daily_settings_table.put_item(Item={
                'key': 'td_auth',
                'value': td_auth_data.text
            })