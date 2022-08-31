from ._anvil_designer import end_stakeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
class end_stake(end_stakeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    print(self.address)
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract, self.team_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
        self.write_maxi_contract, self.write_hex_contract, self.write_team_contract= self.main.web3_wallet.connect_contracts(self.main.signer)
        self.refresh_page()
    except Exception as e:
      raise e
  def refresh_page(self):
    self.current_period = int(self.team_contract.getCurrentPeriod().toNumber())
    self.total_staked_team =int(self.team_contract.addressAmountStakedRunningTotal(self.address).toString())
    self.actively_staked_team = int(self.team_contract.getAddressPeriodEndTotal(self.address, self.current_period).toNumber())
    self.penalty = int(self.team_contract.determine_penalty(self.total_staked_team,self.address).toString())
    self.team_balance =int(self.team_contract.balanceOf(self.address).toNumber())
    self.label_team_balance.text = '{:.8f} ❇️'.format(int(self.team_balance)/100000000)
    self.team_staked = self.total_staked_team
    self.label_team_staked.text = '{:.8f} ❇️'.format(int(self.team_staked)/100000000)
    self.label_team_active_staked.text = '{:.8f} ❇️'.format(int(self.actively_staked_team)/100000000)
    self.flow_panel_penalty.visible = self.penalty>0
    print(self.penalty)
    self.label_penalty.text='{:.8f} ❇️'.format(self.penalty/(100000000))
    
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
    self.button_2.text='Staking {} TEAM'.format(raw_units)
    
    Notification('Pledging {r} MAXI and minting {r} TEAM.'.format(r=raw_units)).show()
    existing_TEAM = self.team_balance
    anvil.js.await_promise(self.write_team_contract.endStake(int(raw_units)*100000000))
    while existing_TEAM==int(self.team_contract.balanceOf(self.address).toString()):
      time.sleep(1)
    self.button_2.enabled=True
    self.button_2.text='Stake TEAM'
    self.text_box_1.text=None
    self.text_box_1_change(sender=self.text_box_1)
    self.button_2_copy.enabled=True
    self.button_2_copy.background='#246BFD'
    self.button_2.foreground='white'
    self.button_2_copy.icon=''
    self.refresh_page()

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    b = TextBox()
    a = alert(b, title='Amount to unstake',buttons=[('Unstake', True), ('Cancel', False)])
    if a:
      anvil.js.await_promise(self.write_team_contract.endStake(int(b.text)*100000000))
      
      self.refresh_page()


