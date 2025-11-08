import { expect, test } from '@playwright/test';

test.describe('Video catalogue', () => {
  test('shows videos', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const videoHeading = page.getByRole('heading', {
      name: /J\. S\. Bach - Bourrée/i,
      level: 2,
    });

    await expect(videoHeading).toBeVisible();
  });
});

