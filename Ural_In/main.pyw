import time
import sys
from site_provider import Ural_In

site = Ural_In()
def main():
    id = ""
    with open('..//buffer//naming.txt', encoding='windows-1251') as f:
        for line in f:
            id = line.strip()
    file = open("../buffer/Ural_In.txt", "w", encoding="windows-1251")
    products = site.check_availability(id)
    for product in products:
        try:
            file.write('Site: ' + str(product.site) + 
                       ' $%$,Naming: '+ str(product.naming) + 
                       ' $%$,Price: ' + str(product.price) + 
                       ' $%$,Amount: ' + str(product.amount) + 
                       ' $%$,ImageSrc :' + str(product.image) + '\n')
        except:
            pass
    file.close()

    

if __name__ == "__main__":
    main()
