import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_valid_location(prompt, nova_speak, nova_listen, retries=3):
    """Repeat prompt until user gives valid input or retries run out"""
    for attempt in range(retries):
        nova_speak(prompt)
        location = nova_listen()
        if location and location.strip():
            return location
        else:
            nova_speak("I didn't catch that. Please say it again.")
    nova_speak("I'm sorry, I couldn't understand the location.")
    return None

def enter_location_details(driver, nova_speak, nova_listen):
    wait = WebDriverWait(driver, 30)  # Increased timeout

    try:
        # Wait for page to fully load
        time.sleep(5)
        
        # Check if we're on the home page or already in the ride booking flow
        try:
            # Look for the "Where to?" button on the home page
            where_to_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Where to?') or contains(., 'Where to')]")
            if where_to_buttons:
                print("✅ Found 'Where to?' button on home page")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", where_to_buttons[0])
                time.sleep(1)
                driver.execute_script("arguments[0].click();", where_to_buttons[0])
                time.sleep(3)  # Wait for the ride booking interface to load
        except Exception as e:
            print(f"Note: No 'Where to?' button found, might already be in booking flow: {e}")
        
        # 🚕 Step 1: Ask for Pickup Location with retries
        pickup_location = get_valid_location("Where should I pick you up from?", nova_speak, nova_listen)
        if not pickup_location:
            return

        # Step 2: Find and click the pickup button with multiple selectors
        pickup_selectors = [
            '[data-testid="pudo-button-pickup"]',
            '[data-testid="pickup-button"]',
            '[aria-label="Pickup location"]',
            '//button[contains(text(), "Pickup")]',
            '//button[contains(@class, "pickup")]',
            '//div[contains(@class, "pickup")]'
        ]
        
        pickup_button = None
        for selector in pickup_selectors:
            try:
                if selector.startswith('//'):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    pickup_button = elements[0]
                    break
            except:
                continue
        
        # If no pickup button found, look for the input field directly
        input_selectors = [
            'input[placeholder="Pickup location"]',
            'input[placeholder*="Pickup"]',
            'input[placeholder="Enter pickup location"]',
            'input[aria-label*="Pickup"]',
            '[data-testid="pickup-input"]',
            'input[placeholder*="Where"]',  # Sometimes the first input is just "Where"
            'input',  # Last resort: try any input field
        ]
        
        input_box = None
        
        # If pickup button found, click it first
        if pickup_button:
            # Scroll to button and click
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pickup_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", pickup_button)
            print("✅ Pickup button clicked!")
            time.sleep(2)  # Wait for input field to appear
            
            # Now look for the input field
            for selector in input_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        input_box = elements[0]
                        break
                except:
                    continue
        else:
            # If no pickup button, try to find input field directly
            print("⚠️ Could not find pickup button, looking for input field directly")
            
            # Try to find any input field
            for selector in input_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        input_box = elements[0]
                        break
                except:
                    continue
        
        # If input box found, enter location
        if input_box:
            # Clear any existing text and enter new location
            input_box.clear()
            input_box.send_keys(pickup_location)
            print(f"✅ Pickup location entered: {pickup_location}")
            time.sleep(3)  # Increased wait time for suggestions to load
        else:
            # Last resort: try to find any input field
            try:
                inputs = driver.find_elements(By.TAG_NAME, "input")
                if inputs:
                    inputs[0].clear()
                    inputs[0].send_keys(pickup_location)
                    print(f"✅ Pickup location entered in first available input: {pickup_location}")
                    time.sleep(3)
                else:
                    print("⚠️ Could not find any input field")
                    nova_speak("I couldn't find where to enter the pickup location. Please try manually.")
                    return
            except Exception as e:
                print(f"⚠️ Could not find pickup input field: {e}")
                nova_speak("I couldn't find where to enter the pickup location. Please try manually.")
                return

        # Step 4: Select the first suggestion with multiple selectors
        suggestion_selectors = [
            '[role="option"]',
            '[data-testid*="suggestion"]',
            '.autocomplete-result',
            '//div[contains(@class, "suggestion")]',
            '//li[contains(@class, "suggestion")]',
            '//div[contains(@class, "autocomplete")]',
            '//div[contains(@class, "result")]'
        ]
        
        first_option = None
        for selector in suggestion_selectors:
            try:
                if selector.startswith('//'):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    first_option = elements[0]
                    break
            except:
                continue
        
        if first_option:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_option)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", first_option)
            print("✅ First pickup suggestion selected")
        else:
            print("⚠️ No pickup suggestions found, trying to continue")
            # Try pressing Enter key as fallback
            try:
                input_box.send_keys(Keys.ENTER)
                print("✅ Pressed Enter key to confirm pickup")
            except:
                pass
            
            # Additional fallback: try clicking any visible button that might confirm the location
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    if button.is_displayed():
                        button_text = button.text.lower()
                        if "confirm" in button_text or "next" in button_text or "continue" in button_text:
                            driver.execute_script("arguments[0].click();", button)
                            print(f"✅ Clicked fallback button: {button_text}")
                            break
            except Exception as e:
                print(f"Note: Could not find fallback button: {e}")

        # Wait for destination input to appear
        time.sleep(5)  # Increased wait time
        
        # 🛬 Step 5: Ask for Destination with retries
        destination = get_valid_location("Where are you going?", nova_speak, nova_listen)
        if not destination:
            return

        # Step 6: Enter destination with multiple selectors
        dest_selectors = [
            'input[placeholder="Dropoff location"]',
            'input[placeholder*="Dropoff"]',
            'input[placeholder*="Where to"]',
            'input[placeholder*="destination"]',
            'input[aria-label*="Destination"]',
            '[data-testid="destination-input"]',
            'input:not([value])'  # Try any empty input field
        ]
        
        # First check if we need to click a destination button
        dest_button_selectors = [
            '[data-testid="pudo-button-destination"]',
            '[data-testid="destination-button"]',
            '[aria-label*="Destination"]',
            '//button[contains(text(), "Destination")]',
            '//button[contains(text(), "Where to")]',
            '//button[contains(@class, "destination")]'
        ]
        
        dest_button = None
        for selector in dest_button_selectors:
            try:
                if selector.startswith('//'):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    dest_button = elements[0]
                    break
            except:
                continue
        
        if dest_button:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dest_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", dest_button)
            print("✅ Destination button clicked!")
            time.sleep(2)  # Wait for input field to appear
        
        # Now look for the destination input field
        destination_box = None
        for selector in dest_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Find the first visible and enabled input
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            destination_box = element
                            break
                    if destination_box:
                        break
            except:
                continue
        
        # If still not found, try to find any input field that's not the pickup field
        if not destination_box:
            try:
                inputs = driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    try:
                        if inp.is_displayed() and inp.is_enabled():
                            # Check if this is not the same as the pickup input
                            if input_box and inp != input_box:
                                destination_box = inp
                                break
                            # If we don't have a reference to the pickup input, use the second input
                            elif inputs.index(inp) > 0:
                                destination_box = inp
                                break
                    except:
                        continue
            except Exception as e:
                print(f"Note: Error finding alternative destination input: {e}")
        
        # If still not found, try clicking on the page where a destination field might be
        if not destination_box:
            try:
                # Try to find elements that might be related to destination input
                potential_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Where to') or contains(text(), 'Destination') or contains(text(), 'Drop-off')]")
                if potential_elements:
                    # Click on the element to potentially reveal the input field
                    driver.execute_script("arguments[0].click();", potential_elements[0])
                    print(f"✅ Clicked on potential destination element: {potential_elements[0].text}")
                    time.sleep(2)
                    
                    # Try to find input fields again
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    if inputs and len(inputs) > 1:
                        destination_box = inputs[1]  # Try the second input field
                    elif inputs:
                        destination_box = inputs[0]  # Or the first if only one exists
            except Exception as e:
                print(f"Note: Error with fallback destination detection: {e}")
        
        # Last resort: try to find any visible element that might accept input
        if not destination_box:
            try:
                # Try clicking in the center of the page to activate any hidden input
                driver.execute_script("document.elementFromPoint(window.innerWidth/2, window.innerHeight/2).click();")
                time.sleep(1)
                
                # Check for any newly appeared inputs
                inputs = driver.find_elements(By.TAG_NAME, "input")
                if inputs:
                    for inp in inputs:
                        if inp.is_displayed() and inp.is_enabled():
                            destination_box = inp
                            break
            except Exception as e:
                print(f"Note: Error with last resort destination detection: {e}")
        
        if destination_box:
            # Clear any existing text and enter new destination
            try:
                destination_box.clear()
            except:
                pass  # Some inputs can't be cleared
            
            destination_box.send_keys(destination)
            print(f"✅ Destination entered: {destination}")
            time.sleep(3)  # Increased wait time for suggestions to load
        else:
            # Try to find any clickable element that might lead to destination input
            try:
                # Look for buttons or elements with text related to destination
                elements = driver.find_elements(By.XPATH, "//button[contains(text(), 'Where') or contains(text(), 'Destination') or contains(text(), 'Next')]")
                if elements:
                    driver.execute_script("arguments[0].click();", elements[0])
                    print(f"✅ Clicked on potential destination button: {elements[0].text}")
                    time.sleep(2)
                    
                    # Try one more time to find the input
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    if inputs:
                        destination_box = inputs[0]
                        destination_box.send_keys(destination)
                        print(f"✅ Destination entered after button click: {destination}")
                        time.sleep(3)
                    else:
                        print("⚠️ Still could not find destination input field")
                        nova_speak("I couldn't find where to enter the destination. Please try manually.")
                        return
                else:
                    print("⚠️ Could not find destination input field or related buttons")
                    nova_speak("I couldn't find where to enter the destination. Please try manually.")
                    return
            except Exception as e:
                print(f"⚠️ Final attempt to find destination input failed: {e}")
                nova_speak("I couldn't find where to enter the destination. Please try manually.")
                return

        # Step 7: Select the first destination suggestion with multiple selectors
        dest_suggestion = None
        for selector in suggestion_selectors:  # Reuse the same selectors as for pickup
            try:
                if selector.startswith('//'):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    dest_suggestion = elements[0]
                    break
            except:
                continue
        
        if dest_suggestion:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dest_suggestion)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", dest_suggestion)
            print("✅ Destination suggestion selected")
        else:
            print("⚠️ No destination suggestions found, trying to continue")
            # Try pressing Enter key as fallback
            try:
                destination_box.send_keys(Keys.ENTER)
                print("✅ Pressed Enter key to confirm destination")
            except:
                pass
            
            # Additional fallback: try clicking any visible button that might confirm the location
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    if button.is_displayed():
                        button_text = button.text.lower()
                        if "confirm" in button_text or "next" in button_text or "continue" in button_text or "search" in button_text:
                            driver.execute_script("arguments[0].click();", button)
                            print(f"✅ Clicked fallback button: {button_text}")
                            break
            except Exception as e:
                print(f"Note: Could not find fallback button: {e}")

        # Wait for ride options to load
        time.sleep(5)
        nova_speak("Locations entered successfully.")

    except Exception as e:
        print("❌ Error in entering locations:", e)
        nova_speak("Something went wrong while entering the locations. Please try again or enter them manually.")
