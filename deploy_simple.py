import subprocess
import os
from datetime import datetime

def simple_deploy():
    print("🚀 Simple deployment to GitHub Pages...")
    
    # Check if frontend builds
    print("🧪 Testing React build...")
    try:
        result = subprocess.run(['npm', 'run', 'build'], 
                              cwd='frontend', 
                              capture_output=True, 
                              text=True, 
                              timeout=120)
        
        if result.returncode != 0:
            print(f"❌ Build failed: {result.stderr}")
            return False
        
        print("✅ React build successful!")
        
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
    
    # Git add, commit, push
    try:
        print("📦 Adding changes to git...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        print("💾 Committing changes...")
        commit_msg = f"🎯 Clean deployment - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        print("🚀 Pushing to GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("🌐 Your site will be live in 2-3 minutes at:")
        print("   https://jchua003.github.io/Marcet-Society-Curated-Calendar-of-Events")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

if __name__ == "__main__":
    simple_deploy()

