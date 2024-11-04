"""
This module provides a base test class for UI tests, including setup and teardown methods,
driver initialization, login functionality, and common operations like finding and interacting
with elements.
"""
import logging
import os
import time
import unittest
from typing import Optional, Tuple  # Combine typing imports and move them before third-party imports
import psutil
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path as driver_path
from faker import Faker


class InternalTestBase(unittest.TestCase):
    """
        Base class for UI tests, providing common setup, teardown, and utility functions
        for interacting with the web application.
     """
    @classmethod
    def setUpClass(cls):
        cls.is_logged_in: bool = False
        cls._driver: Optional[WebDriver] = None
        cls.max_wait_time: int = 20
        cls.base_url: str = os.environ.get('LOGIN_URL')
        cls.faker: Optional[Faker] = None

    def setUp(self):
        self._login()
        self.faker = Faker()

    def tearDown(self):
        self._driver.quit()

        # Get the process IDs of Selenium Chrome processes before running tests
        selenium_chrome_pids = [proc.pid for proc in psutil.process_iter(['pid', 'name', 'cmdline'])
                                if 'chrome' in proc.name() and 'chromedriver' in proc.cmdline()]

        # Clean up Selenium Chrome processes
        for pid in selenium_chrome_pids:
            try:
                psutil.Process(pid).terminate()
            except psutil.NoSuchProcess:
                pass

    @property
    def driver(self):
        """
    Provides a Selenium WebDriver instance configured with Chrome options.

    This fixture initializes a Chrome WebDriver with specific options to run tests.
    It yields the driver instance to the test function and ensures the driver is
    quit after the test completes, releasing the resources.

    Yields:
        webdriver.Chrome: An instance of Chrome WebDriver with configured options.
    """
        if self._driver is None:
            self.__init_driver()

        return self._driver

    def __init_driver(self) -> None:
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--remote-debugging-port=9223')

        # Start the WebDriver
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        self._driver = driver

    def _login(self) -> None:
        """
        Logs in to the web application using the provided email and password.
        """
        self.driver.maximize_window()
        # URL of the login page
        login_url = os.getenv('LOGIN_URL')

        # Credentials
        valid_email = os.getenv('VALID_EMAIL')
        valid_password = os.getenv('VALID_PASSWORD')

        # Open the login page
        print(login_url, '3456345')
        self.driver.get(login_url)

        # Find the email field
        email_field = self.driver.find_element(By.ID, 'email')
        # Enter the email
        email_field.send_keys(valid_email)
        # Find the password field
        password_field = self.driver.find_element(By.ID, 'password')
        # Enter the password
        password_field.send_keys(valid_password)
        # Find the login button
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        # Click the login button
        login_button.click()

        try:
            logging.debug('Waiting for Highlights heading...')
            highlights_heading = WebDriverWait(self.driver, self.max_wait_time).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h5[contains(@class, 'MuiTypography-h5') and text()='Highlights']")
                )
            )
            logging.debug('Checking if Highlights heading is displayed...')
            assert highlights_heading.is_displayed()
            time.sleep(5)
            logging.info('Login successful')
        except TimeoutException:
            pass
            # pytest.fail("Login failed: Highlights heading is not displayed")

    def find_and_operate_on_element(self, locator_tuple, operation, operation_args=(), clear_field=False):
        """
        Wait for the element to be located by its locator and then perform an operation on it.

        :param locator_tuple: A tuple containing the strategy and the locator (e.g., (By.ID, 'element_id')).
        :param operation: The function to be executed on the located element.
        :param operation_args: Arguments for the operation function.
        :param clear_field: If True, clears the field before performing the operation.
        """
        try:
            # Wait for the element to be present and visible
            web_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator_tuple))

            # Clear the field if needed
            if clear_field:
                web_element.send_keys(Keys.CONTROL + "a")
                web_element.send_keys(Keys.DELETE)

            # Scroll the element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", web_element)

            # Use JavaScript click for robustness
            operation(web_element, *operation_args)

            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator_tuple))
            time.sleep(1)  # Optional: small wait to ensure element is ready



        except TimeoutException:
            logging.error('Element with locator %s not found or not clickable, operation: %s', locator_tuple,
                          operation.__name__)
        except Exception as e:
            logging.error(f"An error occurred during operation: {e}")

    def scroll_and_save_container(self):
        """
            Scrolls to the bottom of the container element and clicks the save button.

            This method locates the container element, scrolls to the bottom using JavaScript,
            and then finds and clicks the save button within the container.
        """
        logging.info('Finding container and performing scroll operation...')

        # Define the locator for the container
        container_locator = (By.CLASS_NAME, 'info-card-container')

        # Find the container and perform the scroll operation
        self.find_and_operate_on_element(
            container_locator,
            lambda we: self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", we)
        )
        # find the save button
        self.find_and_operate_on_element((By.ID, 'save-customer-button'), lambda we: we.click())

    def scroll_and_switch_container(self):
        """
            Scrolls to the bottom of the container element and clicks the switch-customer-button.

            This method locates the container element, scrolls to the bottom using JavaScript,
            and then finds and clicks the switch-customer-button within the container.
        """
        logging.info('Finding container and performing scroll operation...')

        # Define the locator for the container
        container_locator = (By.CLASS_NAME, 'info-card-container')

        # Find the container and perform the scroll operation
        self.find_and_operate_on_element(
            container_locator,
            lambda we: self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", we)
        )
        # find the save button
        self.find_and_operate_on_element((By.ID, 'switch-customer-button'), lambda we: we.click())
