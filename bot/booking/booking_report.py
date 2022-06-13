from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()
        self.outdata = []

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR, 
            'div[data-testid="property-card"]'
            )

    def pull_deal_box_attributes(self, **kwargs):

        for box in self.deal_boxes:
            self.outdata.append(
                {k: box.find_element(By.CSS_SELECTOR, s).get_attribute("innerHTML") 
                for k, s in kwargs.items()}
            )       
        
        return self.outdata
