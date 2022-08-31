from ._anvil_designer import stake_pageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import time
class stake_page(stake_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    print(self.address)
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract, self.team_contract, self.reward_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
        self.write_maxi_contract, self.write_hex_contract, self.write_team_contract, self.write_reward_contract= self.main.web3_wallet.connect_contracts(self.main.signer)
        self.refresh_mint()
    except Exception as e:
      raise e
  def refresh_mint(self):
    self.team_balance = self.team_contract.balanceOf(self.address).toNumber()
    #self.maxi_balance = self.maxi_contract.balanceOf(self.address).toNumber()
    self.maxi_balance = int(self.maxi_contract.balanceOf(self.address).toString())
    self.hex_balance = self.hex_contract.balanceOf(self.address).toNumber()
    self.hex_day = self.maxi_contract.getHexDay().toNumber()
    self.minting_phase_end_day = self.team_contract.MINTING_PHASE_END().toNumber()
    self.label_mint_duration.text= '{} Days Remaining'.format(self.minting_phase_end_day-self.hex_day)
    self.link_hex_balance.text = '{:.8f} ⬣'.format(int(self.hex_balance)/100000000) 
    self.label_maxi_balance.text = '{:.8f} Ⓜ️'.format(int(self.maxi_balance)/100000000)
    self.label_team_balance.text = '{:.8f} ❇️'.format(int(self.team_balance)/100000000)
    # Any code you write here will run when the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    if self.text_box_1.text in ['', None, 0]:
      self.button_2.text='MINT TEAM'
      self.button_2.enabled = True
      
      self.units=0
      
    else:
      self.button_2.text = 'MINT {} TEAM'.format(self.text_box_1.text)
      raw_units = float(self.text_box_1.text)
      self.units = int(raw_units*100000000)
    try:
      self.check_approval()
    except Exception as e:
      raise e
      Notification('You must first connect to MetaMask.').show()
      return False
    if self.units>self.approved_maxi:
      self.column_panel_2.visible=True
      self.label_1.visible=True
      self.link_3.visible=True
      self.column_panel_2.role='card'
      self.button_2.enabled = False
      self.label_1.text="First, Maximus needs your permission to interact with {} of your MAXI.".format(raw_units)
      self.button_2_copy.text = 'APPROVE {} MAXI'.format(raw_units)
      
    else:
      self.column_panel_2.visible=False
      self.button_2.enabled = True

  def check_approval(self):
    
    self.approved_maxi = int(self.maxi_contract.allowance(self.main.address, self.main.web3_wallet.TEAM_CONTRACT_ADDRESS).toNumber() or 0)
    
    
    return self.approved_maxi

  def link_maxi_balance_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.text_box_1.text=float(float(self.maxi_balance)/100000000)
    self.text_box_1_change(sender=self.text_box_1)
  def approve_request(self, units):
    try:
      anvil.js.await_promise(self.write_maxi_contract.approve(self.main.web3_wallet.TEAM_CONTRACT_ADDRESS, units))
      
      while self.approved_maxi<self.units:
        self.check_approval()
        time.sleep(1)
        
      self.button_2.text='MINT TEAM'
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
    if units>self.approved_maxi:
      self.column_panel_3.visible=False
      self.column_panel_2.visible=True
      #a = alert(Label(font_size=24,text='Maximus needs your approval to interact with {} of your HEX'.format(raw_units)),buttons=[('Cancel', False)])
      #
    else:
      
      self.button_2_copy.enabled=False
      self.button_2.enabled=False
      self.button_2.text='MINTING {} TEAM'.format(raw_units)
      
      Notification('Pledging {r} MAXI and minting {r} TEAM.'.format(r=raw_units)).show()
      existing_maxi = self.maxi_balance
      anvil.js.await_promise(self.write_team_contract.mintTEAM(units))
      while existing_maxi==int(self.maxi_contract.balanceOf(self.address).toString()):
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

  def link_need_hex_click(self, **event_args):
    """This method is called when the link is clicked"""
    c=ColumnPanel()
    l = Label(text='Get HEX on Uniswap')
    li = Link(text='https://app.uniswap.org/#/swap?inputCurrency=0x2b591e99afe9f32eaa6214f7b7629768c40eeb39&outputCurrency=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=mainnet',url='https://app.uniswap.org/#/swap?inputCurrency=0x2b591e99afe9f32eaa6214f7b7629768c40eeb39&outputCurrency=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=mainnet')

    c.add_component(l)
    c.add_component(li)
    a = alert(c, large=True)

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    if event_args['sender'].icon == 'fa:check':
      pass
    else:
      try:
        tokenSymbol = 'TEAM'
        tokenDecimals = 8
        tokenImage = 'https://watery-decisive-guitar.anvil.app/_/api/name/maxi.jpg';

        from anvil.js.window import ethereum
        a = ethereum.request({
        'method': 'wallet_watchAsset',
        'params': {
          'type': 'ERC20', 
          'options': {
            'address': self.main.web3_wallet.TEAM_CONTRACT_ADDRESS, 
            'symbol': tokenSymbol, 
            'decimals': tokenDecimals, 
            'image': tokenImage, 
          },
        },
      })
        anvil.js.await_promise(a)
        
        event_args['sender'].icon = 'fa:check'
        event_args['sender'].text='TEAM Token Added'
      except Exception as e:
        print(e)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('To protect your security, in order for the Maximus contract to Mint MAXI with your HEX you must approve an exact amount of HEX that the Maximus contract is allowed to use on your behalf.')

  




