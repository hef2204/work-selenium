from selenium.webdriver.common.by import By

from tests.ux_tests.ui_tests.common.base import InternalTestBase


class TestUserPreferences(InternalTestBase):

    def setUp(self):
        super().setUp()
        self.driver.maximize_window()

    def test_profile_changes(self):
        """
            Test to change the name and job title in the user profile.
        """
        random_name = self.faker.name()
        random_title = self.faker.job()
        self.find_and_operate_on_element((By.ID, 'header-profile-button'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'header-profile'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, 'user-edit'), lambda we: we.click())
        self.find_and_operate_on_element((By.ID, ':r0:'), lambda we: we.send_keys(random_name), clear_field=True)
        self.find_and_operate_on_element((By.ID, ':r1:'), lambda we: we.send_keys(random_title), clear_field=True)
        self.find_and_operate_on_element((By.ID, 'user-save'), lambda we: we.click())
        name = self.driver.find_element(By.ID, ':r0:').get_attribute('value')
        job_title = self.driver.find_element(By.ID, ':r1:').get_attribute('value')
        print(name, job_title)
        assert name == random_name
        assert job_title == random_title
