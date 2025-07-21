from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Testing webdriver-manager approach...")

try:
    # Configure Chrome options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    
    # Use webdriver-manager to handle Chrome installation
    print("📥 Installing/updating ChromeDriver...")
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

