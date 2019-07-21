from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

class HysSeleniumer:
    def __init__(self, entry_point):
        self.__ex_path = "C:\webdriver\edgedriver_win64\MicrosoftWebDriver.exe"
        self.driver = webdriver.Edge(executable_path=self.__ex_path);
        self.driver.get(entry_point);

    def wait_by_id(self,idf):
        wait = WebDriverWait(self.driver,10);
        ui = wait.until(EC.presence_of_element_located((By.ID,idf)));
        ui = wait.until(EC.element_to_be_clickable((By.ID,idf)));
        return ui;
    
    def wait_by_xpath(self,xpath):
        wait = WebDriverWait(self.driver,10);
        ui = wait.until(EC.presence_of_element_located((By.XPATH,xpath)));
        ui = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)));
        return ui;
    
    def wait_by_class_name(self,class_name):
        wait = WebDriverWait(self.driver,10);
        ui = wait.until(EC.presence_of_element_located((By.CLASS_NAME,class_name)));
        ui = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,class_name)));
        return ui;
