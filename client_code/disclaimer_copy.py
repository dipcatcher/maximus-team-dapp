from ._anvil_designer import disclaimer_copyTemplate
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


class disclaimer_copy(disclaimer_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    self.raise_event('x-close-alert', value=True)
    if is_ethereum:
      
      
     
    
      a = ethereum.request({
                'method': 'wallet_switchEthereumChain',
                'params': [{ "chainId": '0x1' }]
            })
      anvil.js.await_promise(a)
      anvil.js.window.location.replace("https://go.maximus.cash")
      
    else:
      Notification('To use the dapp you must be on an etherem enabled browser, such as MetaMask.').show()
      try:
        
        open_form('Main_copy')
      except:
        pass
        
