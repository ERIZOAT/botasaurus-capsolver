# examples/recaptcha_v3.py
from botasaurus.browser import browser, Driver
from src.config import Config
from src.capsolver_helper import solve_recaptcha_v3

# Note: Finding a public reCAPTCHA v3 demo that allows external token injection is difficult.
# This example is conceptual and assumes a target site's parameters.
DEMO_URL = "https://www.google.com/recaptcha/api2/demo" # Placeholder
DEMO_SITEKEY = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-" # Placeholder
DEMO_ACTION = "homepage" # Placeholder action

@browser(headless=False)
def solve_recaptcha_v3_with_api(driver: Driver, data: dict):
    """Solve reCAPTCHA v3 using CapSolver API and inject the token."""

    url = data.get("url", DEMO_URL)
    site_key = data.get("site_key", DEMO_SITEKEY)
    page_action = data.get("action", DEMO_ACTION)

    print(f"Loading page: {url}")
    driver.get(url)
    driver.sleep(2)

    try:
        # Step 1: Solve captcha via CapSolver API
        print(f"Solving reCAPTCHA v3 with action: {page_action}...")
        solution = solve_recaptcha_v3(
            website_url=url,
            website_key=site_key,
            page_action=page_action
        )

        token = solution.get("gRecaptchaResponse")
        print(f"Token received. Length: {len(token)}")

        # Step 2: Inject token into the page
        driver.run_js(f"""
            const token = "{token}";
            // v3 typically uses a callback function to receive the token
            if (typeof grecaptcha !== 'undefined' && grecaptcha.getResponse) {{
                // Simulate the grecaptcha.execute callback
                grecaptcha.getResponse = () => token;
            }}
            // Also inject into the hidden field for compatibility
            const responseField = document.querySelector('[name="g-recaptcha-response"]');
            if (responseField) {{
                responseField.value = token;
            }}
        """)
        print("Token injected successfully.")

        # Step 3: Trigger form submission (often automatic with v3)
        # You might need to manually trigger the form submission or the action that uses the token
        # For a real-world scenario, this step would be site-specific.
        print("Token injected. Manual submission or site-specific action required.")

        return {"success": True, "token_length": len(token)}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Run the demo
    result = solve_recaptcha_v3_with_api(data={"url": DEMO_URL, "site_key": DEMO_SITEKEY, "action": DEMO_ACTION})
    print(f"Demo Result: {result}")
