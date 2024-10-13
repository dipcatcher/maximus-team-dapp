from ._anvil_designer import stakeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
import datetime
from ..stake_record import stake_record
from ..stake_list import stake_list
class stake(stakeTemplate):
  def __init__(self, **properties):
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract, self.team_contract, self.reward_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
        self.write_maxi_contract, self.write_hex_contract, self.write_team_contract, self.write_reward_contract= self.main.web3_wallet.connect_contracts(self.main.signer)
        self.base_contract = self.main.web3_wallet.get_base_contract(self.main.provider)
        self.refresh_page()
        
    except Exception as e:
      raise e
  def refresh_page(self):
    print(dir(self.team_contract))
    print(self.address)
    self.team_balance =int(self.team_contract.balanceOf(self.address).toString())
    self.label_team_balance.text = '{:,.8f} ❇️'.format(int(self.team_balance)/100000000)
    self.team_staked = int(self.team_contract.USER_AMOUNT_STAKED(self.address).toString())
    self.label_team_staked.text = '{:,.8f} ❇️'.format(int(self.team_staked)/100000000)
    self.team_supply = self.team_contract.totalSupply().toString()
    self.label_total_liquid.text = '{:,.8f} ❇️'.format(int(self.team_balance)/100000000)
    self.team_staked_total = self.team_contract.GLOBAL_AMOUNT_STAKED().toString()
    
    self.current_period = int(self.team_contract.getCurrentPeriod().toNumber())
    next_staking_period = self.current_period+2 if self.current_period% 2 ==1 else self.current_period+1
    #self.upcoming=int(self.team_contract.globalStakedTeamPerPeriod(next_staking_period).toString())/(10**8)
    self.label_total_staked.text = '{:,.8f} ❇️'.format(int(self.team_staked_total)/100000000)
    
    
    y=(int(1+(self.current_period+1)/2))
    last_day = self.base_contract.RELOAD_PHASE_END().toNumber()
    current_day = self.base_contract.getHexDay().toNumber()
    
    days_remaining = (last_day-current_day)+1
    deadline = datetime.datetime.utcnow().date()+ datetime.timedelta(days=days_remaining)
    self.label_stake_deadline.text = 'Stake before 10/21/2024 to earn rewards from Staking Year {}'.format(deadline.strftime('%m/%d/%Y'), y)
    
    year_text=  "Year {}".format(y)
    self.label_next_year.text = year_text
    #self.label_stake_deadline.text ="calculate days remaining" # base_contract.STAKE_START_DAY - base_contract.getHexDay()
    self.next_staking_period = self.current_period +1 if self.current_period%2==0 else self.current_period+2
    self.label_global_amount_staked.text = "{:,.1f}".format(int(self.team_contract.globalStakedTeamPerPeriod(self.next_staking_period).toString())/(10**8))
    self.column_panel_stake_list.clear()
    self.column_panel_stake_list.add_component(stake_list(main=self.main, stake_page=self))
    # Any code you write here will run when the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.text_box_1.text in ['', None, 0]:
      self.button_2.text='Stake TEAM'
      self.button_2.enabled = True
      
      self.units=0
      
    else:
      self.button_2.text = 'Stake {} TEAM'.format(self.text_box_1.text)
      raw_units = float(self.text_box_1.text)
      self.units = int(raw_units*100000000)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    raw_units = self.units
    self.button_2.enabled=False
    self.button_2.text='Staking {} TEAM'.format(raw_units/(10**8))
    
    existing_TEAM = self.team_balance
    anvil.js.await_promise(self.write_team_contract.stakeTeam(raw_units))
    while existing_TEAM==int(self.team_contract.balanceOf(self.address).toString()):
      time.sleep(1)
    self.button_2.enabled=True
    self.button_2.text='Stake TEAM'
    self.text_box_1.text=None
    self.text_box_1_change(sender=self.text_box_1)
    #self.button_2_copy.enabled=True
    #self.button_2_copy.background='#246BFD'
    #self.button_2.foreground='white'
    #self.button_2_copy.icon=''
    self.refresh_page()

  def link_maxi_balance_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_max_team_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.text_box_1.text=self.team_balance/(10**8)
    self.text_box_1_change(sender=self.link_max_team)

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    if event_args['sender'].icon == 'fa:check':
      pass
    else:
      try:
        tokenSymbol = 'TEAM'
        tokenDecimals = 8
        tokenImage = 'https://perpetuals.anvil.app/_/api/token/logo/TEAM';

        from anvil.js.window import ethereum
        a = ethereum.request({
        'method': 'wallet_watchAsset',
        'params': {
          'type': 'ERC20', 
          'options': {
            'address': self.main.web3_wallet.TEAM_CONTRACT_ADDRESS, 
            'symbol': tokenSymbol, 
            'decimals': tokenDecimals, 
            'image': tokenImage, 
          },
        },
      })
        anvil.js.await_promise(a)
        
        event_args['sender'].icon = 'fa:check'
        event_args['sender'].text='TEAM Token Added'
      except Exception as e:
        print(e)

  



  
    


