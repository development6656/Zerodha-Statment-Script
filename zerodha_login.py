#!/usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json
import pdb
import time
import os

class ZerodhaSelenium( object ):

   def link_still_not_reloaded(self, xpath):
      try:
          #view_button.find_element_by_class_name('btn-blue')
          self.getXpathElement(xpath)
          return True
      except (StaleElementReferenceException):
          return False

  

   def __init__( self ):
      self.timeout = 25
      self.loadCredentials()
      self.driver = webdriver.Chrome("/chromedriver")

   def getCssElement( self, cssSelector ):
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )
   def getXpathElement( self, xpath ):
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout ).until( EC.presence_of_element_located( ( By.XPATH, xpath ) ) )

   def getClassElement( self, classname ):
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout ).until( EC.presence_of_element_located( ( By.CLASS_NAME, classname ) ) )


   def loadCredentials( self ):
      with open( "credentials.json") as credsFile:
         data = json.load( credsFile )
         self.username = data[ 'username' ]
         self.password = data[ 'password' ]
         self.pin      = data[ 'pin' ]
         self.fy       = 2019
         self.fm       = 11
         self.fd       = 1
         self.ty       = 2019
         self.tm       = 12
         self.td       = 1
         self.cy       = 2019
         self.cm       = 12
         self.cd       = 9
         self.file_path= "/home/suman/scripts/stat/"

         #self.security = data[ 'security' ] # for 2FA
   def click_button(self, button, t):
       for i in range(t):
           button.click()

   def set_date(self):
       if(self.cy > self.fy):
           button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/a[1]")
           self.click_button(button, self.cy-self.fy)
       else:
           button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/a[3]")
           self.click_button(button, self.fy-self.cy)

       if(self.cm > self.fm):
          button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/a[2]")
          self.click_button(button, self.cm-self.fm)
       else:
          button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/a[4]")
          self.click_button(button, self.fm-self.cm)

       if(self.cy > self.ty):
          button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/a[1]")
          self.click_button(button, self.cy-self.ty)
       else:
          button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/a[3]")
          self.click_button(button, self.ty-self.cy)

       if(self.cm > self.tm):
          button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/a[2]")
          self.click_button(button, self.cm-self.tm)
       else:
          button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/a[4]")
          self.click_button(button, self.tm-self.cm)

   def wait_for(self, cond_func, xpath):
       start_time = time.time()
       while (time.time() < start_time+3):
           if cond_func(xpath):
               return True
           else:
               time.sleep(0.1)

       raise Exception(
                'Timeout waiting for {}'.format(cond_func.__name__)
                )
       
   def create_pdf(self, file_path):
       from PIL import Image 
       list_imgs = os.listdir(file_path)
       images = []
       for img in list_imgs:
           img = file_path + img
           im  = Image.open(img)
           if im.mode == "RGBA":
               im = im.convert("RGB")
           images.append(im)
       images[0].save("statment.pdf", save_all = True, quality=100, append_images = images[1:])
   def clear_mess(self):
       os.system("rm -r " + self.file_path)
   
   def create_env(self):
       os.system("mkdir " + self.file_path)

   def doLogin( self ):
      
      self.create_env()
      #let's login
      self.driver.get( "https://kite.zerodha.com/")
      try:
         passwordField  = self.getCssElement( "input[type=Password]" )
         passwordField.send_keys( self.password )
         userNameField  = self.getCssElement( "input[placeholder='User ID']" )
         userNameField.send_keys( self.username )
         submitButton   = self.getCssElement( "button[type=submit]" )
         submitButton.click()
         
         try:
            pinField    = self.getCssElement("input[type=password]")
            pinField.send_keys( self.pin )
         except StaleElementReferenceException:
            pinField    = self.getCssElement("input[type=password]")
            pinField.send_keys( self.pin )
         loginButton    = self.getCssElement( "button[type=submit]" )   
         loginButton.click()
        
         print(self.driver.current_url)
         try:
            dropdown    = self.getXpathElement("//a[@class='dropdown-label']")
         except StaleElementReferenceException:
            dropdown    = self.getXpathElement("//a[@class='dropdown-label']")

         dropdown.click()
         console        = self.getXpathElement("//a[@href='https://console.zerodha.com/dashboard/']")
         console.click()
         
         n_window       = self.driver.window_handles[-1]
         self.driver.switch_to.window(n_window)
         print(self.driver.current_url)
         
         report         = self.getXpathElement("//a[@class='dropdown-label reports-label']")
         report.click()

         tradebook      = self.getXpathElement("//a[@href='/reports/tradebook']")
         tradebook.click()

          #set date of which statement you want
         date_range     = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[1]")
         date_range.click()
         self.set_date()
         # set day is still required to figure out
         fr,tr,fc,tc    = (1,2,6,1)
         day_f          = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[1]/div[3]/table/tbody/tr[%d]/td[%d]" %(fr, fc) )
         day_t          = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[3]/div/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[%d]/td[%d]" %(tr, tc) )
         day_f.click()
         day_t.click()
         temp           = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[2]/div/input")
         temp.click()
         try:
             print(self.driver.current_url)
             a_dropdown = Select( self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[1]/select") )
         except StaleElementReferenceException:
             print(self.driver.current_url) 
             a_dropdown = Select( self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[1]/select") )
         
        #statement of all the asset classes
         for asset_i in range(1, len(a_dropdown.options)):
            aa = a_dropdown.select_by_index(asset_i)
            view_button = self.getXpathElement("//*[@id='app']/div[2]/div/div/div/form/div/div[4]/button")
            view_button.click()
            
            self.wait_for(self.link_still_not_reloaded, "//*[@id='app']/div[2]/div/div/div/form/div/div[4]/button")
            # Take ScreenShot
            self.driver.get_screenshot_as_file(self.file_path + str(asset_i) + ".png")
         
         self.create_pdf(self.file_path)
      except TimeoutException:
         print( "Timeout occurred" )

      pdb.set_trace()
      # close chrome
      self.driver.quit()
      self.clear_mess()

if __name__ == "__main__":
   obj = ZerodhaSelenium()
   obj.doLogin()
