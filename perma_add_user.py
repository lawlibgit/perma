from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import re
import creds
import csv

def perma_login(un, pw, driver):
 
    url = 'https://perma.cc/login' 
    driver.get(url)

    title = driver.title
    print(title)

    login_box = driver.find_element(By.ID, "id_username")
    password_box = driver.find_element(By.ID, "id_password")
    login_button = driver.find_element(By.CLASS_NAME, "login")

    login_box.send_keys(un)
    password_box.send_keys(pw)
    login_button.click()
    driver.find_element(By.CLASS_NAME, value="dropdown").click()
    driver.find_element(By.LINK_TEXT, "Organization users").click()
    driver.find_element(By.CLASS_NAME, "icon-plus-sign").click() #+add organization user btn

# Reads emails from a CSV list 
def get_emails(journal_dict):
    journals = input("Enter name of CSV file: ")
    code = input("Enter Organization Code: ") 
# Check if code entered is in the dictionary    
    while int(code) not in journal_dict.values(): 
         print("Please make sure to enter a code from the dictionary above.")
         code = input("Enter Organization Code: ")           
    journal_members = open(journals,'r')
    file = csv.DictReader(journal_members)
    email = []
    for col in file:
        email.append(col['email'])
    return email, code
    
#Add Users to an organization    
def add_user(email_list, driver):
    for user in email_list[0]:
        print(user)
        print(email_list[1])
        
        member_box = driver.find_element(By.NAME, 'email') #box where emails need to be entered
        member_box.send_keys(user)
        driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-inline").click() #Add organization user btn(Manage users and Organizations page)       
        org_list = driver.find_element(By.ID,"id_a-organizations") #list of organization 
        select = Select(org_list)
        select.select_by_value(email_list[1])
        driver.find_element(By.CSS_SELECTOR, "button.btn").click()#Add organization user btn(Add to organization page)
        driver.find_element(By.CLASS_NAME, "icon-plus-sign").click()#+add organization user btn
 
organization_dict = {} 
empty = ""  
    
with open("perma_organizations_list.csv", mode = 'r') as organization_members:
    dict_list = csv.DictReader(organization_members)

    for row in dict_list:
        if row["Code"] == empty:
            print(f"{row['Name']} has no code")
                
        else:
            organization_dict[row["Name"]] = int(row["Code"])           
          


for key, value in organization_dict.items():
    print(f"{key} : {value}")
print(f'The codes above are the perma identifiers. You can use these codes to select which organization you are adding users to.')
 

email_list = get_emails(organization_dict)
print(email_list)       
driver = webdriver.Firefox()
perma_login(creds.login_email, creds.password, driver)
add_user(email_list, driver)
driver.close()



