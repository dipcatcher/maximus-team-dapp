from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_claim.text = '✅' if self.item['claimed'] else 'claim'
    self.label_claimable.text = "{:,.8f}".format(self.item['claimable'])
    if all([not self.item['claimed'], self.item['claimable']>0]):
      self.link_claim.visible=True
    
      
      

    # Any code you write here will run when the form opens.

  def link_claim_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.link_claim.text=='claim':
      self.parent.raise_event('x-click-claim', period=self.item['period'], ticker=self.item['token'], stake_id=self.item['stakeID'])
    #self.reward_contract.claimRewards(self.item['period'], self.item['token'], self.item['stakeID'])

