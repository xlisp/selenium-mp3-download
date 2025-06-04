from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import pickle

def initialize_browser(download_folder="downloads"):
    """Initialize and return a Chrome browser with saved cookies if available"""
    # Create download directory if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    prefs = {"download.default_directory": os.path.abspath(download_folder)}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Load cookies if they exist
    cookies_file = "quark_cookies.pkl"
    if os.path.exists(cookies_file):
        # First go to the domain
        driver.get("https://pan.quark.cn/")
        # Then add the cookies
        cookies = pickle.load(open(cookies_file, "rb"))
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"Could not load cookie: {e}")
        
        print("Loaded saved session. Refreshing page...")
        driver.refresh()
    else:
        # No saved session, need manual login
        driver.get("https://pan.quark.cn/")
        print("Please log in to your Quark account manually...")
        input("Press Enter once you've successfully logged in...")
        
        # Save cookies after login
        print("Saving your login session for future use...")
        pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))
    
    return driver

def download_song(driver, song_name):
    """Download a single song using the existing browser session"""
    try:
        # Go to search page and input song name
        driver.get("https://www.xmwav.com/index/search/")
        
        # Wait for search input to load and enter song name
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "edtSearch"))
        )
        search_input.clear()
        search_input.send_keys(song_name)
        search_input.send_keys(Keys.RETURN)
        
        # Wait for search results - adjusted selector based on actual HTML structure
        result_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul > a[href^='/mscdetail/']"))
        )
        
        link_url = result_link.get_attribute("href")
        print(f"Found song link: {link_url}")
        
        # Navigate to the link directly instead of clicking to avoid stale element issues
        driver.get(link_url)
        
        # On the detail page, find and click the "夸克MP3链接下载" button
        # Using a more robust selector that works with the actual page structure
        quark_download_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/download/') and .//h2[contains(@style, 'background:#f7de0e')]]"))
        )
        
        # Store the current window handle
        original_window = driver.current_window_handle
        
        # Get the href directly and navigate to it instead of clicking
        download_url = quark_download_btn.get_attribute("href")
        driver.execute_script(f"window.open('{download_url}', '_blank');")
        
        # Wait for the new window or tab
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        
        # Switch to the new tab (Quark pan page)
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        # Check if logged in properly (look for download button)
        try:
            # Using a more reliable wait and selector
            download_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.share-download"))
            )
            
            print("Found download button, clicking...")
            # Use JavaScript click for more reliability
            driver.execute_script("arguments[0].click();", download_btn)
            
            # Wait for download to start
            print(f"Downloading '{song_name}'...")
            time.sleep(5)
            
            # Close current tab and switch back to original
            driver.close()
            driver.switch_to.window(original_window)
            
            print(f"Song '{song_name}' has been queued for download")
            return True
            
        except Exception as e:
            print(f"Error finding download button. Login may have expired: {e}")
            # Take a screenshot for debugging
            driver.save_screenshot("error_screenshot.png")
            print("Screenshot saved as 'error_screenshot.png'")
            driver.close()
            driver.switch_to.window(original_window)
            return False
            
    except Exception as e:
        print(f"Error occurred while downloading '{song_name}': {e}")
        return False

def main():
    download_folder = input("Enter download folder path (default is 'downloads'): ") or "downloads"
    
    # Initialize browser with session handling
    driver = initialize_browser(download_folder)
    
    try:
        while True:
            song_name = input("\nEnter the name of the song to download (or 'exit' to quit): ")
            if song_name.lower() == 'exit':
                break
                
            success = download_song(driver, song_name)
            
            if not success:
                print("There was a problem downloading this song.")
                
                # Check if we need to re-login
                retry = input("Do you need to log in again? (y/n): ")
                if retry.lower() == 'y':
                    print("Please log in to Quark manually...")
                    driver.get("https://pan.quark.cn/")
                    input("Press Enter once you've successfully logged in...")
                    
                    # Save new cookies
                    pickle.dump(driver.get_cookies(), open("quark_cookies.pkl", "wb"))
                    print("Login session updated!")
    finally:
        # Don't close the driver automatically - ask user
        close = input("\nDo you want to close the browser? (y/n): ")
        if close.lower() == 'y':
            driver.quit()
            print("Browser closed.")
        else:
            print("Browser left open. You can close it manually when done.")

if __name__ == "__main__":
    main()
