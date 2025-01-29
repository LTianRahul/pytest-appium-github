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
    caps["app"] = "lt://APP10160212451735552335123100"     #Enter the app (.ipa) url here
    caps["isRealMobile"] = True
    caps['build'] = "build"
    caps['name'] = test_name
    caps['project'] = "IOS Pytest"
     # Accessing LT_USERNAME and LT_ACCESS_KEY from environment variables
    LT_USERNAME = os.environ.get('LT_USERNAME')
    LT_ACCESS_KEY = os.environ.get('LT_ACCESS_KEY')
    
    # Make sure both are set correctly in the environment
    if not lt_username or not lt_access_key:
        raise ValueError("LambdaTest username or access key is not set.")
    
    driver = webdriver.Remote("https://{LT_USERNAME}:{LT_ACCESS_KEY}@mobile-hub.lambdatest.com/wd/hub", caps)   #Add LambdaTest username and accessKey here
    request.cls.driver = driver
    
    yield driver
    
    def fin():
        #browser.execute_script("lambda-status=".format(str(not request.node.rep_call.failed if "passed" else "failed").lower()))
        if request.node.rep_call.failed:
            driver.execute_script('lambda-status=failed')
        else:
            driver.execute_script('lambda-status=passed')
        driver.quit()
    request.addfinalizer(fin)
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for LambdaTest reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

