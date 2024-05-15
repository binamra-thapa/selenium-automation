from functions.common_function import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback

def paymode(environment):
    # Initialize WebDriver    
    options = Options()
    # options.add_argument("--headless")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    #Variables
    env= environment
    member_id="108439"
    roc_vendor = "ROC - Vendor page"
    roc_payer = "ROC - Payer page"
    pf_username=f"asdf"
    pf_password="asdf"
    login_url_int = f"https://pmx-{env}-cs.saas-n.com/px/login"
    login_url_ext = f"https://pmx-{env}-web.saas-n.com/px/login"
    login_username=f"hostingapplications@bottomline.com"
    pingfed_url=f"https://pmx-{env}-pingfed-admin.saas-n.com/pingfederate/app"
    keycloak_url=f"https://pmx-{env}-keycloak.saas-n.com/"
    portal_url=f"https://pmx-{env}-portal.saas-n.com/mississippi"
    pxi_url=f"https://pmx-{env}-pxi.saas-n.com/"
    jasper_url=f"https://pmx-{env}-jasper.saas-n.com/jasperserver/login.html"
    roc_url=f"https://pmx-{env}-roc-web.saas-n.com/roc-web/"

    if "qa" in login_url_ext or "qa" in login_url_int:
        login_password="asdf"
    else:
            login_password="ffasdf"

    print(f"Running Tests for {env}")
    # Create screenshot folder
    folder_path = create_screenshot_folder()
    # Get next numeric suffix
    numeric_suffix = get_next_numeric_suffix(folder_path)

    try:
        # Perform Internallogin
        login_page(driver, login_url_int, login_username, login_password, folder_path, numeric_suffix)

        #PaymentsPage: Loads the Payment Page
        payments(driver, folder_path, numeric_suffix)

        # Perform search and navigation: Loads the Home Page
        home_page(driver, folder_path, numeric_suffix,member_id,login_url_int)

        # Perform SS on admin page: Loads the adminPage
        admin_page(driver, folder_path, numeric_suffix)
       

        try:
            # Reports: Loads the reportPage
            glu_export(driver,folder_path,numeric_suffix)

        except Exception as e:
            print("An error occurred during Reports check:")

        # try:
        #     # PerformExports and stuffs
        #     payments_dropdown(driver,folder_path,numeric_suffix)
        # except Exception as e:
        #     print("An error occurred during PerformExports page check:")

        try:
            #Perform action on roc: Loads the payer,vendor page
            roc_page(driver,roc_vendor,roc_payer,folder_path,numeric_suffix)

        except Exception as e:
            print("An error occurred during payer,vendor page check:")
            
    except Exception as e:
        print("An error occurred...Possible: Internal Login Err")

    try:
        # #Perform Login external
        login_page(driver, login_url_ext, login_username, login_password, folder_path, numeric_suffix)
        
        # Perform search and navigation
        home_page(driver, folder_path, numeric_suffix,member_id,login_url_ext)

    except Exception as e:
        print("An error occurred: Exteral Login")

    try:
        check_pingfed(driver, pingfed_url, pf_username, pf_password, folder_path, numeric_suffix)

    except Exception as e:
        print("An error occurred during pingfed check:")

    try:
        # Check Status of Keycloak
        check_status(driver, keycloak_url, folder_path, numeric_suffix)

    except Exception as e:
        print("An error occurred during Keycloak status check:")

    try:
        # Check Status of Portal
        check_status(driver, portal_url, folder_path, numeric_suffix)

    except Exception as e:
        print("An error occurred during Portal status check:")

    try:
        # Check Status of PXI
        check_status(driver, pxi_url, folder_path, numeric_suffix)

    except Exception as e:
        print("An error occurred during PXI status check:")

    try:
        # Check Status of Jasper
        check_status(driver, jasper_url, folder_path, numeric_suffix)

    except Exception as e:
        print("An error occurred during Jasper status check:")

    try:
        # Check Status of ROC
        check_status(driver, roc_url, folder_path, numeric_suffix)

    except Exception as e:
        print("An error occurred during ROC status check:")

    finally:
        # Quit the driver
        driver.quit()


def test_paymode():
    # Initialize WebDriver    
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    #Variables
    env="qa7"
    login_url_int = f"https://pmx-{env}-cs.saas-n.com/px/login"
    login_url_ext = f"https://pmx-{env}-web.saas-n.com/px/login"
    roc_url=f"https://pmx-{env}-roc-web.saas-n.com/roc-web/"


    # login_username=f"ABIRR_{env.upper()}_I@paymode.com"
    login_username=f"hostingapplications@bottomline.com"
    if "qa" in login_url_ext or "qa" in login_url_int:
        login_password="asdf"
    else:
            login_password="asdf"

    pf_username=f"asdf"
    pf_password="asdf"

    pingfed_url=f"https://pmx-{env}-pingfed-admin.saas-n.com/pingfederate/app"
    keycloak_url=f"https://pmx-{env}-keycloak.saas-n.com/"
    portal_url=f"https://pmx-{env}-portal.saas-n.com/mississippi"
    pxi_url=f"https://pmx-{env}-pxi.saas-n.com/"
    jasper_url=f"https://pmx-{env}-jasper.saas-n.com/jasperserver/login.html"

    member_id="108439"
    roc_vendor = "ROC - Vendor page"
    roc_payer = "ROC - Payer page"

    # # #InitialSetup
    folder_path = create_screenshot_folder()
    numeric_suffix = get_next_numeric_suffix(folder_path)

    # roc_web(driver, roc_url, login_username, login_password, folder_path, numeric_suffix)
    # print(pingfed)
    # print(login_url_int)
    # print(login_url_ext)

    # check_pingfed(driver, pingfed_url, pf_username, pf_password, folder_path, numeric_suffix)
    # # Perform login internal
    login_page(driver, login_url_int, login_username, login_password, folder_path, numeric_suffix)
    
    # # # #PaymentsPage
    # # payments(driver, folder_path, numeric_suffix)
    home_page(driver, folder_path, numeric_suffix,member_id,login_url_int)
    admin_page(driver, folder_path, numeric_suffix)

    payments_dropdown(driver,folder_path,numeric_suffix,env)
    # roc_page(driver,roc_vendor,roc_payer,folder_path,numeric_suffix)
    # glu_export(driver,folder_path,numeric_suffix)

    # # #Perform Login external
    # login_page(driver, login_url_ext, login_username, login_password, folder_path, numeric_suffix)
     
    # # check_pingfed(driver, pingfed_url, pf_username, pf_password, folder_path, numeric_suffix)

    # check_status(driver, keycloak_url,folder_path, numeric_suffix)
    # check_status(driver, portal_url,folder_path, numeric_suffix)
    # check_status(driver, pxi_url,folder_path, numeric_suffix)
    # check_status(driver, jasper_url,folder_path, numeric_suffix)
    # driver.quit()