import { test as base } from '@playwright/test';

// Override the base test to automatically log all browser errors to the terminal
export const test = base.extend({
  page: async ({ page }, use) => {
    page.on('pageerror', (exception) => {
      console.error(Uncaught exception in browser: " + exception + ");
    });
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.error(Browser console error: " + msg.text() + ");
      }
    });
    await use(page);
  },
});
export { expect } from '@playwright/test';