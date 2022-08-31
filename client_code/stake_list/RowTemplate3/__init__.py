from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    d_stake_record=self.item
    self.current_period = d_stake_record['current_period']
    menu_items = []
    if self.current_period<=d_stake_record['stake_expiry_period']:
      
      menu_items.append('Early End Stake')
    if self.current_period==d_stake_record['stake_expiry_period']:
      
      menu_items.append('Extend Stake')
    if self.current_period>d_stake_record['stake_expiry_period']:
      
      menu_items.append('End Completed Stake')
      
      menu_items.append('Restake Completed Stake')
      
      menu_items.append('Claim Rewards')
    self.drop_down_menu.items=menu_items
    for k,v in self.item['stakedTeamPerPeriod'].items():
      if v>0:
        self.column_panel_2.add_component(Label(text='{}: {}'.format(k,v)))
      
    # Any code you write here will run when the form opens.
