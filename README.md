# MITM Script Generator

Script generator wrapper for mitm proxy. Easily enable outgoing request handlers for blocking domains and manipulating headers.

Use secure settings to block ads, known trackers, malware and spam.

## How it works

Generates a script that filters headers and blocks domains based on selected option. The script is then run with mitmproxy to intercept and modify requests.

## Prerequisites

Assumes both are installed and available in path:

- mitmproxy
- python3

You can install mitmproxy on mac via brew:
```zsh
brew install mitmproxy
```

See [mitmproxy docs](https://docs.mitmproxy.org/stable/overview-installation/) for more details.

## Running mitmproxy with generated script settings

Current setting options are:
| Option                | Description                                                                                                                        | Blocked Domains         | Blocked Patterns           | Allowed Headers                                                                 | Header Overrides                                                                                                                                                                                                                                                        | Notes |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------|------------------------|----------------------------|--------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| Passthrough           | No request modifications. All requests and headers are allowed.                                                                   | None                   | None                       | ALL                                                                            | None                                                                                                                                                                                                                                                                   | No filtering. |
| Lax                   | Blocks known trackers, ads, spam, and malware. All headers are allowed and unmodified.                                            | COMMON_BLOCKED_DOMAINS | COMMON_TRACKING_PATTERNS   | ALL                                                                            | None                                                                                                                                                                                                                                                                   | Good for most browsing. |
| Secure with cookies   | Blocks known trackers, malware, and spam. Allows cookies and some session headers, but no tracking headers.                       | COMMON_BLOCKED_DOMAINS | COMMON_TRACKING_PATTERNS   | USER_AGENT, ACCEPT, ACCEPT_ENCODING, ACCEPT_LANGUAGE, AUTHORIZATION, COOKIE | USER-AGENT: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 | Allows cookies, but blocks most tracking. |
| Secure                | Blocks known trackers, malware, and spam. No cookies or tracking headers are allowed.                                             | COMMON_BLOCKED_DOMAINS | COMMON_TRACKING_PATTERNS   | USER_AGENT, ACCEPT, ACCEPT_ENCODING, ACCEPT_LANGUAGE, AUTHORIZATION            | USER_AGENT: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 | May break sites due to strict header removal. |
| Brick wall            | Blocks known trackers and malware. Removes all headers from requests.                                                             | COMMON_BLOCKED_DOMAINS | COMMON_TRACKING_PATTERNS   | NONE                                                                           | None                                                                                                                                                                                                                                                                   | Extreme blocking, most sites will break. |
| Fort Knox             | Blocks all requests, regardless of domain or headers.                                                                             | ALL                    | None                       | NONE                                                                           | None                                                                                                                                                                                                                                                                   | No requests allowed. |

**Note:** Header overrides now only apply if the header is present in the request.

To run mitmproxy with a specific setting, set the `MITM_OPTION` environment variable to the name of the setting.

### Example
```zsh
chmod +x run.sh
export MITM_OPTION="Secure with cookies"
./run.sh
```