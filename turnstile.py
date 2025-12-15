# examples/turnstile.py
from botasaurus.browser import browser, Driver
from src.config import Config
from src.capsolver_helper import solve_turnstile

# Public Turnstile demo site
DEMO_URL = "https://peet.ws/turnstile-test/non-interactive.html"
DEMO_SITEKEY = "0x4AAAAAAABS7vwvV6VFfMcD"

@browser(headless=False)
def solve_turnstile_with_api(driver: Driver, data: dict):
    """Solve Cloudflare Turnstile using CapSolver API and inject the token."""

    url = data.get("url", DEMO_URL)
    site_key = data.get("site_key", DEMO_SITEKEY)

    print(f"Loading page: {url}")
    driver.get(url)
    driver.sleep(3)

    try:
        # Step 1: Solve Turnstile via CapSolver API
        print("Solving Cloudflare Turnstile...")
        solution = solve_turnstile(
            website_url=url,
            website_key=site_key
        )

        token = solution.get("token")
        print(f"Token received. Length: {len(token)}")

        # Step 2: Inject token into the page
        driver.run_js(f"""
            const token = "{token}";

            // Find and fill cf-turnstile-response field
            const responseFields = [
                document.querySelector('[name="cf-turnstile-response"]'),
                document.querySelector('[name="cf_turnstile_response"]'),
                document.querySelector('input[name*="turnstile"]')
            ];

            for (const field of responseFields) {{
                if (field) {{
                    field.value = token;
                    break;
                }}
            }}

            // Ensure the token is injected into the form
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {{
                let field = form.querySelector('[name="cf-turnstile-response"]');
                if (!field) {{
                    field = document.createElement('input');
                    field.type = 'hidden';
                    field.name = 'cf-turnstile-response';
                    form.appendChild(field);
                }}
                field.value = token;
            }});
        """)
        print("Token injected successfully.")

        # Step 3: Submit the form
        submit_btn = driver.select('button[type="submit"], input[type="submit"]')
        if submit_btn:
            submit_btn.click()
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
    result = solve_turnstile_with_api(data={"url": DEMO_URL, "site_key": DEMO_SITEKEY})
    print(f"Demo Result: {result}")
