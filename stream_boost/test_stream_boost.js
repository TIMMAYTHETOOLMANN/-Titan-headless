#!/usr/bin/env node
/**
 * Test script for Stream Boost Node.js Implementation
 * Validates dependencies, configuration, and basic functionality
 */

const fs = require('fs');
const path = require('path');

async function testDependencies() {
    console.log('🔄 Testing dependencies...');
    
    try {
        const puppeteer = require('puppeteer-extra');
        const StealthPlugin = require('puppeteer-extra-plugin-stealth');
        const randomUseragent = require('random-useragent');
        const proxyChain = require('proxy-chain');
        const { faker } = require('@faker-js/faker');
        
        console.log('✅ All required modules imported successfully');
        return true;
    } catch (error) {
        console.error('❌ Import error:', error.message);
        return false;
    }
}

async function testConfiguration() {
    console.log('🔄 Testing configuration...');
    
    try {
        const streamBoostPath = path.join(__dirname, 'stream_boost.js');
        if (!fs.existsSync(streamBoostPath)) {
            throw new Error('stream_boost.js not found');
        }
        
        const content = fs.readFileSync(streamBoostPath, 'utf8');
        
        // Check for all 16 modules
        const modules = [
            'launchBrowser',
            'spoofHardware', 
            'emulateDevice',
            'simulateMouse',
            'simulateScroll',
            'engagementActions',
            'throttleNetwork',
            'loadCookies',
            'assignIdentity',
            'spoofReferrer',
            'simulateBehavior',
            'randomTabActivity',
            'monitorQuality',
            'injectAntiFingerprint',
            'launchViewer',
            'simulateAccountWatchHistory'
        ];
        
        const missingModules = modules.filter(module => !content.includes(`async function ${module}`));
        
        if (missingModules.length > 0) {
            throw new Error(`Missing modules: ${missingModules.join(', ')}`);
        }
        
        console.log('✅ All 16 modules found in stream_boost.js');
        console.log('✅ Configuration file validated successfully');
        return true;
    } catch (error) {
        console.error('❌ Configuration error:', error.message);
        return false;
    }
}

async function testBrowserSetup() {
    console.log('🔄 Testing browser setup (dry run)...');
    
    try {
        const puppeteer = require('puppeteer-extra');
        const StealthPlugin = require('puppeteer-extra-plugin-stealth');
        
        puppeteer.use(StealthPlugin());
        
        // Try to find Chrome executable
        const possiblePaths = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium',
            '/usr/bin/google-chrome-unstable'
        ];
        
        let executablePath = undefined;
        const fs = require('fs');
        for (const path of possiblePaths) {
            if (fs.existsSync(path)) {
                executablePath = path;
                console.log(`Found Chrome at: ${path}`);
                break;
            }
        }
        
        if (!executablePath) {
            console.log('⚠️  No Chrome executable found, but this may work if Puppeteer bundled Chrome is available');
        }
        
        // Test browser launch with minimal configuration
        const browser = await puppeteer.launch({
            headless: true,
            executablePath: executablePath,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
        await page.setViewport({ width: 1280, height: 720 });
        
        await browser.close();
        
        console.log('✅ Browser setup test passed');
        return true;
    } catch (error) {
        console.error('❌ Browser setup error:', error.message);
        return false;
    }
}

async function runTests() {
    console.log('🚀 Starting Stream Boost Node.js Tests\n');
    
    const tests = [
        testDependencies,
        testConfiguration,
        testBrowserSetup
    ];
    
    let passed = 0;
    let failed = 0;
    
    for (const test of tests) {
        try {
            const result = await test();
            if (result) {
                passed++;
            } else {
                failed++;
            }
        } catch (error) {
            console.error('❌ Test failed:', error.message);
            failed++;
        }
        console.log(''); // Empty line for readability
    }
    
    console.log('📊 Test Results:');
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    
    if (failed === 0) {
        console.log('🎉 All tests passed! Stream Boost Node.js implementation is ready.');
        process.exit(0);
    } else {
        console.log('⚠️  Some tests failed. Please check the issues above.');
        process.exit(1);
    }
}

// Run tests if this file is executed directly
if (require.main === module) {
    runTests().catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });
}

module.exports = { testDependencies, testConfiguration, testBrowserSetup };