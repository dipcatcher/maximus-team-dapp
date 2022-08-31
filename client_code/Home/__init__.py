from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    u = anvil.server.get_app_origin()
    self.image_1.source=u+'/_/theme/how.PNG'
    self.image_2.source=u+'/_/theme/maxibacking.jpeg'
    self.image_3.source=u+'/_/theme/chart.png'
    print(self.image_1.source)
    

    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().button_1_click()

