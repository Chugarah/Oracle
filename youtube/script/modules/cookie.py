import re
import http.cookiejar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time


class CookieUtils:
    @staticmethod
    def convert_edge_cookies_to_netscape(edge_cookies_path, cookies_path):
        edge_cookies = edge_cookies_path

        cookie_jar = http.cookiejar.MozillaCookieJar()

        for cookie in edge_cookies:
            expiry = None
            if 'expiry' in cookie:
                if isinstance(cookie['expiry'], float):
                    expiry = int(cookie['expiry'])
                elif isinstance(cookie['expiry'], str):
                    try:
                        expiry = int(cookie['expiry'])
                    except ValueError:
                        print(
                            f"Could not convert expiry {cookie['expiry']} to an integer")
                        continue

            c = http.cookiejar.Cookie(
                version=0,
                name=cookie['name'],
                value=cookie['value'],
                port=None,
                port_specified=False,
                domain=cookie['domain'],
                domain_specified=bool(cookie['domain']),
                domain_initial_dot=cookie['domain'].startswith('.'),
                path=cookie['path'],
                path_specified=bool(cookie['path']),
                secure=cookie['secure'],
                expires=expiry,
                discard=True,
                comment=None,
                comment_url=False,
                rest={'HttpOnly': cookie['httpOnly']},
                rfc2109=False,
            )

            cookie_jar.set_cookie(c)

        cookie_jar.save(cookies_path, ignore_discard=True)

    @staticmethod
    def generate_cookie_file(url, browser, user_profile, browser_driver_path, auto_auth_cookie, cookie_timer_path):
        driver = None
        cookies = False
        if browser.lower() == 'chrome':
            options = ChromeOptions()
            options.binary_location = f'{browser_driver_path}'
            options.add_argument(f'user-data-dir={user_profile}')
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        else:
            print(
                f"Unsupported browser: {browser}. Only 'chrome' are supported.")

        try:
            driver.get(url)

            # Wait for the cookies to be loaded
            time.sleep(5)

            # Extract the cookies
            cookies = driver.get_cookies()

            # Call the function with the appropriate paths
            CookieUtils.convert_edge_cookies_to_netscape(
                cookies, auto_auth_cookie)

            if CookieUtils.check_login(cookies):
                # Extract the expiration times and save them to a file
                CookieUtils.extract_and_save_expiration_time(
                    cookies, cookie_timer_path)

                cookies = True
            else:
                cookies = False

        except Exception as e:
            cookies = False
            print(f"An error occurred: {str(e)}")

        driver.quit()
        return cookies

    @staticmethod
    def check_login(cookies):
        required_cookies = ['SID', '__Secure-1PAPISID', 'LOGIN_INFO']
        for cookie in cookies:
            if cookie['name'] in required_cookies:
                return True
        return False

    @staticmethod
    def extract_and_save_expiration_time(output, file_path):
        pattern = r"'expiry': (\d+)"
        expiration_times = []

        for item in output:
            match = re.search(pattern, str(item))
            if match:
                expiration_time = match.group(1)
                expiration_times.append(expiration_time)

        with open(file_path, 'w') as file:
            for expiration_time in expiration_times:
                file.write(expiration_time + '\n')
