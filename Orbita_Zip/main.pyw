import time
import sys
from site_provider import Orbita_Zip

site = Orbita_Zip()
def main():
    id = ""
    with open('..//buffer//naming.txt', encoding='windows-1251') as f:
        for line in f:
            id = line.strip()
    file = open("../buffer/Orbita_Zip.txt", "w")
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
