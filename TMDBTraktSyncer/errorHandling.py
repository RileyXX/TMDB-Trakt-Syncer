import traceback
import requests
import time
try:
    from TMDBTraktSyncer import verifyCredentials
except ImportError:
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
            elif response.status_code in [429, 500, 502, 503, 504, 520, 521, 522]:
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
            if status_code in [200, 201]:
                return response  # Request succeeded, return response
            elif status_code in [504, 429, 502, 503]:
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
        200: "Success",
        501: "Invalid service: this service does not exist",
        401: "Authentication failed: You do not have permissions to access the service",
        405: "Invalid format: This service doesn't exist in that format",
        422: "Invalid parameters: Your request parameters are incorrect",
        404: "Invalid id: The pre-requisite id is invalid or not found",
        401: "Invalid API key: You must be granted a valid key",
        403: "Duplicate entry: The data you tried to submit already exists",
        503: "Service offline: This service is temporarily offline, try again later",
        401: "Suspended API key: Access to your account has been suspended, contact TMDB",
        500: "Internal error: Something went wrong, contact TMDB",
        201: "The item/record was updated successfully",
        200: "The item/record was deleted successfully",
        401: "Authentication failed",
        500: "Failed",
        401: "Device denied",
        401: "Session denied",
        400: "Validation failed",
        406: "Invalid accept header",
        422: "Invalid date range: Should be a range no longer than 14 days",
        200: "Entry not found: The item you are trying to edit cannot be found",
        400: "Invalid page: Pages start at 1 and max at 1000. They are expected to be an integer",
        400: "Invalid date: Format needs to be YYYY-MM-DD",
        504: "Your request to the backend server timed out. Try again",
        429: "Your request count (#) is over the allowed limit of (40)",
        400: "You must provide a username and password",
        400: "Too many append to response objects: The maximum number of remote calls is 20",
        400: "Invalid timezone: Please consult the documentation for a valid timezone",
        400: "You must confirm this action: Please provide a confirm=true parameter",
        401: "Invalid username and/or password: You did not provide a valid login",
        401: "Account disabled: Your account is no longer active. Contact TMDB if this is an error",
        401: "Email not verified: Your email address has not been verified",
        401: "Invalid request token: The request token is either expired or invalid",
        404: "The resource you requested could not be found",
        401: "Invalid token",
        401: "This token hasn't been granted write permission by the user",
        404: "The requested session could not be found",
        401: "You don't have permission to edit this resource",
        401: "This resource is private",
        200: "Nothing to update",
        422: "This request token hasn't been approved by the user",
        405: "This request method is not supported for this resource",
        502: "Couldn't connect to the backend server",
        500: "The ID is invalid",
        403: "This user has been suspended",
        503: "The API is undergoing maintenance. Try again later",
        400: "The input is not valid"
    }

    return error_messages.get(status_code, "Unknown error")

