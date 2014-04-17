"""
API: phantomjs
"""

from selenium import webdriver
import logging

class PhantomJSAPI():
    """
    api for phantom.js: this class will intialize a driver for phantom js
    and provide a method to save image for phantom js.
    """

    def __init__(self):
        try:
            self.driver = webdriver.PhantomJS()
        except WebDriverException, err:
            logging.error(err)
    def get_website_screenshot(self, url, save_path):
        """
        This method will save the website screenshot as image,
        and save it to the save_path.
        params:
            > url: url string link to the website which will be caugth a screenshot
            > save_path: where to save image.
        """

        self.driver.get(url)
        res = self.driver.save_screenshot(save_path)
        return res
    
    def __del__(self):
	self.driver.quit()
