#!/usr/bin/env python
# coding: utf-8

import os
import re
import time
from datetime import datetime
import json
from pathlib import Path
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,\
StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import yaml


def create_url_with_keys(base_url, keys):
    for key in keys:
        base_url += key + "%20"
    url = base_url[:-3]
    return url


# get superlinks from element.
def get_superlinks(element):
    links = []
    ele_html = element.get_attribute("outerHTML")
    soup = BeautifulSoup(ele_html, "html.parser")
    a_links = soup.find_all("a")
    # Iterate through the anchor elements and print their href attributes
    for a_link in a_links:
        link = a_link.get("href")
        links.append(link)
    return links

def check_comments(list_text):
    for text in list_text:
        text = text.lower()
        # print(text)
        if text.endswith((" comments", " comment")):
            return True, text
    return False, ""

def post_xpath(n_th_post):
    return (f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]"
           f"/div[1]/div[2]/div/div/div/div/div/div[{n_th_post+1}]")


class FacebookScraper:
    def __init__(self) -> None:
        """
        Initializes the FacebookScraper class.
        """
        self.root_dir = Path(
            os.getcwd(),
        )

        # self.my_user_name = None
        # self.my_password = None
        self.options = Options()
        # self.options.add_argument('--headless')
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-extensions")
        self.options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_setting_values.notifications": 1,
            },
        )
        self.comment_reply_titles = []
        self.badges = ["Top fan", "Author"]
        self.driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install(),
            ),
            options=self.options,
        )

    def login(self, url) -> None:
        try:
            # Load credentials from secure source
            self._load_credentials()
            # self.my_user_name = credentials['username']
            # self.my_password = credentials['password']
        except KeyError as e:
            print(f"Missing credential: {e}")
            return

        # Navigate to Facebook and handle cookies
        self._navigate_to_facebook(url)

        # Login with user credentials
        self._login_with_credentials()

        # Wait for successful login
        self._wait_for_successful_login()

    def _load_credentials(self):
        try:
            # Load credentials from YAML file
            path = self.root_dir / "secret.yaml"
            with open(path) as f:
                secret = yaml.load(f, Loader=yaml.FullLoader)
                self.my_user_name = secret["credentials"]["username"]
                self.my_password = secret["credentials"]["password"]
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error loading YAML confidential file: {e}")
            # return

        # Replace this with your actual implementation
        # return {'username': self.my_user_name, 'password': self.my_password}

    def _navigate_to_facebook(self, url) -> None:
        self.driver.get(url)
        WebDriverWait(self.driver, 2)
        try:
            cookies_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[text()="Allow all cookies"]'),
                ),
            )
            cookies_button.click()
        except TimeoutException:
            print(
                "Allow all cookies button not found within the specified time.",
            )

    def _login_with_credentials(self) -> None:
        try:
            email_field = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "email")),
            )
            password_field = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "pass")),
            )
            email_field.send_keys(self.my_user_name)
            password_field.send_keys(self.my_password)
            login_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "login")),
            )
            login_button.click()
        except NoSuchElementException as e:
            print(f"Login element not found: {e}")
        except Exception as e:
            print(f"Login error: {e}")

    def _wait_for_successful_login(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "facebook")),
            )
        except TimeoutException:
            print(
                "Login confirmation timeout! Unable to verify successful login.",
            )

    def position_the_element(
        self,
        element: WebElement,
    ) -> None:
        window_height = self.driver.execute_script(
            "return window.innerHeight;",
        )

        # Get the bottom position of the element relative to the viewport
        element_bottom = self.driver.execute_script(
            "return arguments[0].getBoundingClientRect().bottom;",
            element,
        )

        # Calculate the scroll distance needed to align the bottom of the
        # element with the bottom of the screen
        scroll_distance = element_bottom - window_height

        if scroll_distance > 0:
            # Scroll to the calculated distance
            self.driver.execute_script(
                "window.scrollBy(0, arguments[0]);",
                scroll_distance,
            )
            time.sleep(3)

    def find_elements_with_wait(
        self,
        type_of_path: str,
        element_xpath: str,
    ) -> WebElement | None:
        try:
            elements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(
                    (getattr(By, type_of_path), element_xpath)
                ),
            )
            return elements

        except TimeoutException:
            print(f"Timeout waiting for elements with XPath: {element_xpath}")
            return None

    def find_element_with_wait(
        self,
        type_of_path: str,
        element_xpath: str,
    ) -> WebElement | None:
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (getattr(By, type_of_path), element_xpath)
                ),
            )
            return element

        except TimeoutException:
            print(f"Timeout waiting for element with XPath: {element_xpath}")
            return None

    def click_element_with_retry(self) -> None:
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//span[text()="Top comments" or text()="Most relevant"]',
                    ),
                ),
            )
            element.click()
        except Exception as e:
            time.sleep(3)
            print(f"An error occurred when clicking 'Top comments': {e}")

    def click_all_comments_button(self) -> None:
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//span[text()="All comments" or text()="Oldest"]',
                    ),
                ),
            ).click()
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking on all comments button: {e}")

    def locate_scrollbar(self) -> WebElement:
        try:
            time.sleep(2)
            scrollbar_xpath = (
                "//*[starts-with(@id,"
                ' "mount_0")]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div'
                "/div/div/div/div/div/div[2]/div[5]"
            )
            scrollbar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, scrollbar_xpath)),
            )
            return scrollbar
        except Exception as e:
            print(f"An error occurred when locating the scroll bar element: {e}")

    def extent_comment_contains(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        try:
            # Wait for the div elements with the specified conditions
            div_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        (
                            '//div[@role="button" and (contains(text(), "See more")'
                            ' or contains(text(), " replies") or'
                            ' contains(text(), "1 reply"))]'
                        ),
                    ),
                ),
            )
        except Exception:
            div_elements = []
        # Wait for the span elements with the specified condition
        try:
            span_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//span[contains(text(), "View more comments")]'),
                ),
            )
            time.sleep(5)
        except Exception:
            span_elements = []

        extent_buttons = div_elements + span_elements
        if extent_buttons == []:
            pass
        elif len(extent_buttons) == 1:
            extent_buttons[0].click()
        elif len(extent_buttons) > 1:
            for button in extent_buttons:
                try:
                    button.click()
                except Exception as e:
                    print("some button not clickable ", e)

        if self.is_scroll_at_end():
            return "No more extensions"
        return "continue"

    def extract_and_save_comment(
        self,
        row_comments: list[WebElement],
        comments: list[dict[str, str]],
        list_row_comments: list,
    ):
        for row_comment in row_comments:
            if row_comment.text in ["Write a comment…", ""]:
                pass
            else:
                list_row_comments.append(row_comment.text.split("\n"))

        for list_result in list_row_comments:
            comment = {}
            if list_result == "":
                continue
            comment["Commentor"] = list_result[0]
            comment["text"] = list_result[1]
            comment["date of Comment"] = list_result[2]

            comments.append(comment)
        return comments

    def close_popup(self):
        try:
            close_buttons = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '[aria-label="Close"]')
                ),
            )

            if not close_buttons:
                print("No close buttons found.")
                return

            for button in reversed(close_buttons):
                try:
                    button.click()
                    time.sleep(2)
                    print("Popup closed successfully.")
                    return
                except Exception as e:
                    print(f"Error occurred when closing pop-up container, try alternative: {e}")

            print("All attempts to close popup failed.")
        except Exception as e:
            print(f"Error occurred while locating close buttons: {e}")

    def is_scroll_at_end(self):
        if not hasattr(self, "driver") or not self.driver:
            raise ValueError("WebDriver instance not provided.")

        # Get the current scroll position
        current_scroll_position = self.driver.execute_script(
            "return window.scrollY;",
        )

        # Get the total height of the body
        total_body_height = self.driver.execute_script(
            "return document.body.scrollHeight;",
        )

        # Define a threshold (adjust as needed)
        threshold = 20

        # Check if the current scroll position is close to the end
        return (
            current_scroll_position
            + self.driver.execute_script(
                "return window.innerHeight;",
            )
            >= total_body_height - threshold
        )

    def get_extension_elements(self) -> List[WebElement]:
        try:
            self.find_elements_with_wait(
                "XPATH", "//span[contains(text(), 'View ') and contains(text(), ' repl')]"
            )
            elements_with_view_replies = self.find_elements_with_wait(
                "XPATH", "//span[contains(text(), 'View ') and contains(text(), ' repl')]"
            )
        except:
            elements_with_view_replies = []
        
        try:
            self.find_elements_with_wait(
                "XPATH", "//div[contains(text(), 'See more')]"
            )
            elements_with_see_more = self.find_elements_with_wait(
                "XPATH", "//div[contains(text(), 'See more')]"
            )

        except:
            elements_with_see_more = []
        return elements_with_view_replies + elements_with_see_more

    def post_xpath(self, n_th_post):
        return f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[{n_th_post+1}]"

    def collect_comments_replies(self, comment_element):
        # scraper.comment_reply_titles.append(comment_element.get_attribute("aria-label"))
        comment_contain = {}
        comment_element = scraper.find_element_with_wait(
            "XPATH",
            f'//div[contains(@aria-label, "{comment_element.get_attribute("aria-label")}")]',
        )
        results = self.extract_data_from_list(comment_element.text.split("\n"))
        comment_contain["Commenter"] = results[0]
        comment_contain["Comment Date"] = results[1]
        comment_contain["Text"] = results[2]
        reply_elements = comment_element.find_elements(
            By.XPATH,
            './parent::*/following-sibling::div//descendant-or-self::div[contains(@aria-label, "Reply by ")]',
        )
        reply_section = []
        if len(reply_elements) == 0:
            comment_contain["Reply"] = []
        else:
            for reply_element in reply_elements:
                reply_contains = {}
                if (
                    reply_element.get_attribute("aria-label")
                    in self.comment_reply_titles
                ):
                    continue
                # reply = self.collect_comments_replies(reply_element)
                reply_results = scraper.extract_data_from_list(
                    reply_element.text.split("\n")
                )
                reply_contains["Commenter"] = reply_results[0]
                reply_contains["Comment Date"] = reply_results[1]
                reply_contains["Text"] = reply_results[2]
                reply_contains["Reply"] = self.collect_comments_replies(reply_element)
                reply_section.append(reply_contains)
            comment_contain["Reply"] = reply_section
        return comment_contain

    def extract_data_from_list(self, arr: list):
        # corner case:
        like_index = arr.index("Like")
        date_index = like_index - 1
        date = arr[date_index]
        if arr[0] in self.badges:
            author = arr[1]
            text = arr[2:date_index]
        else:
            author = arr[0]
            date = arr[date_index]
            text = arr[1:date_index]
        return author, date, text

    def get_extension(self, elements):
        for element in elements:
            try:
                # Scroll to the element to ensure it's in view
                ActionChains(self.driver).move_to_element(element).perform()
                time.sleep(2)
                # Click on the element
                try:
                    element.click()

                    time.sleep(2)

                except StaleElementReferenceException:
                    # Retry the click if the element is stale
                    print("Stale element, retrying click")
                    continue

            except Exception as e:
                # Handle exceptions or retry logic if needed
                print(f"Error when getting extensions: {e}")
                continue










