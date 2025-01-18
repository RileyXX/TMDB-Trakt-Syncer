import traceback
import requests
from requests.exceptions import ConnectionError, RequestException, Timeout, TooManyRedirects, SSLError, ProxyError
import time
from datetime import datetime, timedelta
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from TMDBTraktSyncer import verifyCredentials as VC
from TMDBTraktSyncer import errorLogger as EL

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

def make_trakt_request(url, headers=None, params=None, payload=None, max_retries=10):

    # Set default headers if none are provided
    if headers is None:
        # Get credentials
        trakt_client_id, _, trakt_access_token, _, _ = VC.prompt_get_credentials()
        
        headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': trakt_client_id,
            'Authorization': f'Bearer {trakt_access_token}'
        }
    
    retry_delay = 1  # Initial delay between retries (in seconds)
    retry_attempts = 0  # Count of retry attempts made
    connection_timeout = 20  # Timeout for requests (in seconds)
    total_wait_time = sum(retry_delay * (2 ** i) for i in range(max_retries))  # Total possible wait time

    # Retry loop to handle network errors or server overload scenarios
    while retry_attempts < max_retries:
        response = None
        try:
            # Send GET or POST request depending on whether a payload is provided
            if payload is None:
                if params:
                    # GET request with query parameters
                    response = requests.get(url, headers=headers, params=params, timeout=connection_timeout)
                else:
                    # GET request without query parameters
                    response = requests.get(url, headers=headers, timeout=connection_timeout)
            else:
                # POST request with JSON payload
                response = requests.post(url, headers=headers, json=payload, timeout=connection_timeout)

            # If request is successful, return the response
            if response.status_code in [200, 201, 204]:
                return response
            
            # Handle retryable server errors and rate limit exceeded
            elif response.status_code in [429, 500, 502, 503, 504, 520, 521, 522]:
                retry_attempts += 1  # Increment retry counter

                # Respect the 'Retry-After' header if provided, otherwise use default delay
                retry_after = int(response.headers.get('Retry-After', retry_delay))
                if response.status_code != 429:
                    remaining_time = total_wait_time - sum(retry_delay * (2 ** i) for i in range(retry_attempts))
                    print(f"   - Server returned {response.status_code}. Retrying after {retry_after}s... "
                          f"({retry_attempts}/{max_retries}) - Time remaining: {remaining_time}s")
                    EL.logger.warning(f"Server returned {response.status_code}. Retrying after {retry_after}s... "
                                      f"({retry_attempts}/{max_retries}) - Time remaining: {remaining_time}s")

                time.sleep(retry_after)  # Wait before retrying
                retry_delay *= 2  # Apply exponential backoff for retries
            
            else:
                # Handle non-retryable HTTP status codes
                status_message = get_trakt_message(response.status_code)
                error_message = f"Request failed with status code {response.status_code}: {status_message}"
                print(f"   - {error_message}")
                EL.logger.error(f"{error_message}. URL: {url}")
                return response  # Exit with failure for non-retryable errors

        # Handle Network errors (connection issues, timeouts, SSL, etc.)
        except (ConnectionError, Timeout, TooManyRedirects, SSLError, ProxyError) as network_error:
            retry_attempts += 1  # Increment retry counter
            remaining_time = total_wait_time - sum(retry_delay * (2 ** i) for i in range(retry_attempts))
            print(f"   - Network error: {network_error}. Retrying ({retry_attempts}/{max_retries})... "
                  f"Time remaining: {remaining_time}s")
            EL.logger.warning(f"Network error: {network_error}. Retrying ({retry_attempts}/{max_retries})... "
                              f"Time remaining: {remaining_time}s")
            
            time.sleep(retry_delay)  # Wait before retrying
            retry_delay *= 2  # Apply exponential backoff for retries

        # Handle general request-related exceptions (non-retryable)
        except requests.exceptions.RequestException as req_err:
            error_message = f"Request failed with exception: {req_err}"
            print(f"   - {error_message}")
            EL.logger.error(error_message, exc_info=True)
            return None  # Exit on non-retryable exceptions

    # If all retries are exhausted, log and return failure
    error_message = "Max retry attempts reached with Trakt API, request failed."
    print(f"   - {error_message}")
    EL.logger.error(error_message)
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

def make_tmdb_request(url, headers=None, payload=None, max_retries=5):
    """
    Makes an HTTP request to the TMDB API, with retry logic for certain error codes and connection issues.
    Retries on network issues or server errors, with exponential backoff.

    :param url: The URL for the TMDB API request
    :param headers: Optional headers (defaults to including authorization token)
    :param payload: Optional JSON payload for POST requests
    :param max_retries: Maximum number of retry attempts in case of failure
    :return: The API response or None if all retries fail
    """
    
    
    if headers is None:
        # Get credentials
        _, _, _, _, tmdb_access_token = VC.prompt_get_credentials()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {tmdb_access_token}'  # Assuming VC.tmdb_access_token is valid
        }

    retry_delay = 1  # Initial delay between retries in seconds
    retry_attempts = 0
    connection_timeout = 20  # Timeout for each request in seconds

    while retry_attempts < max_retries:
        response = None
        try:        
            # Send GET or POST request based on payload
            if payload is None:
                response = requests.get(url, headers=headers, timeout=connection_timeout)
            else:
                response = requests.post(url, headers=headers, json=payload, timeout=connection_timeout)

            if response is None:
                # If the response is None, treat it as retryable
                retry_attempts += 1
                time_remaining = sum(retry_delay * (2 ** i) for i in range(max_retries - retry_attempts))
                error_message = (
                    f"Received no response (None). Retrying {retry_attempts}/{max_retries}. "
                    f"Time remaining: {time_remaining}s"
                )
                print(f"   - {error_message}")
                EL.logger.error(error_message)
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue  # Skip the current loop and retry

            status_code = response.status_code

            if status_code in [200, 201]:
                return response  # Success! Return the response.
            elif status_code in [504, 429, 502, 503]:
                # Retryable errors, such as rate limiting or server issues
                retry_attempts += 1
                time_remaining = sum(retry_delay * (2 ** i) for i in range(max_retries - retry_attempts))
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                # Skip logging rate limit errors
                if status_code != 429:
                    status_message = get_tmdb_message(status_code)
                    error_message = (
                        f"Request failed with status code {status_code}: {status_message}. "
                        f"Retrying {retry_attempts}/{max_retries}. Time remaining: {time_remaining}s"
                    )
                    print(f"   - {error_message}")
                    EL.logger.error(error_message)
            else:
                # Non-retryable errors, exit loop and return None
                status_message = get_tmdb_message(status_code)
                error_message = f"Request failed with status code {status_code}: {status_message}"
                print(f"   - {error_message}")
                EL.logger.error(error_message)
                return None

        except (ConnectionError, Timeout, TooManyRedirects, SSLError, ProxyError) as network_error:
            # Handle network errors or timeouts that are retryable
            retry_attempts += 1
            time_remaining = sum(retry_delay * (2 ** i) for i in range(max_retries - retry_attempts))
            error_message = (
                f"Network error: {network_error}. Retrying {retry_attempts}/{max_retries}. "
                f"Time remaining: {time_remaining}s"
            )
            print(f"   - {error_message}")
            EL.logger.error(error_message, exc_info=True)
            time.sleep(retry_delay)  # Wait before retrying
            retry_delay *= 2  # Exponential backoff for retries

        except RequestException as e:
            # Handle other non-network related exceptions (e.g., HTTP errors)
            error_message = f"Request failed with exception: {e}"
            print(f"   - {error_message}")
            EL.logger.error(error_message, exc_info=True)
            return None

    # If max retries reached, log the error and return None
    error_message = "Max retry attempts reached with TMDB API, request failed."
    print(f"   - {error_message}")
    EL.logger.error(error_message)
    return None

def get_tmdb_message(status_code):
    """
    Returns a message based on the status code returned from the TMDB API.

    :param status_code: The status code returned by the TMDB API
    :return: A string with the corresponding error message
    """
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

    # Default to 'Unknown error' if status code is not found in the dictionary
    return error_messages.get(status_code, "Unknown error")
    
# Function to filter out items that share the same Title, Year, and Type
# AND have non-matching TMDB_ID values
def filter_mismatched_items(trakt_list, tmdb_list):
    # Define the keys to be used for comparison
    comparison_keys = ['Title', 'Year', 'Type', 'TMDB_ID']

    # Group items by (Title, Year, Type)
    trakt_grouped = {}
    for item in trakt_list:
        if all(key in item for key in comparison_keys):
            key = (item['Title'], item['Year'], item['Type'])
            trakt_grouped.setdefault(key, set()).add(item['TMDB_ID'])

    tmdb_grouped = {}
    for item in tmdb_list:
        if all(key in item for key in comparison_keys):
            key = (item['Title'], item['Year'], item['Type'])
            tmdb_grouped.setdefault(key, set()).add(item['TMDB_ID'])

    # Find conflicting items (same Title, Year, Type but different TMDB_IDs)
    conflicting_items = {
        key for key in trakt_grouped.keys() & tmdb_grouped.keys()  # Only consider shared keys
        if trakt_grouped[key] != tmdb_grouped[key]  # Check if TMDB_IDs differ
    }
    
    # Filter out conflicting items from both lists
    filtered_trakt_list = [
        item for item in trakt_list if (item['Title'], item['Year'], item['Type']) not in conflicting_items
    ]
    filtered_tmdb_list = [
        item for item in tmdb_list if (item['Title'], item['Year'], item['Type']) not in conflicting_items
    ]

    return filtered_trakt_list, filtered_tmdb_list