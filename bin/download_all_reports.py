import logging, os, time
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SELENIUM_SERVER = os.environ.get(
    'SELENIUM_SERVER',
    'http://localhost:4444/wd/hub'
)

SELENIUM_BROWSER = os.environ.get(
    'SELENIUM_BROWSER',
    'CHROME'
)


def run():
    '''
    Uses a web browser to download all available FDIC call report data from the
    URL defined as DOWNLOADS_PAGE above.

    Uses Selenium which must be running using, e.g.

        java -jar selenium-server-standalone-2.43.1.jar

    By default the script tries to connect to a server running locally on
    port 4444, but this may be overridden through use of the SELENIUM_SERVER
    environment variable.

    The standalone Selenium server tries to use the default system browser.
    To use a different browser like Chrome, add this command-line option to
    the java call:

        -Dwebdriver.chrome.driver=/path/to/chromedriver

    Also set the SELENIUM_BROWSER environment variable to CHROME.

    This program triggers downloads in tab-delimited format which get
    saved to the default browser download location.
    '''
    with selenium_driver() as driver:
        count = 0

        while True:
            logger.info('navigating to data download page')
            driver.get('https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx')

            logger.info('setting download type to single period')
            dl_type = Select(driver.find_element_by_id('ListBox1'))
            dl_type.select_by_value('ReportingSeriesSinglePeriod')
            time.sleep(3)

            logger.info('finding available reporting periods')
            periods = Select(driver.find_element_by_id('DatesDropDownList'))

            if not count:
                logger.info('{} available reporting periods: {}'.format(
                    len(periods.options),
                    ', '.join([period.text for period in periods.options])
                ))

            if count == len(periods.options):
                break

            period = periods.options[count]
            logger.info('downloading data for period {}'.format(period.text))

            periods.select_by_index(count)
            time.sleep(3)

            submit_button = driver.find_element_by_id('Download_0')
            submit_button.click()
            time.sleep(3)

            count += 1

        logger.info('waiting for last download to finish')
        time.sleep(30)


@contextmanager
def selenium_driver():
    logger.info('connecting to local Selenium server at {}'.format(
        SELENIUM_SERVER
    ))
    capabilities = getattr(DesiredCapabilities, SELENIUM_BROWSER)

    driver = webdriver.Remote(
        SELENIUM_SERVER,
        desired_capabilities=capabilities
    )

    try:
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(10)

        yield driver
    finally:
        logger.info('disconnecting from local Selenium server')
        driver.quit()


if __name__ == '__main__':
    run()
