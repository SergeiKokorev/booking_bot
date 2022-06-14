# This file contain class for filtrating and sorting search results

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(
            By.CSS_SELECTOR,
            'div[data-filters-group*="class"]'
        )
        stars_child_elements = star_filtration_box.find_elements(By.TAG_NAME, 'input')
        star_values = [str(star) for star in star_values]
        try:
            start_child_elements = [
                element for element in stars_child_elements
                if element.get_attribute("value").split("=")[1] in star_values
            ]
            for element in start_child_elements:
                element.click()
        except IndexError:
            raise IndexError(f"Index out of range.")

    def sort_by(self, sort_by: str = None):
        div_container = self.driver.find_element(
            By.CSS_SELECTOR,
            'div[data-sort-bar-container*="sort-bar"]'
        )

        a_elements = div_container.find_elements(By.TAG_NAME, "a")
        a_element_ids = [e.get_attribute("data-type") for e in a_elements]
        a = (None if sort_by not in a_element_ids
             else a_elements.pop(a_element_ids.index(sort_by)))

        if a:
            self.driver.execute_script("arguments[0].click();", a)
