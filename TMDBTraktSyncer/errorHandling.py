import traceback
import requests
import time
try:
    from TMDBTraktSyncer import verifyCredentials
except:
    import verifyCredentials

def report_error(error_message):
    github_issue_url = "https://github.com/RileyXX/TMDB-Trakt-Syncer/issues/new?template=bug_report.yml"
    traceback_info = traceback.format_exc()

    print("\n--- ERROR ---")
    print(error_message)
    print("Please submit the error to GitHub with the following information:")
    print("-" * 50)
    print(traceback_info)
    print("-" * 50)
    print(f"Submit the error here: {github_issue_url}")
    print("-" * 50)

def make_trakt_request(url, headers=None, payload=None, max_retries=3):
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': verifyCredentials.trakt_client_id,
            'Authorization': f'Bearer {verifyCredentials.trakt_access_token}'
        }

    retry_delay = 5  # seconds between retries
    retry_attempts = 0

    while retry_attempts < max_retries:
        response = None
        try:
            if payload is None:
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, headers=headers, json=payload)

            if response.status_code in [200, 201, 204]:
                return response  # Request succeeded, return response
            elif response.status_code in [429, 502, 503, 504, 520, 521, 522]:
                # Server overloaded or rate limit exceeded, retry after delay
                retry_attempts += 1
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff for retries
            else:
                # Handle other status codes as needed
                error_message = get_trakt_message(response.status_code)
                print(f"Request failed with status code {response.status_code}: {error_message}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed with exception: {e}")
            return None

    print("Max retry attempts reached with Trakt API, request failed.")
    return None

def get_trakt_message(status_code):
    error_messages = {
        200: "Success",
        201: "Success - new resource created (POST)",
        204: "Success - no content to return (DELETE)",
        400: "Bad Request - request couldn't be parsed",
        401: "Unauthorized - OAuth must be provided",
        403: "Forbidden - invalid API key or unapproved app",
        404: "Not Found - method exists, but no record found",
        405: "Method Not Found - method doesn't exist",
        409: "Conflict - resource already created",
        412: "Precondition Failed - use application/json content type",
        420: "Account Limit Exceeded - list count, item count, etc",
        422: "Unprocessable Entity - validation errors",
        423: "Locked User Account - have the user contact support",
        426: "VIP Only - user must upgrade to VIP",
        429: "Rate Limit Exceeded",
        500: "Server Error - please open a support ticket",
        502: "Service Unavailable - server overloaded (try again in 30s)",
        503: "Service Unavailable - server overloaded (try again in 30s)",
        504: "Service Unavailable - server overloaded (try again in 30s)",
        520: "Service Unavailable - Cloudflare error",
        521: "Service Unavailable - Cloudflare error",
        522: "Service Unavailable - Cloudflare error"
    }

    return error_messages.get(status_code, "Unknown error")

def make_tmdb_request(url, headers=None, payload=None, max_retries=3):
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {verifyCredentials.tmdb_v4_token}'
        }

    retry_delay = 5  # seconds between retries
    retry_attempts = 0

    while retry_attempts < max_retries:
        response = None
        try:
            if payload is None:
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, headers=headers, json=payload)

            status_code = response.status_code
            if status_code in [1, 12, 13]:
                return response  # Request succeeded, return response
            elif status_code in [24, 25, 43, 46, 429]:
                # Rate limit exceeded, retry after delay
                retry_attempts += 1
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff for retries
            elif status_code in [501, 401, 405, 422, 404, 403, 409, 503, 500, 504, 429, 400, 406,
                                 422, 504, 429, 400, 400, 400, 401, 401, 401, 500, 401, 401, 401,
                                 404, 401, 401, 404, 401, 401, 404, 401, 200, 422, 405, 502, 500,
                                 403, 503, 400]:
                # Handle specific status codes as needed
                error_message = get_tmdb_message(status_code)
                print(f"Request failed with status code {status_code}: {error_message}")
                return None
            else:
                # Request failed with an unknown status code
                print(f"Request failed with unknown status code: {status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed with exception: {e}")
            return None

    print("Max retry attempts reached with TMDB API, request failed.")
    return None

def get_tmdb_message(status_code):
    error_messages = {
        1: "Success",
        2: "Invalid service: this service does not exist",
        3: "Authentication failed: You do not have permissions to access the service",
        4: "Invalid format: This service doesn't exist in that format",
        5: "Invalid parameters: Your request parameters are incorrect",
        6: "Invalid id: The pre-requisite id is invalid or not found",
        7: "Invalid API key: You must be granted a valid key",
        8: "Duplicate entry: The data you tried to submit already exists",
        9: "Service offline: This service is temporarily offline, try again later",
        10: "Suspended API key: Access to your account has been suspended, contact TMDB",
        11: "Internal error: Something went wrong, contact TMDB",
        12: "The item/record was updated successfully",
        13: "The item/record was deleted successfully",
        14: "Authentication failed",
        15: "Failed",
        16: "Device denied",
        17: "Session denied",
        18: "Validation failed",
        19: "Invalid accept header",
        20: "Invalid date range: Should be a range no longer than 14 days",
        21: "Entry not found: The item you are trying to edit cannot be found",
        22: "Invalid page: Pages start at 1 and max at 1000. They are expected to be an integer",
        23: "Invalid date: Format needs to be YYYY-MM-DD",
        24: "Your request to the backend server timed out. Try again",
        25: "Your request count is over the allowed limit",
        26: "You must provide a username and password",
        27: "Too many append to response objects: The maximum number of remote calls is 20",
        28: "Invalid timezone: Please consult the documentation for a valid timezone",
        29: "You must confirm this action: Please provide a confirm=true parameter",
        30: "Invalid username and/or password: You did not provide a valid login",
        31: "Account disabled: Your account is no longer active. Contact TMDB if this is an error",
        32: "Email not verified: Your email address has not been verified",
        33: "Invalid request token: The request token is either expired or invalid",
        34: "The resource you requested could not be found",
        35: "Invalid token",
        36: "This token hasn't been granted write permission by the user",
        37: "The requested session could not be found",
        38: "You don't have permission to edit this resource",
        39: "This resource is private",
        40: "Nothing to update",
        41: "This request token hasn't been approved by the user",
        42: "This request method is not supported for this resource",
        43: "Couldn't connect to the backend server",
        44: "The ID is invalid",
        45: "This user has been suspended",
        46: "The API is undergoing maintenance. Try again later",
        47: "The input is not valid"
    }

    return error_messages.get(status_code, "Unknown error")
