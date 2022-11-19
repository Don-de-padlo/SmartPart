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


class Forumauto(Site):
    def __init__(self):
        super().__init__(self.__class__.__name__, "https://forumauto.parts", can_load_cookies = False, need_authorization = False)

    def _authorize(self):
        pass    

    def _check_availability(self, id):
        products = []
        search_input = self.driver.find_element(by = By.XPATH, value = "//div[@class='b-header-search-input']/div/input")
        search_input.clear()
        search_input.send_keys(id + Keys.ENTER)
        
        title = ''
        while(True):
            try:
                self.driver.implicitly_wait(2)  
                self.driver.find_element(by = By.XPATH, value = "//span[@class = 'wait-message']")
                self.driver.implicitly_wait(0)
                time.sleep(1)
            except:
                self.driver.implicitly_wait(10)  
                title = self.driver.find_element(by = By.XPATH, value = "//h1[@class = 'main-title']").text
                self.driver.implicitly_wait(0)
                if(title.startswith('Вы шукали') == True):
                    try:
                        h2 = self.driver.find_element(by = By.XPATH, value = "//h2[@class = 'blank-search-title']").text
                        if(h2.startswith('Зараз ми не знайшли пропозицій')):
                            break
                    except:
                        pass
                    products.extend(self._get_products_from_page())
                    break
                else:
                    if(title.endswith('NOBRAND')):
                        break
                    elif(title == 'Номер знайдений в каталогах наступних виробників'):
                        self.driver.implicitly_wait(10)
                        item_list = self.driver.find_element(by = By.XPATH, value = "//table[@id='brand-selection-table']/tbody").find_elements(by = By.XPATH, value = "./tr[@data-url]")
                        self.driver.implicitly_wait(0)
                        if(len(item_list) == 0):
                            break
                        links_list = []
                        for i in item_list:
                            product_link = i.get_attribute('data-url')
                            if(len(product_link) == 0):
                                raise Exception('2')
                            links_list.append(product_link)
 
                        for product_link in links_list:
                            self.driver.get(self.link + product_link)
                            products_from_page = self._get_products_from_page()
                            products.extend(products_from_page)
                        break
                    else:
                        raise Exception('1')

        products.sort()
        return products

    def _get_products_from_page(self):
        products = []
        self.driver.implicitly_wait(10)
        item_list = self.driver.find_element(by = By.XPATH, value = "//table[@role='price-data-content-result-table']/tbody").find_elements(by = By.XPATH, value = "./tr[@id]")
        self.driver.implicitly_wait(0)
        del item_list[20:]
        image = ''
        try:
            image = self.driver.find_element(by = By.XPATH, value = "//div[@class='b-td']/a/img").get_attribute('src')
        except:
            pass
        
        name = ''
        for item in item_list:
            try:
                item_description = item.find_element(by = By.XPATH, value = "./td[@class = 'b-nep-mstd-3']")
                name = item_description.find_element(by = By.XPATH, value = "./div[2]").get_attribute('title')
            except NoSuchElementException:
                pass

            amount = item.find_element(by = By.XPATH, value = "./td[@class = 'b-nep-mstd-8']/div[@class = 'b-nep-mstd-amount']").text.replace(' ', '')
            if(amount.isdigit() == False):
                amount = 'Є'
            price = float(item.find_element(by = By.XPATH, value = "./td[@class = 'b-nep-mstd-10']/div[@class = 'b-nep-mstd-price']/span").text.replace(' ', ''))
            product = Product(self.name, price, amount, name, image)
            products.append(product)

        return products

    def _check_authorized(self):
        return True


