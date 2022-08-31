

import anvil.server
from anvil.tables import app_tables
import datetime

import requests
import json


@anvil.server.callable
def estimate_earnings(amount, days):
  data = {}
  current_day_data = get_current_day()
  current_day=current_day_data['day']
  current_payout=current_day_data['payout']
  price_url='https://uniswapdataapi.azurewebsites.net/api/hexPrice'
  price = float(anvil.http.request(price_url, json=True)['hexUsd'])
  
  return data


@anvil.server.callable
def get_daily_data():
  query = """query {
  dailyDataUpdates(orderBy: endDay, orderDirection: desc) {
    endDay
    payoutPerTShare
    payout
    shares
    beginDay
    timestamp
    updaterAddr
    
    
    
  }
  }
  """
  url = 'https://api.thegraph.com/subgraphs/name/codeakk/hex'
  r = requests.post(url, json={'query': query})
  print(r)
  json_data = json.loads(r.text)

  daily_data_updates = json_data['data']['dailyDataUpdates']
    
  return daily_data_updates


@anvil.server.callable
def start_get_stakes():
  addresses=['0x0d86EB9f43C57f6FF3BC9E23D8F9d82503f0e84b']
  print(addresses)
  #return anvil.server.launch_background_task('get_stakes',addresses)

@anvil.server.background_task
@anvil.server.callable
def get_stakes(addresses):
    current_day_data = get_current_day()
    current_day=current_day_data['day']
    current_payout=current_day_data['payout']
    price_url='https://uniswapdataapi.azurewebsites.net/api/hexPrice'
    price = float(anvil.http.request(price_url, json=True)['hexUsd'])
  
    address_list=''
    first=True
    for a in addresses:
      if first:
        address_list+='["'
        first=False
      else:
        address_list+='", "'
        
      address_list+=a
    query_list=address_list
    query_list+='"]'
      
    
    query = """query {
          stakeStarts(where: { stakerAddr_in: *address* ,stakeEnd:null},orderBy: stakeTShares, orderDirection: desc) {
            id
            stakerAddr
            stakeId
            stakeTShares
            timestamp
            startDay
            endDay
            stakedDays
            stakeShares
            stakeTShares
            stakedHearts
            
            
          }
        }
        """.replace('*address*', query_list)
    url = 'https://api.thegraph.com/subgraphs/name/codeakk/hex'
    r = requests.post(url, json={'query': query})
    print(r)
    try:
      json_data = json.loads(r.text)
    except:
      json_data = json.loads(r.text)
    stake_starts = json_data['data']['stakeStarts']
    data = []
    for s in stake_starts:
      row = dict(s)
      row['stakedHex']=int(int(s['stakedHearts'])/(10**8))
     
      
      value_to_date = earnings_to_date(s['startDay'], current_day,s['stakeTShares'],row['stakedHex'])
      
      row['currentValue']=value_to_date
      row['daysRemaining']=int(s['endDay'])-current_day
      row['currentDayPayout']=current_day_data['payout']
      row['currentPrice']=price
      for k in ['id', 'stakeId', 'stakeShares', 'stakedHearts']:
        row.pop(k, None)
      data.append(row)
    app_tables.search_log.add_row(addresses=addresses,results=data,searched_at=datetime.datetime.utcnow())
    
    return data
  

  
def earnings_to_date(start, end, t_shares, principal):

  
  query="""{
  dailyDataUpdates(first:1000,where:{beginDay_gte:*start*, endDay_lte:*end*},orderBy: endDay, orderDirection: desc) {
    beginDay
    endDay
    payoutPerTShare
    payout
    shares
    timestamp
  }
}
""".replace('*start*',str(start)).replace('*end*',str(end))
  url = 'https://api.thegraph.com/subgraphs/name/codeakk/hex'
  r = requests.post(url, json={'query': query})
  
  json_data = json.loads(r.text)
  
  daily_data_updates = json_data['data']['dailyDataUpdates']
  
  earnings_to_date =0
  bpd=0
  for d in daily_data_updates:
    earnings_to_date+=float(t_shares)*float(d['payoutPerTShare'])
  if int(start)<353 and int(end)>354:
    bpd+=float(t_shares)*3641.7317
    
  earnings_to_date+=bpd
  print(earnings_to_date)
  print(t_shares, start,end)
  
  return int(earnings_to_date+principal)
    

def get_current_day():
  query="""{
  dailyDataUpdates(first:1,orderBy: endDay, orderDirection: desc) {
    beginDay
    endDay
    payoutPerTShare
    payout
    shares
    timestamp
  }
}
"""
  url = 'https://api.thegraph.com/subgraphs/name/codeakk/hex'
  r = requests.post(url, json={'query': query})
  
  json_data = json.loads(r.text)

  daily_data_updates = json_data['data']['dailyDataUpdates']
  return {'day':daily_data_updates[0]['endDay'],'payout':daily_data_updates[0]['payoutPerTShare']}
  
