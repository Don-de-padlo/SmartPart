import data_provider
import driver_provider
import time
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class Site(ABC):
    def __init__(self, name, link, can_load_cookies = True, need_authorization = True):
        self.link = link
        self.name = name
        self.driver = driver_provider.get_driver('C:\\chromedriver\\chromedriver\\chromedriver\\chromedriver.exe')
        #self.driver.maximize_window()
        self.can_load_cookies = can_load_cookies
        self.need_authorization = need_authorization
        self._enter_to_site()

    def _enter_to_site(self):
        authorized = False
        self.driver.get(self.link)
        if self.need_authorization:
            if self.can_load_cookies:
                try:
                    cookies = data_provider.get_cookies(self.driver, self.name)
                    self.set_cookies(cookies)
                    self.driver.refresh()
                    self._check_authorized()
                    authorized = True
                except Exception:
                    print(self.name + ": Cookies not found. Authorize.")
                    self._load_data()
                    try:
                        self._authorize()
                        self._check_authorized()
                        authorized = True
                        data_provider.save_cookies(self.driver, self.name)
                    except Exception as ex:
                        print(self.name + ": ERROR DURING AUTHORIZATION!" )
                        print(ex)

            else:
                self._load_data()
                try:
                    self._authorize()
                    self._check_authorized()
                    authorized = True
                except:
                    print(self.name + ": ERROR DURING AUTHORIZATION!" )

            if(authorized):
                print(self.name + ': AUTHORIZED!')
            else:
                print(self.name + ': AUTHORIZATION FAILED!')
                self.driver.close()
                self.driver.quit()

    def _load_data(self):
        try:
            data = data_provider.load_data(self.name)
            self.login = data['login']
            self.password = data['password']
        except Exception as ex:
            print("Can't load data")
            self.login = input(f'{self.name}: Enter login: ')
            self.password = input(f'{self.name}: Enter password: ')
            data_provider.save_data(self.name, self.login, self.password)

    def check_availability(self, id):
        result = []
        try:
            self.driver.get(self.link)
            result = self._check_availability(id)
        except Exception as ex:
            print(self.name + ": ERROR during searching!")
            print(ex)
        finally:
            print(self.name + ": " + str(len(result)))
            return result

    def set_cookies(self, cookies):
        self.driver.delete_all_cookies()
        for cookie in cookies:
            self.driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry') if k in cookie})    

    @abstractmethod    
    def _check_availability(self, id):
        pass

    @abstractmethod
    def _authorize(self):
        pass

    @abstractmethod
    def _check_authorized(self):
        pass

class Product():
    def __init__(self, site, price, amount, naming, image):
        self.site = site
        self.price = price
        self.amount = amount
        self.naming = naming
        self.image = image
    def __lt__(self, other):
        return self.price < other.price

class Autoklad(Site):
    def __init__(self):
        super().__init__(self.__class__.__name__, "https://www.autoklad.ua/ua/", can_load_cookies = False, need_authorization = False)

    def _authorize(self):
        pass    

    def _check_availability(self, id):
        search_popup = self.driver.find_element(by = By.XPATH, value = "//button[i[@class = 'icon-search']]")
        search_popup.click()
        WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH, "//div[@class='arcticmodal-container']")))
        search_input = self.driver.find_element(by = By.XPATH, value = "//input[@id='id_search_live']")
        search_input.clear()
        search_input.send_keys(id + Keys.ENTER)
        try:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Результати пошуку за фразою')]")))
        except:
            WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, "//strong[text() = 'Товар не знайдено']")))
            return []

        item_list = self.driver.find_element(by = By.XPATH, value = "//ul[@class='drop-search-list']").find_elements(by = By.XPATH, value = "./li/a")
        products = []
        for item in item_list:
            try:
                item.find_element(by = By.XPATH, value = "./div[3]/div/span")
            except:
                continue
            price = item.find_element(by = By.XPATH, value = "./div[3]/div/span[1]").text
            amount = 'Є'
            name = item.find_element(by = By.XPATH, value = "./div[1]/span[3]").text
            product = Product(self.name, price,  amount, name, '')
            products.append(product)

        products.sort()
        del products[5:]
        return products

    def _check_authorized(self):
        return True

