import data_provider
import driver_provider
import time
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class Site(ABC):
    def __init__(self, name, link, can_load_cookies = True, need_authorization = True):
        self.link = link
        self.name = name
        self.driver = driver_provider.get_driver('C:\\chromedriver\\chromedriver\\chromedriver\\chromedriver.exe')
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
    def __init__(self, site, price, amount, naming , image):
        self.site = site
        self.price = price
        self.amount = amount
        self.naming = naming
        self.image = image
    def __lt__(self, other):
        return self.price < other.price

class Ural_In(Site):
    def __init__(self):
        super().__init__(self.__class__.__name__, "https://ural.in.ua/ua/", can_load_cookies = False, need_authorization = False)

    def _authorize(self):
        pass    

    def _check_availability(self, id):
        search_input = self.driver.find_element(by = By.XPATH, value = "//input[@id='search_term']")
        search_input.clear()
        search_input.send_keys(id + Keys.ENTER)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//span[@title='найдено']")))
        amount_in_page = int(self.driver.find_element(by = By.XPATH, value = "//span[@title='найдено']").text.split(' ')[0])
        if(amount_in_page == 0):
            return []

        item_list = self.driver.find_elements(by = By.XPATH , value= "//ul/li[@class='cs-product-gallery__item js-productad']")
        products = []

        for item in item_list:
            amount_text = item.find_element(by = By.XPATH , value = "./div/div/div[2]/span").text
            if(amount_text ==  'В наявності'):
                amount = 'Є'
                price_span = item.find_element(by = By.XPATH, value = "./div/div/div[3]/span")
                price_span_text = price_span.get_attribute('class')
                if(price_span_text.endswith('unknown')):
                    continue

                price_list = price_span.text.split(' ')[:-1]
                price_text = "".join([str(i) for i in price_list])
                price = float(price_text)

                naming_list = item.find_element(by = By.XPATH , value = "./div/div/div/a").text
                naming_text = "".join([str(i) for i in naming_list])
                naming = str(naming_text)

                image_text = item.find_element(by = By.XPATH , value = "./div/a[4]/img").get_attribute("src")
                image = str(image_text)

                product = Product(self.name, price,  amount , naming , image)
                products.append(product)

        products.sort()
        #del products[15:]
        return products

    def _check_authorized(self):
        return True


