from ._anvil_designer import disclaimerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js.window
import anvil.js
try:
  from anvil.js.window import ethereum
  is_ethereum=True
except:
  is_ethereum=False


class disclaimer(disclaimerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('x-close-alert', value=True)
    if is_ethereum:
      #c = confirm("Choose Network", buttons=[("Ethereum", True), ("Pulsechain", False)])
      b=[("Ethereum", True), ("PulseChain", False), ("ETHPOW", "ETHPOW"), ("ETHFAIR", "ETHFAIR")]#, ("Testnet", None)]
      aa = alert("Choose Network", buttons=b)
      if aa==True:
        chain_id = '0x1'
      elif aa == False:
        chain_id = "0x171"
      elif aa ==None:
        chain_id =  "0x7A69"
      elif aa =="ETHPOW":
        chain_id="0x2711"
      elif aa == "ETHFAIR":
        chain_id = "0x7D44C"
      try:
        a = ethereum.request({
                  'method': 'wallet_switchEthereumChain',
                  'params': [{ "chainId": chain_id }] #'0x1
              })
        anvil.js.await_promise(a)
      except:
        pass
      self.clear()
      open_form('Main', chain_id=chain_id)
    else:
      Notification('To use the dapp you must be on an etherem enabled browser, such as MetaMask.').show()
      try:
        
        open_form('Main_copy_copy')
      except:
        pass
        
