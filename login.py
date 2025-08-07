from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# === Check if user is already logged in ===
def is_logged_in(driver):
    try:
        # Try to find login button - if present, user is NOT logged in
        # Updated selector to be more robust
        login_elements = driver.find_elements(By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), 'Login')]")
        if login_elements:
            return False
        
        # Alternative check: look for profile icon which indicates logged in state
        profile_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='header-account-button']") 
        if profile_elements:
            return True
            
        return True  # Default to assuming logged in if no login button found
    except Exception as e:
        print(f"Error checking login status: {e}")
        return False  # Default to not logged in on error

# === Click login button if needed ===
def click_login_button(driver, speak_func):
    # Wait for page to fully load
    time.sleep(5)
    
    if is_logged_in(driver):
        speak_func("You're already logged in. Skipping login.")
        return

    speak_func("It looks like you're not logged in yet. Attempting to log in.")

    try:
        # Try multiple selectors to find login button
        login_selectors = [
            "//button[contains(text(), 'Log in')]",
            "//button[contains(text(), 'Login')]",
            "button.css-dHHA-DQ",
            "[data-testid='header-login-button']"
        ]
        
        login_btn = None
        for selector in login_selectors:
            try:
                if selector.startswith("//"):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    login_btn = elements[0]
                    break
            except:
                continue
        
        if login_btn:
            # Scroll to button and click
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", login_btn)
            print("✅ Login button clicked!")
            speak_func("Please complete the login process manually.")
        else:
            print("⚠️ Could not find login button")
            speak_func("I couldn't find the login button. Please try to log in manually.")
    except Exception as e:
        print(f"⚠️ Failed to click login button: {e}")
        speak_func("Couldn't click the login button. Please try manually.")

    # Wait for manual login
    for i in range(60):
        if is_logged_in(driver):
            speak_func("Login detected. You're now logged in.")
            return
        time.sleep(2)

    speak_func("Login not detected within time. Please try again.")
