import { expect, test } from '@playwright/test';

test.describe('Not found page', () => {
  test('unknown URL shows the 404 page', async ({ page }) => {
    await page.goto('/does-not-exist', { waitUntil: 'networkidle' });

    await expect(page).toHaveTitle('Page Not Found - Andy Grails');
    await expect(page.locator('h1.error-code')).toHaveText('404');
    await expect(
      page.getByRole('heading', { name: 'Page Not Found', level: 2 })
    ).toBeVisible();
  });

  test('"Back to Home" button navigates to home', async ({ page }) => {
    await page.goto('/does-not-exist', { waitUntil: 'networkidle' });

    await page.getByRole('button', { name: 'Back to Home' }).click();

    await expect(page).toHaveURL('/');
    await expect(page).toHaveTitle('Andy Grails');
  });
});
