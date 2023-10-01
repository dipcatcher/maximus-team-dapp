from ._anvil_designer import stake_dataTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import ethers
import anvil.js
urls = {}
urls['ETH']="https://eth-mainnet.g.alchemy.com/v2/CjAeOzPYt5r6PmpSkW-lL1NL7qfZGzIY"
urls['PLS']="https://rpc.pulsechain.com"
team_address = "0xb7c9e99da8a857ce576a830a9c19312114d9de02"
team_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EarlyEndStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EndExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"ExtendStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"minter","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"RestakeExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"current_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"},{"indexed":False,"internalType":"bool","name":"is_initial","type":"bool"}],"name":"Stake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"ESCROW_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GLOBAL_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"IS_MINTING_ONGOING","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MYSTERY_BOX_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_REWARD_DISTRIBUTION_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"USER_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"earlyEndStakeTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"endCompletedStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"extendStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"finalizeMinting","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker_address","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getAddressPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"string","name":"ticker","type":"string"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getClaimableAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"current_period","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"},{"internalType":"uint256","name":"period","type":"uint256"}],"name":"getPeriodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getPoolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getSupportedTokens","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"globalStakedTeamPerPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isStakingPeriod","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mintTEAM","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"periodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"poolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"prepareClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"restakeExpiredStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"stakeTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakes","outputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"stake_expiry_period","type":"uint256"},{"internalType":"bool","name":"initiated","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
class stake_data(stake_dataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    data = self.get_early_end_stake_data()
    for chain, stake_data in data.items():
      title = Label(text=chain, role='text', underline=True)
      self.add_component(title)
      for k,v in stake_data.items():
        rt =RichText(content="<b>{}: </b>{:,} TEAM".format(k,int(v)), format='restricted_html')
        self.add_component(rt)
  def get_early_end_stake_data(self):
    self.providers = {}
    self.providers['ETH'] = ethers.providers.JsonRpcProvider(urls["ETH"])
    self.providers["PLS"]= ethers.providers.JsonRpcProvider(urls["PLS"])
    self.contracts ={"eTEAM":ethers.Contract(team_address, team_abi, self.providers['ETH']),
                    "pTEAM": ethers.Contract(team_address, team_abi, self.providers['PLS'])}
    

    data = {}
    data["Ethereum"]={}
    data['PulseChain'] = {}
    data['Ethereum']['Period 1 TEAM Staked'] = int(self.contracts['eTEAM'].globalStakedTeamPerPeriod(1).toString())/(10**8)
    data['PulseChain']['Period 1 TEAM Staked'] = int(self.contracts['pTEAM'].globalStakedTeamPerPeriod(1).toString())/(10**8)
    
    #TODO: get a list of all the EarlyEndStake events event: EarlyEndStake(address indexed staker,uint256 amount,uint256 staking_period,uint256 stakeID).
    early_end_stake_topic = ethers.utils.id("EarlyEndStake(address,uint256,uint256,uint256)")

    # Define the filter
    filter_eth = {
      'fromBlock': 'earliest',
      'toBlock': 'latest',
      'address': team_address,
      'topics': [early_end_stake_topic]
    }
  
    filter_pls = {
      'fromBlock': 'earliest',
      'toBlock': 'latest',
      'address': team_address,
      'topics': [early_end_stake_topic]
    }
  
    # Fetch logs
    eth_logs = self.providers['ETH'].getLogs(filter_eth)
    pls_logs = self.providers['PLS'].getLogs(filter_pls)
    # Decode the logs
    eth_decoded_logs = [self.contracts['eTEAM'].interface.parseLog(log) for log in eth_logs]
    pls_decoded_logs = [self.contracts['eTEAM'].interface.parseLog(log) for log in pls_logs]
    e_total = 0
    for log in eth_decoded_logs:
      e_total+=int(log.args[1].toString())
    data['Ethereum']['Early End Staked'] = e_total/(10**8)
    data['Ethereum']['Penalty Burn'] = data['Ethereum']['Early End Staked'] *.0369

    p_total = 0
    for log in pls_decoded_logs:
      p_total+=int(log.args[1].toString())
    data['PulseChain']['Early End Staked'] = p_total/(10**8)
    data['PulseChain']['Penalty Burn'] = data['PulseChain']['Early End Staked'] *.0369
    return data
    

    # Any code you write here will run before the form opens.
