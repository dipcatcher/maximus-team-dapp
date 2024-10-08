from ._anvil_designer import connect_pageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class connect_page(connect_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.address=None
    self.main = properties['main']

    # Any code you write here will run when the form opens.
  def button_connect_dapp_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.main.button_connect_dapp_click(sender=event_args['sender'])
    
  