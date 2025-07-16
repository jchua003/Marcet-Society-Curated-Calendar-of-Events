from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Testing real Google Chrome...")

try:
    # Configure Chrome options for Codespaces
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--single-process')
    options.add_argument('--remote-debugging-port=9222')
    
    # Use the real Chrome binary
    options.binary_location = '/usr/bin/google-chrome'
    
    print("📥 Setting up ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    print("🌐 Creating Chrome driver...")
    driver = webdriver.Chrome(service=service, options=options)
    
    print("🧪 Testing Google...")
    driver.get('https://www.google.com')
    print(f"✅ SUCCESS! Page title: {driver.title}")
    
    print("🧪 Testing Met Museum...")
    driver.get('https://www.metmuseum.org')
    print(f"✅ SUCCESS! Page title: {driver.title}")
    
    driver.quit()
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

