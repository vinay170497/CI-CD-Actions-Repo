from playwright.sync_api import Page
import time

'''
def test_playwrightBasics(playwright):

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com")

def test_playwrightShortCut(page:Page):
    
    page.goto("https://rahulshettyacademy.com")
'''
"""
For CSS selector derived from ID and Classname for that locator:
# along with id
. along with classname
"""

def test_coreLocators(playwright):

    
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("Learning@830$3mK2")
    page.get_by_role("combobox").select_option("teach")
    page.locator("#terms").check()
    page.get_by_role(role = "button",name="Sign In").click()
    
    time.sleep(5)

