import { expect, test } from '@playwright/test';

test.describe('Search', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });
    await expect(page.locator('.video-card').first()).toBeVisible();
  });

  test('a term from the first card title keeps that card', async ({
    page,
  }) => {
    const cards = page.locator('.video-card');
    const totalCards = await cards.count();
    const firstTitle = await cards
      .first()
      .locator('h2.video-card-heading')
      .innerText();
    const term = firstTitle
      .split(/\s+/)
      .reduce((longest, word) => (word.length > longest.length ? word : longest));

    await page.getByPlaceholder('Filter by title and description').fill(term);
    await page.getByRole('button', { name: 'Search' }).click();

    await expect(cards.first()).toBeVisible();
    await expect(cards.locator('h2.video-card-heading')).toContainText([
      firstTitle,
    ]);
    expect(await cards.count()).toBeLessThanOrEqual(totalCards);
  });

  test('a nonsense term shows no cards', async ({ page }) => {
    await page
      .getByPlaceholder('Filter by title and description')
      .fill('no-such-video-xyzzy');
    await page.getByRole('button', { name: 'Search' }).click();

    await expect(page.locator('.video-card')).toHaveCount(0);
  });

  test('an empty term shows all cards again', async ({ page }) => {
    const cards = page.locator('.video-card');
    const totalCards = await cards.count();
    const filter = page.getByPlaceholder('Filter by title and description');

    await filter.fill('no-such-video-xyzzy');
    await page.getByRole('button', { name: 'Search' }).click();
    await expect(cards).toHaveCount(0);

    await filter.fill('');
    await page.getByRole('button', { name: 'Search' }).click();
    await expect(cards).toHaveCount(totalCards);
  });
});
