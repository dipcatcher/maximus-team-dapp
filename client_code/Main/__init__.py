from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home
from ..stake import stake
from ..stake_list import stake_list

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

import anvil.js
anvil.js.report_all_exceptions(False, reraise=False)
try:
  from anvil.js.window import ethers, ethereum
  is_ethereum=True
except:
  Notification('This dapp may only be used with a browser with MetaMask Wallet enabled.').show()
  is_ethereum=False




class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.address=None
    
   
    
    
    self.ongoing = True
    
    self.provider=None
    if not is_ethereum:
      
      #self.clear()
      #self.add_component(Main_copy())
      open_form('Main_copy')
    
    else:
      
          
      try:
        self.provider = anvil.js.await_promise(ethers.providers.Web3Provider(ethereum))
        
        try:
          anvil.js.await_promise(ethereum.request({"method": 'eth_requestAccounts' }))
        except anvil.js.ExternalError as e:
          print(e)
        self.signer= self.provider.getSigner()
          
        self.address=self.signer.getAddress()
        
        self.web3_wallet =chain_interface()
        self.add_component(self.web3_wallet)
        try:
          self.button_connect_dapp_click()
        except:
          import time
          time.sleep(1)
          self.button_connect_dapp_click()
      except Exception as e:
        print(e)
  
      
      self.menu_click(sender=self.link_mint)
      
        
        
  

  def button_connect_dapp_click(self, **event_args):
    """This method is called when the button is clicked"""
   
    a=False
    chain_id='0x1'#'0x1' 
    
    self.is_connected = self.web3_wallet.connect_network(chain_id)

    

   

    if self.address is not None:

      abbr = '{}...{}'.format(self.address[0:5], self.address[-5:])
      self.button_connect_dapp.text=abbr
      self.button_connect_dapp.remove_from_parent()
      self.button_connect_dapp.background='#202F52'
      self.button_connect_dapp.foreground='#8E97CD'
      self.navbar_links.add_component(self.button_connect_dapp)
      self.panel_connect.clear()
      self.menu_click(sender=self.link_mint)

    
    #anvil.js.await_promise(self.provider.send("eth_requestAccounts", []))
    
    
    

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


  


  




  



