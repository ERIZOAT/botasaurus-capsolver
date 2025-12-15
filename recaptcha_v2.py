# examples/recaptcha_v2.py
from botasaurus.browser import browser, Driver
from src.config import Config
from src.capsolver_helper import solve_recaptcha_v2

# Google's official reCAPTCHA v2 demo site
DEMO_URL = "https://www.google.com/recaptcha/api2/demo"
DEMO_SITEKEY = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"

@browser(headless=False)
def solve_recaptcha_v2_with_api(driver: Driver, data: dict):
    """Solve reCAPTCHA v2 using CapSolver API and inject the token."""

    url = data.get("url", DEMO_URL)
    site_key = data.get("site_key", DEMO_SITEKEY)

    print(f"Loading page: {url}")
    driver.get(url)
    driver.sleep(2)

    try:
        # Step 1: Solve captcha via CapSolver API
        print("Solving reCAPTCHA v2...")
        solution = solve_recaptcha_v2(
            website_url=url,
            website_key=site_key
        )

        token = solution.get("gRecaptchaResponse")
        print(f"Token received. Length: {len(token)}")

        # Step 2: Inject token into the page
        driver.run_js(f"""
            // Set the hidden textarea value
            const responseField = document.querySelector('[name="g-recaptcha-response"]');
            if (responseField) {{
                responseField.value = "{token}";
            }}

            // Trigger callback if available
            if (typeof ___grecaptcha_cfg !== 'undefined') {{
                try {{
                    const clients = ___grecaptcha_cfg.clients;
                    for (const key in clients) {{
                        const client = clients[key];
                        if (client && client.callback) {{
                            client.callback("{token}");
                        }}
                    }}
                }} catch (e) {{}}
            }}
        """)
        print("Token injected successfully.")

        # Step 3: Submit the form
        submit_button = driver.select('input[type="submit"]')
        if submit_button:
            submit_button.click()
            driver.sleep(5) # Wait for submission result
            print("Form submitted. Check the browser for success message.")
        else:
            print("Submit button not found.")

        return {"success": True, "token_length": len(token)}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Run the demo
    result = solve_recaptcha_v2_with_api(data={"url": DEMO_URL, "site_key": DEMO_SITEKEY})
    print(f"Demo Result: {result}")
