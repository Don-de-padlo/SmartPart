import time
import sys
from site_provider import Forumauto

site = Forumauto()
def main():
    id = ""
    with open('..//buffer//naming.txt', encoding='windows-1251') as f:
        for line in f:
            id = line.strip()
    file = open("../buffer/Forumauto.txt", "w")
    products = site.check_availability(id)
    for product in products:
        file.write('Site: ' + str(product.site) + 
                   ' $%$,Naming: '+ str(product.naming) + 
                   ' $%$,Price: ' + str(product.price) + 
                   ' $%$,Amount: ' + str(product.amount) + 
                   ' $%$,ImageSrc :' + str(product.image) + '\n')
    file.close()

if __name__ == "__main__":
    main()

#for product in products:
#print('Site: ' + str(product.site) + 
#      ' Naming: '+ str(product.naming) + 
#      ' ,Price: ' + str(product.price) + 
#      ' ,Amount: ' + str(product.amount) + 
#      ' ImageSrc :' + str(product.image))