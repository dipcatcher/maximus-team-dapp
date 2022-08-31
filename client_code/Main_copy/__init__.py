from ._anvil_designer import Main_copyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..disclaimer import disclaimer
class Main_copy(Main_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_connect_dapp_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(disclaimer(), large=True, dismissible=False, buttons=[])

