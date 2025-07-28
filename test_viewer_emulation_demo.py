#!/usr/bin/env python3
"""
Test script for the viewer emulation demo functionality
"""

from viewer_emulation import (
    ViewerBehavior, GeoIPRotator, BandwidthSimulator, HumanInteraction,
    DeviceEmulator, EngagementAI, FeatureUtilizer, ViewerCluster,
    BufferingSimulator, FingerprintRandomizer
)

def run_viewer_emulation_demo():
    print("\n[Viewer Emulation Demo]")
    
    print("1. Testing ViewerBehavior...")
    ViewerBehavior().simulate_actions(duration=2)  # Reduced for testing
    
    print("\n2. Testing GeoIPRotator...")
    GeoIPRotator().rotate_proxy()
    
    print("\n3. Testing BandwidthSimulator...")
    BandwidthSimulator().simulate_bandwidth()
    
    print("\n4. Testing HumanInteraction...")
    HumanInteraction().simulate_engagement()
    
    print("\n5. Testing DeviceEmulator...")
    DeviceEmulator().get_user_agent()
    
    print("\n6. Testing EngagementAI...")
    EngagementAI().decide_watch_time(video_length=300)
    
    print("\n7. Testing FeatureUtilizer...")
    FeatureUtilizer().utilize_features()
    
    print("\n8. Testing ViewerCluster...")
    ViewerCluster().simulate_cluster(viewers=3)  # Reduced for testing
    
    print("\n9. Testing BufferingSimulator...")
    BufferingSimulator().simulate_buffering()
    
    print("\n10. Testing FingerprintRandomizer...")
    FingerprintRandomizer().randomize_fingerprint()
    
    print("\n✓ All viewer emulation modules tested successfully!")

if __name__ == "__main__":
    run_viewer_emulation_demo()