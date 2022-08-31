from ._anvil_designer import earning_calculatorTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def calculate(days, payout, principal):
  bpb_eff = principal/10 if principal > 150000000 else (principal**2)/(10*150000000)
  total_earnings = (days * payout * bpb_eff) / (2 * 23195)
  return total_earnings
def earnigns_per_team_staked(total_earnings, percent_maxi, percent_team_staked):
  total_supply = 2*percent_maxi*294330316
  number_of_team_staked = total_supply*percent_team_staked
  return total_earnings/number_of_team_staked

class earning_calculator(earning_calculatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.pools = {'BASE': 365, 
                  'TRIO': 3*365, 
                  'LUCKY': 7*365, 
                  'DECI': 10*365}
    self.recalculate()
    
  
    
  def recalculate(self, **event_args):
    """This method is called when the text in this text box is edited"""
    
    earnings = calculate(self.pools[self.drop_down_1.selected_value], 
                         float(self.text_box_daily_payout.text), 
                         float(self.text_box_principal.text))
    self.label_earnings.text = earnings 
    self.label_earnings_per_team.text = earnigns_per_team_staked(earnings, float(self.text_box_maxi_minted.text/100), float(self.text_box_team_staked.text/100))

