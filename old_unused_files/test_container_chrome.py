from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Testing container-friendly Chrome setup...")

try:
    # Configure Chrome options for containers
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-client-side-phishing-detection')
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--disable-oopr-debug-crash-dump')
    options.add_argument('--no-crash-upload')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu-sandbox')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-network-service-logging')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-prompt-on-repost')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-windows10-custom-titlebar')
    options.add_argument('--force-color-profile=srgb')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-pings')
    options.add_argument('--no-zygote')
    options.add_argument('--password-store=basic')
    options.add_argument('--use-mock-keychain')
    options.add_argument('--single-process')
    options.add_argument('--remote-debugging-port=9222')
    
    print("📥 Installing ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    print("🌐 Creating Chrome driver...")
    driver = webdriver.Chrome(service=service, options=options)
    
    print("🧪 Testing Google...")
    driver.get('https://www.google.com')
    print(f"✅ SUCCESS! Page title: {driver.title}")
    
    driver.quit()
    print("✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

