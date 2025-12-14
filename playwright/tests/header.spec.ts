import { expect, test } from '@playwright/test';

test.describe('Header', () => {
  test('has header element', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const header = page.locator('header.brand-name');
    await expect(header).toBeVisible();
  });

  test('has logo image', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const logo = page.locator('header img.brand-logo');
    await expect(logo).toBeVisible();
    await expect(logo).toHaveAttribute('src', '/assets/logo.svg');
  });

  test('has brand text', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const brandText = page.locator('header .brand-text');
    await expect(brandText).toBeVisible();
    await expect(brandText).toHaveText('Andy Grails');
  });

  test('logo link navigates to home', async ({ page }) => {
    // Start from a different page
    await page.goto('/privacy', { waitUntil: 'networkidle' });

    const logoLink = page.locator('header a.logo-link');
    await logoLink.click();

    await expect(page).toHaveURL('/');
  });

  test('brand text click navigates to home', async ({ page }) => {
    // Start from a different page
    await page.goto('/imprint', { waitUntil: 'networkidle' });

    const brandText = page.locator('header .brand-text');
    await brandText.click();

    await expect(page).toHaveURL('/');
  });
});
