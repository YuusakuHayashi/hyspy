from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

entry_url = "https://trello.com";
driver = webdriver.Edge(executable_path="C:\webdriver\edgedriver_win64\MicrosoftWebDriver.exe");
driver.get(entry_url);
entry_btn = driver.find_element_by_class_name("btn btn-sm btn-link text-white");
entry_btn.click();

#def wait_and_key_send(idf):
#    try:
#        url = WebDriverWait(driver, 10).until(
#            EC.presence_of_element_located((By.ID, idf))
#        )
#    finally:
#        return url

def wait_by_id(idf):
    wait = WebDriverWait(driver,10);
    ui = wait.until(EC.presence_of_element_located((By.ID,idf)));
    ui = wait.until(EC.element_to_be_clickable((By.ID,idf)));
    return ui;

ui = wait_by_id("user");
ui.send_keys("***************************");

#ui = wait_by_id("password");
#ui.send_keys("********");

ui = wait_by_id("login");
ui.click();
