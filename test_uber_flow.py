# test_uber_flow.py

import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from login import click_login_button, is_logged_in
from location import enter_location_details

# Mock nova_speak and nova_listen functions for testing
def mock_nova_speak(text):
    print(f"🔊 MOCK NOVA: {text}")

def mock_nova_listen():
    # For testing, we'll return predefined responses
    global listen_count
    responses = [
        "123 Main Street",  # Pickup location
        "456 Market Street"  # Destination
    ]
    
    if listen_count < len(responses):
        response = responses[listen_count]
        listen_count += 1
        print(f"🎙️ MOCK USER: {response}")
        return response
    else:
        return "yes"  # Default response for any other questions

# Main test function
def test_uber_flow():
    global listen_count
    listen_count = 0
    
    print("\n🧪 STARTING UBER FLOW TEST\n")
    
    try:
        # Configure Chrome options
        options = uc.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 "
            "Mobile/15E148 Safari/604.1"
        )
        
        # Initialize Chrome driver
        print("🌐 Initializing Chrome driver...")
        driver = uc.Chrome(version_main=138, options=options)
        driver.set_window_size(420, 900)
        
        # Open Uber mobile site
        print("🌐 Opening Uber mobile website...")
        driver.get("https://m.uber.com/go/home")
        
        # Test login functionality
        print("\n🔑 TESTING LOGIN FUNCTIONALITY\n")
        print(f"👀 Logged in status before: {is_logged_in(driver)}")
        click_login_button(driver, mock_nova_speak)
        time.sleep(5)  # Wait for potential login process
        print(f"👀 Logged in status after: {is_logged_in(driver)}")
        
        # Test location selection
        print("\n📍 TESTING LOCATION SELECTION\n")
        enter_location_details(driver, mock_nova_speak, mock_nova_listen)
        
        # Wait for manual verification
        print("\n✅ TEST COMPLETED - Please verify the results in the browser window")
        print("The browser will close in 30 seconds...")
        time.sleep(30)
        
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
    finally:
        try:
            driver.quit()
            print("🔒 Browser closed")
        except:
            pass

if __name__ == "__main__":
    test_uber_flow()