import pickle

def save_data(filename, login, password):
    data = {'login': login, 'password': password}
    pickle.dump(data, open(f"{filename}_data", "wb"))
    print("DATA SAVED!")

def load_data(filename):
    return pickle.load(open(f"{filename}_data", "rb"))

def save_cookies(driver, filename):
    pickle.dump(driver.get_cookies(), open(f"{filename}_cookies", "wb"))
    print("COOKIES SAVED!")

def load_cookies(driver, filename):
    cookies = pickle.load(open(f"{filename}_cookies", "rb"))
    #for cookie in cookies:
    #    driver.add_cookie(cookie)
    driver.delete_all_cookies()
    for cookie in cookies:

        driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry') if k in cookie})    
    #print(cookie)   

    print("COOKIES LOADED!")
    driver.refresh()
