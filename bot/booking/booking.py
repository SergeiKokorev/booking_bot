import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import booking.constants as const
from booking.booking_filtaration import BookingFiltration
from booking.booking_report import BookingReport
from booking.tools import clean_html


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH,
                 teardown=False):
        self.teardown = teardown
        self.driver_path = driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def accept_cookies(self):
        try:
            WebDriverWait(self, 10).until(ec.visibility_of_element_located(
                (By.ID, const.COOKIES_ACCEPT_BTN))
            ).click()
        except Exception as ex:
            raise Exception("Accept cookies button nas not been found.")

    def change_currency(self, currency=None):
        currency_element = self.find_element(
            By.CSS_SELECTOR,
            "button[data-modal-header-async-type='currencyDesktop']"
        )
        currency_element.click()
        selected_currency_element = self.find_element(
            By.CSS_SELECTOR,
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go=None):
        search_place = self.find_element(By.ID, "ss")
        search_place.clear()
        search_place.send_keys(place_to_go)
        first_result = self.find_element(
            By.CSS_SELECTOR,
            'li[data-i*="0"]'
        )
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
            By.CSS_SELECTOR,
            f'td[data-date*="{check_in_date}"]'
        )
        check_out_element = self.find_element(
            By.CSS_SELECTOR,
            f'td[data-date*="{check_out_date}"]'
        )
        check_in_element.click()
        check_out_element.click()

    def change_guests(self, children_ages: list = [],
                      element_count: int = 0,
                      element_id: str = None,
                      element_css_selector: str = None):

        self.find_element(By.ID, "xp__guests__toggle").click()

        element = self.find_element(By.ID, element_id)
        num_element = element.get_attribute("value")
        min_element = element.get_attribute("min")
        max_element = element.get_attribute("max")

        try:
            num_clicks = int(element_count) - int(num_element)

            css_selector = "input-stepper-subtract-button" \
                if num_clicks < 0 else "input-stepper-add-button"

            element_btn = self.find_element(
                By.CSS_SELECTOR,
                f'button[data-bui-ref*="{css_selector}"][aria-describedby*="{element_css_selector}"]'
            )

            for _ in range(abs(num_clicks)):
                element_btn.click()

            if 'children' in element_css_selector:
                age_elements = self.find_elements(By.NAME, "age")
                if not children_ages:
                    children_ages = [0] * len(age_elements)
                elif len(children_ages) < len(age_elements):
                    children_ages.append(*[0] * (len(age_elements) - len(children_ages)))
                for idx, element in enumerate(age_elements):
                    element.click()
                    options = element.find_elements(By.TAG_NAME, "option")
                    options = [option for option in options if option.get_attribute("value")]

                    ages = [int(age.get_attribute("value"))
                            for age in options
                            if age.get_attribute("value")]

                    children_ages = [
                        max(ages) if abs(age) > max(ages) else age
                        for age in children_ages
                    ]

                    for option in options:
                        if option.get_attribute("value") == str(children_ages[idx]):
                            option.click()

        except NoSuchElementException as er:
            print(f"Element has not been found. An error occurred {er}")
        except ValueError as er:
            print(f"A value must be integer. An error occurred {er}")

    def get_search_results(self):
        search_button = self.find_element(
            By.CLASS_NAME,
            "sb-searchbox__button "
        )
        if search_button:
            search_button.click()

    def apply_filtration(self, **kwargs):
        filtration = BookingFiltration(driver=self)

        keys = kwargs.keys()

        if 'sort_by' in keys:
            filtration.sort_by(kwargs['sort_by'])
        if 'star_values' in keys:
            filtration.apply_star_rating(*kwargs['star_values'])

    def save_results(self):
        results_box = self.find_element(By.ID, 'search_results_table')
        report = BookingReport(results_box)
        pull_attr_dict = {
            'hotel': 'div[data-testid="title"]',
            'price': 'span[class="fcab3ed991 bd73d13072"]',
        }
        results = report.pull_deal_box_attributes(**pull_attr_dict)
        
