#!/usr/bin/env python3

print("Testing scraper setup...")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print("✅ Selenium imported successfully")
    
    # Create options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    print("🔧 Creating Chrome driver...")
    
    # Simple driver creation
    driver = webdriver.Chrome(options=options)
    
    print("🌐 Testing Google...")
    driver.get('https://www.google.com')
    print(f"✅ Success! Page title: {driver.title}")
    
    driver.quit()
    print("✅ Test completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install selenium webdriver-manager")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Let's try a different approach...")
    
    # Try alternative approach
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        print("🔧 Trying webdriver-manager approach...")
        
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://www.google.com')
        print(f"✅ Alternative approach works! Page title: {driver.title}")
        driver.quit()
        
    except Exception as e2:
        print(f"❌ Alternative also failed: {e2}")
        print("Let's check system setup...")
        
        import subprocess
        import os
        
        # Check Chrome installation
        try:
            result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
            print(f"Chrome version: {result.stdout.strip()}")
        except:
            print("❌ Chrome not found")
        
        # Check ChromeDriver
        try:
            result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
            print(f"ChromeDriver version: {result.stdout.strip()}")
        except:
            print("❌ ChromeDriver not found")
        
        # Check if files exist
        chrome_paths = ['/usr/bin/google-chrome', '/usr/bin/chromium-browser', '/usr/bin/chrome']
        driver_paths = ['/usr/bin/chromedriver', '/usr/local/bin/chromedriver']
        
        print("\n📁 Checking file locations:")
        for path in chrome_paths + driver_paths:
            if os.path.exists(path):
                print(f"✅ Found: {path}")
            else:
                print(f"❌ Missing: {path}")

