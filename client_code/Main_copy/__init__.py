from ._anvil_designer import Main_copyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


import webbrowser
import time

from ..dashboard_page import dashboard_page

from ..offline_dashboard import offline_dashboard

from ..mint_page_copy import mint_page_copy
from ..redeem_page_copy import redeem_page_copy
from ..dashboard_page_copy import dashboard_page_copy

from ..disclaimer import disclaimer

try:
  from anvil.js.window import ethers, ethereum
except:
  pass

import anvil.js
anvil.js.report_all_exceptions(False, reraise=False)



print(anvil.server.get_app_origin())


class Main_copy(Main_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.address=None
    
    
    





  def button_connect_dapp_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    alert(disclaimer(), large=True, dismissible=False, buttons=[])
  
  def menu_click(self, **event_args):
    """This method is called when the link is clicked"""
    b = event_args['sender'].text
    if b=='Mint':
     
      self.content_panel.clear()
      
      try:
        self.m = mint_page_copy(main=self)
        
        self.content_panel.add_component(self.m)
      except:
        pass


    if b=='Redeem':
      self.content_panel.clear()
      
      self.content_panel.add_component(redeem_page_copy(main=self))
      

    if b =='Dashboard':
      self.content_panel.clear()
      try:
        #self.d = dashboard_page(main=self)
        
        self.d=offline_dashboard(main=self)
        self.content_panel.add_component(self.d)
      except Exception as e:
        raise e
    if b=='Calculator':
      self.content_panel.clear()
      self.c=calculator_page()
      self.content_panel.add_component(self.c)

  



