from ._anvil_designer import Main_copy_copyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home
from ..stake import stake
from ..stake_list import stake_list
import Maximus_dash
from Maximus_dash.table_dash_copy import table_dash_copy
import datetime
import webbrowser
import time
from ..earning_calculator import earning_calculator

try:
  from ..mint_page import mint_page
  from ..dashboard_page import dashboard_page
  from ..redeem_page import redeem_page
  from ..connect_page import connect_page
  from ..calculator_page import calculator_page
  from ..disclaimer import disclaimer
  from ..disclaimer_copy import disclaimer_copy
  from ..chain_interface import chain_interface
  from ..Main_copy import Main_copy
except:

  pass






class Main_copy_copy(Main_copy_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.address=None




    
  def menu_click(self, **event_args):
    """This method is called when the link is clicked"""
    b = event_args['sender'].text
    print('v')

    if b=='Stake':
      self.content_panel.clear()
      print(self)
      self.content_panel.add_component(stake(main=self),full_width_row=True)
    if b=='Mint':
      self.content_panel.clear()
      self.m = mint_page(main=self) if self.ongoing else Label(foreground='white', text='MAXI Minting Phase is over.')
      self.content_panel.add_component(self.m,full_width_row=True)


    if b=='Redeem':
      self.content_panel.clear()
      self.r = redeem_page(main=self) if self.ongoing else Label(foreground='white', text='MAXI Minting Phase is over.')
      self.content_panel.add_component(self.r,full_width_row=True)

    if b =='Dashboard':
      self.content_panel.clear()
      from ..offline_dashboard import offline_dashboard
      self.d = offline_dashboard(main=self) #dashboard_page(main=self)
      self.content_panel.add_component(self.d,full_width_row=True)
    if b=='Calculator':
      self.content_panel.clear()
      self.c=calculator_page()
      self.content_panel.add_component(self.c,full_width_row=True)
    if b == 'Earnings Calculator':
      self.content_panel.clear()
      self.content_panel.add_component(earning_calculator())



  def link_connect_to_chain_click(self, **event_args):
    pass

  def link_disclaimer_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(disclaimer_copy(),large=True, title='IMPORTANT DISCLAIMER')

  def link_earnings_calculator_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_minting_dashboard_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(table_dash_copy())



