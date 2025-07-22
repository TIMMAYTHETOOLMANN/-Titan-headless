#!/usr/bin/env python3
"""
Titan Headless - Unified Deployment System
Main entry point supporting both live stream and static video deployments
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

from deployment_core import (
    DeploymentConfig, ConfigManager, DeploymentValidator, DeploymentMode
)
from live_stream_deployment import LiveStreamDeployment
from static_video_deployment import StaticVideoDeployment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TitanHeadlessDeployment:
    """Unified deployment controller for both live stream and static video"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.live_stream_deployment = None
        self.static_video_deployment = None
        
    async def deploy(self):
        """Deploy based on configuration mode"""
        logger.info(f"🚀 Starting Titan Headless deployment in {self.config.deployment_mode.value} mode")
        
        if self.config.deployment_mode == DeploymentMode.LIVE_STREAM:
            await self._deploy_live_stream()
        elif self.config.deployment_mode == DeploymentMode.STATIC_VIDEO:
            await self._deploy_static_video()
        elif self.config.deployment_mode == DeploymentMode.BOTH:
            await self._deploy_both()
        else:
            logger.error(f"Unknown deployment mode: {self.config.deployment_mode}")
    
    async def _deploy_live_stream(self):
        """Deploy live stream deployment only"""
        self.live_stream_deployment = LiveStreamDeployment(self.config)
        await self.live_stream_deployment.deploy()
    
    async def _deploy_static_video(self):
        """Deploy static video deployment only"""
        self.static_video_deployment = StaticVideoDeployment(self.config)
        await self.static_video_deployment.deploy()
    
    async def _deploy_both(self):
        """Deploy both live stream and static video deployments"""
        logger.info("Deploying both live stream and static video systems")
        
        # Create both deployments
        self.live_stream_deployment = LiveStreamDeployment(self.config)
        self.static_video_deployment = StaticVideoDeployment(self.config)
        
        # Run both deployments concurrently
        tasks = [
            self.live_stream_deployment.deploy(),
            self.static_video_deployment.deploy()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error in dual deployment: {str(e)}")
            await self.shutdown()
    
    async def shutdown(self):
        """Shutdown all active deployments"""
        logger.info("Shutting down Titan Headless deployment...")
        
        shutdown_tasks = []
        
        if self.live_stream_deployment:
            shutdown_tasks.append(self.live_stream_deployment.shutdown())
        
        if self.static_video_deployment:
            shutdown_tasks.append(self.static_video_deployment.shutdown())
        
        if shutdown_tasks:
            await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        logger.info("✅ Titan Headless deployment shutdown complete")
    
    def status_report(self):
        """Generate comprehensive status report"""
        print(f"\n{'='*80}")
        print(f"🎯 TITAN HEADLESS DEPLOYMENT STATUS")
        print(f"{'='*80}")
        print(f"Deployment Mode: {self.config.deployment_mode.value.upper()}")
        print(f"Configuration: {self.config.shared.profile_base}")
        print(f"Base Port: {self.config.shared.base_port}")
        print(f"Resource Thresholds: CPU {self.config.shared.cpu_threshold}%, RAM {self.config.shared.ram_threshold}%")
        
        if self.live_stream_deployment:
            self.live_stream_deployment.status_report()
        
        if self.static_video_deployment:
            self.static_video_deployment.status_report()
        
        print(f"{'='*80}\n")

def create_sample_configs():
    """Create sample configuration files for different deployment modes"""
    
    # Live Stream Configuration
    from deployment_core import PlatformConfig
    live_config = DeploymentConfig()
    live_config.deployment_mode = DeploymentMode.LIVE_STREAM
    live_config.live_stream.platforms = {
        'youtube': PlatformConfig(True, 10, 'https://www.youtube.com/@{account}/live'),
        'kick': PlatformConfig(True, 11, 'https://www.kick.com/{account}'),
        'twitch': PlatformConfig(True, 15, 'https://www.twitch.tv/{account}')
    }
    ConfigManager.save_config(live_config, "deployment_config_live.yaml")
    
    # Static Video Configuration
    static_config = DeploymentConfig()
    static_config.deployment_mode = DeploymentMode.STATIC_VIDEO
    ConfigManager.save_config(static_config, "deployment_config_static.yaml")
    
    # Both Modes Configuration
    both_config = DeploymentConfig()
    both_config.deployment_mode = DeploymentMode.BOTH
    both_config.live_stream.platforms = {
        'youtube': PlatformConfig(True, 5, 'https://www.youtube.com/@{account}/live'),
        'kick': PlatformConfig(True, 5, 'https://www.kick.com/{account}'),
        'twitch': PlatformConfig(True, 5, 'https://www.twitch.tv/{account}')
    }
    both_config.static_video.windows = 10
    ConfigManager.save_config(both_config, "deployment_config_both.yaml")
    
    logger.info("Sample configuration files created:")
    logger.info("  - deployment_config_live.yaml")
    logger.info("  - deployment_config_static.yaml")
    logger.info("  - deployment_config_both.yaml")

def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="Titan Headless - Unified Deployment System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Deployment Modes:
  live_stream    - Deploy live stream watching across multiple platforms
  static_video   - Deploy static YouTube video watching
  both          - Deploy both live stream and static video systems

Examples:
  python titan_deployment.py --mode live_stream --config deployment_config_live.yaml
  python titan_deployment.py --mode static_video
  python titan_deployment.py --mode both --create-configs
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['live_stream', 'static_video', 'both'],
        help='Deployment mode'
    )
    
    parser.add_argument(
        '--config', 
        default='deployment_config.yaml',
        help='Configuration file path (default: deployment_config.yaml)'
    )
    
    parser.add_argument(
        '--create-configs',
        action='store_true',
        help='Create sample configuration files and exit'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Validate configuration and exit'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create sample configs if requested
    if args.create_configs:
        create_sample_configs()
        return
    
    try:
        # Load configuration
        config = ConfigManager.load_config(args.config)
        
        # Override deployment mode if specified
        if args.mode:
            config.deployment_mode = DeploymentMode(args.mode)
        
        # Validate configuration
        issues = DeploymentValidator.validate_config(config)
        if issues:
            logger.error("Configuration validation failed:")
            for issue in issues:
                logger.error(f"  - {issue}")
            sys.exit(1)
        
        if args.validate_only:
            logger.info("✅ Configuration is valid")
            return
        
        # Create and run deployment
        deployment = TitanHeadlessDeployment(config)
        deployment.status_report()
        
        asyncio.run(deployment.deploy())
        
    except KeyboardInterrupt:
        logger.info("🛑 User interruption detected")
    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                      Titan Headless v2.0                            ║
    ║                  Unified Deployment System                           ║
    ║                                                                      ║
    ║  Modular deployment system for live stream and static video         ║
    ║  viewing across multiple platforms.                                  ║
    ║                                                                      ║
    ║  Features:                                                           ║
    ║  • Live Stream Deployment (YouTube, Kick, Twitch)                  ║
    ║  • Static Video Deployment (YouTube)                               ║
    ║  • Dual Mode Deployment (Both simultaneously)                      ║
    ║  • Advanced Stealth & Human Emulation                              ║
    ║  • Resource Monitoring & Management                                ║
    ║  • Configurable Proxy Support                                      ║
    ║                                                                      ║
    ║  Press Ctrl+C to stop all windows                                  ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    main()