"""
This module contains UI tests for the Mission view feature.
"""
import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ux_tests.ui_tests.common.base import InternalTestBase
from tests.mission_api import MissionAPIDomainMission


class TestMissionView(InternalTestBase):
    """
    Test cases for validating the Mission view and filters.
    """
    def setUp(self):
        super().setUp()
        self.missions_to_delete: List[str] = []
        self.mission_api_handler: MissionAPIDomainMission = MissionAPIDomainMission()

    def __remove_missions(self):
        for mission_template_id in self.missions_to_delete:
            self.mission_api_handler.delete_mission(int(mission_template_id))

    def test_mission_filters(self):
        """
        Checks if the filters are displayed on the web application and if the number of results is more or equal to 5.
        """
        self.driver.maximize_window()
        self.find_and_operate_on_element((By.ID, 'missions'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'task_type'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, '12'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'operator'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'f738a3a2-2f52-478b-adad-8da1f2e92af1'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())
        results_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.MuiTablePagination-displayedRows.css-1chpzqh'))).text
        results_number = int(results_text.split(' ')[2])
        assert results_number >= 5

    def test_navigation(self):
        """
        Tests the navigation and URL consistency across different pages.
        """
        self.driver.maximize_window()
        self.find_and_operate_on_element((By.ID, 'missions'), lambda we: we.click())

        mission_found = False
        mission_id = '7146'

        while not mission_found:
            self.find_and_operate_on_element((By.ID, mission_id), lambda we: we.click())
            mission_found = True
            self.find_and_operate_on_element((By.ID, 'pagination-next-button'), lambda we: we.click())
            url = self.driver.current_url
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(url)
            assert self.driver.current_url == url

    def test_mission_view(self):
        """Tests the gallery functionality."""
        """TODO: Implement mission view tests"""
        pass  # Consider removing if not immediately implementing

    def test_gallery(self):
        """Tests the creation of mission templates."""
        """TODO: Implement gallery tests"""
        pass  # Consider removing if not immediately implementing

    def test_mission_templates_creation(self):
        """
                Tests the creation of mission templates.
        """
        self.driver.maximize_window()
        self.find_and_operate_on_element((By.ID, 'missions'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'Manage mission types'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'Create Template'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'template-next-button'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'select-checkbox-follow_line'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'template-next-button'), lambda we: we.click())
        self.find_and_operate_on_element(
            (By.ID, 'Scan HeightThe height at which the aircraft will take photos (meters).0'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, '5050 meters'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'Scan SpeedThe speed at which the aircraft will fly (m/s).1'),
                                         lambda we: we.click())
        self.find_and_operate_on_element((By.ID, '1010 m/s'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'goal-settings-select-Camera Type'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, '2Thermal Camera'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'template-next-button'), lambda we: we.click())
        random_name = self.faker.name()
        self.find_and_operate_on_element((By.ID, 'create-template-name'), lambda we: we.send_keys(random_name))
        self.find_and_operate_on_element((By.ID, 'create-template-description'), lambda we: we.send_keys(random_name))
        time.sleep(5)
        self.find_and_operate_on_element((By.ID, 'create-template'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'name'), lambda we: we.send_keys(random_name))
        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())
        mission_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//td[contains(text(), '{random_name}')]/..")
            )
        )
        mission_template_id: int = int(mission_element.get_attribute('id'))
        mission_template_data: dict = self.mission_api_handler.get_mission(mission_template_id=mission_template_id)
        print(mission_template_data)
        self.missions_to_delete.append(str(mission_template_id))
        assert random_name == mission_template_data['name']
        print(self.missions_to_delete)
        self.__remove_missions()
        print(self.missions_to_delete)
