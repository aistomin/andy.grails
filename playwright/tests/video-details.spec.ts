import { expect, test } from '@playwright/test';

test.describe('Video details page', () => {
  test('"More ..." on a card opens the details of that video', async ({
    page,
  }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const firstCard = page.locator('.video-card').first();
    await expect(firstCard).toBeVisible();
    const cardTitle = await firstCard
      .locator('h2.video-card-heading')
      .innerText();

    await firstCard.getByRole('link', { name: 'More ...' }).click();

    await expect(page).toHaveURL(/\/details\/\d+$/);
    await expect(page.locator('h2.section-heading')).toHaveText(cardTitle);
    await expect(page).toHaveTitle(`${cardTitle} - Andy Grails`);
  });
});
