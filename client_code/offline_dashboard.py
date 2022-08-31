from ._anvil_designer import offline_dashboardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.http
import anvil.server

try:
  from anvil.js.window import ethers, Web3
except Exception as e:
  alert(e)
import anvil.js
MAXI_CONTRACT_ADDRESS ="0x0d86EB9f43C57f6FF3BC9E23D8F9d82503f0e84b"
class offline_dashboard(offline_dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    try:
      self.address = properties['search_address']
      
    except:
      self.address = None
    self.main=properties['main']
    
    
    
    
    
  
    

    # Any code you write here will run when the form opens.
  def text_box_address_change(self, **event_args):
    self.address=event_args['sender'].text
    if self.address not in [None, ""]:
      self.address=Web3.utils.toChecksumAddress(self.address)
      print(self.address)
      self.get_values()
  def get_values(self):
    results = self.results
    self.hex_treasury = results['Total HEX']
    if self.address is None:
      try:
        self.address= self.main.address
        self.your_maxi_balance= anvil.server.call('maxi_balance',self.address)
        
      except:
        self.address=None
        self.your_maxi_balance=0
        self.text_box_address.visible=True
    else:
      
      self.your_maxi_balance= anvil.server.call('maxi_balance',self.address)
   
      
    """{'Total HEX': 71639417.88762201, 'T Share Potential': 10227.4514464652, 
    'MAXI Supply': 71637126.91393201, 'Hedron Mintable': 284067463925.5708,
    'Mint Phase Start Day': 865, 'Mint Phase End Day': 879, 'Current HEX Day': 869}"""
    self.total_maxi_supply = results['MAXI Supply']
    self.hex_day=results['Current HEX Day']
    self.end_day=results['Mint Phase End Day']
    self.label_current_day.text="HEX day {}".format(self.hex_day)
    self.label_stake_start.text="HEX day {}".format(results['Stake Start Day'])
    self.label_stake_end.text="HEX day {}".format(results['Stake End Day'])
    self.label_treasury_value_hex.text = '{:,} HEX'.format(self.hex_treasury)
    url='https://uniswapdataapi.azurewebsites.net/api/hexPrice'
    r = anvil.http.request(url,json=True)
    self.hex_price=float(r['hexUsd'])
    self.treasury_value = self.hex_price*self.hex_treasury
    self.label_treasury_value_usd.text = "${:,}".format(int(self.treasury_value))
    
    
    
    
    self.label_total_treasury_hex.text=self.label_treasury_value_hex.text
    self.label_accrued_hex.text="Incl. {:,} HEX Accrued".format(int(results['HEX Accrued']))
    # TODO pull maxi price from nomics or uniswap API
    self.maxi_price = results['MAXI Price USD']
    self.label_maxi_market_price_usd.text="${:,.3f}".format(self.maxi_price)
    self.label_maxi_market_price_hex.text="{:,.1f}% {}".format(results['Premium']*100, 'Premium' if results['Premium']>0 else 'Discount')
    self.label_hedron_treasury.text="{:,} HDRN minted".format(int(results['Hedron Minted']))
    self.label_hedron_total.text="Estimated {:,} HDRN Total".format( int(results['Hedron Mintable']))

    self.label_maxi_supply.text = '{:,.3f} MAXI'.format(self.total_maxi_supply)
    
    self.label_maxi_contract_address.text=MAXI_CONTRACT_ADDRESS
    #scalar = self.hex_treasury/(150000000) if self.hex_treasury<150000000 else 1
    
    #self.effective_hex = (3*self.hex_treasury)+(float(self.hex_treasury)*float(scalar)*float(.10))
    #t_share_rate=int(anvil.http.request('https://hexvisionpublicapi.azurewebsites.net/api/StakingInfo',json=True)["shareRate"])/10
   
    self.num_t_shares = results['T Share Potential']
    
    self.label_tshares.text="{:,.4f}".format(self.num_t_shares)
    try:
      t = "{:,.4f}".format(self.num_t_shares)
      b = "{} (Your T Shares: {:,.4f})".format(t, self.num_t_shares*self.your_maxi_balance/self.total_maxi_supply)
      self.label_tshares.text=b
    except Exception as e:
      print(e)
    stake_url = 'https://hexvisionpublicapi.azurewebsites.net/api/StakingInfo'
    re = anvil.http.request(stake_url, json=True)
    self.daily_payout = float(re['latestDayPayoutTotal'])/float(re['stakeSharesTotal']/1000000000000)
    self.text_box_payout.text=int(self.daily_payout/100000000)
    self.text_box_hex_future_price.text=self.hex_price
    query = '''{
 pair(id: "0x035a397725d3c9fc5ddd3e56066b7b64c749014e"){
     token0 {
       id
       symbol
       name
       derivedETH
      
     }
     token1 {
       id
       symbol
       name
       derivedETH
     }
     reserve0
     reserve1
     reserveUSD
     trackedReserveETH
     token0Price
     token1Price
     volumeUSD
     txCount

    }
    }'''
    d={'query':query}
    gql = anvil.http.request("https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",data=d,json=True,method="POST")
  
    try:
      self.hedron_price_hex= float(gql['data']['pair']['token1Price'])
      display = "{:.8f}".format(float(self.hex_price)/float(self.hedron_price_hex))
      self.text_box_hedron_price.text=display
    except Exception as e:
      self.text_box_hedron_price.text=.000001
      print(e)
    
    
    
    hedron_usd = self.hex_price/self.hedron_price_hex
    
    
    self.redemption_value_hex = float(self.hex_treasury)/float(self.total_maxi_supply)
    self.redemption_value_hedron = float(results['Hedron Minted'])/float(self.total_maxi_supply)
    self.backing_per_maxi_usd = (self.redemption_value_hex*self.hex_price)+(self.redemption_value_hedron*hedron_usd)
    self.label_backing_per_maxi_usd.text = "${:,.5f}".format(self.backing_per_maxi_usd)
    self.total_treasury_value = self.treasury_value + (self.redemption_value_hedron*hedron_usd)
    self.redeemable_hex = self.total_treasury_value*(self.your_maxi_balance/self.total_maxi_supply)
    self.label_redemption_value_usd.text = "${:,.3f}".format(self.redeemable_hex)
    self.label_your_balance_maxi.text='{:,.3f} MAXI ({:.3f}% of Pool)\nRedeemable for {:,.1f} HEX and {:,} HDRN'.format(self.your_maxi_balance, 100*self.your_maxi_balance/self.total_maxi_supply, self.redemption_value_hex*self.your_maxi_balance, int(self.redemption_value_hedron*self.your_maxi_balance))
    self.label_backing_per_maxi_hex.text = "{:,.5f} HEX and {:,} HDRN".format(self.redemption_value_hex, self.redemption_value_hedron)
    self.calculate_estimate()
    
  def calculate_estimate(self, **event_args):
    try:
      self.potential_hex_earnings = self.num_t_shares*5555*float(self.text_box_payout.text)
      self.hdrn= self.results['Hedron Mintable']
      self.total_hex_value = self.potential_hex_earnings*float(self.text_box_hex_future_price.text)
      self.total_hedron_value_usd = self.hdrn*float(self.text_box_hedron_price.text)
      
      self.label_est_yield.text="${:,}".format(int(self.total_hedron_value_usd+self.total_hex_value))
      self.total_treasury_value_est = self.total_hedron_value_usd + int((self.potential_hex_earnings+self.hex_treasury)*float(self.text_box_hex_future_price.text))
      self.label_treasury_value_usd_est.text ="${:,}".format(int(self.total_treasury_value_est))
      self.label_treasury_breakdown.text = "{:,} HEX and {:,} Hedron".format(int(self.potential_hex_earnings),int(self.results['Hedron Mintable']))
      self.label_treasury_breakdown_copy.text = "{:,} HEX and {:,} Hedron".format(int(self.potential_hex_earnings+self.hex_treasury),int(self.results['Hedron Mintable']))
      self.label_treasury_value_usd_est_copy.text = "${:,}".format(self.total_treasury_value_est/self.total_maxi_supply)
      self.label_treasury_breakdown_copy_2.text = "{:,.3} HEX and {:,} Hedron".format(float(self.potential_hex_earnings+self.hex_treasury)/float(self.total_maxi_supply),int(float(self.results['Hedron Mintable'])/float(self.total_maxi_supply)))
      try:
        t = "{:,.4f}".format(self.num_t_shares)
        b = "{} (Your T Shares: {:,.4f})".format(t, self.num_t_shares*self.your_maxi_balance/self.total_maxi_supply)
        self.label_your_est.text= "{:,} HEX and {:,} Hedron".format(int(self.potential_hex_earnings)*self.your_maxi_balance/self.total_maxi_supply,int(self.results['Hedron Mintable']*self.your_maxi_balance/self.total_maxi_supply))
        self.label_redeemable_value_usd_est_copy_2.text = "${:,}".format(self.your_maxi_balance*self.total_treasury_value_est/self.total_maxi_supply)
      except Exception as e:
        raise e
    except Exception as e:
      pass
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    if event_args['sender'].selected_value=='Present Value':
      self.panel_estimator.visible=False
    else:
      self.panel_estimator.visible=True

  def column_panel_chart_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    if False:
      i = HtmlTemplate()
      html='''<script src="https://anvil.works/embed.js" async></script>
  <iframe style="width:100%;" data-anvil-embed src="https://maximedia.anvil.app/#minting"></iframe>'''
      i.html=html
      self.column_panel_chart.add_component(i)

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.results = app_tables.dashboard.get(name='dashboard')['results']
    print(self.results)
    self.get_values()
    
  

 
 



