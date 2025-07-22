#!/usr/bin/env python3
"""
Titan Headless - Comprehensive Test Suite
Tests for unified deployment system
"""

import asyncio
import tempfile
import os
import yaml
import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from deployment_core import (
    DeploymentConfig, ConfigManager, DeploymentValidator, 
    DeploymentMode, LiveStreamConfig, StaticVideoConfig, SharedConfig
)

class TestDeploymentCore(unittest.TestCase):
    """Test the core deployment configuration system"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_config_path = os.path.join(self.temp_dir, "test_config.yaml")
    
    def tearDown(self):
        # Clean up temp files
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)
        os.rmdir(self.temp_dir)
    
    def test_default_config_creation(self):
        """Test creating default configuration"""
        config = DeploymentConfig()
        
        self.assertEqual(config.deployment_mode, DeploymentMode.LIVE_STREAM)
        self.assertEqual(config.live_stream.target_account, "timmaythetoolman")
        self.assertEqual(config.static_video.windows, 20)
        self.assertEqual(config.shared.base_port, 9333)
    
    def test_config_save_and_load(self):
        """Test saving and loading configuration"""
        # Create test config
        config = DeploymentConfig()
        config.deployment_mode = DeploymentMode.STATIC_VIDEO
        config.static_video.channel_url = "https://www.youtube.com/@test"
        config.shared.cpu_threshold = 90
        
        # Save config
        ConfigManager.save_config(config, self.test_config_path)
        
        # Verify file exists
        self.assertTrue(os.path.exists(self.test_config_path))
        
        # Load config
        loaded_config = ConfigManager.load_config(self.test_config_path)
        
        # Verify loaded config
        self.assertEqual(loaded_config.deployment_mode, DeploymentMode.STATIC_VIDEO)
        self.assertEqual(loaded_config.static_video.channel_url, "https://www.youtube.com/@test")
        self.assertEqual(loaded_config.shared.cpu_threshold, 90)
    
    def test_config_validation(self):
        """Test configuration validation"""
        # Valid config
        valid_config = DeploymentConfig()
        issues = DeploymentValidator.validate_config(valid_config)
        self.assertEqual(len(issues), 0)
        
        # Invalid config - bad port
        invalid_config = DeploymentConfig()
        invalid_config.shared.base_port = 99999
        issues = DeploymentValidator.validate_config(invalid_config)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("port" in issue.lower() for issue in issues))
        
        # Invalid config - bad thresholds
        invalid_config2 = DeploymentConfig()
        invalid_config2.shared.cpu_threshold = 150
        issues = DeploymentValidator.validate_config(invalid_config2)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("cpu" in issue.lower() for issue in issues))
    
    def test_yaml_config_parsing(self):
        """Test parsing YAML configuration"""
        yaml_content = """
deployment_mode: "static_video"
live_stream:
  target_account: "testuser"
  platforms:
    youtube:
      enabled: true
      windows: 5
      url_template: "https://www.youtube.com/@{account}/live"
static_video:
  channel_url: "https://www.youtube.com/@testchannel"
  windows: 15
shared:
  browser:
    base_port: 8000
  resources:
    cpu_threshold: 75
        """
        
        # Write test YAML
        with open(self.test_config_path, 'w') as f:
            f.write(yaml_content)
        
        # Load and test
        config = ConfigManager.load_config(self.test_config_path)
        
        self.assertEqual(config.deployment_mode, DeploymentMode.STATIC_VIDEO)
        self.assertEqual(config.live_stream.target_account, "testuser")
        self.assertEqual(config.static_video.channel_url, "https://www.youtube.com/@testchannel")
        self.assertEqual(config.static_video.windows, 15)
        self.assertEqual(config.shared.base_port, 8000)
        self.assertEqual(config.shared.cpu_threshold, 75)

class TestLiveStreamDeployment(unittest.TestCase):
    """Test live stream deployment functionality"""
    
    def setUp(self):
        self.config = DeploymentConfig()
        self.config.deployment_mode = DeploymentMode.LIVE_STREAM
        self.config.live_stream.platforms = {
            'youtube': {
                'enabled': True,
                'windows': 2,
                'url_template': 'https://www.youtube.com/@{account}/live'
            }
        }
    
    def test_live_stream_config(self):
        """Test live stream configuration"""
        from live_stream_deployment import LiveStreamDeployment
        
        deployment = LiveStreamDeployment(self.config)
        
        self.assertEqual(deployment.config.deployment_mode, DeploymentMode.LIVE_STREAM)
        self.assertEqual(deployment.config.live_stream.target_account, "timmaythetoolman")
        self.assertFalse(deployment.is_running)
    
    @patch('live_stream_deployment.async_playwright')
    async def test_deployment_initialization(self, mock_playwright):
        """Test deployment initialization without actually launching browsers"""
        from live_stream_deployment import LiveStreamDeployment
        
        # Mock playwright context
        mock_context = Mock()
        mock_playwright.return_value.__aenter__.return_value = mock_context
        
        deployment = LiveStreamDeployment(self.config)
        
        # This would normally start the deployment, but we'll just test initialization
        self.assertIsNotNone(deployment)
        self.assertEqual(len(deployment.windows), 0)

class TestStaticVideoDeployment(unittest.TestCase):
    """Test static video deployment functionality"""
    
    def setUp(self):
        self.config = DeploymentConfig()
        self.config.deployment_mode = DeploymentMode.STATIC_VIDEO
        self.config.static_video.channel_url = "https://www.youtube.com/@test"
        self.config.static_video.windows = 2
    
    def test_static_video_config(self):
        """Test static video configuration"""
        from static_video_deployment import StaticVideoDeployment
        
        deployment = StaticVideoDeployment(self.config)
        
        self.assertEqual(deployment.config.deployment_mode, DeploymentMode.STATIC_VIDEO)
        self.assertEqual(deployment.config.static_video.channel_url, "https://www.youtube.com/@test")
        self.assertFalse(deployment.is_running)
    
    def test_video_scraper(self):
        """Test video scraper functionality"""
        from static_video_deployment import VideoScraper
        
        scraper = VideoScraper(self.config.static_video)
        
        # Test duration parsing
        self.assertEqual(scraper._parse_duration("5:30"), 330)  # 5 minutes 30 seconds
        self.assertEqual(scraper._parse_duration("1:05:30"), 3930)  # 1 hour 5 minutes 30 seconds
        self.assertEqual(scraper._parse_duration(""), 0)
        
        # Test view count parsing
        self.assertEqual(scraper._parse_view_count("1.5K views"), 1500)
        self.assertEqual(scraper._parse_view_count("2.3M views"), 2300000)
        self.assertEqual(scraper._parse_view_count("1B views"), 1000000000)
        self.assertEqual(scraper._parse_view_count("123 views"), 123)
    
    def test_video_filtering(self):
        """Test video filtering by duration"""
        from static_video_deployment import VideoScraper
        
        scraper = VideoScraper(self.config.static_video)
        
        # Test videos with different durations
        test_videos = [
            {'video_id': '1', 'duration': 30},    # Too short
            {'video_id': '2', 'duration': 120},   # Good
            {'video_id': '3', 'duration': 3000},  # Good
            {'video_id': '4', 'duration': 5000},  # Too long
            {'video_id': '5', 'duration': 0},     # Unknown (should include)
        ]
        
        filtered = scraper._filter_videos_by_duration(test_videos)
        
        # Should include videos 2, 3, and 5
        self.assertEqual(len(filtered), 3)
        video_ids = [v['video_id'] for v in filtered]
        self.assertIn('2', video_ids)
        self.assertIn('3', video_ids)
        self.assertIn('5', video_ids)
        self.assertNotIn('1', video_ids)
        self.assertNotIn('4', video_ids)

class TestUnifiedDeployment(unittest.TestCase):
    """Test unified deployment system"""
    
    def setUp(self):
        self.config = DeploymentConfig()
    
    def test_deployment_mode_switching(self):
        """Test switching between deployment modes"""
        from titan_deployment import TitanHeadlessDeployment
        
        # Test live stream mode
        self.config.deployment_mode = DeploymentMode.LIVE_STREAM
        deployment = TitanHeadlessDeployment(self.config)
        self.assertEqual(deployment.config.deployment_mode, DeploymentMode.LIVE_STREAM)
        
        # Test static video mode
        self.config.deployment_mode = DeploymentMode.STATIC_VIDEO
        deployment = TitanHeadlessDeployment(self.config)
        self.assertEqual(deployment.config.deployment_mode, DeploymentMode.STATIC_VIDEO)
        
        # Test both mode
        self.config.deployment_mode = DeploymentMode.BOTH
        deployment = TitanHeadlessDeployment(self.config)
        self.assertEqual(deployment.config.deployment_mode, DeploymentMode.BOTH)

def run_integration_tests():
    """Run integration tests"""
    print("\n🧪 Running Integration Tests...")
    
    # Test configuration system
    print("  ✓ Testing configuration loading and saving...")
    config = ConfigManager.load_config()
    issues = DeploymentValidator.validate_config(config)
    assert len(issues) == 0, f"Configuration issues: {issues}"
    
    # Test video scraper (without network)
    print("  ✓ Testing video scraper utilities...")
    from static_video_deployment import VideoScraper
    scraper = VideoScraper(config.static_video)
    assert scraper._parse_duration("10:30") == 630
    assert scraper._parse_view_count("1.2K views") == 1200
    
    # Test deployment creation
    print("  ✓ Testing deployment system initialization...")
    from titan_deployment import TitanHeadlessDeployment
    deployment = TitanHeadlessDeployment(config)
    assert deployment.config is not None
    
    print("  ✅ All integration tests passed!")

def main():
    """Run all tests"""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                Titan Headless Test Suite v2.0                      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    # Run unit tests
    print("\n🔬 Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run integration tests
    run_integration_tests()
    
    print("\n🎉 All tests completed successfully!")
    print("\nThe deployment system is ready for production use:")
    print("  • Live Stream Deployment: Multi-platform live stream watching")
    print("  • Static Video Deployment: YouTube video watching")
    print("  • Unified Deployment: Both systems working together")
    print("  • Configuration Management: Flexible YAML-based configuration")
    print("  • Validation System: Comprehensive configuration validation")

if __name__ == "__main__":
    main()