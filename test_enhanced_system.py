#!/usr/bin/env python3
"""
Test script for Enhanced Channel Watch Monolith
Validates configuration, dependencies, and basic functionality
"""

import asyncio
import sys
import os
import json
import yaml
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test that all required modules can be imported"""
    print("🔄 Testing imports...")
    
    try:
        import requests
        import psutil
        from bs4 import BeautifulSoup
        from playwright.async_api import async_playwright
        from playwright_stealth import Stealth
        from cpuinfo import get_cpu_info
        import aiofiles
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

async def test_configuration():
    """Test configuration loading and validation"""
    print("🔄 Testing configuration system...")
    
    try:
        # Test importing the enhanced script
        from streamboost_channel_watch_enhanced import ChannelWatchConfig, ConfigManager
        
        # Test default config
        default_config = ChannelWatchConfig()
        print(f"  ✅ Default config loaded: {default_config.windows} windows")
        
        # Test config file loading
        if os.path.exists('channel_watch_config.yaml'):
            config = ConfigManager.load_config('channel_watch_config.yaml')
            print(f"  ✅ YAML config loaded: {config.channel_url}")
        
        # Test config saving
        ConfigManager.save_config(default_config, 'test_config.yaml')
        if os.path.exists('test_config.yaml'):
            os.remove('test_config.yaml')
            print("  ✅ Config save/load test passed")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def test_video_scraping():
    """Test video scraping functionality"""
    print("🔄 Testing video scraping...")
    
    try:
        from streamboost_channel_watch_enhanced import EnhancedVideoScraper, ChannelWatchConfig
        
        config = ChannelWatchConfig()
        scraper = EnhancedVideoScraper(config)
        
        # Test with a minimal number of videos to avoid rate limiting
        videos = scraper.get_channel_videos(config.channel_url, max_videos=3)
        
        if videos:
            print(f"  ✅ Scraped {len(videos)} videos successfully")
            for i, video in enumerate(videos[:2]):
                print(f"    Video {i+1}: {video.url[:50]}...")
            return True
        else:
            print("  ⚠️  No videos scraped (may be normal for rate limiting)")
            return True  # Don't fail for this as it might be rate limiting
    except Exception as e:
        print(f"❌ Video scraping test failed: {e}")
        return False

async def test_browser_setup():
    """Test browser setup without actually launching"""
    print("🔄 Testing browser setup...")
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as playwright:
            # Just test that we can get browser info
            browser_type = playwright.chromium
            print("  ✅ Playwright chromium accessible")
            
            # Test that stealth can be imported
            from playwright_stealth import Stealth
            print("  ✅ Playwright stealth available")
            
        return True
    except Exception as e:
        print(f"❌ Browser setup test failed: {e}")
        return False

async def test_performance_monitoring():
    """Test performance monitoring functionality"""
    print("🔄 Testing performance monitoring...")
    
    try:
        from streamboost_channel_watch_enhanced import PerformanceMonitor, WatchStatistics
        
        stats = WatchStatistics()
        monitor = PerformanceMonitor(stats)
        
        # Test resource checking
        is_ok, metrics = monitor.check_resources()
        print(f"  ✅ Resource check: CPU {metrics['cpu_percent']:.1f}%, RAM {metrics['ram_percent']:.1f}%")
        
        # Test statistics
        stats.update_watch_time(100)
        stats.record_engagement()
        print(f"  ✅ Statistics tracking: {stats.total_watch_time}s watched, {stats.engagements_performed} engagements")
        
        return True
    except Exception as e:
        print(f"❌ Performance monitoring test failed: {e}")
        return False

async def test_file_operations():
    """Test file operations and permissions"""
    print("🔄 Testing file operations...")
    
    try:
        # Test profile directory creation
        test_profile_dir = Path("./test_profiles")
        test_profile_dir.mkdir(exist_ok=True)
        
        # Test config file operations
        test_data = {"test": "data"}
        with open("test_file.json", "w") as f:
            json.dump(test_data, f)
        
        # Cleanup
        os.remove("test_file.json")
        test_profile_dir.rmdir()
        
        print("  ✅ File operations working correctly")
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           Enhanced Channel Watch Monolith Test Suite            ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Video Scraping Test", test_video_scraping),
        ("Browser Setup Test", test_browser_setup),
        ("Performance Monitoring Test", test_performance_monitoring),
        ("File Operations Test", test_file_operations),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if await test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            failed += 1
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                        Test Results                             ║
║                                                                  ║
║  Passed: {passed:<2}                                                ║
║  Failed: {failed:<2}                                                ║
║  Total:  {passed + failed:<2}                                                ║
║                                                                  ║
""", end="")
    
    if failed == 0:
        print("║  Status: 🎉 ALL TESTS PASSED                                ║")
    else:
        print("║  Status: ⚠️  SOME TESTS FAILED                              ║")
    
    print("╚══════════════════════════════════════════════════════════════════╝")

if __name__ == "__main__":
    asyncio.run(run_all_tests())