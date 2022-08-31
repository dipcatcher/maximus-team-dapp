from ._anvil_designer import mint_page_copyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import time
class mint_page_copy(mint_page_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    
    
    '''self.address = self.main.address
    if self.address is not None:
      try:
        if self.main.provider is not None:
          self.maxi_contract, self.hex_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
          self.write_maxi_contract, self.write_hex_contract = self.main.web3_wallet.connect_contracts(self.main.signer)
          self.refresh_mint()
      except Exception as e:
        print(e)'''
  def refresh_mint(self):
    
    self.maxi_balance = self.maxi_contract.balanceOf(self.address).toNumber()
    self.hex_balance = self.hex_contract.balanceOf(self.address).toNumber()
    self.hex_day = self.maxi_contract.getHexDay().toNumber()
    self.minting_phase_end_day = self.maxi_contract.getMintingPhaseEndDay().toNumber()
    self.label_mint_duration.text= '{} Days Remaining'.format(self.minting_phase_end_day-self.hex_day)
    self.link_hex_balance.text = '{:.8f} ⬣'.format(int(self.hex_balance)/100000000) 
    self.label_maxi_balance.text = '{:.8f} Ⓜ️'.format(int(self.maxi_balance)/100000000)
    # Any code you write here will run when the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    if self.text_box_1.text in ['', None, 0]:
      self.button_2.text='MINT MAXI'
      self.button_2.enabled = True
      
      self.units=0
      
    else:
      self.button_2.text = 'MINT {} MAXI'.format(self.text_box_1.text)
      raw_units = float(self.text_box_1.text)
      self.units = int(raw_units*100000000)
    try:
      self.check_approval()
    except Exception as e:
      raise e
      Notification('You must first connect to MetaMask.').show()
      return False
    if self.units>self.approved_hex:
      self.column_panel_2.visible=True
      self.label_1.visible=True
      self.link_3.visible=True
      self.column_panel_2.role='card'
      self.button_2.enabled = False
      self.label_1.text="First, Maximus needs your permission to interact with {} of your HEX.".format(raw_units)
      self.button_2_copy.text = 'APPROVE {} HEX'.format(raw_units)
      
    else:
      self.column_panel_2.visible=False
      self.button_2.enabled = True

  def check_approval(self):
    
    self.approved_hex = int(self.hex_contract.allowance(self.main.address, self.main.web3_wallet.MAXI_CONTRACT_ADDRESS).toNumber() or 0)
    
    
    return self.approved_hex

  def link_hex_balance_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.text_box_1.text=float(float(self.hex_balance)/100000000)
    self.text_box_1_change(sender=self.text_box_1)
  def approve_request(self, units):
    try:
      anvil.js.await_promise(self.write_hex_contract.approve(self.main.web3_wallet.MAXI_CONTRACT_ADDRESS, units))
      
      while self.approved_hex<self.units:
        self.check_approval()
        time.sleep(1)
        
      self.button_2.text='MINT MAXI'
      #self.column_panel_2.visible=False
      self.label_1.visible=False
      self.link_3.visible=False
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVING", "APPROVED")
      self.button_2_copy.background='green'
      self.column_panel_2.role=''
      self.button_2_copy.enabled=False
      self.button_2_copy.icon='fa:check'
      self.button_2.enabled=True
    except Exception as e:
      raise e
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVING", "APPROVE")
      self.text_box_1_change()
  def button_2_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    if 'APPROVE' in self.button_2_copy.text:
      
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVE", "APPROVING")
      self.button_2_copy.enabled=False
      self.approve_request(self.units)
    else:
      self.text_box_1_change()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    """This method is called when the button is clicked"""
    try:
      raw_units = float(self.text_box_1.text)
    except:
      return False
    units = int(raw_units*100000000)
    try:
      self.check_approval()
    except:
      Notification('You must connect to MetaMask on Ethereum Mainnet.').show()
      return False
    if units>self.approved_hex:
      self.column_panel_3.visible=False
      self.column_panel_2.visible=True
      #a = alert(Label(font_size=24,text='Maximus needs your approval to interact with {} of your HEX'.format(raw_units)),buttons=[('Cancel', False)])
      #
    else:
      print('good')
      self.button_2_copy.enabled=False
      self.button_2.enabled=False
      self.button_2.text='MINTING {} MAXI'.format(raw_units)
      
      Notification('Pledging {r} HEX and minting {r} MAXI.'.format(r=raw_units)).show()
      existing_hex = self.hex_balance
      anvil.js.await_promise(self.write_maxi_contract.pledgeHEX(units))
      while existing_hex==self.hex_contract.balanceOf(self.address).toNumber():
        time.sleep(1)
      self.button_2.enabled=True
      self.button_2.text='MINT MAXI'
      self.text_box_1.text=None
      self.text_box_1_change(sender=self.text_box_1)
      self.button_2_copy.enabled=True
      self.button_2_copy.background='#246BFD'
      self.button_2.foreground='white'
      self.button_2_copy.icon=''
      self.refresh_mint()



