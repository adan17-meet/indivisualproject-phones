# coding: utf-8 
from database import *

products = [
    
{"name":'Iphone 7', "year": "2016", "brand":'Apple', 'color':'pink', 'description':'iPhone 7 now has the best performance and battery life ever, as well as new finishes, water resistance, and stereo speakers.', 'photo':'https://staticshop.o2.co.uk/product/images/iphone-7-plus-rose-gold_sku-header.png?cb=e55ba7b828e6e70c863cc29ad975d2ff', 'price':'1200'},
{'name':'Galaxy s7', 'year': '2016', 'brand':'Samsung', 'color':'black' ,'description':'Experience the newest Samsung phone! The Galaxy S7 & Galaxy S7 edge feature water-resistance, enhanced cameras and ability to add a microSD Card.', 'photo':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvc6R3M9EMemwqTDZoAAlIfX98YBJtQvniiWAaYb3Mx6avZ2ww', 'price':'1150'},
{'name':'Galaxy s6', 'year': '2015', 'brand':'Samsung', 'color':'white', 'description':'Samsung Galaxy S6 smartphone with 5.10-inch 1440x2560 display powered by 1.5GHz octa-core processor alongside 3GB of RAM and 16-megapixel', 'photo':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTDepRuopDE-MZAgXUnqKag_KfgzQFekeypIHOX-EyKBqoILTG', 'price':'980'},
{'name':'Galaxy s5', 'year': '2014', 'brand':'Samsung', 'color':'black' ,'description':'Samsung Galaxy S5 smartphone with 5.10-inch 1080x1920 display powered by 1.9GHz octa-core processor alongside 2GB of RAM and 16-megapixel.', 'photo':'http://easydeal.pk/image/data/samsung/GS5Blk_600x600_xlarge_Grp_1.jpg', 'price':'750'},
{'name':'Iphone 6s', 'year': '2015', 'brand':'Apple', 'color':'pink', 'description':'Apple iPhone 6s smartphone. Announced 2015, September. Features 3G, 4.7" LED-backlit IPS LCD display, 12 MP camera, Wi-Fi, GPS, Bluetooth.', 'photo':'https://i.ebayimg.com/00/s/ODIxWDEwMjQ=/z/BA8AAOSwGIRXbT5n/$_86.JPG', 'price':'1000'},
{'name':'Galaxy 6s Plus', 'year': '2015', 'brand':'Apple', 'color':'black', 'description':'Apple iPhone 6 Plus smartphone. Announced 2014, September. Features 3G, 5.5" LED-backlit IPS LCD display, 8 MP camera', 'photo':'http://d2ydh70d4b5xgv.cloudfront.net/images/e/9/apple-iphone-6-plus-silver-16gb-a1522-at-t-only-read-description-13-295efdfc62388847b5de5d523c361ff9.jpg', 'price':'1500'},

]


for product in products:
    newProduct = Product(name=product['name'], description=product['description'], year	=product['year'], photo=product['photo'], brand= product['brand'], color=product['color'],price=int(product['price']))
    import pdb
    #pdb.set_trace()	
    session.add(newProduct)
    session.commit()

print("Done!")

products = session.query(Product).all() 
for product in products:
	print(product.name)
	print(product.price)



