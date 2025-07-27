#!/usr/bin/env python3
"""
Enhanced Nexus Test Suite - Validates all 15 enhancements
JARVIS NEXUS Enhancement Protocol Validation
"""

import unittest
import sys
import os
import time
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Add the enhanced_nexus module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from enhanced_nexus import (
        DynamicWatchDuration, AdvancedMousePatterns, IntelligentEngagement,
        VideoInteractionTiming, SessionPersistence, AdaptiveFailover,
        GeoDistributedRouting, ProxyHealthMonitoring, StealthRotationPatterns,
        ConnectionPoolManagement, RealTimeMetricsSync, PlatformAPIIntegration,
        AnalyticsDashboard, CrossPlatformCoordination, VerificationSystem,
        MetricsDatabase, NexusConfig, ViewerSession
    )
except ImportError as e:
    print(f"⚠️  Import error: {e}")
    print("Installing missing dependencies...")
    os.system("pip install numpy fake-useragent")
    try:
        from enhanced_nexus import (
            DynamicWatchDuration, AdvancedMousePatterns, IntelligentEngagement,
            VideoInteractionTiming, SessionPersistence, AdaptiveFailover,
            GeoDistributedRouting, ProxyHealthMonitoring, StealthRotationPatterns,
            ConnectionPoolManagement, RealTimeMetricsSync, PlatformAPIIntegration,
            AnalyticsDashboard, CrossPlatformCoordination, VerificationSystem,
            MetricsDatabase, NexusConfig, ViewerSession
        )
    except ImportError:
        print("❌ Failed to import enhanced_nexus. Running basic validation only.")

class TestEnhancement1_DynamicWatchDuration(unittest.TestCase):
    """Test Enhancement 1: Dynamic Watch Duration Algorithms"""
    
    def setUp(self):
        self.config = Mock()
        self.duration_calc = DynamicWatchDuration(self.config)
    
    def test_live_stream_duration(self):
        """Test live stream duration calculation"""
        duration = self.duration_calc.calculate_watch_duration('live_stream')
        self.assertGreater(duration, 300)  # At least 5 minutes
        self.assertLess(duration, 7200)    # Less than 2 hours
        print(f"✅ Live stream duration: {duration}s")
    
    def test_vod_duration(self):
        """Test VOD duration calculation"""
        duration = self.duration_calc.calculate_watch_duration('vod')
        self.assertGreater(duration, 180)  # At least 3 minutes
        self.assertLess(duration, 3600)    # Less than 1 hour
        print(f"✅ VOD duration: {duration}s")
    
    def test_short_content_duration(self):
        """Test short content duration calculation"""
        duration = self.duration_calc.calculate_watch_duration('short_content')
        self.assertGreater(duration, 30)   # At least 30 seconds
        self.assertLess(duration, 600)     # Less than 10 minutes
        print(f"✅ Short content duration: {duration}s")

class TestEnhancement2_AdvancedMousePatterns(unittest.TestCase):
    """Test Enhancement 2: Advanced Mouse Movement Patterns"""
    
    def setUp(self):
        self.mouse_patterns = AdvancedMousePatterns()
    
    def test_bezier_curve_generation(self):
        """Test smooth bezier curve generation"""
        start = (100, 100)
        end = (500, 400)
        curve = self.mouse_patterns.generate_bezier_curve(start, end)
        
        self.assertTrue(len(curve) > 10)
        self.assertEqual(curve[0], start)
        self.assertEqual(curve[-1], end)
        print(f"✅ Bezier curve generated with {len(curve)} points")
    
    def test_movement_patterns(self):
        """Test different movement patterns"""
        viewport = {'width': 1280, 'height': 800}
        
        for profile in ['casual', 'focused', 'distracted', 'engaged']:
            pattern = self.mouse_patterns._get_movement_pattern(profile, viewport)
            self.assertTrue(len(pattern) > 0)
            print(f"✅ {profile} pattern: {len(pattern)} movements")

class TestEnhancement3_IntelligentEngagement(unittest.TestCase):
    """Test Enhancement 3: Intelligent Engagement Simulation"""
    
    def setUp(self):
        self.config = Mock()
        self.engagement = IntelligentEngagement(self.config)
    
    def test_engagement_level_determination(self):
        """Test engagement level determination"""
        high_engagement = self.engagement._determine_engagement_level(2000)
        medium_engagement = self.engagement._determine_engagement_level(800)
        low_engagement = self.engagement._determine_engagement_level(300)
        
        self.assertEqual(high_engagement, 'high')
        self.assertEqual(medium_engagement, 'medium')
        self.assertEqual(low_engagement, 'low')
        print("✅ Engagement levels correctly determined")
    
    @patch('enhanced_nexus.Page')
    def test_engagement_simulation(self, mock_page):
        """Test engagement simulation"""
        mock_page.query_selector.return_value = Mock()
        
        interactions = self.engagement.simulate_engagement(
            mock_page, 'youtube', 1200
        )
        
        self.assertIsInstance(interactions, list)
        print(f"✅ Generated {len(interactions)} engagement interactions")

class TestEnhancement4_VideoInteractionTiming(unittest.TestCase):
    """Test Enhancement 4: Video Interaction Timing"""
    
    def setUp(self):
        self.video_timing = VideoInteractionTiming()
    
    @patch('enhanced_nexus.Page')
    def test_video_interactions(self, mock_page):
        """Test video interaction simulation"""
        mock_page.keyboard = Mock()
        
        interactions = self.video_timing.simulate_video_interactions(
            mock_page, 'youtube', 600
        )
        
        self.assertIsInstance(interactions, list)
        print(f"✅ Generated {len(interactions)} video interactions")

class TestEnhancement5_SessionPersistence(unittest.TestCase):
    """Test Enhancement 5: Session Persistence"""
    
    def setUp(self):
        self.config = Mock()
        self.persistence = SessionPersistence(self.config)
        self.test_session_id = "test_session_123"
    
    def test_session_fingerprint_generation(self):
        """Test session fingerprint generation"""
        fingerprint1 = self.persistence.generate_session_fingerprint(
            'youtube', 'proxy1'
        )
        fingerprint2 = self.persistence.generate_session_fingerprint(
            'twitch', 'proxy1'
        )
        
        self.assertNotEqual(fingerprint1, fingerprint2)
        self.assertEqual(len(fingerprint1), 12)
        print(f"✅ Session fingerprints: {fingerprint1}, {fingerprint2}")
    
    def test_session_data_persistence(self):
        """Test session data save/load"""
        test_data = {
            'platform': 'youtube',
            'duration': 600,
            'proxy': 'test_proxy'
        }
        
        self.persistence.save_session_data(self.test_session_id, test_data)
        loaded_data = self.persistence.load_session_data(self.test_session_id)
        
        self.assertEqual(loaded_data['platform'], 'youtube')
        self.assertEqual(loaded_data['duration'], 600)
        print("✅ Session data persistence working")
    
    def tearDown(self):
        """Clean up test files"""
        session_file = self.persistence.session_dir / f"{self.test_session_id}.json"
        if session_file.exists():
            session_file.unlink()

class TestEnhancement6_AdaptiveFailover(unittest.TestCase):
    """Test Enhancement 6: Adaptive Failover System"""
    
    def setUp(self):
        self.config = Mock()
        self.failover = AdaptiveFailover(self.config)
    
    def test_failure_type_detection(self):
        """Test failure type detection"""
        rate_limit_error = Exception("rate limit exceeded")
        timeout_error = Exception("connection timeout")
        
        self.assertEqual(
            self.failover.detect_failure_type(rate_limit_error, 429),
            'rate_limit'
        )
        self.assertEqual(
            self.failover.detect_failure_type(timeout_error),
            'connection_timeout'
        )
        print("✅ Failure type detection working")
    
    def test_recovery_strategy_selection(self):
        """Test recovery strategy selection"""
        context = {'retry_count': 1}
        
        rate_limit_recovery = self.failover.execute_recovery_strategy(
            'rate_limit', context
        )
        proxy_ban_recovery = self.failover.execute_recovery_strategy(
            'proxy_ban', context
        )
        
        self.assertEqual(rate_limit_recovery['action'], 'delay_retry')
        self.assertEqual(proxy_ban_recovery['action'], 'switch_proxy')
        print("✅ Recovery strategies correctly selected")

class TestEnhancement7_GeoDistributedRouting(unittest.TestCase):
    """Test Enhancement 7: Geo-distributed Routing"""
    
    def setUp(self):
        self.config = Mock()
        self.geo_routing = GeoDistributedRouting(self.config)
    
    def test_proxy_scoring(self):
        """Test proxy geographical scoring"""
        geo_info_us = {'country': 'US', 'region': 'east'}
        geo_info_eu = {'country': 'GB', 'region': 'london'}
        
        us_score = self.geo_routing._calculate_geo_score(
            geo_info_us, ['US_EAST']
        )
        eu_score = self.geo_routing._calculate_geo_score(
            geo_info_eu, ['US_EAST']
        )
        
        self.assertGreater(us_score, eu_score)
        print(f"✅ Geo scoring: US={us_score}, EU={eu_score}")
    
    def test_optimal_proxy_selection(self):
        """Test optimal proxy selection"""
        proxies = ['proxy1:8080', 'proxy2:8080', 'proxy3:8080']
        
        with patch.object(self.geo_routing, '_get_proxy_geo_info') as mock_geo:
            mock_geo.return_value = {'country': 'US', 'region': 'west'}
            
            selected = self.geo_routing.select_optimal_proxy(proxies, 'youtube')
            self.assertIn(selected, proxies)
            print(f"✅ Selected proxy: {selected}")

class TestEnhancement8_ProxyHealthMonitoring(unittest.TestCase):
    """Test Enhancement 8: Proxy Health Monitoring"""
    
    def setUp(self):
        self.config = Mock()
        self.health_monitor = ProxyHealthMonitoring(self.config)
    
    def test_proxy_metrics_initialization(self):
        """Test proxy metrics initialization"""
        proxies = ['proxy1:8080', 'proxy2:8080']
        self.health_monitor.start_monitoring(proxies)
        
        self.assertEqual(len(self.health_monitor.proxy_metrics), 2)
        self.assertTrue(self.health_monitor.monitoring_active)
        print("✅ Proxy monitoring initialized")
    
    def test_health_score_calculation(self):
        """Test proxy health score calculation"""
        test_proxy = 'test_proxy:8080'
        
        # Initialize with test data
        from enhanced_nexus import ProxyMetrics
        self.health_monitor.proxy_metrics[test_proxy] = ProxyMetrics(
            proxy_url=test_proxy,
            success_rate=0.8,
            avg_response_time=2.0,
            last_used=datetime.now(),
            failure_count=1,
            geo_location='US',
            is_active=True
        )
        
        score = self.health_monitor.get_proxy_score(test_proxy)
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 1.0)
        print(f"✅ Proxy health score: {score}")

class TestEnhancement9_StealthRotationPatterns(unittest.TestCase):
    """Test Enhancement 9: Stealth Rotation Patterns"""
    
    def setUp(self):
        self.config = Mock()
        self.stealth_rotation = StealthRotationPatterns(self.config)
    
    def test_rotation_decision(self):
        """Test proxy rotation decision logic"""
        # Test time-based rotation
        should_rotate_short = self.stealth_rotation.should_rotate_proxy(
            'proxy1', 100
        )
        should_rotate_long = self.stealth_rotation.should_rotate_proxy(
            'proxy1', 1000
        )
        
        # Long usage should definitely trigger rotation
        self.assertTrue(should_rotate_long)
        print(f"✅ Rotation decisions: short={should_rotate_short}, long={should_rotate_long}")
    
    def test_pattern_selection(self):
        """Test rotation pattern selection"""
        proxies = ['proxy1:8080', 'proxy2:8080', 'proxy3:8080']
        
        selected = self.stealth_rotation.select_next_proxy(
            proxies, 'proxy1:8080', None
        )
        
        self.assertIn(selected, proxies)
        self.assertNotEqual(selected, 'proxy1:8080')
        print(f"✅ Selected next proxy: {selected}")

class TestEnhancement10_ConnectionPoolManagement(unittest.TestCase):
    """Test Enhancement 10: Connection Pool Management"""
    
    def setUp(self):
        self.config = Mock()
        self.pool_manager = ConnectionPoolManagement(self.config)
    
    def test_connection_creation(self):
        """Test connection pool creation"""
        proxy = 'test_proxy:8080'
        
        conn1 = self.pool_manager.get_connection(proxy)
        conn2 = self.pool_manager.get_connection(proxy)
        
        self.assertIsNotNone(conn1)
        self.assertIsNotNone(conn2)
        self.assertNotEqual(conn1['id'], conn2['id'])
        print(f"✅ Created connections: {conn1['id']}, {conn2['id']}")
    
    def test_connection_reuse(self):
        """Test connection reuse"""
        proxy = 'test_proxy:8080'
        
        # Get connection and release it
        conn = self.pool_manager.get_connection(proxy)
        self.pool_manager.release_connection(proxy, conn)
        
        # Get connection again - should reuse
        conn2 = self.pool_manager.get_connection(proxy)
        self.assertEqual(conn['id'], conn2['id'])
        print("✅ Connection reuse working")

class TestEnhancement11_RealTimeMetricsSync(unittest.TestCase):
    """Test Enhancement 11: Real-time Metrics Synchronization"""
    
    def setUp(self):
        self.config = Mock()
        self.metrics_db = MetricsDatabase(':memory:')  # In-memory DB for testing
        self.metrics_sync = RealTimeMetricsSync(self.config, self.metrics_db)
    
    def test_platform_apis_initialization(self):
        """Test platform APIs initialization"""
        apis = self.metrics_sync._initialize_platform_apis()
        
        self.assertIn('youtube', apis)
        self.assertIn('twitch', apis)
        self.assertIn('kick', apis)
        print("✅ Platform APIs initialized")
    
    def test_local_viewer_count(self):
        """Test local viewer count calculation"""
        count = self.metrics_sync._get_local_viewer_count('youtube')
        
        self.assertGreater(count, 0)
        print(f"✅ Local viewer count: {count}")

class TestEnhancement12_PlatformAPIIntegration(unittest.TestCase):
    """Test Enhancement 12: Platform-specific API Integration"""
    
    def setUp(self):
        self.config = Mock()
        self.api_integration = PlatformAPIIntegration(self.config)
    
    def test_api_endpoints_configuration(self):
        """Test API endpoints configuration"""
        self.assertIn('youtube', self.api_integration.api_endpoints)
        self.assertIn('twitch', self.api_integration.api_endpoints)
        self.assertIn('kick', self.api_integration.api_endpoints)
        print("✅ API endpoints configured")
    
    def test_verification_methods(self):
        """Test verification method existence"""
        # Test that verification methods exist
        self.assertTrue(hasattr(self.api_integration, '_verify_youtube_viewers'))
        self.assertTrue(hasattr(self.api_integration, '_verify_twitch_viewers'))
        self.assertTrue(hasattr(self.api_integration, '_verify_kick_viewers'))
        print("✅ Verification methods available")

class TestEnhancement13_AnalyticsDashboard(unittest.TestCase):
    """Test Enhancement 13: Analytics Dashboard"""
    
    def setUp(self):
        self.config = Mock()
        self.metrics_db = MetricsDatabase(':memory:')
        self.analytics = AnalyticsDashboard(self.config, self.metrics_db)
    
    def test_analytics_report_generation(self):
        """Test analytics report generation"""
        report = self.analytics.generate_analytics_report()
        
        self.assertIn('generated_at', report)
        self.assertIn('session_statistics', report)
        self.assertIn('system_health', report)
        print("✅ Analytics report generated")
    
    def test_system_health_metrics(self):
        """Test system health metrics"""
        health = self.analytics._get_system_health()
        
        self.assertIn('cpu_usage', health)
        self.assertIn('memory_usage', health)
        self.assertIn('status', health)
        print(f"✅ System health: {health['status']}")

class TestEnhancement14_CrossPlatformCoordination(unittest.TestCase):
    """Test Enhancement 14: Cross-platform Session Coordination"""
    
    def setUp(self):
        self.config = Mock()
        self.coordination = CrossPlatformCoordination(self.config)
    
    def test_viewer_ratio_calculation(self):
        """Test viewer ratio calculation"""
        platforms = ['youtube', 'twitch', 'kick']
        ratios = self.coordination._calculate_viewer_ratios(platforms)
        
        self.assertIn('youtube', ratios)
        self.assertIn('twitch', ratios)
        self.assertIn('kick', ratios)
        
        # YouTube should have highest ratio
        self.assertGreater(ratios['youtube'], ratios['kick'])
        print(f"✅ Viewer ratios: {ratios}")
    
    def test_coordinated_events_generation(self):
        """Test coordinated events generation"""
        events = self.coordination._generate_coordinated_events()
        
        self.assertIsInstance(events, list)
        if events:
            event = events[0]
            self.assertIn('type', event)
            self.assertIn('delay', event)
        print(f"✅ Generated {len(events)} coordinated events")

class TestEnhancement15_VerificationSystem(unittest.TestCase):
    """Test Enhancement 15: Verification System"""
    
    def setUp(self):
        self.config = Mock()
        self.api_integration = Mock()
        self.verification = VerificationSystem(self.config, self.api_integration)
    
    def test_channel_name_mapping(self):
        """Test channel name mapping"""
        youtube_channel = self.verification._get_channel_name('youtube')
        twitch_channel = self.verification._get_channel_name('twitch')
        
        self.assertIsInstance(youtube_channel, str)
        self.assertIsInstance(twitch_channel, str)
        print(f"✅ Channel mapping: YT={youtube_channel}, Twitch={twitch_channel}")
    
    def test_verification_status(self):
        """Test verification status reporting"""
        status = self.verification.get_verification_status()
        
        self.assertIn('verification_active', status)
        self.assertIn('last_results', status)
        self.assertIn('overall_health', status)
        print(f"✅ Verification status: {status['overall_health']}")

class TestMetricsDatabase(unittest.TestCase):
    """Test Metrics Database functionality"""
    
    def setUp(self):
        self.metrics_db = MetricsDatabase(':memory:')
    
    def test_database_initialization(self):
        """Test database initialization"""
        # Check if tables were created
        with sqlite3.connect(self.metrics_db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('viewer_sessions', tables)
        self.assertIn('proxy_metrics', tables)
        self.assertIn('platform_metrics', tables)
        print("✅ Database tables initialized")
    
    def test_session_saving(self):
        """Test session data saving"""
        session = ViewerSession(
            session_id="test_123",
            platform="youtube",
            start_time=datetime.now(),
            duration=600,
            interactions=[],
            proxy_used="test_proxy",
            user_agent="test_agent",
            geo_location="US",
            engagement_score=0.8
        )
        
        self.metrics_db.save_session(session)
        
        # Verify saved
        with sqlite3.connect(self.metrics_db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM viewer_sessions WHERE session_id = ?",
                (session.session_id,)
            )
            count = cursor.fetchone()[0]
        
        self.assertEqual(count, 1)
        print("✅ Session saved to database")

def run_enhancement_tests():
    """Run all enhancement tests"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                Enhanced Nexus Test Suite v3.0                       ║
║                JARVIS NEXUS Enhancement Protocol                     ║
║                      Validation Testing                              ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Test classes for all 15 enhancements
    test_classes = [
        TestEnhancement1_DynamicWatchDuration,
        TestEnhancement2_AdvancedMousePatterns,
        TestEnhancement3_IntelligentEngagement,
        TestEnhancement4_VideoInteractionTiming,
        TestEnhancement5_SessionPersistence,
        TestEnhancement6_AdaptiveFailover,
        TestEnhancement7_GeoDistributedRouting,
        TestEnhancement8_ProxyHealthMonitoring,
        TestEnhancement9_StealthRotationPatterns,
        TestEnhancement10_ConnectionPoolManagement,
        TestEnhancement11_RealTimeMetricsSync,
        TestEnhancement12_PlatformAPIIntegration,
        TestEnhancement13_AnalyticsDashboard,
        TestEnhancement14_CrossPlatformCoordination,
        TestEnhancement15_VerificationSystem,
        TestMetricsDatabase
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n🧪 Running {test_class.__name__}...")
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        
        try:
            result = runner.run(suite)
            total_tests += result.testsRun
            passed_tests += result.testsRun - len(result.failures) - len(result.errors)
            failed_tests += len(result.failures) + len(result.errors)
            
            if result.failures or result.errors:
                print(f"❌ {test_class.__name__}: {len(result.failures + result.errors)} failures")
                for failure in result.failures + result.errors:
                    print(f"   • {failure[0]}: {failure[1].split(chr(10))[0]}")
            else:
                print(f"✅ {test_class.__name__}: All tests passed")
                
        except Exception as e:
            print(f"⚠️  {test_class.__name__}: {str(e)}")
            failed_tests += 1
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                        Test Results Summary                          ║
║                                                                      ║
║  Total Tests: {total_tests:3d}                                             ║
║  Passed:      {passed_tests:3d}                                             ║
║  Failed:      {failed_tests:3d}                                             ║
║                                                                      ║
║  Success Rate: {(passed_tests/max(1,total_tests)*100):5.1f}%                                    ║
║                                                                      ║
║  Status: {'🎉 ALL ENHANCEMENTS VALIDATED' if failed_tests == 0 else '⚠️  SOME TESTS FAILED'}                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    return failed_tests == 0

if __name__ == "__main__":
    success = run_enhancement_tests()
    sys.exit(0 if success else 1)