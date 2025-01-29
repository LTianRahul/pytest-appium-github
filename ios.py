from os import environ
import pytest
from appium import webdriver

@pytest.fixture(scope='function')
def test_setup_ios(request):
    test_name = request.node.name
    build = environ.get('BUILD', "Pytest IOS Sample")
    
    caps = {}
    caps["deviceName"] = "iPhone 11"
    caps["platformName"] = "iOS"
    caps["platformVersion"] = "14"
    caps["app"] = "lt://APP10160212451735552335123100"  # Enter the app (.ipa) URL here
    caps["isRealMobile"] = True
    caps['build'] = "build"
    caps['name'] = test_name
    caps['project'] = "IOS Pytest"
    
    # Accessing LT_USERNAME and LT_ACCESS_KEY from environment variables
    LT_USERNAME = environ.get('LT_USERNAME')  # Get username from environment variables
    LT_ACCESS_KEY = environ.get('LT_ACCESS_KEY')  # Get access key from environment variables
    
    # Make sure both are set correctly in the environment
    if not LT_USERNAME or not LT_ACCESS_KEY:
        raise ValueError("LambdaTest username or access key is not set.")
    
    # Use f-string to correctly format the URL with the credentials
    driver = webdriver.Remote(
        f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@mobile-hub.lambdatest.com/wd/hub",  # Format the URL properly
        caps
    )
    
    request.cls.driver = driver
    
    yield driver
    
    def fin():
        # This code updates the LambdaTest status based on test result
        if request.node.rep_call.failed:
            driver.execute_script('lambda-status=failed')
        else:
            driver.execute_script('lambda-status=passed')
        driver.quit()
    
    request.addfinalizer(fin)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This sets the result as a test attribute for LambdaTest reporting.
    outcome = yield
    rep = outcome.get_result()

    # Set a report attribute for each phase of a call, which can be "setup", "call", or "teardown"
    setattr(item, "rep_" + rep.when, rep)
