# 🤖 Botasaurus Captcha Solver Integration

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/omkarcloud/botasaurus?style=social)](https://github.com/omkarcloud/botasaurus)

A robust, ready-to-use Python template for bypassing reCAPTCHA v2, reCAPTCHA v3, and Cloudflare Turnstile in web scraping projects using **Botasaurus** (for anti-detection) and **CapSolver** (for solving).

---

## ✨ Features

- **Seamless Integration:** Combines the power of Botasaurus's anti-detection with CapSolver's API.
- **Multi-Captcha Support:** Ready-to-use examples for reCAPTCHA v2, v3, and Cloudflare Turnstile.
- **Clean Architecture:** Separated configuration, helper functions, and examples for easy maintenance.
- **Token Injection:** Demonstrates how to correctly inject the solved token back into the browser context using Botasaurus.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- A CapSolver API Key (Get yours from the [CapSolver Dashboard](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github&utm_medium=readme&utm_campaign=manus-rewrite-botasaurus))

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/this-repo.git
cd this-repo
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root and add your API key:

```env
# .env
CAPSOLVER_API_KEY=CAP-YOUR_API_KEY_HERE
```

### 4. Run Examples

Execute any of the example scripts located in the `examples/` directory:

```bash
# Example for reCAPTCHA v2
python examples/recaptcha_v2.py

# Example for Cloudflare Turnstile
python examples/turnstile.py
```

---

## 📂 Project Structure

```
.
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── .env (ignored by git)
└── src/
    ├── config.py             # Loads API key and defines endpoints
    └── capsolver_helper.py   # Core functions for creating and polling CapSolver tasks
└── examples/
    ├── recaptcha_v2.py       # Complete example for reCAPTCHA v2
    ├── recaptcha_v3.py       # Complete example for reCAPTCHA v3
    └── turnstile.py          # Complete example for Cloudflare Turnstile
```

---

## ⚙️ Core Implementation

The core logic is split into configuration and the solving helper.

### `src/config.py`

Handles environment variable loading and API endpoint definitions.

```python
# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

class Config:
    """Configuration class for CapSolver integration."""
    CAPSOLVER_API_KEY: str = os.getenv("CAPSOLVER_API_KEY", "")
    CAPSOLVER_API_URL = "https://api.capsolver.com"
    CREATE_TASK_ENDPOINT = f"{CAPSOLVER_API_URL}/createTask"
    GET_RESULT_ENDPOINT = f"{CAPSOLVER_API_URL}/getTaskResult"

    @classmethod
    def validate(cls) -> bool:
        if not cls.CAPSOLVER_API_KEY:
            print("Error: CAPSOLVER_API_KEY not set! Check your .env file.")
            return False
        return True
```

### `src/capsolver_helper.py`

Contains the reusable functions for solving different captcha types.

```python
# src/capsolver_helper.py (Simplified for README)
import time
import requests
from src.config import Config

def _poll_task_result(payload: dict, timeout: int) -> dict:
    # ... (Polling logic as described in the article) ...
    pass

def solve_recaptcha_v2(website_url: str, website_key: str, is_invisible: bool = False) -> dict:
    """Solves reCAPTCHA v2 and returns the gRecaptchaResponse token."""
    if not Config.validate():
        raise Exception("Invalid configuration")
    
    task = {
        "type": "ReCaptchaV2TaskProxyLess",
        "websiteURL": website_url,
        "websiteKey": website_key,
        "isInvisible": is_invisible
    }
    # ... (Task creation and polling via _poll_task_result) ...
    # Returns {'gRecaptchaResponse': '...'}
    pass

def solve_recaptcha_v3(website_url: str, website_key: str, page_action: str) -> dict:
    """Solves reCAPTCHA v3 and returns the gRecaptchaResponse token."""
    # ... (Implementation similar to v2, but with pageAction) ...
    # Returns {'gRecaptchaResponse': '...'}
    pass

def solve_turnstile(website_url: str, website_key: str, action: str = None) -> dict:
    """Solves Cloudflare Turnstile and returns the token."""
    # ... (Implementation similar to v2, but with AntiTurnstileTaskProxyLess) ...
    # Returns {'token': '...'}
    pass
```

---

## 💡 Best Practices

| Practice | Description |
| :--- | :--- |
| **Immediate Use** | Captcha tokens expire quickly (~2 minutes). Inject and submit immediately after receiving the token. |
| **Error Handling** | Always wrap API calls in `try...except` blocks to handle network or API failures gracefully. |
| **Rate Limiting** | Use `driver.sleep()` between actions to mimic human behavior and avoid triggering anti-bot measures. |
| **Configuration** | Use the `Config.validate()` method before making any API calls. |

---

## 🎁 Special Offer

Boost your automation budget instantly! Use bonus code **CAPN** when topping up your CapSolver account to get an extra **5% bonus** on every recharge—with no limits!

Redeem it now in your [CapSolver Dashboard](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github&utm_medium=readme&utm_campaign=manus-rewrite-botasaurus)!

![](https://assets.capsolver.com/prod/posts/aws-waf-captcha-solution/qMMCl6UIh7Ob-d2b5ca33bd970f64a6301fa75ae2eb22.png)

---

## 🤝 Contributing

We welcome contributions! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to submit pull requests, report bugs, and suggest features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Botasaurus GitHub Repository](https://github.com/omkarcloud/botasaurus)
- [CapSolver Dashboard](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github&utm_medium=readme&utm_campaign=manus-rewrite-botasaurus)
- [CapSolver Captcha Detector Extension](https://chromewebstore.google.com/detail/capsolver-captcha-solver)
- [Guide on Identifying Captcha Parameters](https://www.capsolver.com/blog/Extension/identify-any-captcha-and-parameters)
