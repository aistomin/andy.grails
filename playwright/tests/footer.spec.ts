import { expect, test } from '@playwright/test';

test.describe('Footer', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });
  });

  test('has footer element', async ({ page }) => {
    const footer = page.locator('footer.footer');
    await expect(footer).toBeVisible();
  });

  test('has copyright text', async ({ page }) => {
    const copyright = page.locator('footer .footer-center p');
    await expect(copyright).toBeVisible();
    await expect(copyright).toContainText('2025 Andy Grails');
  });

  test.describe('Navigation links', () => {
    test('has Privacy link', async ({ page }) => {
      const privacyLink = page.locator('footer a[href="/privacy"]');
      await expect(privacyLink).toBeVisible();
      await expect(privacyLink).toHaveText('Privacy');
    });

    test('has Imprint link', async ({ page }) => {
      const imprintLink = page.locator('footer a[href="/imprint"]');
      await expect(imprintLink).toBeVisible();
      await expect(imprintLink).toHaveText('Imprint');
    });

    test('has Developer link', async ({ page }) => {
      const developerLink = page
        .locator('footer .footer-left a')
        .filter({ hasText: 'Developer' });
      await expect(developerLink).toBeVisible();
    });

    test('has Support link', async ({ page }) => {
      const supportLink = page
        .locator('footer .footer-left a')
        .filter({ hasText: 'Support' });
      await expect(supportLink).toBeVisible();
      await expect(supportLink).toHaveAttribute('target', '_blank');
    });

    test('Privacy link navigates to privacy page', async ({ page }) => {
      const privacyLink = page.locator('footer a[href="/privacy"]');
      await privacyLink.click();
      await expect(page).toHaveURL('/privacy');
    });

    test('Imprint link navigates to imprint page', async ({ page }) => {
      const imprintLink = page.locator('footer a[href="/imprint"]');
      await imprintLink.click();
      await expect(page).toHaveURL('/imprint');
    });
  });

  test.describe('Social media links', () => {
    test('has YouTube link', async ({ page }) => {
      const youtubeLink = page.getByRole('link', { name: 'YouTube' });
      await expect(youtubeLink).toBeVisible();
      await expect(youtubeLink).toHaveAttribute('target', '_blank');
      await expect(youtubeLink).toHaveAttribute('rel', 'noopener noreferrer');
    });

    test('has Instagram link', async ({ page }) => {
      const instagramLink = page.getByRole('link', { name: 'Instagram' });
      await expect(instagramLink).toBeVisible();
      await expect(instagramLink).toHaveAttribute('target', '_blank');
      await expect(instagramLink).toHaveAttribute('rel', 'noopener noreferrer');
    });

    test('has Facebook link', async ({ page }) => {
      const facebookLink = page.getByRole('link', { name: 'Facebook' });
      await expect(facebookLink).toBeVisible();
      await expect(facebookLink).toHaveAttribute('target', '_blank');
      await expect(facebookLink).toHaveAttribute('rel', 'noopener noreferrer');
    });
  });
});
