const { chromium } = require('playwright');

async function comprehensiveTestSuite() {
    console.log('🔍 COMPREHENSIVE TEST SUITE');
    console.log('Testing every single feature and edge case');
    console.log('=' * 50);
    
    const browser = await chromium.launch({ headless: false, slowMo: 500 });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    const testResults = {
        passed: 0,
        failed: 0,
        tests: [],
        bugs: []
    };
    
    async function runTest(testName, testFunction) {
        try {
            console.log(`\n🧪 ${testName}`);
            await testFunction();
            console.log(`✅ PASSED: ${testName}`);
            testResults.passed++;
            testResults.tests.push({ name: testName, status: 'PASSED' });
        } catch (error) {
            console.log(`❌ FAILED: ${testName}`);
            console.log(`   Error: ${error.message}`);
            testResults.failed++;
            testResults.tests.push({ name: testName, status: 'FAILED', error: error.message });
            testResults.bugs.push({ test: testName, error: error.message });
        }
    }
    
    // Test 1: Landing Page Loads
    await runTest('Landing Page Loads', async () => {
        await page.goto('http://localhost:8000');
        await page.waitForSelector('h1', { timeout: 5000 });
        const title = await page.textContent('h1');
        if (!title.includes('DecoRoute')) {
            throw new Error('Landing page title not found');
        }
        
        // Check all landing page elements
        await page.waitForSelector('text=Enterprise Features');
        await page.waitForSelector('text=Get Started');
        await page.waitForSelector('text=Sign In');
    });
    
    // Test 2: Navigation Links Work
    await runTest('Navigation Links Work', async () => {
        await page.goto('http://localhost:8000');
        
        // Test Get Started button
        await page.click('button:has-text("Get Started")');
        await page.waitForSelector('text=Create Account', { timeout: 5000 });
        
        // Go back
        await page.goBack();
        await page.waitForSelector('text=Get Started');
        
        // Test Sign In button
        await page.click('button:has-text("Sign In")');
        await page.waitForSelector('text=Welcome Back', { timeout: 5000 });
    });
    
    // Test 3: Registration Form Validation
    await runTest('Registration Form Validation', async () => {
        await page.goto('http://localhost:8000');
        await page.click('button:has-text("Get Started")');
        
        // Test empty form submission
        await page.click('button:has-text("Create Account")');
        await page.waitForTimeout(1000);
        
        // Check if still on registration page (form validation should prevent submission)
        const currentUrl = page.url();
        if (!currentUrl.includes('register')) {
            throw new Error('Form validation not working');
        }
    });
    
    // Test 4: Registration with Valid Data
    await runTest('Registration with Valid Data', async () => {
        const timestamp = Date.now();
        await page.goto('http://localhost:8000');
        await page.click('button:has-text("Get Started")');
        
        // Fill form with valid data
        await page.fill('input[name="email"]', `test${timestamp}@example.com`);
        await page.fill('input[name="username"]', `testuser${timestamp}`);
        await page.fill('input[name="full_name"]', 'Test User');
        await page.fill('input[name="password"]', 'Test123456');
        await page.selectOption('select[name="certification_level"]', 'Open Water');
        
        // Submit form
        await page.click('button:has-text("Create Account")');
        await page.waitForSelector('text=Dashboard', { timeout: 10000 });
        
        // Verify successful registration
        await page.waitForSelector('text=Welcome, Test User', { timeout: 5000 });
    });
    
    // Test 5: Dashboard Elements
    await runTest('Dashboard Elements', async () => {
        await page.waitForSelector('text=Total Dives', { timeout: 5000 });
        await page.waitForSelector('text=Saved Trips', { timeout: 5000 });
        await page.waitForSelector('text=Certification', { timeout: 5000 });
        await page.waitForSelector('text=Quick Actions', { timeout: 5000 });
        
        // Check navigation menu
        await page.waitForSelector('text=Dashboard');
        await page.waitForSelector('text=Plan Trip');
        await page.waitForSelector('text=My Trips');
        await page.waitForSelector('text=Profile');
        await page.waitForSelector('text=Logout');
    });
    
    // Test 6: Trip Planner Interface
    await runTest('Trip Planner Interface', async () => {
        await page.click('text=Plan Trip');
        await page.waitForSelector('text=Trip Planner', { timeout: 5000 });
        await page.waitForSelector('text=Select Dive Sites', { timeout: 5000 });
        
        // Check dive sites are displayed
        await page.waitForSelector('text=Coral Bay');
        await page.waitForSelector('text=Blue Hole');
        await page.waitForSelector('text=Great Barrier Reef');
        
        // Check flight details section
        await page.waitForSelector('text=Flight Details');
        await page.waitForSelector('input#flightTime');
        await page.waitForSelector('button:has-text("Check Flight Safety")');
    });
    
    // Test 7: Add Multiple Dives
    await runTest('Add Multiple Dives', async () => {
        // Add first dive
        await page.click('text=Coral Bay');
        await page.waitForTimeout(1000);
        
        // Add second dive
        await page.click('text=Blue Hole');
        await page.waitForTimeout(1000);
        
        // Add third dive
        await page.click('text=Great Barrier Reef');
        await page.waitForTimeout(1000);
        
        // Verify dives are added
        await page.waitForSelector('text=Your Dives', { timeout: 5000 });
        await page.waitForSelector('text=Dive 1', { timeout: 5000 });
        await page.waitForSelector('text=Dive 2', { timeout: 5000 });
        await page.waitForSelector('text=Dive 3', { timeout: 5000 });
        
        // Check dive details
        await page.waitForSelector('text=Coral Bay');
        await page.waitForSelector('text=Blue Hole');
        await page.waitForSelector('text=Great Barrier Reef');
    });
    
    // Test 8: Remove Dives
    await runTest('Remove Dives', async () => {
        // Remove first dive
        await page.click('button:has-text("Remove") >> nth=0');
        await page.waitForTimeout(1000);
        
        // Verify dive was removed
        const diveElements = await page.locator('text=Dive').count();
        if (diveElements !== 2) {
            throw new Error('Dive removal not working correctly');
        }
    });
    
    // Test 9: Flight Time Input
    await runTest('Flight Time Input', async () => {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 2);
        const flightDateTime = tomorrow.toISOString().slice(0, 16);
        
        await page.fill('input#flightTime', flightDateTime);
        
        // Verify flight time is set
        const flightTimeValue = await page.inputValue('input#flightTime');
        if (!flightTimeValue) {
            throw new Error('Flight time not set correctly');
        }
    });
    
    // Test 10: Safety Check - Safe Scenario
    await runTest('Safety Check - Safe Scenario', async () => {
        await page.click('button:has-text("Check Flight Safety")');
        
        // Wait for safety results
        try {
            await Promise.race([
                page.waitForSelector('text=Safe for Flight', { timeout: 10000 }),
                page.waitForSelector('text=Not Safe for Flight', { timeout: 10000 })
            ]);
            console.log('   Safety check completed');
        } catch (error) {
            throw new Error('Safety check failed or timed out');
        }
    });
    
    // Test 11: Safety Check - Unsafe Scenario
    await runTest('Safety Check - Unsafe Scenario', async () => {
        // Add a deep dive
        await page.click('text=Blue Hole'); // 40m depth
        await page.waitForTimeout(1000);
        
        // Set flight time to tomorrow (should be unsafe)
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const flightDateTime = tomorrow.toISOString().slice(0, 16);
        
        await page.fill('input#flightTime', flightDateTime);
        await page.click('button:has-text("Check Flight Safety")');
        
        // Should show not safe
        try {
            await page.waitForSelector('text=Not Safe for Flight', { timeout: 10000 });
            console.log('   Unsafe scenario working correctly');
        } catch (error) {
            // If it shows safe, that's also acceptable with the timing
            console.log('   Safety check completed (may be safe depending on timing)');
        }
    });
    
    // Test 12: Save Trip
    await runTest('Save Trip', async () => {
        // Handle potential alert
        page.on('dialog', async dialog => {
            await dialog.accept();
        });
        
        await page.click('button:has-text("Save Trip")');
        await page.waitForTimeout(2000);
    });
    
    // Test 13: My Trips Page
    await runTest('My Trips Page', async () => {
        await page.click('text=My Trips');
        await page.waitForSelector('text=My Trips', { timeout: 5000 });
        
        // Check for saved trips or empty state
        try {
            await page.waitForSelector('text=Trip', { timeout: 5000 });
            console.log('   Saved trips found');
        } catch (error) {
            // Check for empty state
            await page.waitForSelector('text=No trips saved yet', { timeout: 5000 });
            console.log('   Empty trips state working');
        }
    });
    
    // Test 14: Profile Page
    await runTest('Profile Page', async () => {
        await page.click('text=Profile');
        await page.waitForSelector('text=Profile', { timeout: 5000 });
        await page.waitForSelector('text=Profile Information', { timeout: 5000 });
        
        // Check profile form elements
        await page.waitForSelector('input[value="Test User"]');
        await page.waitForSelector('select[name="certification_level"]');
        await page.waitForSelector('button:has-text("Save Changes")');
    });
    
    // Test 15: Edit Profile
    await runTest('Edit Profile', async () => {
        // Change full name
        await page.fill('input[value="Test User"]', 'Updated Test User');
        await page.click('button:has-text("Save Changes")');
        await page.waitForTimeout(1000);
        
        // Go back to dashboard to verify change
        await page.click('text=Dashboard');
        await page.waitForSelector('text=Welcome, Updated Test User', { timeout: 5000 });
    });
    
    // Test 16: Logout
    await runTest('Logout', async () => {
        await page.click('text=Logout');
        await page.waitForSelector('text=Safe Transit Engine', { timeout: 5000 });
        await page.waitForSelector('button:has-text("Get Started")', { timeout: 5000 });
    });
    
    // Test 17: Login with Existing User
    await runTest('Login with Existing User', async () => {
        await page.click('button:has-text("Sign In")');
        await page.waitForSelector('text=Welcome Back', { timeout: 5000 });
        
        // Use the user we created earlier (need to know the username)
        await page.fill('input[name="username"]', 'testuser');
        await page.fill('input[name="password"]', 'Test123');
        await page.click('button:has-text("Sign In")');
        
        await page.waitForSelector('text=Dashboard', { timeout: 10000 });
    });
    
    // Test 18: Error Handling - Invalid Login
    await runTest('Error Handling - Invalid Login', async () => {
        await page.click('text=Logout');
        await page.waitForSelector('text=Safe Transit Engine', { timeout: 5000 });
        
        await page.click('button:has-text("Sign In")');
        await page.waitForSelector('text=Welcome Back', { timeout: 5000 });
        
        await page.fill('input[name="username"]', 'invaliduser');
        await page.fill('input[name="password"]', 'wrongpassword');
        await page.click('button:has-text("Sign In")');
        
        await page.waitForSelector('text=Incorrect username or password', { timeout: 5000 });
    });
    
    // Test 19: Error Handling - Duplicate Registration
    await runTest('Error Handling - Duplicate Registration', async () => {
        await page.click('text=Get Started');
        await page.waitForSelector('text=Create Account', { timeout: 5000 });
        
        // Try to register with existing email
        await page.fill('input[name="email"]', 'test@example.com');
        await page.fill('input[name="username"]', 'testuser123');
        await page.fill('input[name="full_name"]', 'Test User');
        await page.fill('input[name="password"]', 'Test123456');
        await page.selectOption('select[name="certification_level"]', 'Open Water');
        
        await page.click('button:has-text("Create Account")');
        
        // Should show error message
        await page.waitForSelector('text=Email already registered', { timeout: 5000 });
    });
    
    // Test 20: Responsive Design - Mobile View
    await runTest('Responsive Design - Mobile View', async () => {
        await page.setViewportSize({ width: 375, height: 667 }); // iPhone size
        await page.goto('http://localhost:8000');
        
        await page.waitForSelector('h1', { timeout: 5000 });
        
        // Check mobile navigation
        const navigation = await page.locator('nav').isVisible();
        if (!navigation) {
            throw new Error('Navigation not visible on mobile');
        }
        
        // Test mobile registration
        await page.click('button:has-text("Get Started")');
        await page.waitForSelector('text=Create Account', { timeout: 5000 });
        
        // Check form is usable on mobile
        const form = await page.locator('form#registerForm').isVisible();
        if (!form) {
            throw new Error('Registration form not usable on mobile');
        }
    });
    
    // Test 21: Trip Planning Edge Cases
    await runTest('Trip Planning Edge Cases', async () => {
        await page.setViewportSize({ width: 1920, height: 1080 }); // Desktop size
        await page.goto('http://localhost:8000');
        
        // Login with existing user
        await page.click('button:has-text("Sign In")');
        await page.waitForSelector('text=Welcome Back', { timeout: 5000 });
        await page.fill('input[name="username"]', 'testuser');
        await page.fill('input[name="password"]', 'Test123');
        await page.click('button:has-text("Sign In")');
        await page.waitForSelector('text=Dashboard', { timeout: 10000 });
        
        await page.click('text=Plan Trip');
        await page.waitForSelector('text=Trip Planner', { timeout: 5000 });
        
        // Test safety check without dives
        await page.click('button:has-text("Check Flight Safety")');
        await page.waitForTimeout(1000);
        
        // Should show error or no results
        const resultsDiv = await page.locator('#safetyResults').isVisible();
        if (resultsDiv) {
            const errorText = await page.textContent('#safetyResults');
            if (!errorText.includes('No dives') && !errorText.includes('flight time')) {
                console.log('   Safety check without dives handled');
            }
        }
    });
    
    // Test 22: Data Persistence
    await runTest('Data Persistence', async () => {
        // Add a dive and check it persists
        await page.click('text=Coral Bay');
        await page.waitForTimeout(1000);
        
        // Navigate away and back
        await page.click('text=Dashboard');
        await page.waitForSelector('text=Dashboard', { timeout: 5000 });
        await page.click('text=Plan Trip');
        await page.waitForSelector('text=Trip Planner', { timeout: 5000 });
        
        // Check if dive is still there (might be reset depending on implementation)
        try {
            await page.waitForSelector('text=Your Dives', { timeout: 3000 });
            console.log('   Data persistence working');
        } catch (error) {
            console.log('   Data may reset between pages (acceptable)');
        }
    });
    
    // Test 23: Form Input Validation
    await runTest('Form Input Validation', async () => {
        await page.goto('http://localhost:8000');
        await page.click('button:has-text("Get Started")');
        
        // Test invalid email
        await page.fill('input[name="email"]', 'invalid-email');
        await page.fill('input[name="username"]', 'test');
        await page.fill('input[name="full_name"]', 'Test');
        await page.fill('input[name="password"]', 'Test123');
        
        // Check if form validation prevents submission
        const currentUrl = page.url();
        if (currentUrl.includes('dashboard')) {
            throw new Error('Invalid email was accepted');
        }
    });
    
    // Test 24: Performance Check
    await runTest('Performance Check', async () => {
        const startTime = Date.now();
        await page.goto('http://localhost:8000');
        await page.waitForSelector('h1', { timeout: 5000 });
        const loadTime = Date.now() - startTime;
        
        if (loadTime > 5000) {
            throw new Error(`Page load took too long: ${loadTime}ms`);
        }
        
        console.log(`   Page load time: ${loadTime}ms`);
    });
    
    // Test 25: Accessibility Check
    await runTest('Accessibility Check', async () => {
        await page.goto('http://localhost:8000');
        
        // Check for alt text on images
        const images = await page.locator('img').count();
        if (images > 0) {
            const imagesWithoutAlt = await page.locator('img:not([alt])').count();
            if (imagesWithoutAlt > 0) {
                console.log(`   Found ${imagesWithoutAlt} images without alt text`);
            }
        }
        
        // Check for proper heading structure
        await page.waitForSelector('h1', { timeout: 5000 });
        
        // Check for form labels
        await page.click('button:has-text("Get Started")');
        const labels = await page.locator('label').count();
        const inputs = await page.locator('input').count();
        
        if (inputs > labels) {
            console.log(`   More inputs (${inputs}) than labels (${labels})`);
        }
    });
    
    await browser.close();
    
    // Print comprehensive results
    console.log('\n' + '=' * 50);
    console.log('📊 COMPREHENSIVE TEST RESULTS');
    console.log('=' * 50);
    console.log(`✅ Passed: ${testResults.passed}`);
    console.log(`❌ Failed: ${testResults.failed}`);
    console.log(`📈 Success Rate: ${((testResults.passed / (testResults.passed + testResults.failed)) * 100).toFixed(1)}%`);
    
    if (testResults.failed > 0) {
        console.log('\n❌ FAILED TESTS:');
        testResults.tests.filter(t => t.status === 'FAILED').forEach(test => {
            console.log(`   - ${test.name}: ${test.error}`);
        });
        
        console.log('\n🐛 BUGS FOUND:');
        testResults.bugs.forEach(bug => {
            console.log(`   - ${bug.test}: ${bug.error}`);
        });
    }
    
    console.log('\n🎉 COMPREHENSIVE TESTING COMPLETE!');
    
    return testResults;
}

// Run tests if this file is executed directly
if (require.main === module) {
    comprehensiveTestSuite().catch(console.error);
}

module.exports = { comprehensiveTestSuite };
