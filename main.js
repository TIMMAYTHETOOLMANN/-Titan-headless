// ===========================================
// MAIN.JS - ENHANCED TITAN HEADLESS LAUNCHER
// Integrates 10-module enhancement system with existing stream_boost functionality
// ===========================================

const path = require('path');
const fs = require('fs');

// Import enhancement modules
const {
    detectOS,
    ensureDependencies,
    optimizeForHeadless,
    proxyGeoCheck,
    fakeMediaDevices,
    simulateSystemLoad,
    manageCookies,
    humanLikeActions,
    recoverSession,
    checkSystemRequirements,
    createPackageJsonIfMissing
} = require('./enhancements.js');

// Enhanced configuration
const CONFIG = {
    STREAM_URL: process.env.STREAM_URL || "https://www.youtube.com/watch?v=YOUR_STREAM_ID",
    VIEWER_COUNT: parseInt(process.env.VIEWER_COUNT) || 50,
    SESSION_DURATION: parseInt(process.env.SESSION_DURATION) || 300000, // 5 minutes
    PROXY_LIST: [
        "http://user:pass@proxy1.com:8000",
        "http://user:pass@proxy2.com:8000"
        // Add more proxies as needed
    ],
    HEADLESS: process.env.HEADLESS !== 'false', // Default to headless
    ENABLE_ENHANCEMENTS: process.env.ENABLE_ENHANCEMENTS !== 'false' // Default enabled
};

// Lazy load puppeteer dependencies
let puppeteer, StealthPlugin, randomUseragent, proxyChain, faker;

async function initializeDependencies() {
    try {
        puppeteer = require('puppeteer-extra');
        StealthPlugin = require('puppeteer-extra-plugin-stealth');
        randomUseragent = require('random-useragent');
        proxyChain = require('proxy-chain');
        faker = require('faker');
        
        puppeteer.use(StealthPlugin());
        console.log('[INFO] Dependencies loaded successfully');
        return true;
    } catch (error) {
        console.log('[ERROR] Failed to load dependencies:', error.message);
        console.log('[INFO] Attempting to install dependencies...');
        ensureDependencies();
        return false;
    }
}

// Enhanced browser launcher with all 10 modules integrated
async function launchEnhancedBrowser(proxy, sessionId) {
    let browser, page;
    
    try {
        // Module 4: Proxy health check
        if (CONFIG.ENABLE_ENHANCEMENTS && proxy) {
            const isHealthy = await proxyGeoCheck(proxy);
            if (!isHealthy) {
                console.log(`[WARN] Proxy ${proxy} failed health check, proceeding anyway...`);
            }
        }

        const newProxy = proxy ? await proxyChain.anonymizeProxy(proxy) : null;
        const ua = randomUseragent.getRandom();
        
        // Find Chrome executable (enhanced detection)
        const possiblePaths = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium',
            '/usr/bin/google-chrome-unstable',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', // macOS
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', // Windows
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        ];
        
        let executablePath = undefined;
        for (const chromePath of possiblePaths) {
            if (fs.existsSync(chromePath)) {
                executablePath = chromePath;
                break;
            }
        }
        
        const launchArgs = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--disable-web-security',
            '--disable-blink-features=AutomationControlled',
            '--window-size=1280,720'
        ];

        if (newProxy) {
            launchArgs.push(`--proxy-server=${newProxy}`);
        }

        browser = await puppeteer.launch({
            headless: CONFIG.HEADLESS,
            executablePath: executablePath,
            args: launchArgs,
        });

        page = await browser.newPage();
        await page.setUserAgent(ua);

        if (CONFIG.ENABLE_ENHANCEMENTS) {
            // Apply all enhancement modules
            await Promise.all([
                fakeMediaDevices(page),              // Module 5
                simulateSystemLoad(page),            // Module 6
                manageCookies(page, sessionId),      // Module 7
            ]);

            // Enhanced hardware spoofing
            await page.evaluateOnNewDocument(() => {
                // Hardware spoofing
                Object.defineProperty(navigator, 'hardwareConcurrency', { 
                    get: () => Math.floor(Math.random() * 4) + 2 
                });
                Object.defineProperty(navigator, 'deviceMemory', { 
                    get: () => [4, 8, 16][Math.floor(Math.random() * 3)] 
                });
                
                // WebGL spoofing
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) {
                        return 'Intel Inc.';
                    }
                    if (parameter === 37446) {
                        return 'Intel(R) Iris(TM) Graphics 6100';
                    }
                    return getParameter.call(this, parameter);
                };
            });
        }

        return { browser, page };
    } catch (error) {
        if (browser) await browser.close();
        throw error;
    }
}

// Enhanced viewer simulation
async function launchEnhancedViewer(proxy, sessionId) {
    let browser, page;
    
    try {
        const result = await launchEnhancedBrowser(proxy, sessionId || `session_${Date.now()}`);
        browser = result.browser;
        page = result.page;

        console.log(`[INFO] Launching enhanced viewer ${sessionId} with proxy: ${proxy || 'direct'}`);

        // Navigate to stream
        await page.goto(CONFIG.STREAM_URL, { waitUntil: "networkidle2" });

        if (CONFIG.ENABLE_ENHANCEMENTS) {
            // Module 8: Human-like actions
            await humanLikeActions(page);
        }

        // Extended session behavior
        const behaviorsInterval = setInterval(async () => {
            try {
                if (CONFIG.ENABLE_ENHANCEMENTS) {
                    await humanLikeActions(page);
                }
                // Random scroll and interaction
                await page.evaluate(() => {
                    window.scrollBy(0, Math.floor(Math.random() * 100) - 50);
                });
            } catch (error) {
                console.log(`[WARN] Behavior simulation error for ${sessionId}:`, error.message);
            }
        }, 30000 + Math.random() * 20000); // Every 30-50 seconds

        // Clean up after session duration
        setTimeout(async () => {
            clearInterval(behaviorsInterval);
            if (browser) {
                await browser.close();
                console.log(`[INFO] Session ${sessionId} completed`);
            }
        }, CONFIG.SESSION_DURATION);

    } catch (error) {
        console.log(`[ERROR] Enhanced viewer ${sessionId} failed:`, error.message);
        
        if (CONFIG.ENABLE_ENHANCEMENTS) {
            // Module 9: Session recovery
            await recoverSession(error, proxy, (retryProxy) => 
                launchEnhancedViewer(retryProxy, `${sessionId}_retry`)
            );
        }
        
        if (browser) await browser.close();
    }
}

// Main execution function
async function main() {
    console.log('🚀 Starting Titan Headless Enhanced');
    
    // Module 1: OS Detection
    const platform = detectOS();
    
    // System requirements check
    checkSystemRequirements();
    
    // Create package.json if missing
    createPackageJsonIfMissing();
    
    // Module 3: Headless optimization
    if (platform === 'linux') {
        optimizeForHeadless();
    }
    
    // Initialize dependencies
    const depsReady = await initializeDependencies();
    if (!depsReady) {
        console.log('[INFO] Dependencies installed. Please restart the application.');
        process.exit(0);
    }

    console.log(`[INFO] Configuration:`);
    console.log(`  Stream URL: ${CONFIG.STREAM_URL}`);
    console.log(`  Viewer Count: ${CONFIG.VIEWER_COUNT}`);
    console.log(`  Session Duration: ${CONFIG.SESSION_DURATION}ms`);
    console.log(`  Headless Mode: ${CONFIG.HEADLESS}`);
    console.log(`  Enhancements: ${CONFIG.ENABLE_ENHANCEMENTS ? 'Enabled' : 'Disabled'}`);

    // Launch viewers with staggered timing
    for (let i = 0; i < CONFIG.VIEWER_COUNT; i++) {
        const proxy = CONFIG.PROXY_LIST.length > 0 ? CONFIG.PROXY_LIST[i % CONFIG.PROXY_LIST.length] : null;
        const sessionId = `viewer_${i + 1}`;
        
        // Launch viewer (non-blocking)
        launchEnhancedViewer(proxy, sessionId);
        
        // Stagger launches to avoid overwhelming system
        const delay = 2000 + Math.random() * 3000; // 2-5 second random delay
        await new Promise(resolve => setTimeout(resolve, delay));
        
        console.log(`[INFO] Launched viewer ${i + 1}/${CONFIG.VIEWER_COUNT}`);
    }

    console.log('🎯 All viewers launched successfully!');
    console.log(`📊 Monitoring ${CONFIG.VIEWER_COUNT} concurrent sessions...`);
    
    // Keep process alive
    process.on('SIGINT', () => {
        console.log('\n[INFO] Shutting down gracefully...');
        process.exit(0);
    });
}

// Handle unhandled rejections
process.on('unhandledRejection', (reason, promise) => {
    console.log('[ERROR] Unhandled Rejection at:', promise, 'reason:', reason);
});

// Start the application
if (require.main === module) {
    main().catch(error => {
        console.error('[FATAL] Application failed to start:', error);
        process.exit(1);
    });
}

module.exports = {
    main,
    launchEnhancedViewer,
    launchEnhancedBrowser,
    CONFIG
};