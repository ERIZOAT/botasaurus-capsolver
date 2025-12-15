# src/capsolver_helper.py
import time
import requests
from src.config import Config

def _poll_task_result(payload: dict, timeout: int = 120) -> dict:
    """Internal function to poll the CapSolver API for the task result."""
    
    # 1. Create task
    response = requests.post(Config.CREATE_TASK_ENDPOINT, json=payload)
    result = response.json()

    if result.get("errorId") and result.get("errorId") != 0:
        raise Exception(f"Failed to create task: {result.get('errorDescription')}")

    task_id = result.get("taskId")

    # 2. Poll for result
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(2)

        result_payload = {
            "clientKey": Config.CAPSOLVER_API_KEY,
            "taskId": task_id
        }

        response = requests.post(Config.GET_RESULT_ENDPOINT, json=result_payload)
        result = response.json()

        if result.get("status") == "ready":
            return result.get("solution", {})

        elif result.get("status") == "failed":
            raise Exception(f"Task failed: {result.get('errorDescription')}")

    raise Exception(f"Timeout: No result obtained after {timeout} seconds")


def solve_recaptcha_v2(
    website_url: str,
    website_key: str,
    is_invisible: bool = False,
    timeout: int = 120
) -> dict:
    """Solve reCAPTCHA v2 using CapSolver API."""

    if not Config.validate():
        raise Exception("Invalid configuration - check your API key")

    task = {
        "type": "ReCaptchaV2TaskProxyLess",
        "websiteURL": website_url,
        "websiteKey": website_key,
    }

    if is_invisible:
        task["isInvisible"] = True

    payload = {
        "clientKey": Config.CAPSOLVER_API_KEY,
        "task": task
    }
    
    return _poll_task_result(payload, timeout)


def solve_recaptcha_v3(
    website_url: str,
    website_key: str,
    page_action: str,
    min_score: float = 0.3,
    timeout: int = 120
) -> dict:
    """Solve reCAPTCHA v3 using CapSolver API."""

    if not Config.validate():
        raise Exception("Invalid configuration - check your API key")

    task = {
        "type": "ReCaptchaV3TaskProxyLess",
        "websiteURL": website_url,
        "websiteKey": website_key,
        "pageAction": page_action,
        "minScore": min_score
    }

    payload = {
        "clientKey": Config.CAPSOLVER_API_KEY,
        "task": task
    }
    
    return _poll_task_result(payload, timeout)


def solve_turnstile(
    website_url: str,
    website_key: str,
    action: str = None,
    cdata: str = None,
    timeout: int = 120
) -> dict:
    """Solve Cloudflare Turnstile using CapSolver API."""

    if not Config.validate():
        raise Exception("Invalid configuration - check your API key")

    task = {
        "type": "AntiTurnstileTaskProxyLess",
        "websiteURL": website_url,
        "websiteKey": website_key,
    }

    metadata = {}
    if action:
        metadata["action"] = action
    if cdata:
        metadata["cdata"] = cdata

    if metadata:
        task["metadata"] = metadata

    payload = {
        "clientKey": Config.CAPSOLVER_API_KEY,
        "task": task
    }
    
    return _poll_task_result(payload, timeout)
