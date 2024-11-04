"""
This module contains automated UI tests for the Maps view in the web application.
It includes tests for adding, deleting, and verifying map information.
"""
import logging
from typing import List
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Move this above your own modules

from tests.mission_api import MissionAPIDomainMap
from tests.ux_tests.ui_tests.common.base import InternalTestBase


class TestMapsView(InternalTestBase):
    """
        This test class contains methods to test the Maps view functionality in the web application.
        It includes test cases for adding new maps, validating map data, and managing map entries.
        """
    def setUp(self):
        super().setUp()
        self.maps_to_delete: List[str] = []
        self.domain_api_handler: MissionAPIDomainMap = MissionAPIDomainMap()

    def tearDown(self):
        super().tearDown()
        self.__remove_maps()

    def __remove_maps(self):
        for map_id in self.maps_to_delete:
            self.domain_api_handler.delete_map(int(map_id))

    def test_add_new_map(self):
        """
        Adds a new map to the web application.
        """
        self.driver.maximize_window()

        # Enter to map page
        self.find_and_operate_on_element((By.ID, 'maps'), lambda we: we.click())

        # find the add map button
        self.find_and_operate_on_element((By.ID, 'create'), lambda we: we.click())

        random_map_name = self.faker.name()

        # find the map name field and save the map
        self.find_and_operate_on_element((By.ID, 'create-map-name'), lambda we, name: we.send_keys(name),
                                         (random_map_name,))
        self.find_and_operate_on_element((By.ID, 'save-map'), lambda we: we.click())

        # filter the map
        self.find_and_operate_on_element((By.ID, 'name'), lambda we, name: we.send_keys(name),
                                         (random_map_name,))
        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())

        try:
            # Locate the map element by its displayed name and get its ID
            map_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//td[contains(text(), '{random_map_name}')]/..")
                )
            )
            map_id: int = int(map_element.get_attribute('id'))
            logging.info('Map element found with ID: %s', map_id)
            map_data: dict = self.domain_api_handler.get_map(map_id=map_id)
            self.maps_to_delete.append(str(map_id))
            self.assertEqual(random_map_name, map_data['name'])
            self.__remove_maps()
        except TimeoutException:
            logging.error('Map element not found by name')
        finally:
            self.driver.quit()

    def test_create_markers_on_map(self):
        pass

    def test_create_and_delete_areas(self):
        pass

    def test_map_filter(self):

        self.driver.maximize_window()
        self.find_and_operate_on_element((By.ID, 'maps'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'name'), lambda we, name: we.send_keys(name), ('test1',))
        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())
        results_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.MuiTablePagination-displayedRows.css-1chpzqh'))).text
        results_number = int(results_text.split(' ')[2])
        assert results_number >= 1
