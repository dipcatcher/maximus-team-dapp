from ._anvil_designer import set_providerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import ethers, ethereum
from ..Main_copy import Main_copy

class set_provider(set_providerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      self.provider = ethers.providers.Web3Provider(ethereum)
      self.provider.send("eth_requestAccounts", [])
      self.clear()
      has_provider=True
      
      #self.add_component(Main(has_provider=True))
      
    except Exception as e:
      has_provider=False
      alert(str(e))
    #open_form('Main_copy')
    anvil.js.window.location.replace("https://sour-twin-effort.anvil.app/#dapp")
   
    
