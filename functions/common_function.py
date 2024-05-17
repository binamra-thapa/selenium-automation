import os
import sys
import time
import shutil
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_screenshot_folder():
    today = date.today()
    folder_name = today.strftime("%Y-%m-%d")
    ss_folder = "/Users/binamra.thapa/Desktop/My/Devops/selenium-automation/screenshots"
    folder_path = os.path.join(ss_folder, folder_name)
    if os.path.exists(folder_path):
        shutil.rmtree(ss_folder)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def get_next_numeric_suffix(folder_path):
    all_files = os.listdir(folder_path)
    existing_files = [filename for filename in all_files if "_page" in filename]
    numeric_suffix = len(existing_files) + 1
    return numeric_suffix

def take_screenshot(driver, folder_path, filename):
    screenshot_path = os.path.join(folder_path, filename)
    driver.save_screenshot(screenshot_path)

def login_page(driver, login_url, login_username, login_password, folder_path, numeric_suffix):
    today = date.today()
    driver.get(login_url)
    if "cs" in login_url:
        login_page = "int"
    else:
        login_page = "ext"

    try:
        no_upstream = driver.find_element(By.XPATH, "//*[contains(text(), 'no healthy upstream')]")
        print(f"{login_url} contains 'no healthy upstream' message. Aborting.")
    except Exception as e:
        pass  # Continue if the message is not found
    
    username = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "input-0")))
    password = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "input-1")))
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
    
    username.send_keys(login_username)
    password.send_keys(login_password)

    print(f"{login_page}ernal login completed.")
    login_screenshot_filename = f"{login_page}-login-{today}-{numeric_suffix}.png"
    take_screenshot(driver, folder_path, login_screenshot_filename)
    login_button.click()

def check_pingfed(driver, login_url, login_username, login_password, folder_path, numeric_suffix):
    #needs work
    today = date.today()
    driver.get(login_url)

    username = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))
    password = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "password")))
    sign_on = driver.find_element(By.XPATH, "//tr[@class='login-button ui-row-2 even']//input[@type='submit' and @value='Sign On']")
    
    username.send_keys(login_username)
    password.send_keys(login_password)
    sign_on.click()
    time.sleep(4)
    print("Pingfed check Completed Successfully ...")
    login_screenshot_filename = f"pingfed-login-{today}-{numeric_suffix}.png"
    take_screenshot(driver, folder_path, login_screenshot_filename)

def check_status(driver,login_url, folder_path, numeric_suffix):
    today = date.today()
    # driver.get(login_url)
    driver.execute_script("window.open('" + login_url + "', '_blank');")
    if "keycloak" in login_url:
        index = "keycloak"
    elif "portal" in login_url:
        index = "portal"
    elif "pxi" in login_url:
        index = "pxi"
    elif "jasper" in login_url:
        index = "jasper"
    else:
        index = "ROC"
    driver.switch_to.window(driver.window_handles[-1])

        # Check if the page contains "no healthy upstream" message
    try:
        no_upstream = driver.find_element(By.XPATH, "//*[contains(text(), 'no healthy upstream')]")
        print(f"{login_url} contains 'no healthy upstream' message. Aborting.")
        return
    except Exception as e:
        pass  # Continue if the message is not found

    time.sleep(5)
    print(f"{login_url} check Completed succesfully...")
    index_screenshot_filename = f"{index}-login-{today}-{numeric_suffix}.png"
    take_screenshot(driver, folder_path, index_screenshot_filename)

def home_page(driver, folder_path, numeric_suffix,member_id,extra):
    today = date.today()
    if "cs" in extra:
        logged_page = "int"
    else:
        logged_page = "ext"
    memberId = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "input-8")))
    memberId.send_keys(member_id)
    
    print(f"{logged_page}ernal Home page loads successfully.")
    logged_screenshot_filename = f"{logged_page}-logged_page-{today}-{numeric_suffix}.png"
    take_screenshot(driver, folder_path, logged_screenshot_filename)

    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    search_button.click()

def admin_page(driver, folder_path, numeric_suffix):
    today = date.today()
    # Wait until the search results are loaded
    time.sleep(5)
    
    try:
        no_upstream = driver.find_element(By.XPATH, "//*[contains(text(), 'no healthy upstream')]")
        print(f"Admin Page contains 'no healthy upstream' message. Aborting.")
        return
    except Exception as e:
        pass  # Continue if the message is not found
    print("Admin page loads successfully.")
    # Take a screenshot
    admin_screenshot_filename = f"admin_page-{today}-{numeric_suffix}.png"
    take_screenshot(driver, folder_path, admin_screenshot_filename)
    
def roc_page(driver,roc_vendor,roc_payer,folder_path,numeric_suffix):
    today = date.today()
    initial_window_handle = driver.current_window_handle


    ul_elements = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME, "rocLinksList-0-2-579")))
    options = ul_elements.find_elements(By.TAG_NAME, "li")
    
    for option in options:
        if option.text == roc_vendor or option.text == roc_payer:
            option_text = option.text.replace(" ", "-")  # Replace spaces with underscores
            option.click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(10)

             # Take a screenshot
            roc_screenshot_filename = f"{option_text}-{today}-{numeric_suffix}.png"
            take_screenshot(driver, folder_path, roc_screenshot_filename)   
            # Switch back to the initial tab
            driver.switch_to.window(initial_window_handle)
    
    print("Roc page loads successfully.")

def payments(driver, folder_path, numeric_suffix):
    today = date.today()
    initial_window_handle = driver.current_window_handle
    try:
        link_element = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '//a[@target="_self" and @href="/paymode/payments.jsp"]')))
        link_element.send_keys(Keys.COMMAND + Keys.RETURN)

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        print("payment page loads successfully.")
        payments_screenshot_filename = f"payments_page-{today}-{numeric_suffix}.png"
        take_screenshot(driver, folder_path, payments_screenshot_filename)
        driver.switch_to.window(initial_window_handle)
    except Exception as e:
        print("An error occurred during payment page check:")
    finally:
        # Switch back to the original tab, regardless of whether an exception occurred or not
        driver.switch_to.window(initial_window_handle)

def payments_dropdown(driver,folder_path,numeric_suffix,env):
    today = date.today()
    env = env
    link = f"https://pmx-{env}-cs.saas-n.com/px/payments/incoming/received"
    driver.execute_script("window.open('" + link + "', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])


    #ClickTheButton
    button_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-0-2-600")))
    button_element.click()

    seven_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'modificationDatePeriod-range-option-Last 90 Days')))
    # Click the button
    seven_button.click()

    form = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "searchForm-0-2-549")))
    search_button = form.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    search_button.click()


    dropdown_element = driver.find_element(By.ID, "select-0")
    dropdown_element.click()
    print("Payments page-exports loads successfully.")
    time.sleep(5)
    # Get all the options within the dropdown
    options = dropdown_element.find_elements(By.TAG_NAME, "option")
    # Check if there are any options
    if len(options) > 0:
        print("Payments page Dropdown has values")
    else:
        print("Payments page Dropdown is empty")
    dropdown_element.click()


#NeedsWORK
    # ul_elements = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME, "dropdown-menu dropdown-menu-right")))
    # options = ul_elements.find_elements(By.TAG_NAME, "li")

    # for li in options:
    #     print(li.text)
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Export']")))
    button.click()
    # export = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn btn-tertiary dropdown-trigger")))
    # export.click()

    # # download_button = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn btn-tertiary undefined")))
    # # download_button[0].click()
    # # download_button[1].click()

    # ul_elements = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME, "dropdown-menu dropdown-menu-right")))
    # options = ul_elements.find_elements(By.TAG_NAME, "li")
    # options[0].click
    # options[1].click

def roc_web(driver, roc_url, login_username, login_password, folder_path, numeric_suffix):
    today = date.today()
    driver.execute_script("window.open('" + roc_url + "', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "menu1")))
    login_screenshot_filename = f"roc-login-{today}-{numeric_suffix}.png"
    take_screenshot(driver, folder_path, login_screenshot_filename)

def glu_export(driver,folder_path,numeric_suffix):

    today = date.today()
    initial_window_handle = driver.current_window_handle

    try:
        reports = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '//a[@target="_self" and @href="/px/reports/dashboard"]')))
        reports.send_keys(Keys.COMMAND + Keys.RETURN) # payments_dropdown = driver.find_element(By.CLASS_NAME, "navTabsList-0-2-60")

        driver.switch_to.window(driver.window_handles[-1])


        remittance_report = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/px/reports/vendor/payments"]')))
        remittance_report.send_keys(Keys.COMMAND + Keys.RETURN) 
        driver.switch_to.window(driver.window_handles[-1])

        form = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "searchForm-0-2-565")))
        report_search = form.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
        report_search.click()

        #Export to xlsx 
        export = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "actionableIcon-0-2-728")))
        export[2].click()

        download_button = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menuButton-0-2-751")))
        download_button[0].click()


        print("Reports page loads successfully.")

        glu_reports_screenshot_filename = f"reports_page-{today}-{numeric_suffix}.png"
        take_screenshot(driver, folder_path, glu_reports_screenshot_filename)

        driver.switch_to.window(initial_window_handle)
    except Exception as e:
        # Handle the exception, print error message, etc.
        print("An error occurred during Reports check:")


    finally:
        driver.switch_to.window(initial_window_handle)

# def open_link(driver, href):
#     # Open the link in a new tab
