#!/usr/bin/env python3
"""
Nexus Maximus Test Suite
Comprehensive testing of the enhanced streaming system
"""

import sys
import os
import unittest
import tempfile
import yaml
from unittest.mock import Mock, patch, MagicMock

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import nexus_maximus
    from nexus_maximus import NexusConfig, ProxyManager, BehaviorSimulator, StreamWindow, ResourceMonitor, NexusMaximus
except ImportError as e:
    print(f"❌ Failed to import nexus_maximus: {e}")
    sys.exit(1)

class TestNexusConfig(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        self.test_config = {
            'streaming': {
                'youtube': {
                    'url': 'https://youtube.com/test',
                    'count': 5,
                    'enabled': True
                }
            },
            'proxy': {
                'enabled': False,
                'file': 'test_proxies.txt'
            }
        }
        
        # Create temporary config file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(self.test_config, self.temp_file)
        self.temp_file.close()
        
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_config_loading(self):
        """Test configuration file loading"""
        config = NexusConfig(self.temp_file.name)
        self.assertIsNotNone(config.config)
        self.assertEqual(config.get('streaming.youtube.url'), 'https://youtube.com/test')
        
    def test_nested_config_access(self):
        """Test nested configuration access"""
        config = NexusConfig(self.temp_file.name)
        self.assertEqual(config.get('streaming.youtube.count'), 5)
        self.assertEqual(config.get('nonexistent.key', 'default'), 'default')

class TestProxyManager(unittest.TestCase):
    """Test proxy management"""
    
    def setUp(self):
        self.config = Mock()
        self.config.get.side_effect = lambda key, default=None: {
            'proxy.file': 'test_proxies.txt',
            'proxy.geo_filtering.enabled': False,
            'proxy.geo_filtering.countries': []
        }.get(key, default)
        
        # Create temporary proxy file
        self.temp_proxy_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_proxy_file.write("127.0.0.1:8080\n")
        self.temp_proxy_file.write("127.0.0.1:8081\n")
        self.temp_proxy_file.close()
        
        # Update config to use our temp file
        self.config.get.side_effect = lambda key, default=None: {
            'proxy.file': self.temp_proxy_file.name,
            'proxy.geo_filtering.enabled': False,
            'proxy.geo_filtering.countries': []
        }.get(key, default)
        
    def tearDown(self):
        os.unlink(self.temp_proxy_file.name)
    
    def test_proxy_loading(self):
        """Test proxy file loading"""
        proxy_manager = ProxyManager(self.config)
        self.assertEqual(len(proxy_manager.proxies), 2)
        self.assertIn("127.0.0.1:8080", proxy_manager.proxies)
        
    def test_proxy_rotation(self):
        """Test proxy rotation"""
        proxy_manager = ProxyManager(self.config)
        proxy1 = proxy_manager.get_proxy()
        proxy2 = proxy_manager.get_proxy()
        self.assertNotEqual(proxy1, proxy2)

class TestBehaviorSimulator(unittest.TestCase):
    """Test human behavior simulation"""
    
    def setUp(self):
        self.config = Mock()
        self.config.get.side_effect = lambda key, default=None: {
            'behavior.human_simulation': True,
            'behavior.mouse_movements': True,
            'behavior.scroll_simulation': True,
            'behavior.click_simulation': True
        }.get(key, default)
        
    def test_behavior_simulator_init(self):
        """Test behavior simulator initialization"""
        simulator = BehaviorSimulator(self.config)
        self.assertIsNotNone(simulator.user_agent)
        
    @patch('nexus_maximus.Page')
    def test_simulate_mouse_movements(self, mock_page):
        """Test mouse movement simulation"""
        simulator = BehaviorSimulator(self.config)
        mock_page.mouse = Mock()
        
        simulator.simulate_mouse_movements(mock_page)
        self.assertTrue(mock_page.mouse.move.called)

class TestResourceMonitor(unittest.TestCase):
    """Test resource monitoring"""
    
    def setUp(self):
        self.config = Mock()
        self.config.get.side_effect = lambda key, default=None: {
            'system.cpu_threshold': 85,
            'system.memory_threshold': 85
        }.get(key, default)
        
    @patch('nexus_maximus.psutil')
    def test_resource_check_pass(self, mock_psutil):
        """Test resource check when within limits"""
        mock_psutil.cpu_percent.return_value = 50
        mock_psutil.virtual_memory.return_value = Mock(percent=60)
        
        monitor = ResourceMonitor(self.config)
        self.assertTrue(monitor.check_resources())
        
    @patch('nexus_maximus.psutil')
    def test_resource_check_fail(self, mock_psutil):
        """Test resource check when exceeding limits"""
        mock_psutil.cpu_percent.return_value = 90
        mock_psutil.virtual_memory.return_value = Mock(percent=60)
        
        monitor = ResourceMonitor(self.config)
        self.assertFalse(monitor.check_resources())

class TestNexusMaximus(unittest.TestCase):
    """Test main Nexus Maximus controller"""
    
    def setUp(self):
        # Create a test config file
        self.test_config = {
            'streaming': {
                'youtube': {
                    'url': 'https://youtube.com/test',
                    'count': 1,
                    'enabled': True
                },
                'twitch': {
                    'url': 'https://twitch.tv/test',
                    'count': 0,
                    'enabled': False
                }
            }
        }
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(self.test_config, self.temp_file)
        self.temp_file.close()
        
    def tearDown(self):
        os.unlink(self.temp_file.name)
        
    def test_get_enabled_platforms(self):
        """Test platform filtering"""
        nexus = NexusMaximus(self.temp_file.name)
        platforms = nexus.get_enabled_platforms()
        
        self.assertEqual(len(platforms), 1)
        self.assertEqual(platforms[0][0], 'Youtube')
        self.assertEqual(platforms[0][2], 1)

def run_validation_tests():
    """Run validation tests for core components"""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              Nexus Maximus Test Suite                           ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Run unit tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestNexusConfig,
        TestProxyManager,
        TestBehaviorSimulator,
        TestResourceMonitor,
        TestNexusMaximus
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    if result.wasSuccessful():
        print("🎉 All tests passed! Nexus Maximus core functionality validated.")
        return True
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False

def test_configuration_validation():
    """Test configuration file validation"""
    print("\n📋 Testing configuration validation...")
    
    try:
        # Test main config
        if os.path.exists('nexus_config.yaml'):
            config = NexusConfig('nexus_config.yaml')
            platforms = []
            for platform in ['youtube', 'twitch', 'kick']:
                if config.get(f'streaming.{platform}.enabled', False):
                    platforms.append(platform)
            
            print(f"✅ Configuration loaded successfully")
            print(f"   Enabled platforms: {platforms}")
            
        # Test proxy file
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                proxy_count = sum(1 for line in f if line.strip())
            print(f"✅ Proxy file loaded: {proxy_count} proxies available")
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def main():
    """Main test execution"""
    all_passed = True
    
    # Run unit tests
    all_passed &= run_validation_tests()
    
    # Test configuration
    all_passed &= test_configuration_validation()
    
    print("\n" + "="*70)
    if all_passed:
        print("🎯 All tests passed! Nexus Maximus is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())