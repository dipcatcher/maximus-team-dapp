from ._anvil_designer import redeem_pageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import time
class redeem_page(redeem_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
        self.write_maxi_contract, self.write_hex_contract = self.main.web3_wallet.connect_contracts(self.main.signer)
        self.refresh_redeem()
    except Exception as e:
      Notification('You must connect to MetaMask to mint MAXI.').show()
    
  
  def refresh_redeem(self):
    
    self.maxi_balance = self.maxi_contract.balanceOf(self.address).toNumber()
    self.hex_balance = self.hex_contract.balanceOf(self.address).toNumber()
    self.label_redeem_hex_balance.text = '{:.8f} ⬣'.format(int(self.hex_balance)/100000000) 
    self.link_maxi_balance.text = '{:.8f} Ⓜ️'.format(int(self.maxi_balance)/100000000)
    
    # Any code you write here will run when the form opens.

  def button_redeem_hex_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.address is not None:
      if self.redeem_units <= float(self.maxi_balance):
        event_args['sender'].text=event_args['sender'].text.replace('REDEEM', "REDEEMING")
        current_maxi = self.maxi_balance
        anvil.js.await_promise(self.write_maxi_contract.redeemHEX(self.redeem_units))
        while current_maxi==self.maxi_contract.balanceOf(self.address).toNumber():
          time.sleep(.5)
        #self.call_js('redeemHEX', self.redeem_units, self.address)
        self.refresh_redeem()
      else:
        Notification('Insufficient MAXI.').show()
        self.refresh_redeem()
    else:
      Notification('Please connect MetaMask to Ethereum Mainnet.').show()

  def text_box_redeem_maxi_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.text_box_redeem_maxi.text in ['', None]:
      self.button_redeem_hex.text='REDEEM HEX'
      self.button_redeem_hex.enabled = False
      self.units=0
    else:
      self.button_redeem_hex.text = 'REDEEM {} HEX'.format(self.text_box_redeem_maxi.text)
      raw_units = float(self.text_box_redeem_maxi.text)
      self.redeem_units = int(raw_units*100000000)
      self.button_redeem_hex.enabled=True

  def link_max_maxi_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.text_box_redeem_maxi.text=float(float(self.maxi_balance)/100000000)
    self.text_box_redeem_maxi_change(sender=self.text_box_redeem_maxi)

  def text_box_redeem_maxi_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass






