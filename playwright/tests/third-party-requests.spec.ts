import { expect, test, type Page } from '@playwright/test';

/**
 * Sending a visitor's IP address to a third party without consent is a GDPR
 * problem for a `.de` site, so a page must only load resources from the app's
 * own origin. These tests record every request the main frame makes while a
 * page loads and fail if any of them goes somewhere else.
 *
 * Requests made from inside the YouTube iframes are ignored for now. They are
 * covered by https://github.com/aistomin/andy.grails.frontend/issues/676 and
 * this check should be tightened once that is decided.
 */
test.describe('Third-party requests', () => {
  test('home page loads resources from its own origin only', async ({
    page,
    baseURL,
  }) => {
    const foreignRequests = recordForeignRequests(page, baseURL!);

    await page.goto('/', { waitUntil: 'networkidle' });

    expect(foreignRequests, thirdPartyHint(foreignRequests)).toEqual([]);
  });

  test('video details page loads resources from its own origin only', async ({
    page,
    baseURL,
  }) => {
    await page.goto('/', { waitUntil: 'networkidle' });
    const detailsPath = await page
      .locator('a[href^="/details/"]')
      .first()
      .getAttribute('href');
    expect(
      detailsPath,
      'home page should link to a video details page'
    ).not.toBeNull();

    const foreignRequests = recordForeignRequests(page, baseURL!);

    await page.goto(detailsPath!, { waitUntil: 'networkidle' });

    expect(foreignRequests, thirdPartyHint(foreignRequests)).toEqual([]);
  });
});

/**
 * Starts collecting the URLs of all requests the main frame of the page sends
 * to an origin other than the app's own. Requests made by child frames (the
 * YouTube embeds) are skipped.
 */
function recordForeignRequests(page: Page, appUrl: string): string[] {
  const appOrigin = new URL(appUrl).origin;
  const foreignRequests: string[] = [];
  page.on('request', (request) => {
    if (request.frame() !== page.mainFrame()) {
      return;
    }
    if (new URL(request.url()).origin !== appOrigin) {
      foreignRequests.push(request.url());
    }
  });
  return foreignRequests;
}

function thirdPartyHint(foreignRequests: string[]): string {
  const urls = foreignRequests.join('\n');
  return `The page sent requests to third-party hosts:\n${urls}`;
}
