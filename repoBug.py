import asyncio
from playwright.async_api import async_playwright
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure this is set before any other asyncio operations or Playwright imports
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logger.info("WindowsSelectorEventLoopPolicy has been set for minimal test.")

async def minimal_playwright_test():
    logger.info("Starting minimal Playwright test...")
    async with async_playwright() as p: # Error traces back to here
        browser = None
        try:
            browser = await p.chromium.launch(headless=True) # Attempting to use Playwright's bundled Chromium
            logger.info("Browser launched.")
            page = await browser.new_page()
            logger.info("New page created.")
            await page.goto("https://example.com", timeout=30000)
            logger.info(f"Navigated to example.com, page title: {await page.title()}")
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error during minimal test: {e}", exc_info=True)
        finally:
            if browser and browser.is_connected():
                await browser.close()
                logger.info("Browser closed.")
            else:
                logger.warning("Browser was not successfully launched or already closed.")

if __name__ == "__main__":
    try:
        asyncio.run(minimal_playwright_test())
    except Exception as e:
        logger.critical(f"Top-level error running minimal test: {e}", exc_info=True)
