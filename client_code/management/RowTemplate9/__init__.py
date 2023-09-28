from ._anvil_designer import RowTemplate9Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate9(RowTemplate9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.write_maxi_contract, self.write_hex_contract, self.write_team_contract, self.write_reward_contract= get_open_form().web3_wallet.connect_contracts(get_open_form().signer)
    # Any code you write here will run before the form opens.

  def button_stage_click(self, **event_args):
    self.item['Token']
    try:
      event_args['sender'].enabled=False
      
      a = anvil.js.await_promise(self.write_team_contract.prepareClaim(self.item['Token']))
      event_args['sender'].text = "Staging..."
      a.wait()
      event_args['sender'].text = "Succesfully Staged"
      event_args['sender'].icon = 'fa:check'
    except Exception as e:
      raise e
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)
      event_args['sender'].enabled=True




