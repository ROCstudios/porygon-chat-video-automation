import os
from image_gen import ASSETS_DIR, verify_assets

def check_setup():
    print(f"Checking setup...")
    print(f"Assets directory: {ASSETS_DIR}")
    
    try:
        verify_assets()
        print("✅ Setup check passed!")
    except Exception as e:
        print(f"❌ Setup check failed: {str(e)}")

if __name__ == "__main__":
    check_setup()
