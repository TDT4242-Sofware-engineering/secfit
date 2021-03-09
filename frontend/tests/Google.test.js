describe('SecFit', () => {
  beforeAll(async () => {
    await page.goto('http://secfit.vassbo.as');
  });

  it('should be titled "SecFit"', async () => {
    const navTitle = await page.$(".navbar-brand")
    const title = await page.evaluate((title) => title.innerText, navTitle)
    expect(title).toBe("SecFit")
  });
});

