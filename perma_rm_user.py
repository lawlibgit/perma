#! /usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import creds
import csv

def perma_login(un, pw, driver):
    url = 'https://perma.cc/login'
    
    driver.get(url)

    login_box = driver.find_element(By.ID, "id_username")
    password_box = driver.find_element(By.ID, "id_password")
    login_button = driver.find_element(By.CLASS_NAME, "login")

    login_box.send_keys(un)
    password_box.send_keys(pw)
    login_button.click()

def nav_to_rm(driver,journal_dict):
    perma_login(creds.login_email, creds.password, driver)
    journal_values = journal_dict.values()
            
    for journal_value in journal_values:
        journal_url = f"https://perma.cc/manage/organization-users?org={journal_value}&sort=date_joined"
        journal_key = list(journal_dict.keys())[list(journal_dict.values()).index(journal_value)]
        deleting = True
        while deleting == True:
            driver.get(journal_url)
            user_count = (driver.find_element(By.CLASS_NAME, "count-number").text)
            users = int(user_count)
# If No Users
            if users == 0:
               print(f"{journal_key}")
               print("no users")
               deleting = False
            else:
               deleting = True   
# Getting the creation year        
               texto = (driver.find_element(By.CLASS_NAME, "item-activity").text)
               split_texto = re.split(r'\n',texto)
               creation = split_texto[0]
               creation_year = int(creation[-4:])            
# Comparing creation year and Deleting
 #             creation_cutoff = 2019
               if creation_year <= creation_cutoff:
                  print(texto)
                  print(users)
                  print(creation_year)
                  print("ready to delete")   
                  driver.find_element(By.CLASS_NAME, "action.action-delete").click()
                  driver.find_element(By.CLASS_NAME, "btn.btn-default.btn-xs.leave-org-btn").click()
               else:
                 print(f"{journal_key}")
                 print(f"no members before {creation_cutoff}")
                 deleting = False       
# Creating dictionary from the CSV  
org_dict = open("perma_organizations_list.csv", mode = 'r')
file = csv.DictReader(org_dict)
journal_dict = {}

for row in file:
   if row['Jrnl'] == "Y":
      journal_dict[row["Abbreviation"]] = row["Code"]
   else:
      continue 
#       print("Members from ",row['Name'],"will not be removed")
#print(journal_dict)  
    
                
# ------------------------------------

texto = ""
deleting = True
print(f'These are the Perma organizations this script will act on. Please update the CSV file if you need to make changes.')
for key, value in journal_dict.items():
    print(f'{key}: {value}')
proceed = input("Enter 'y' if you would like to proceed. Anything else will result in the script quitting: \n")
if proceed == 'y':
    creation_cutoff = int(input("Enter the cutoff year you would like members to be removed: "))
    driver = webdriver.Firefox()
    nav_to_rm(driver,journal_dict)
    driver.close()
else:
    print('Please re-run the script when you are ready to proceed')


