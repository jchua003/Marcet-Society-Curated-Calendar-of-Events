from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Testing stable Chrome setup...")

try:
    # More robust Chrome options for containers
    options = Options()
    options.add_argument('--headless=new')  # Use new headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--disable-oopr-debug-crash-dump')
    options.add_argument('--no-crash-upload')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu-sandbox')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-background-media')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions-file-access-check')
    options.add_argument('--disable-extensions-http-throttling')
    options.add_argument('--disable-extensions-https-throttling')
    options.add_argument('--disable-gpu-watchdog')
    options.add_argument('--disable-hang-monitor')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-prompt-on-repost')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-pings')
    options.add_argument('--no-zygote')
    options.add_argument('--password-store=basic')
    options.add_argument('--use-mock-keychain')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--user-data-dir=/tmp/chrome-user-data')
    options.add_argument('--disable-ipc-flooding-protection')
    
    # Set user agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Use the installed Chrome binary
    options.binary_location = '/usr/bin/google-chrome'
    
    print("📥 Setting up ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    print("🌐 Creating Chrome driver...")
    driver = webdriver.Chrome(service=service, options=options)
    
    # Set timeouts
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    
    print("🧪 Testing Google...")
    driver.get('https://www.google.com')
    time.sleep(2)
    print(f"✅ SUCCESS! Page title: {driver.title}")
    
    print("🧪 Testing simple HTML...")
    driver.get('data:text/html,<html><head><title>Test</title></head><body><h1>Hello World</h1></body></html>')
    time.sleep(1)
    print(f"✅ SUCCESS! Simple HTML title: {driver.title}")
    
    driver.quit()
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

