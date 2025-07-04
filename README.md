
Simple wrapper for generating mitmproxy request handler script with configurable settings and preset options.

## Prerequisites

Assumes both are installed and available in path:

- mitmproxy
- python3

## Running mitmproxy with generated script settings

Current setting options are:
| Option      | Description                                                        | Blocked Domains         | Blocked Patterns           | Allowed Headers                                    | Header Overrides                                                                                                                                                                                                                                                                         |
|-------------|--------------------------------------------------------------------|------------------------|----------------------------|----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Passthrough | No request modifications                                           | None                   | None                       | ALL                                               | None                                                                                                                                                                                                                                                                                     |
| Secure      | Block known trackers, malware and spam. No cookies, no tracking headers. | COMMON_BLOCKED_DOMAINS | COMMON_TRACKING_PATTERNS   | USER_AGENT, ACCEPT, ACCEPT_ENCODING, ACCEPT_LANGUAGE | USER_AGENT: Mozilla/5.0 (compatible)<br>ACCEPT: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8<br>ACCEPT_ENCODING: gzip, deflate, br<br>ACCEPT_LANGUAGE: en-US,en;q=0.5 |
| Brick wall  | Block known trackers and malware. Remove all headers.              | COMMON_BLOCKED_DOMAINS | COMMON_TRACKING_PATTERNS   | NONE                                              | None                                                                                                                                                                                                                                                                                     |
| Fort Knox   | Blocks all requests.                                               | ALL                    | None                       | NONE                                              | None                                                                                                                                                                                                                                                                                     |

To run mitmproxy with a specific setting, set the `MITM_OPTION` environment variable to the name of the setting.

### Example
```zsh
chmod +x startup.sh
export MITM_OPTION="YourOptionName"
./startup.sh
```