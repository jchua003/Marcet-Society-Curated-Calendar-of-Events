import subprocess
from datetime import datetime

# Simple, reliable deployment
try:
    # Build the frontend
    print("🔨 Building React app...")
    subprocess.run(['npm', 'run', 'build'], cwd='frontend', check=True)
    
    # Git operations
    print("📦 Deploying to GitHub...")
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', f'🎨 Deploy categorized UI - {datetime.now().strftime("%Y-%m-%d %H:%M")}'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    
    print("✅ SUCCESS! Your site is deploying...")
    print("🌐 Live in 2-3 minutes: https://jchua003.github.io/Marcet-Society-Curated-Calendar-of-Events")
    
except Exception as e:
    print(f"❌ Error: {e}")

