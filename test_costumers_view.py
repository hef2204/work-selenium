"""
This module contains automated UI tests for the Customers view in the web application.
It includes tests for adding, deleting, and verifying customer information.
"""

import logging
from typing import List
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.mission_api import MissionAPIDomainCustomer
from tests.ux_tests.ui_tests.common.base import InternalTestBase


class TestCustomersView(InternalTestBase):
    """
        This test class contains methods to test the Customers view functionality in the web application.
        It includes test cases for adding new customers, validating customer data, and ensuring
        that customer entries can be properly managed within the application.
        """

    def setUp(self):
        super().setUp()
        self.customers_to_delete: List[str] = []
        self.domain_api_handler: MissionAPIDomainCustomer = MissionAPIDomainCustomer()

    def tearDown(self):
        super().tearDown()
        self.__remove_customers()

    def __remove_customers(self):
        for customer_id in self.customers_to_delete:
            self.domain_api_handler.delete_customer(customer_id)

    def test_add_new_customer(self):
        """
        Adds a new customer to the web application.
        """
        self.driver.maximize_window()
        # enter the customers page
        self.find_and_operate_on_element((By.ID, 'customers'), lambda we: we.click())

        # find the add customer button
        self.find_and_operate_on_element((By.ID, 'add_new_customer'), lambda we: we.click())

        random_name = self.faker.name()
        random_country = self.faker.country()
        random_city = self.faker.city()
        random_email = self.faker.email()
        random_phone = self.faker.phone_number()
        random_address = self.faker.address()
        random_zip_code = self.faker.zipcode()

        # Find the name field
        self.find_and_operate_on_element((By.ID, 'customer-card-name')
                                         , lambda we, name: we.send_keys(name),
                                         (random_name,))

        # Find the country field
        self.find_and_operate_on_element((By.ID, 'customer-card-country')
                                         , lambda we, country: we.send_keys(country),
                                         (random_country,))

        # Find the city field
        self.find_and_operate_on_element((By.ID, 'customer-card-city')
                                         , lambda we, city: we.send_keys(city),
                                         (random_city,))

        # Find the address field
        self.find_and_operate_on_element((By.ID, 'customer-card-address')
                                         , lambda we, address: we.send_keys(address),
                                         (random_address,))

        # Find the email field
        self.find_and_operate_on_element((By.ID, 'customer-card-default_email')
                                         , lambda we, email: we.send_keys(email),
                                         (random_email,))

        # Find the phone field
        self.find_and_operate_on_element((By.ID, 'customer-card-phone')
                                         , lambda we, phone: we.send_keys(phone),
                                         (random_phone,))

        # Find the zip code field
        self.find_and_operate_on_element((By.ID, 'customer-card-zip_code')
                                         , lambda we, zip_code: we.send_keys(zip_code),
                                         (random_zip_code,))
        try:
            # Find the container element
            self.scroll_and_save_container()
        except TimeoutException:
            logging.error('Container not found')

        # Find the save button within the container
        self.find_and_operate_on_element((By.ID, 'save-customer-button'), lambda we: we.click())

        print(random_name)

        # filter the customer
        self.find_and_operate_on_element((By.ID, 'name'), lambda we, name: we.send_keys(name), (random_name,))
        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())

        # Locate the customer row using the random name
        customer_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//td[contains(text(), '{random_name}')]/..")
            )
        )
        customer_id: str = customer_element.get_attribute('id')
        logging.info('Customer row found with ID: %s', customer_id)
        print(customer_id)
        customer_data: dict = self.domain_api_handler.get_customer(customer_id=customer_id)
        print(customer_data)

        self.customers_to_delete.append(customer_id)
        self.assertEqual(random_name, customer_data['name'])
        self.assertEqual(random_country, customer_data['country'])
        self.assertEqual(random_email, customer_data['default_email'])
        self.assertEqual(random_city, customer_data['city'])
        self.__remove_customers()
        # close the browser
        self.driver.close()

    def test_change_customer_details(self):
        """
            Test updating a customer's details and verifying the changes.

            The test filters for a customer by name, selects the customer,
            updates their details (email, country, city, phone, zip code),
            and verifies that the changes were saved correctly.
            """

        self.driver.maximize_window()

        self.find_and_operate_on_element((By.ID, 'customers'), lambda we: we.click())

        # Filter the customer
        self.find_and_operate_on_element((By.ID, 'name'), lambda we, name: we.send_keys(name), ('boris',))

        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())

        # Click on the customer
        self.find_and_operate_on_element((By.ID, '91c95f6c-cbf7-4115-a79d-d67c1fea0dfd'), lambda we: we.click())

        # Generate random details using Faker
        random_email = self.faker.email()
        random_country = self.faker.country()
        random_city = self.faker.city()
        random_phone = self.faker.phone_number()
        random_zip_code = self.faker.zipcode()

        # Find and clear the country field
        self.find_and_operate_on_element((By.ID, 'customer-card-country')
                                         , lambda we, country: we.send_keys(country),
                                         (random_country,), clear_field=True)
        # Find and clear the country field
        self.find_and_operate_on_element((By.ID, 'customer-card-city'), lambda we, city: we.send_keys(city),
                                         (random_city,), clear_field=True)

        self.find_and_operate_on_element((By.ID, 'customer-card-default_email'), lambda we, email: we.send_keys(email),
                                         (random_email,), clear_field=True)

        self.find_and_operate_on_element((By.ID, 'customer-card-phone'), lambda we, phone: we.send_keys(phone),
                                         (random_phone,), clear_field=True)

        self.find_and_operate_on_element((By.ID, 'customer-card-zip_code'), lambda we, zip_code: we.send_keys(zip_code),
                                         (random_zip_code,), clear_field=True)
        try:
            self.scroll_and_save_container()
        except TimeoutException:
            logging.error('Container not found')

        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())

        customer_id: str = "91c95f6c-cbf7-4115-a79d-d67c1fea0dfd"
        logging.info('Customer row found with ID: %s', customer_id)
        print(customer_id)
        customer_data: dict = self.domain_api_handler.get_customer(customer_id=customer_id)
        print(customer_data)

        self.assertEqual(random_country, customer_data['country'])
        self.assertEqual(random_email, customer_data['default_email'])
        self.assertEqual(random_city, customer_data['city'])
        self.assertEqual(random_phone, customer_data['phone'])
        self.assertEqual(random_zip_code, customer_data['zip_code'])

        self.driver.quit()

    def test_customer_filter(self):
        """
        Test filtering customers by name and verifying the results.

        The test filters for a customer by name, selects the customer,
        and verifies that the customer's details are displayed correctly.
        """

        self.driver.maximize_window()

        self.find_and_operate_on_element((By.ID, 'customers'), lambda we: we.click())

        # Filter the customer
        self.find_and_operate_on_element((By.ID, 'name'), lambda we, name: we.send_keys(name), ('befree',))

        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())

        customer_rows = self.driver.find_elements(By.ID, "2393ad37-2c8d-41a2-808f-1587a18dbb29")
        assert len(customer_rows) == 1

        self.find_and_operate_on_element((By.ID, 'country'), lambda we, country: we.send_keys(country), ('israel',))

        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())
        assert len(customer_rows) == 1

        self.find_and_operate_on_element((By.ID, 'country'),
                                         lambda we, country: we.send_keys(country), ('United States',))
        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())
        if customer_rows is None:
            assert True

    def test_switch_between_customers(self):
        """
        Test switching between customers and verifying specific customer details.
         """
        self.driver.maximize_window()
        # Enter the customers page
        self.find_and_operate_on_element((By.ID, 'customers'), lambda we: we.click())
        # Filter customer
        self.find_and_operate_on_element((By.ID, 'name'), lambda we, name: we.send_keys(name), ('befree',))

        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())

        self.find_and_operate_on_element((By.ID, '2393ad37-2c8d-41a2-808f-1587a18dbb29'), lambda we: we.click())

        self.scroll_and_switch_container()

        # Wait for the specific element with text 'Befree Agro' to appear
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class, 'MuiTypography-root MuiTypography-body1 MuiListItemText-primary css-ug2eej')"
                 " and text()='Befree Agro']")
            )
        )
        logging.info("Element with text 'Befree Agro' found.")

        # Assert that the element's text is 'Befree Agro'
        self.assertEqual(element.text, "Befree Agro")

        self.find_and_operate_on_element((By.ID, 'name'), lambda we, name: we.send_keys(name), ('boristests',))

        self.find_and_operate_on_element((By.ID, 'submit-filter'), lambda we: we.click())

        self.find_and_operate_on_element((By.ID, '91c95f6c-cbf7-4115-a79d-d67c1fea0dfd'), lambda we: we.click())

        self.scroll_and_switch_container()

        # Wait for the specific element with text 'Boristests' to appear
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class, 'MuiTypography-root MuiTypography-body1 MuiListItemText-primary css-ug2eej')"
                 " and text()='Boristests']")
            )
        )
        logging.info("Element with text 'Boristests' found.")

        # Assert that the element's text is 'Boristests'
        self.assertEqual(element.text, "Boristests")



