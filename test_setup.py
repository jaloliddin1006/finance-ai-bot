"""
Test script to verify setup
"""
import os
import sys


def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    # Set dummy environment variables
    os.environ['BOT_TOKEN'] = 'test_token'
    os.environ['DB_PASSWORD'] = 'test_pass'
    os.environ['GEMINI_API_KEY'] = 'test_key'
    
    try:
        from app.models import User
        print("✓ Models module")
        
        from app.handlers import setup_routers
        print("✓ Handlers module")
        
        from app.services import gemini_service
        print("✓ Services module")
        
        from config import settings
        print("✓ Config module")
        
        from config.database import TORTOISE_ORM
        print("✓ Database configuration")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_models():
    """Test model structure"""
    print("\nTesting models...")
    
    try:
        from app.models import User
        
        # Check if User has required fields
        required_fields = ['telegram_id', 'username', 'first_name', 'last_name']
        model_fields = User._meta.fields_map.keys()
        
        for field in required_fields:
            if field in model_fields:
                print(f"✓ User.{field}")
            else:
                print(f"✗ User.{field} missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False


def test_configuration():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from config import settings
        
        # Check if settings has required attributes
        required_attrs = ['bot_token', 'db_password', 'gemini_api_key', 'database_url']
        
        for attr in required_attrs:
            if hasattr(settings, attr):
                print(f"✓ settings.{attr}")
            else:
                print(f"✗ settings.{attr} missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def main():
    """Main test function"""
    print("=" * 50)
    print("Finance AI Bot - Setup Verification")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Models", test_models),
        ("Configuration", test_configuration),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 All tests passed! Setup is correct.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
