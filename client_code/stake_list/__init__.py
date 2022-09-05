from ._anvil_designer import stake_listTemplate
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
from ..stake_record_card import stake_record_card
class stake_list(stake_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    self.stake_page = properties['stake_page']
    
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract, self.team_contract, self.reward_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
        
        self.write_maxi_contract, self.write_hex_contract, self.write_team_contract, self.write_reward_contract= self.main.web3_wallet.connect_contracts(self.main.signer)
        self.refresh_page()
    except Exception as e:
      raise e
  def get_stake_record_data(self, user, stakeID):
    '''struct StakeRecord {
        address staker; // staker
        uint256 balance; // the remaining balance of the stake.
        uint stakeID; // how a user identifies their stakes. Each period stake increments stakeID.
        uint256 stake_expiry_period; // what period this stake is scheduled to serve through. May be extended to the next staking period during the stake_expiry_period.
        mapping(uint => uint256) stakedTeamPerPeriod; // A record of the number of TEAM that successfully served each staking period during this stake. This number crystallizes as each staking period ends and is used to claim rewards.
        bool initiated;
    }'''
    stake_record = self.team_contract.stakes(user, stakeID)
    d_stake_record = {}
    d_stake_record['address']=stake_record[0]
    d_stake_record['balance']=int(stake_record[1].toString())
    d_stake_record['stakeID']=stake_record[2].toNumber()
    d_stake_record['stake_expiry_period']=stake_record[3].toNumber()
    d_stake_record['initiated']=stake_record[4]
    print(d_stake_record)
    b = {}
    for m in range(d_stake_record['stakeID'],d_stake_record['stake_expiry_period']+1):
      
      b[m]=int(self.team_contract.getAddressPeriodEndTotal(user, m, d_stake_record['stakeID']).toString())
      
    d_stake_record['stakedTeamPerPeriod'] = b
    d_stake_record['amount_actively_staked']=d_stake_record['balance']
    d_stake_record['current_period']=self.current_period
    return d_stake_record
  def refresh_page(self):
    self.current_period = self.team_contract.getCurrentPeriod().toNumber()
    self.stake_records = []
    for n in range(self.current_period+3):
      
      stake_record = self.get_stake_record_data(self.address, n)
      if stake_record['initiated']:
        self.label_day.text='Your Stakes'
        self.stake_records.append(stake_record)
        self.column_panel_1.add_component(stake_record_card(stake_record=stake_record, team_contract=self.team_contract, write_team_contract=self.write_team_contract, address=self.address, read_reward_contract=self.reward_contract, write_reward_contract=self.write_reward_contract, main=self.main, stake_page=self.stake_page))
  
    
      
    # Any code you write here will run when the form opens.
