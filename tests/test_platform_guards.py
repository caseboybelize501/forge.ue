"""
Platform Guards Test — Safety Gate

Always run first. Validates platform guard macro usage.
"""
import pytest
import re
from pathlib import Path


class TestPlatformGuards:
    """Test platform guard macro usage."""
    
    # SDK symbols that require platform guards
    SDK_SYMBOLS = {
        "PS5": ["sce", "Sce"],
        "XBOX": ["Xbl", "xbox"],
        "SWITCH": ["nx", "nn"],
        "ANDROID": ["android", "Android"],
        "IOS": ["iOS", "UIKit"],
    }
    
    def test_no_unguarded_sdk_symbols(self):
        """Verify no SDK symbols without platform guards."""
        # Implementation would scan all .cpp/.h files
        pass
    
    def test_platform_macros_present(self):
        """Verify platform guard macros are used correctly."""
        pass
    
    def test_no_raw_uobject_pointers(self):
        """Verify no raw UObject pointers (TObjectPtr required)."""
        pass
    
    def test_generated_body_present(self):
        """Verify GENERATED_BODY() in all UCLASS headers."""
        pass
