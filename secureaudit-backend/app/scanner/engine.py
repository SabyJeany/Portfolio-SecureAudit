import requests
import ssl
import socket
import time
from urllib.parse import urlparse
"""
scanner/engine.py — Web security scan enginec
This file implements the ScanEngine class, which performs passive security checks
"""




class ScanEngine:
    """
    Main security scan engine for SecureAudit.
    
    Uses only passive HTTP requests — no exploitation
    or attack attempts are made against the target site.
    
    Example usage:
        engine = ScanEngine("https://example.com")
        findings = engine.run_scan()
    """

    def __init__(self, url: str, timeout: int = 10):
        """
        Initialize the scanner with the target URL.
        
        Args:
            url: the URL to analyze (must start with http:// or https://)
            timeout: maximum delay in seconds for each request
        """
        self.url = url
        self.timeout = timeout
        self.parsed = urlparse(url)
        self.hostname = self.parsed.hostname
        self.findings = []

    def run_scan(self) -> list:
        """
        Run all security checks on the target URL.
        
        Returns:
            list of findings — each finding is a dictionary
            with check_name, status, severity, description, recommendation
        """
        self.findings = []
        self.findings.append(self.check_https())
        self.findings.extend(self.check_headers())
        self.findings.append(self.check_ssl())
        self.findings.append(self.check_redirects())
        self.findings.append(self.check_robots())
        return self.findings

    def check_https(self) -> dict:
        """
        Check if the site uses HTTPS.
        
        HTTPS encrypts data between the browser and the server.
        Without HTTPS, data travels in plain text and can be intercepted.
        
        Returns:
            finding dict with status pass/fail and severity critical/info
        """
        is_https = self.parsed.scheme == 'https'
        return {
            "check_name": "HTTPS",
            "status": "pass" if is_https else "fail",
            "severity": "critical" if not is_https else "info",
            "description": (
                "The site uses HTTPS — communications are encrypted."
                if is_https else
                "The site does not use HTTPS — data is transmitted in plain text."
            ),
            "recommendation": (
                "No action needed."
                if is_https else
                "Install an SSL certificate and redirect all HTTP traffic to HTTPS."
            )
        }

    def check_headers(self) -> list:
        """
        Check the presence of HTTP security headers.
        
        Headers checked:
        - Content-Security-Policy (CSP): prevents XSS attacks
        - X-Frame-Options: prevents clickjacking
        - X-Content-Type-Options: prevents MIME sniffing
        - Strict-Transport-Security (HSTS): enforces HTTPS
        - Referrer-Policy: controls referrer information leakage
        
        Returns:
            list of findings, one per header checked
        """
        findings = []
        try:
            response = requests.get(self.url, timeout=self.timeout, verify=False)
            headers = response.headers

            security_headers = [
                {
                    "header": "Content-Security-Policy",
                    "check_name": "CSP Header",
                    "severity": "critical",
                    "description_fail": "Content-Security-Policy header is missing. Your site is vulnerable to XSS attacks.",
                    "description_pass": "Content-Security-Policy header is present.",
                    "recommendation": "Add: Content-Security-Policy: default-src 'self'; script-src 'self'"
                },
                {
                    "header": "X-Frame-Options",
                    "check_name": "X-Frame-Options Header",
                    "severity": "medium",
                    "description_fail": "X-Frame-Options header is missing. Your site may be vulnerable to clickjacking.",
                    "description_pass": "X-Frame-Options header is present.",
                    "recommendation": "Add: X-Frame-Options: DENY"
                },
                {
                    "header": "X-Content-Type-Options",
                    "check_name": "X-Content-Type-Options Header",
                    "severity": "medium",
                    "description_fail": "X-Content-Type-Options header is missing. Browsers may interpret files incorrectly.",
                    "description_pass": "X-Content-Type-Options header is present.",
                    "recommendation": "Add: X-Content-Type-Options: nosniff"
                },
                {
                    "header": "Strict-Transport-Security",
                    "check_name": "HSTS Header",
                    "severity": "medium",
                    "description_fail": "Strict-Transport-Security (HSTS) header is missing. Browsers may connect via HTTP.",
                    "description_pass": "HSTS header is present — browsers will always use HTTPS.",
                    "recommendation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains"
                },
                {
                    "header": "Referrer-Policy",
                    "check_name": "Referrer-Policy Header",
                    "severity": "low",
                    "description_fail": "Referrer-Policy header is missing. Sensitive URLs may be leaked to third parties.",
                    "description_pass": "Referrer-Policy header is present.",
                    "recommendation": "Add: Referrer-Policy: strict-origin-when-cross-origin"
                },
            ]

            for h in security_headers:
                present = h["header"] in headers
                findings.append({
                    "check_name": h["check_name"],
                    "status": "pass" if present else "fail",
                    "severity": h["severity"] if not present else "info",
                    "description": h["description_pass"] if present else h["description_fail"],
                    "recommendation": "No action needed." if present else h["recommendation"]
                })

        except requests.RequestException as e:
            findings.append({
                "check_name": "HTTP Headers",
                "status": "fail",
                "severity": "critical",
                "description": f"Could not reach the site: {str(e)}",
                "recommendation": "Make sure the URL is correct and the site is accessible."
            })

        return findings

    def check_ssl(self) -> dict:
        """
        Check the validity of the SSL certificate.
        
        An expired or invalid SSL certificate exposes users to
        man-in-the-middle attacks and browser security warnings.
        
        Returns:
            finding dict with certificate status and days until expiration
        """
        if self.parsed.scheme != 'https':
            return {
                "check_name": "SSL Certificate",
                "status": "fail",
                "severity": "critical",
                "description": "No SSL certificate — site is not using HTTPS.",
                "recommendation": "Install an SSL certificate (Let's Encrypt is free)."
            }

        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.hostname, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()
                    expire_date = ssl.cert_time_to_seconds(cert['notAfter'])
                    days_left = (expire_date - time.time()) / 86400

                    if days_left < 0:
                        return {
                            "check_name": "SSL Certificate",
                            "status": "fail",
                            "severity": "critical",
                            "description": "SSL certificate has expired!",
                            "recommendation": "Renew your SSL certificate immediately."
                        }
                    elif days_left < 30:
                        return {
                            "check_name": "SSL Certificate",
                            "status": "fail",
                            "severity": "medium",
                            "description": f"SSL certificate expires in {int(days_left)} days.",
                            "recommendation": "Renew your SSL certificate soon."
                        }
                    else:
                        return {
                            "check_name": "SSL Certificate",
                            "status": "pass",
                            "severity": "info",
                            "description": f"SSL certificate is valid — expires in {int(days_left)} days.",
                            "recommendation": "No action needed."
                        }

        except ssl.SSLError as e:
            return {
                "check_name": "SSL Certificate",
                "status": "fail",
                "severity": "critical",
                "description": f"SSL error: {str(e)}",
                "recommendation": "Fix your SSL certificate configuration."
            }
        except Exception as e:
            return {
                "check_name": "SSL Certificate",
                "status": "fail",
                "severity": "medium",
                "description": f"Could not verify SSL certificate: {str(e)}",
                "recommendation": "Make sure your SSL certificate is properly configured."
            }

    def check_redirects(self) -> dict:
        """
        Check that HTTP redirects to HTTPS.
        
        Without this redirect, users may access the site
        over unencrypted HTTP without knowing it.
        
        Returns:
            finding dict indicating whether redirect is configured
        """
        try:
            http_url = f"http://{self.hostname}"
            response = requests.get(
                http_url,
                timeout=self.timeout,
                allow_redirects=True,
                verify=False
            )
            final_url = response.url

            if final_url.startswith('https://'):
                return {
                    "check_name": "HTTP to HTTPS Redirect",
                    "status": "pass",
                    "severity": "info",
                    "description": "HTTP traffic is correctly redirected to HTTPS.",
                    "recommendation": "No action needed."
                }
            else:
                return {
                    "check_name": "HTTP to HTTPS Redirect",
                    "status": "fail",
                    "severity": "medium",
                    "description": "HTTP is not redirected to HTTPS. Users may browse the site unencrypted.",
                    "recommendation": "Configure a 301 redirect from HTTP to HTTPS on your server."
                }

        except Exception as e:
            return {
                "check_name": "HTTP to HTTPS Redirect",
                "status": "fail",
                "severity": "low",
                "description": f"Could not check redirect: {str(e)}",
                "recommendation": "Make sure HTTP to HTTPS redirect is configured."
            }

    def check_robots(self) -> dict:
        """
        Check for the presence of robots.txt.
        
        robots.txt tells search engines which pages not to index.
        Its absence may expose sensitive URLs to public indexing.
        
        Returns:
            finding dict indicating whether robots.txt exists
        """
        try:
            robots_url = f"{self.parsed.scheme}://{self.hostname}/robots.txt"
            response = requests.get(robots_url, timeout=self.timeout, verify=False)

            if response.status_code == 200:
                return {
                    "check_name": "robots.txt",
                    "status": "pass",
                    "severity": "info",
                    "description": "robots.txt file is present.",
                    "recommendation": "No action needed."
                }
            else:
                return {
                    "check_name": "robots.txt",
                    "status": "fail",
                    "severity": "low",
                    "description": "robots.txt file is missing.",
                    "recommendation": "Create a robots.txt file to control search engine indexing."
                }

        except Exception as e:
            return {
                "check_name": "robots.txt",
                "status": "fail",
                "severity": "low",
                "description": f"Could not check robots.txt: {str(e)}",
                "recommendation": "Make sure your site is accessible and has a robots.txt file."
            }