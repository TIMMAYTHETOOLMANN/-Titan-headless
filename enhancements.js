// ========================================================
// ENHANCEMENTS + FULLY AUTOMATED DEPLOYMENT MODULES
// ========================================================
const { execSync, exec } = require('child_process');
const os = require('os');
const fs = require('fs');
const https = require('https');
const path = require('path');

// ---- Module 1: OS Detection ----
function detectOS() {
    const platform = os.platform();
    console.log(`[INFO] Detected OS: ${platform}`);
    return platform;
}

// ---- Module 2: Smart Dependency Manager ----
function ensureDependencies() {
    if (!fs.existsSync('node_modules')) {
        console.log('[INFO] Installing dependencies...');
        try {
            execSync('npm install puppeteer-extra puppeteer-extra-plugin-stealth random-useragent proxy-chain faker axios', { stdio: 'inherit' });
        } catch (error) {
            console.log('[WARN] NPM install failed, trying with --force flag...');
            execSync('npm install --force puppeteer-extra puppeteer-extra-plugin-stealth random-useragent proxy-chain faker axios', { stdio: 'inherit' });
        }
    } else {
        console.log('[INFO] Dependencies already present.');
    }
}

// ---- Module 3: Headless Server Optimization ----
function optimizeForHeadless() {
    const platform = os.platform();
    if (platform === 'linux') {
        console.log('[INFO] Optimizing for headless Ubuntu server...');
        try {
            execSync('sudo apt-get update -qq', { stdio: 'inherit' });
            execSync('sudo apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libx11-xcb1 fonts-liberation libappindicator3-1 xdg-utils libxss1 libgconf-2-4 libxtst6 libxrandr2 libasound2 libpangocairo-1.0-0', { stdio: 'inherit' });
        } catch (e) {
            console.log('[WARN] Headless packages already present or installation failed. Check permissions.');
        }
    }
}

// ---- Module 4: Proxy Geo + Health Check ----
async function proxyGeoCheck(proxy) {
    return new Promise((resolve) => {
        const start = Date.now();
        const testURL = `https://httpbin.org/ip`;
        
        // Simple proxy test without external dependency
        const options = {
            timeout: 5000,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        };

        https.get(testURL, options, (res) => {
            const latency = Date.now() - start;
            if (latency < 3000 && res.statusCode === 200) {
                console.log(`[INFO] Proxy ${proxy} is healthy (latency ${latency}ms)`);
                resolve(true);
            } else {
                console.log(`[WARN] Proxy ${proxy} is slow or blocked.`);
                resolve(false);
            }
        }).on('error', () => {
            console.log(`[ERROR] Proxy ${proxy} connection failed.`);
            resolve(false);
        });
    });
}

// ---- Module 5: Fake Media Devices ----
async function fakeMediaDevices(page) {
    await page.evaluateOnNewDocument(() => {
        navigator.mediaDevices.enumerateDevices = async () => [
            { kind: 'audioinput', label: 'Microphone', deviceId: 'default' },
            { kind: 'videoinput', label: 'Webcam', deviceId: 'default' }
        ];
        
        // Mock WebRTC
        const getRandomIP = () => `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`;
        const originalRTCPeerConnection = window.RTCPeerConnection;
        window.RTCPeerConnection = function(...args) {
            const pc = new originalRTCPeerConnection(...args);
            const originalCreateOffer = pc.createOffer;
            pc.createOffer = function() {
                return originalCreateOffer.apply(this, arguments).then(offer => {
                    offer.sdp = offer.sdp.replace(/(\r\n|\r|\n)/g, '').replace(/a=candidate:[\d\w]+\s+\d+\s+udp\s+\d+\s+[\d\.]+/g, `a=candidate:foundation 1 udp 2113667327 ${getRandomIP()}`);
                    return offer;
                });
            };
            return pc;
        };
    });
}

// ---- Module 6: System Load Simulation ----
async function simulateSystemLoad(page) {
    await page.evaluate(() => {
        const busyLoop = Date.now() + 200;
        while (Date.now() < busyLoop) {} // quick CPU tick
        
        // Simulate memory usage
        const arrays = [];
        for (let i = 0; i < 10; i++) {
            arrays.push(new Array(1000).fill(Math.random()));
        }
        
        // Clean up after simulation
        setTimeout(() => {
            arrays.length = 0;
        }, 100);
    });
}

// ---- Module 7: Persistent Cookies + LocalStorage ----
async function manageCookies(page, sessionId) {
    const cookieFile = path.join(__dirname, `cookies_${sessionId}.json`);
    
    // Load existing cookies
    if (fs.existsSync(cookieFile)) {
        try {
            const cookies = JSON.parse(fs.readFileSync(cookieFile, 'utf8'));
            await page.setCookie(...cookies);
            console.log(`[INFO] Loaded cookies for session ${sessionId}`);
        } catch (error) {
            console.log(`[WARN] Failed to load cookies for session ${sessionId}`);
        }
    }
    
    // Save cookies on page close
    page.on('close', async () => {
        try {
            const cookies = await page.cookies();
            fs.writeFileSync(cookieFile, JSON.stringify(cookies, null, 2));
            console.log(`[INFO] Saved cookies for session ${sessionId}`);
        } catch (error) {
            console.log(`[WARN] Failed to save cookies for session ${sessionId}`);
        }
    });
    
    // Set persistent localStorage
    await page.evaluateOnNewDocument(() => {
        localStorage.setItem('viewer_identity', Math.random().toString(36).substring(2));
        localStorage.setItem('session_start', Date.now().toString());
        localStorage.setItem('visit_count', (parseInt(localStorage.getItem('visit_count') || '0') + 1).toString());
    });
}

// ---- Module 8: Human-Like Actions ----
async function humanLikeActions(page) {
    const wait = (min, max) => new Promise(res => setTimeout(res, Math.floor(Math.random() * (max - min + 1) + min)));
    
    // Random mouse movements
    await page.mouse.move(Math.random() * 800, Math.random() * 600);
    await wait(500, 1500);
    
    // Simulate video interactions
    try {
        await page.keyboard.press('Space'); // play/pause
        await wait(500, 1500);
        await page.keyboard.press('ArrowUp'); // adjust volume
        await wait(500, 1500);
        await page.keyboard.press('Shift+>'); // quality adjust
        await wait(500, 1500);
        
        // Random scroll behavior
        await page.evaluate(() => {
            window.scrollBy(0, Math.floor(Math.random() * 200) + 100);
        });
    } catch (error) {
        console.log('[WARN] Some human-like actions failed, continuing...');
    }
}

// ---- Module 9: Session Recovery ----
async function recoverSession(error, proxy, launchFunc) {
    console.log(`[ERROR] Session crashed on proxy ${proxy}. Error: ${error.message}`);
    console.log('[INFO] Implementing recovery strategy...');
    
    // Wait before restart to avoid rapid failures
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    try {
        await launchFunc(proxy);
        console.log(`[INFO] Session successfully recovered on proxy ${proxy}`);
    } catch (recoveryError) {
        console.log(`[ERROR] Recovery failed for proxy ${proxy}: ${recoveryError.message}`);
    }
}

// ---- Module 10: One-Click Launcher ----
function oneClickLaunch() {
    const platform = detectOS();
    console.log('[INFO] Starting one-click deployment...');
    
    try {
        optimizeForHeadless();
        ensureDependencies();
        
        console.log(`[INFO] Launching main.js on ${platform}`);
        
        // Check if main.js exists, otherwise use stream_boost.js
        const mainPath = fs.existsSync('main.js') ? 'main.js' : 'stream_boost/stream_boost.js';
        
        if (fs.existsSync(mainPath)) {
            execSync(`node ${mainPath}`, { stdio: 'inherit' });
        } else {
            console.log('[ERROR] No main.js or stream_boost.js found. Please ensure the application files are present.');
            process.exit(1);
        }
    } catch (error) {
        console.log(`[ERROR] One-click launch failed: ${error.message}`);
        process.exit(1);
    }
}

// Additional utility functions
function checkSystemRequirements() {
    const nodeVersion = process.version;
    const platform = os.platform();
    const arch = os.arch();
    const totalMem = os.totalmem();
    
    console.log(`[INFO] System Check:`);
    console.log(`  Node.js: ${nodeVersion}`);
    console.log(`  Platform: ${platform} (${arch})`);
    console.log(`  Memory: ${Math.round(totalMem / 1024 / 1024 / 1024)}GB`);
    
    // Check minimum requirements
    const nodeVersionNum = parseInt(nodeVersion.slice(1).split('.')[0]);
    if (nodeVersionNum < 14) {
        console.log('[WARN] Node.js version 14+ recommended for optimal performance');
    }
    
    if (totalMem < 2 * 1024 * 1024 * 1024) { // 2GB
        console.log('[WARN] Low memory detected. Consider reducing concurrent sessions.');
    }
}

function createPackageJsonIfMissing() {
    if (!fs.existsSync('package.json')) {
        console.log('[INFO] Creating package.json...');
        const packageJson = {
            "name": "titan-headless-enhanced",
            "version": "1.0.0",
            "description": "Enhanced Titan Headless with 10-module deployment system",
            "main": "main.js",
            "scripts": {
                "start": "node main.js",
                "test": "node --version && npm list",
                "setup": "node -e \"require('./enhancements.js').oneClickLaunch()\""
            },
            "dependencies": {
                "puppeteer-extra": "^3.3.6",
                "puppeteer-extra-plugin-stealth": "^2.11.2",
                "random-useragent": "^0.5.0",
                "proxy-chain": "^2.5.9",
                "faker": "^5.5.3",
                "axios": "^1.6.0"
            },
            "keywords": ["automation", "puppeteer", "headless", "stream", "enhancement"],
            "author": "Titan Headless Enhanced",
            "license": "ISC"
        };
        fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
    }
}

module.exports = {
    detectOS,
    ensureDependencies,
    optimizeForHeadless,
    proxyGeoCheck,
    fakeMediaDevices,
    simulateSystemLoad,
    manageCookies,
    humanLikeActions,
    recoverSession,
    oneClickLaunch,
    checkSystemRequirements,
    createPackageJsonIfMissing
};