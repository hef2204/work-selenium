"""
Module for UI tests for the web application.
"""
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ux_tests.ui_tests.common.base import InternalTestBase


class InternalTestBaseView(InternalTestBase):
    """
    Base class for verifying the existence of elements in the web application.
    """

    def test_side_menu(self):
        """
        Tests the side menu of the web application appearance.
        """
        self.driver.maximize_window()

        # Function to find element with wait
        def find_element_with_wait(locator):
            try:
                return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            except TimeoutException:  # Specify the exception type(s)
                return None

        # Check each element
        mission_element = find_element_with_wait((By.ID, 'missions'))
        assert mission_element is not None and mission_element.is_displayed(), """Mission element not found
         or not displayed"""

        map_element = find_element_with_wait((By.ID, 'maps'))
        assert map_element is not None and map_element.is_displayed(), """Map element not found or not displayed"""

        download_element = find_element_with_wait((By.ID, 'download'))
        assert download_element is not None and download_element.is_displayed(), """Download element not found
         or not displayed"""

        admin_settings_element = find_element_with_wait((By.ID, 'admin-settings'))
        assert admin_settings_element is not None and admin_settings_element.is_displayed(), """Admin settings element
         not found or not displayed"""

        customers_element = find_element_with_wait((By.ID, 'customers'))
        assert customers_element is not None and customers_element.is_displayed(), """Customers element not found
        or not displayed"""

        recognition_element = find_element_with_wait((By.ID, 'recognition'))
        assert recognition_element is not None and recognition_element.is_displayed(), """Recognition element not found
         or not displayed"""

        highlights_element = find_element_with_wait((By.ID, 'highlights'))
        assert highlights_element is not None and highlights_element.is_displayed(), """Highlights element not found
         or not displayed"""

    def test_upper_menu(self):
        """
        Placeholder for testing the upper menu of the web application.
        """
        self.driver.maximize_window()

        def find_element_with_wait(locator):
            try:
                return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            except TimeoutException:  # Specify the exception type(s)
                return None

        # Check each element
        header_profile_button_element = find_element_with_wait((By.ID, 'header-profile-button'))
        assert header_profile_button_element is not None and header_profile_button_element.is_displayed(), """Header
         profile button element not found or not displayed"""
        notifications_button_element = find_element_with_wait((By.ID, 'notifications-button'))
        assert notifications_button_element is not None and notifications_button_element.is_displayed(), """Notifications
         button element not found or not displayed"""
        full_screen_button_element = find_element_with_wait((By.CSS_SELECTOR, "[title='Full screen']"))
        assert full_screen_button_element is not None and full_screen_button_element.is_displayed(), (
            "Full screen button element not found or not displayed"
        )
        # select_language_button_element = find_element_with_wait(
        #     (By.CSS_SELECTOR, "[title='Select language']"))
        # assert select_language_button_element is not None and select_language_button_element.is_displayed(), (
        #     "Select language button element not found or not displayed"
        # )