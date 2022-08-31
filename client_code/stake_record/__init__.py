from ._anvil_designer import stake_recordTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
try:
  from anvil.js.window import ethers, ethereum, Web3
except:
  pass
class stake_record(stake_recordTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract, self.team_contract, self.reward_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
        
        self.write_maxi_contract, self.write_hex_contract, self.write_team_contract, self.write_reward_contract= self.main.web3_wallet.connect_contracts(self.main.signer)
        self.refresh_page()
    except Exception as e:
      raise e
  def refresh_page(self):
    
    
    self.team_balance =int(self.team_contract.balanceOf(self.address).toString())
    #self.label_team_balance.text = '{:.8f} ❇️'.format(int(self.team_balance)/100000000)
    self.team_staked = int(self.team_contract.USER_AMOUNT_STAKED(self.address).toString())
    #self.label_team_staked.text = '{:.8f} ❇️'.format(int(self.team_staked)/100000000)
    self.team_supply = self.team_contract.totalSupply().toString()
    #self.label_total_liquid.text = '{:.8f} ❇️'.format(int(self.team_supply)/100000000)
    self.team_staked_total = self.team_contract.GLOBAL_AMOUNT_STAKED().toString()
    #self.label_total_staked.text = '{:.8f} ❇️'.format(int(self.team_staked_total)/100000000)
    #self.label_deadline.text = '1 day, 2 hours'
    """['0x8D0Ad00CDC30fF99964488748802f104fB749caE', <BigNumber proxyobject>, <BigNumber proxyobject>, <BigNumber proxyobject>, <BigNumber proxyobject>, <BigNumber proxyobject>, True]"""
    stake_record = self.team_contract.stakes(self.address, 1)
    d_stake_record = {}
    d_stake_record['address']=stake_record[0]
    d_stake_record['initial_period']=stake_record[1].toNumber()
    d_stake_record['amount']=stake_record[2].toNumber()
    d_stake_record['amount_unstaked']=stake_record[3].toNumber()
    d_stake_record['stakeID']=stake_record[4].toNumber()
    d_stake_record['stake_expiry_period']=stake_record[5].toNumber()
    d_stake_record['initiated']=stake_record[6]
    d_stake_record['stakedTeamPerPeriod'] = self.team_contract.getAddressPeriodEndTotal(self.address, d_stake_record['stake_expiry_period'], d_stake_record['stakeID']).toNumber()
    
    for k, v in d_stake_record.items():
      self.card_1.add_component(Label(text='{}: {}'.format(k,v)))
    
    d ={}
    d['didStakeClaim']=self.team_contract.didStakeClaim(self.address,d_stake_record['stakeID'],d_stake_record['stake_expiry_period'],"HEX")
    self.current_period = self.team_contract.getCurrentPeriod().toNumber()
    #getPeriodRedemptionRates (string,uint256)
    next_staking_period = self.current_period+2 if self.current_period% 2 ==1 else self.current_period+1
    d['globalStakedTeamPerPeriod']=int(self.team_contract.globalStakedTeamPerPeriod(next_staking_period).toString())
    d['GLOBAL_AMOUNT_STAKED']=int(self.team_contract.GLOBAL_AMOUNT_STAKED().toString())
    d['isStakingPeriod']=self.team_contract.isStakingPeriod()
    d['currentPeriod']=self.current_period
    
    d['USER_AMOUNT_STAKED']=int(self.team_contract.USER_AMOUNT_STAKED(self.address).toString())
    self.d_stake_record = d_stake_record 
    for k, v in d.items():
        self.card_2.add_component(Label(text='{}: {}'.format(k,v)))

    if self.current_period<=d_stake_record['stake_expiry_period']:
      self.button_early_end_stake.visible=True
    if self.current_period==d_stake_record['stake_expiry_period']:
      self.button_extend_stake.visible=True
    if self.current_period>d_stake_record['stake_expiry_period']:
      self.button_end_completed_stake.visible=True
      self.button_restake_completed_stake.visible=True
      self.button_claim_rewards.visible=True
      
    
    
      
  
      # Any code you write here will run when the form opens.

  def menu_click(self, **event_args):
    t = event_args['sender'].text
    if 'Early' in t:
      existing_TEAM = self.team_balance
      tb = TextBox(type='number')
      a = alert(tb, title='Enter Amount to End Stake', buttons=[('End Stake', True), ('Cancel', False)])
      if a:
        raw_units=int(tb.text)
      anvil.js.await_promise(self.write_team_contract.earlyEndStakeTeam(self.d_stake_record['stakeID'],int(raw_units)*100000000))
      while existing_TEAM==int(self.team_contract.balanceOf(self.address).toString()):
        time.sleep(1)
    if 'End Completed Stake' in t:
      existing_TEAM = self.team_balance
      tb = TextBox(type='number')
      a = alert(tb, title='Enter Amount to End Stake', buttons=[('End Stake', True), ('Cancel', False)])
      if a:
        raw_units=int(tb.text)
      anvil.js.await_promise(self.write_team_contract.endCompletedStake(self.d_stake_record['stakeID'],int(raw_units)*100000000))
      while existing_TEAM==int(self.team_contract.balanceOf(self.address).toString()):
        time.sleep(1)
    if 'Extend' in t:
      
      tb = TextBox(type='number')
      a = alert(title='Are you sure you want to extend your stake into the next staking period?', buttons=[('Yes', True), ('Cancel', False)])
      if a:
        current_expiry = self.d_stake_record['stake_expiry_period']
        anvil.js.await_promise(self.write_team_contract.extendStake(self.d_stake_record['stakeID']))
        while current_expiry==int(self.team_contract.stakes(self.address, 1)[5].toString()):
          time.sleep(1)
    if 'Restake' in t:
      current_amount_staked = self.d_stake_record['amount']-self.d_stake_record['amount']
      anvil.js.await_promise(self.write_team_contract.restakeExpiredStake(self.d_stake_record['stakeID']))
      while current_amount_staked>0:
        time.sleep(1)
    if "Claim" in t:
      anvil.js.await_promise(self.write_reward_contract.claim(self.d_stake_record['stake_expiry_period'], 'HEX',self.d_stake_record['stakeID']))
      while self.team_contract.didStakeClaim(self.address,d_stake_record['stakeID'],d_stake_record['stake_expiry_period'],"HEX")==false:
        time.sleep()

    self.refresh_page()
  

