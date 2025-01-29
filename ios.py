from os import environ
import pytest
from appium import webdriver

from appium.options.ios import XCUITestOptions  # Corrected import statement

@pytest.fixture(scope='function')
def test_setup_ios(request):
    test_name = request.node.name
    options = XCUITestOptions().load_capabilities({
        # Specify device and os_version for testing
        "lt:options": {
            "w3c": True,
            "platformName": "ios",
            "deviceName": "iPhone.*",
            "platformVersion": "16",
            "isRealMobile": True,
            "app": "lt://APP10160212451735552335123100"
        }
    })
    driver = webdriver.Remote("https://{LT_USERNAME}:{LT_ACCESS_KEY}@mobile-hub.lambdatest.com/wd/hub", options=options)   #Add LambdaTest username and accessKey here
    request.cls.driver = driver
    
    yield driver
    
    def fin():
        if request.node.rep_call.failed:
            driver.execute_script('lambda-status=failed')
        else:
            driver.execute_script('lambda-status=passed')
        driver.quit()
    request.addfinalizer(fin)
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)
