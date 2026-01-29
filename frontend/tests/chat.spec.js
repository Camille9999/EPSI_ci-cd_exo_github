const { test, expect } = require('@playwright/test');

test('chatbot answers a question', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('input[placeholder="Posez une question..."]')).toBeVisible();
  await page.fill('input[placeholder="Posez une question..."]', 'Quelle est la capitale de la France ?');
  await page.click('button[type="submit"]');
  // Wait for bot response (should appear after user message)
  await expect(page.locator('#messages .bot')).toHaveText(/Paris|Bot:/, { timeout: 10000 });
});
