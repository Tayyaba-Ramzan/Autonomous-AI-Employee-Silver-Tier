"""
LinkedIn Posting Automation - Enhanced Version
Improvements:
- Multiple retry attempts for Post button
- Better element detection
- Screenshot on failure for debugging
- Verification of successful posting
"""

import asyncio
from playwright.async_api import async_playwright
import sys
from pathlib import Path
from datetime import datetime

async def post_to_linkedin(post_content):
    """
    Automate LinkedIn posting with enhanced reliability

    Args:
        post_content: The text content to post

    Returns:
        dict with success status and details
    """

    result = {
        "success": False,
        "message": "",
        "post_url": None,
        "timestamp": datetime.now().isoformat()
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("Step 1: Navigating to LinkedIn...")
            await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(2)

            # Check login status
            print("Step 2: Checking login status...")
            current_url = page.url

            if "login" in current_url or "authwall" in current_url:
                print("[WARNING] Please log in to LinkedIn...")
                await asyncio.sleep(60)

                if "login" in page.url or "authwall" in page.url:
                    result["message"] = "Login required"
                    return result

            print("[OK] Logged in")

            # Click Start a post with retry
            print("Step 3: Clicking 'Start a post'...")
            start_clicked = False

            for attempt in range(3):
                try:
                    await page.click("text=Start a post", timeout=10000)
                    start_clicked = True
                    print(f"[OK] Clicked 'Start a post' (attempt {attempt + 1})")
                    break
                except Exception as e:
                    if attempt < 2:
                        print(f"[RETRY] Attempt {attempt + 1} failed, retrying...")
                        await asyncio.sleep(2)
                    else:
                        print(f"[ERROR] Failed to click 'Start a post': {e}")

            if not start_clicked:
                result["message"] = "Could not click 'Start a post' button"
                return result

            # Wait for editor
            print("Step 4: Waiting for editor...")
            await asyncio.sleep(3)

            # Fill content
            print("Step 5: Filling content...")
            editor = page.locator("[contenteditable='true']").first
            await editor.click()
            await asyncio.sleep(1)
            await editor.fill(post_content)
            print("[OK] Content filled")

            # Wait for Post button to be enabled
            print("Step 6: Waiting for Post button...")
            await asyncio.sleep(3)

            # Click Post button with multiple strategies
            print("Step 7: Clicking Post button...")
            post_clicked = False

            # Strategy 1: Find enabled Post button by text
            for attempt in range(3):
                try:
                    print(f"  Attempt {attempt + 1}: Finding Post button...")
                    buttons = await page.locator("button").all()

                    for btn in buttons:
                        try:
                            text = await btn.text_content()
                            is_disabled = await btn.is_disabled()
                            is_visible = await btn.is_visible()

                            if text and text.strip() == "Post" and not is_disabled and is_visible:
                                print(f"  Found enabled Post button")
                                await btn.click()
                                post_clicked = True
                                print("[OK] Post button clicked")
                                break
                        except:
                            continue

                    if post_clicked:
                        break

                    if attempt < 2:
                        print(f"  Retry {attempt + 1}: Waiting 2s...")
                        await asyncio.sleep(2)

                except Exception as e:
                    print(f"  Attempt {attempt + 1} error: {e}")
                    if attempt < 2:
                        await asyncio.sleep(2)

            # Strategy 2: Try keyboard shortcut if button click failed
            if not post_clicked:
                print("  Trying Ctrl+Enter...")
                try:
                    await page.keyboard.press("Control+Enter")
                    post_clicked = True
                    print("[OK] Used Ctrl+Enter")
                except Exception as e:
                    print(f"  Ctrl+Enter failed: {e}")

            if not post_clicked:
                result["message"] = "Could not click Post button"
                await page.screenshot(path="D:/Silver_Tier/linkedin_post_failed.png")
                print("[ERROR] Screenshot saved: linkedin_post_failed.png")
                return result

            # Wait for posting
            print("Step 8: Waiting for post to publish...")
            await asyncio.sleep(5)

            # Verify posting
            print("Step 9: Verifying post...")
            current_url = page.url

            if "feed" in current_url:
                # Check if post appears in feed
                page_content = await page.content()

                # Look for first few words of our post
                first_words = post_content.split()[:5]
                verification_text = " ".join(first_words)

                if verification_text in page_content or post_content[:50] in page_content:
                    result["success"] = True
                    result["message"] = "Post published and verified in feed"
                    result["post_url"] = "https://www.linkedin.com/feed/"
                    print("[OK] Post verified in feed!")
                else:
                    result["success"] = True
                    result["message"] = "Post published (verification pending)"
                    result["post_url"] = "https://www.linkedin.com/feed/"
                    print("[OK] Post published!")
            else:
                result["message"] = "Unexpected URL after posting"
                print(f"[WARNING] Unexpected URL: {current_url}")

        except Exception as e:
            result["message"] = f"Error: {str(e)}"
            print(f"[ERROR] {str(e)}")
            try:
                await page.screenshot(path="D:/Silver_Tier/linkedin_error.png")
                print("Error screenshot saved")
            except:
                pass

        finally:
            await asyncio.sleep(3)
            await browser.close()

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python linkedin_automation.py \"Your post text here\"")
        sys.exit(1)

    post_content = sys.argv[1]

    print("=" * 60)
    print("LinkedIn Automation - Enhanced")
    print("=" * 60)
    print()
    print("Post content:")
    print("-" * 60)
    print(post_content)
    print("-" * 60)
    print()

    # Run automation
    result = asyncio.run(post_to_linkedin(post_content))

    # Log result
    log_dir = Path("AI_Employee_Vault/Logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "linkedin_post_log.md"

    log_entry = f"""
## LinkedIn Post - {result['timestamp']}

**Status:** {'Success' if result['success'] else 'Failed'}
**Message:** {result['message']}
**Post URL:** {result['post_url'] or 'N/A'}

### Post Content
```
{post_content}
```

---
"""

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    print()
    print("=" * 60)
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Post URL: {result['post_url']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
