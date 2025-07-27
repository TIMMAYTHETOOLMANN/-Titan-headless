#!/usr/bin/env python3
"""
Enhanced StreamBoost Wrapper - Integrates 15 JARVIS enhancements
Maintains compatibility with existing streamboost.py while adding enhancements
"""

import sys
import os
from pathlib import Path

# Import enhanced system
try:
    from enhanced_nexus import EnhancedNexusMaximus
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False
    print("⚠️  Enhanced Nexus not available, falling back to standard mode")

# Import original streamboost
try:
    from streamboost import StreamBoostController
    ORIGINAL_AVAILABLE = True
except ImportError:
    ORIGINAL_AVAILABLE = False

def main():
    """Enhanced StreamBoost with fallback compatibility"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    Enhanced StreamBoost v3.0                        ║
║                  JARVIS NEXUS Protocol Active                        ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Use enhanced system if available
    if ENHANCED_AVAILABLE:
        print("🚀 Launching Enhanced Nexus with 15 JARVIS enhancements...")
        try:
            enhanced_system = EnhancedNexusMaximus("enhanced_nexus_config.yaml")
            enhanced_system.run()
            return
        except FileNotFoundError:
            print("⚠️  enhanced_nexus_config.yaml not found, trying nexus_config.yaml...")
            try:
                enhanced_system = EnhancedNexusMaximus("nexus_config.yaml")
                enhanced_system.run()
                return
            except Exception as e:
                print(f"❌ Enhanced system failed: {e}")
                print("🔄 Falling back to original system...")
    
    # Fallback to original system
    if ORIGINAL_AVAILABLE:
        print("🔄 Launching original StreamBoost system...")
        import asyncio
        from streamboost import main as original_main
        asyncio.run(original_main())
    else:
        print("❌ No StreamBoost system available")
        sys.exit(1)

if __name__ == "__main__":
    main()
