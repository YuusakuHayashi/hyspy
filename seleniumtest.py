from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from hys import hysfiler

entry_url = "https://trello.com/login";
next_url  = "https://trello.com/******************"
driver = webdriver.Edge(executable_path="C:\webdriver\edgedriver_win64\MicrosoftWebDriver.exe");
driver.get(entry_url);

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

def wait_by_xpath(xpath):
    wait = WebDriverWait(driver,10);
    ui = wait.until(EC.presence_of_element_located((By.XPATH,xpath)));
    ui = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)));
    return ui;

def wait_by_class_name(class_name):
    wait = WebDriverWait(driver,10);
    ui = wait.until(EC.presence_of_element_located((By.CLASS_NAME,class_name)));
    ui = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,class_name)));
    return ui;

hys = hysfiler.HysFiler("cfg.txt")
cfg = hys.read_user_cfg()

ui = wait_by_id("user");
ui.send_keys(cfg["email"]);

#ui = wait_by_id("password");
#ui.send_keys("********");

ui = wait_by_id("login");
ui.click();

driver.get(next_url);

ui = wait_by_xpath("//*[@id='board']/div[1]/div/div[2]/a[1]");
ui.click();

ui = wait_by_class_name("mod-card-back-title js-card-detail-title-input");
ui.click();
