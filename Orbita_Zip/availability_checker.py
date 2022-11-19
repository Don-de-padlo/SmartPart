from sites_fabric import get_sites
import time
sites = get_sites()
def check_availability(id):
    products = []
    for site in sites:
        products_from_site = site.check_availability(id)
        products.extend(products_from_site)
    products.sort()
    #del products[5:]

    file = open("../buffer/res2.txt", "w")

    for product in products:
        print('Site: ' + str(product.site) + ' Naming: '+ str(product.naming) + ' ,Price: ' + str(product.price) + ' ,Amount: ' + str(product.amount) + ' ImageSrc :' + str(product.image))
        
        file.write('Site: ' + str(product.site) + ' $%$,Naming: '+ str(product.naming) + ' $%$,Price: ' + str(product.price) + ' $%$,Amount: ' + str(product.amount) + ' $%$,ImageSrc :' + str(product.image) + '\n')
        
        
    file.close()
    return products

