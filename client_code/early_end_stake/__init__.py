from ._anvil_designer import early_end_stakeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class early_end_stake(early_end_stakeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.raw_amount = 0
    self.team_balance= properties['team_balance']
    self.label_amount_staked.text = "{} ❇️".format(self.team_balance)
    # Any code you write here will run when the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if event_args['sender'].text not in ['', None, 0]:
      self.raw_amount=float(event_args['sender'].text)
      penalty=.0369*self.raw_amount
      self.label_1.text = "Early Ending {} TEAM results in a {} penalty. You will receive {} TEAM and the penalized amount will remain permanently burnt.".format(
        self.raw_amount, penalty, self.raw_amount-penalty
      )

  def link_max_team_click(self, **event_args):
    """This method is called when the link is clicked"""
    
    self.text_box_1_copy.text=self.team_balance
    self.text_box_1_change(sender=self.text_box_1_copy)

    
    
    

