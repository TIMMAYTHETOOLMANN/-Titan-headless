#!/usr/bin/env python3
"""
Titan Headless - Core Deployment Modules
Provides unified deployment capabilities for both live stream and static video viewing
"""

import asyncio
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

class DeploymentMode(Enum):
    LIVE_STREAM = "live_stream"
    STATIC_VIDEO = "static_video"
    BOTH = "both"

@dataclass
class PlatformConfig:
    """Configuration for a streaming platform"""
    enabled: bool = True
    windows: int = 10
    url_template: str = ""

@dataclass
class LiveStreamConfig:
    """Configuration for live stream deployment"""
    target_account: str = "timmaythetoolman"
    platforms: Dict[str, PlatformConfig] = field(default_factory=lambda: {
        'youtube': PlatformConfig(True, 10, 'https://www.youtube.com/@{account}/live'),
        'kick': PlatformConfig(True, 11, 'https://www.kick.com/{account}'),
        'twitch': PlatformConfig(True, 15, 'https://www.twitch.tv/{account}')
    })
    check_interval: int = 30
    fallback_to_videos: bool = True
    max_wait_time: int = 300

@dataclass
class StaticVideoConfig:
    """Configuration for static video deployment"""
    channel_url: str = "https://www.youtube.com/@timmaythetoolan"
    windows: int = 20
    max_videos: int = 25
    min_video_duration: int = 60
    max_video_duration: int = 3600
    rotate_video_every: List[int] = field(default_factory=lambda: [180, 320])
    prefer_popular: bool = True
    engagement_rate: float = 0.3

@dataclass
class SharedConfig:
    """Shared configuration for both deployment types"""
    base_port: int = 9333
    profile_base: str = "./profiles"
    window_width: int = 1280
    window_height: int = 800
    headless: bool = False
    cpu_threshold: int = 85
    ram_threshold: int = 85
    proxy_list: List[str] = field(default_factory=list)
    log_level: str = "INFO"
    statistics_enabled: bool = True

@dataclass
class DeploymentConfig:
    """Unified deployment configuration"""
    deployment_mode: DeploymentMode = DeploymentMode.LIVE_STREAM
    live_stream: LiveStreamConfig = field(default_factory=LiveStreamConfig)
    static_video: StaticVideoConfig = field(default_factory=StaticVideoConfig)
    shared: SharedConfig = field(default_factory=SharedConfig)

class ConfigManager:
    """Manages configuration loading and validation"""
    
    @staticmethod
    def load_config(config_path: str = "deployment_config.yaml") -> DeploymentConfig:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                data = yaml.safe_load(file)
            
            return ConfigManager._parse_config(data)
        except FileNotFoundError:
            logging.warning(f"Config file {config_path} not found, using defaults")
            return DeploymentConfig()
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return DeploymentConfig()
    
    @staticmethod
    def _parse_config(data: Dict) -> DeploymentConfig:
        """Parse configuration dictionary into structured config"""
        config = DeploymentConfig()
        
        # Parse deployment mode
        if 'deployment_mode' in data:
            config.deployment_mode = DeploymentMode(data['deployment_mode'])
        
        # Parse live stream config
        if 'live_stream' in data:
            ls_data = data['live_stream']
            config.live_stream = LiveStreamConfig(
                target_account=ls_data.get('target_account', 'timmaythetoolman'),
                check_interval=ls_data.get('live_detection', {}).get('check_interval', 30),
                fallback_to_videos=ls_data.get('live_detection', {}).get('fallback_to_videos', True),
                max_wait_time=ls_data.get('live_detection', {}).get('max_wait_time', 300)
            )
            
            # Parse platforms
            if 'platforms' in ls_data:
                for platform, platform_data in ls_data['platforms'].items():
                    config.live_stream.platforms[platform] = PlatformConfig(
                        enabled=platform_data.get('enabled', True),
                        windows=platform_data.get('windows', 10),
                        url_template=platform_data.get('url_template', '')
                    )
        
        # Parse static video config
        if 'static_video' in data:
            sv_data = data['static_video']
            config.static_video = StaticVideoConfig(
                channel_url=sv_data.get('channel_url', 'https://www.youtube.com/@timmaythetoolan'),
                windows=sv_data.get('windows', 20),
                max_videos=sv_data.get('video_selection', {}).get('max_videos', 25),
                min_video_duration=sv_data.get('video_selection', {}).get('min_video_duration', 60),
                max_video_duration=sv_data.get('video_selection', {}).get('max_video_duration', 3600),
                rotate_video_every=sv_data.get('video_selection', {}).get('rotate_video_every', [180, 320]),
                prefer_popular=sv_data.get('video_selection', {}).get('prefer_popular', True),
                engagement_rate=sv_data.get('engagement', {}).get('rate', 0.3)
            )
        
        # Parse shared config
        if 'shared' in data:
            shared_data = data['shared']
            config.shared = SharedConfig(
                base_port=shared_data.get('browser', {}).get('base_port', 9333),
                profile_base=shared_data.get('browser', {}).get('profile_base', './profiles'),
                window_width=shared_data.get('browser', {}).get('window_width', 1280),
                window_height=shared_data.get('browser', {}).get('window_height', 800),
                headless=shared_data.get('browser', {}).get('headless', False),
                cpu_threshold=shared_data.get('resources', {}).get('cpu_threshold', 85),
                ram_threshold=shared_data.get('resources', {}).get('ram_threshold', 85),
                proxy_list=shared_data.get('proxy', {}).get('proxy_list', []),
                log_level=shared_data.get('monitoring', {}).get('log_level', 'INFO'),
                statistics_enabled=shared_data.get('monitoring', {}).get('statistics_enabled', True)
            )
        
        return config
    
    @staticmethod
    def save_config(config: DeploymentConfig, config_path: str = "deployment_config.yaml"):
        """Save configuration to YAML file"""
        try:
            # Convert to dictionary structure for YAML serialization
            data = {
                'deployment_mode': config.deployment_mode.value,
                'live_stream': {
                    'target_account': config.live_stream.target_account,
                    'platforms': {
                        name: {
                            'enabled': platform.enabled,
                            'windows': platform.windows,
                            'url_template': platform.url_template
                        } for name, platform in config.live_stream.platforms.items()
                    },
                    'live_detection': {
                        'check_interval': config.live_stream.check_interval,
                        'fallback_to_videos': config.live_stream.fallback_to_videos,
                        'max_wait_time': config.live_stream.max_wait_time
                    }
                },
                'static_video': {
                    'channel_url': config.static_video.channel_url,
                    'windows': config.static_video.windows,
                    'video_selection': {
                        'max_videos': config.static_video.max_videos,
                        'min_video_duration': config.static_video.min_video_duration,
                        'max_video_duration': config.static_video.max_video_duration,
                        'rotate_video_every': config.static_video.rotate_video_every,
                        'prefer_popular': config.static_video.prefer_popular
                    },
                    'engagement': {
                        'rate': config.static_video.engagement_rate
                    }
                },
                'shared': {
                    'browser': {
                        'base_port': config.shared.base_port,
                        'profile_base': config.shared.profile_base,
                        'window_width': config.shared.window_width,
                        'window_height': config.shared.window_height,
                        'headless': config.shared.headless
                    },
                    'resources': {
                        'cpu_threshold': config.shared.cpu_threshold,
                        'ram_threshold': config.shared.ram_threshold
                    },
                    'proxy': {
                        'proxy_list': config.shared.proxy_list
                    },
                    'monitoring': {
                        'log_level': config.shared.log_level,
                        'statistics_enabled': config.shared.statistics_enabled
                    }
                }
            }
            
            with open(config_path, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
                
        except Exception as e:
            logging.error(f"Error saving config: {e}")

class DeploymentValidator:
    """Validates deployment configurations"""
    
    @staticmethod
    def validate_config(config: DeploymentConfig) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Validate deployment mode
        if config.deployment_mode not in DeploymentMode:
            issues.append(f"Invalid deployment mode: {config.deployment_mode}")
        
        # Validate live stream config
        if config.deployment_mode in [DeploymentMode.LIVE_STREAM, DeploymentMode.BOTH]:
            if not config.live_stream.target_account:
                issues.append("Live stream target account is required")
            
            if not config.live_stream.platforms:
                issues.append("At least one platform must be configured for live streams")
            
            for platform_name, platform_config in config.live_stream.platforms.items():
                if platform_config.enabled and not platform_config.url_template:
                    issues.append(f"URL template required for enabled platform: {platform_name}")
        
        # Validate static video config
        if config.deployment_mode in [DeploymentMode.STATIC_VIDEO, DeploymentMode.BOTH]:
            if not config.static_video.channel_url:
                issues.append("Static video channel URL is required")
            
            if config.static_video.windows <= 0:
                issues.append("Static video windows must be greater than 0")
        
        # Validate shared config
        if config.shared.base_port < 1024 or config.shared.base_port > 65535:
            issues.append("Base port must be between 1024 and 65535")
        
        if config.shared.cpu_threshold < 0 or config.shared.cpu_threshold > 100:
            issues.append("CPU threshold must be between 0 and 100")
        
        if config.shared.ram_threshold < 0 or config.shared.ram_threshold > 100:
            issues.append("RAM threshold must be between 0 and 100")
        
        return issues

if __name__ == "__main__":
    # Test the configuration system
    config = ConfigManager.load_config()
    issues = DeploymentValidator.validate_config(config)
    
    if issues:
        print("Configuration issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ Configuration is valid")
        print(f"Deployment mode: {config.deployment_mode.value}")
        print(f"Live stream account: {config.live_stream.target_account}")
        print(f"Static video channel: {config.static_video.channel_url}")