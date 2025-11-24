import { expect, test } from '@playwright/test';

test.describe('Home page', () => {
  test('shows videos', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const videoHeading = page.getByRole('heading', {
      name: /J\. S\. Bach - Bourrée/i,
      level: 2,
    });

    await expect(videoHeading).toBeVisible();
  });

  test('has correct page title', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });
    await expect(page).toHaveTitle('Andy Grails');
  });
});
