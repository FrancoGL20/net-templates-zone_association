from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from pathlib import Path
import os
import sys
import traceback
import subprocess

# Try to close any existing Edge processes
def kill_edge_processes():
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'msedge.exe'], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            subprocess.run(['taskkill', '/f', '/im', 'msedgedriver.exe'], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            print("Edge processes closed successfully")
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'msedge'], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            print("Edge processes closed successfully")
    except Exception as e:
        print(f"Could not close Edge processes: {e}")

# Environment variables configuration
ENV_URL = ""
ENV_USER = ""
ENV_PASS = ""

# Try to read from .env file
try:
    # Look for .env file in parent directory
    env_path = Path(__file__).parents[1] / ".env"
    
    if env_path.exists():
        with open(env_path.as_posix(), "rt", encoding="utf-8") as file:
            for line in file:
                if line.startswith("ENV_URL="):
                    ENV_URL=line.split("=")[1].replace("\n", "").strip("\"")
                elif line.startswith("ENV_USER="):
                    ENV_USER=line.split("=")[1].replace("\n", "").strip("\"")
                elif line.startswith("ENV_PASS="):
                    ENV_PASS=line.split("=")[1].replace("\n", "").strip("\"")
    else:
        raise FileNotFoundError(".env file not found")
        
except Exception as e:
    print(f"Error reading .env file: {e}")
    print("Please verify the .env file is in the same directory as the bat file.")
    input("Press Enter to exit...")
    sys.exit(1)

print(f"URL: {ENV_URL}")
print(f"Username: {ENV_USER}")
print(f"Password: {'*' * len(ENV_PASS)}")  # Hide password in output

# Edge browser configuration
try:
    # Try to close any existing Edge processes
    kill_edge_processes()
    
    # Configure Edge options
    edge_options = Options()
    edge_options.add_argument("--start-maximized") # Maximize window
    edge_options.add_argument("--no-first-run") # Skip first run (Edge will not show the first run page)
    edge_options.add_argument("--no-default-browser-check") # Skip default browser check (Edge will not show the default browser check page)
    edge_options.add_argument("--disable-extensions") # Disable extensions (Edge will not show the extensions page)
    edge_options.add_argument("--disable-popup-blocking") # Disable popup blocking (Edge will not block popups)
    edge_options.add_argument("--disable-blink-features=AutomationControlled") # Disable blink features (Edge will not show the automation control page)
    
    # Initialize Edge driver
    print("Starting Edge browser...")
    driver = webdriver.Edge(options=edge_options)
    wait = WebDriverWait(driver, 20)
    wait_fast = WebDriverWait(driver, 3)
    
    # Go to environment url
    driver.get(ENV_URL)
except Exception as e:
    print(f"Error initializing browser: {e}")
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)


def write_html_in_file(html: str | list):
    """Writes HTML content to a file named 'source.html'.

    Args:
        html (str | list): The HTML content to be written. It can be a string or a list of strings.
    """
    try:
        output_path = Path(__file__).parents[1] / "source.html"
        with open(output_path.as_posix(), mode="wt", encoding="utf-8") as out:
            out.writelines(html)
    except Exception as e:
        print(f"Error writing HTML file: {e}")


try:
    # * LOGIN
    # Go to content frame -> results frame (login)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"i2ui_shell_content")))
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"results")))
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='loginUser']"))
    ).send_keys(ENV_USER)
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='dspLoginPassword']"))
    ).send_keys(ENV_PASS)
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"loginBox\"]/span[1]/span"))
    ).click()

    # * GO TO ZONE LOCATION
    # Go to default frame (top frame) -> i2ui_shell_content frame -> nav frame (navigation)
    driver.switch_to.default_content() # n: frame default
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"i2ui_shell_content"))) # n: i2ui_shell_content
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"nav"))) # n: nav

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#TREECELL_navigation_1 > a"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#TREECELL_navigation_1_2 > a"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#TREECELL_navigation_1_2_1 > a:nth-child(2)"))).click()

    # Go to default frame (top frame) -> i2ui_shell_content frame -> results frame
    driver.switch_to.parent_frame() # n: i2ui_shell_content
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"results"))) # n: results

    # Find the zone_location.csv file in parent directory
    zone_location_path = Path(__file__).parents[1] / "zone_location.csv"
    
    if not zone_location_path.exists():
        print("Error: zone_location.csv file not found")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"zone_location.csv file found at: {zone_location_path}")
    
    # Create path for temporary file
    temp_zone_location_path = Path(__file__).parents[1] / "temp_zone_location.csv"

    with open(zone_location_path.as_posix(), "rt", encoding="utf-8") as file, open(temp_zone_location_path.as_posix(), "wt", encoding="utf-8") as temp_file:
        for line in file:
            try:
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"input[value='{line.split(',')[0]}']"))).click()
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='GEO_AREAS_']"))).click()
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='LOCATION_ASSOCIATION_']"))).click()
                # Write the location id
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='locationID']"))).send_keys(line.split(",")[1])
                # Select the location type DC for all associations
                select=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#locationType_options")))
                select=Select(select)
                select.select_by_value("DC")
                
                # Click on submit
                submit_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='javascript:submitSubmit (document.GeoAreaForm);']")))
                actions = ActionChains(driver)
                actions.move_to_element(submit_button).pause(0.7).click().perform()

                # Get text from the element
                driver.switch_to.parent_frame() # n: i2ui_shell_content
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"results"))) # n: results

                write_html_in_file(driver.page_source)
                try:
                    wait_fast.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.success")))
                    temp_file.write(f"{line[0:len(line)-1]},TRUE\n")
                except:
                    temp_file.write(f"{line[0:len(line)-1]},FALSE\n")
                
                # Go to default frame (top frame) -> i2ui_shell_content frame -> results frame
                driver.switch_to.default_content() # n: frame default
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"i2ui_shell_content"))) # n: i2ui_shell_content
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"nav"))) # n: nav
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#TREECELL_navigation_1_2_1 > a:nth-child(2)"))).click()
                driver.switch_to.parent_frame() # n: i2ui_shell_content
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"results"))) # n: results
            except Exception as e:
                print(f"Error processing line {line}: {e}")
                temp_file.write(f"{line[0:len(line)-1]},ERROR\n")
except Exception as e:
    print(f"Error during execution: {e}")
    traceback.print_exc()
finally:
    print("Process completed. Closing browser...")
    try:
        driver.quit()
    except:
        pass
