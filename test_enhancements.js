#!/usr/bin/env node

// ======================================
// TEST ENHANCEMENTS - Validate 10 Modules
// ======================================

const enhancements = require('./enhancements.js');
const fs = require('fs');

console.log('🧪 Testing Titan Headless Enhanced Modules\n');

let passedTests = 0;
let totalTests = 0;

function test(description, testFunction) {
    totalTests++;
    try {
        const result = testFunction();
        if (result === true || result === undefined) {
            console.log(`✅ ${description}`);
            passedTests++;
        } else {
            console.log(`❌ ${description} - Failed`);
        }
    } catch (error) {
        console.log(`❌ ${description} - Error: ${error.message}`);
    }
}

async function asyncTest(description, testFunction) {
    totalTests++;
    try {
        const result = await testFunction();
        if (result === true || result === undefined) {
            console.log(`✅ ${description}`);
            passedTests++;
        } else {
            console.log(`❌ ${description} - Failed`);
        }
    } catch (error) {
        console.log(`❌ ${description} - Error: ${error.message}`);
    }
}

async function runTests() {
    console.log('📋 Testing Core Modules:\n');

    // Module 1: OS Detection
    test('Module 1: OS Detection', () => {
        const os = enhancements.detectOS();
        return typeof os === 'string' && os.length > 0;
    });

    // Module 2: Package.json Creation
    test('Module 2: Package.json Management', () => {
        enhancements.createPackageJsonIfMissing();
        return fs.existsSync('package.json');
    });

    // Module 3: System Requirements Check
    test('Module 3: System Requirements Check', () => {
        enhancements.checkSystemRequirements();
        return true; // If it runs without error, it passes
    });

    // Module 4: Proxy Health Check (mock test)
    await asyncTest('Module 4: Proxy Health Check Interface', async () => {
        // Test that the function exists and can be called
        const result = await enhancements.proxyGeoCheck('http://invalid-proxy:8000');
        return typeof result === 'boolean';
    });

    // Test configuration validation
    test('Configuration: Main.js exists', () => {
        return fs.existsSync('main.js');
    });

    test('Configuration: Enhancements.js exists', () => {
        return fs.existsSync('enhancements.js');
    });

    test('Configuration: Run scripts exist', () => {
        return fs.existsSync('run.sh') && fs.existsSync('run.bat');
    });

    test('Configuration: Run.sh is executable', () => {
        const stats = fs.statSync('run.sh');
        return (stats.mode & parseInt('111', 8)) !== 0; // Check execute permissions
    });

    // Test module exports
    test('Exports: All 10 core modules exported', () => {
        const requiredFunctions = [
            'detectOS',
            'ensureDependencies', 
            'optimizeForHeadless',
            'proxyGeoCheck',
            'fakeMediaDevices',
            'simulateSystemLoad',
            'manageCookies',
            'humanLikeActions',
            'recoverSession',
            'oneClickLaunch'
        ];
        
        return requiredFunctions.every(func => typeof enhancements[func] === 'function');
    });

    // Test main.js can be required
    test('Integration: Main.js module loads', () => {
        const main = require('./main.js');
        return typeof main.main === 'function';
    });

    console.log('\n📊 Test Results:');
    console.log(`   Passed: ${passedTests}/${totalTests}`);
    console.log(`   Success Rate: ${Math.round((passedTests / totalTests) * 100)}%`);

    if (passedTests === totalTests) {
        console.log('\n🎉 All tests passed! Titan Headless Enhanced is ready for deployment.');
        return true;
    } else {
        console.log('\n⚠️  Some tests failed. Please check the issues above.');
        return false;
    }
}

// Run tests if called directly
if (require.main === module) {
    runTests().then(success => {
        process.exit(success ? 0 : 1);
    });
}

module.exports = { runTests };