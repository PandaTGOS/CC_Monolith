import sqlite3
import requests
import random
def get_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM products')
    
    products = []
    rows = cursor.fetchall()
    
    for i in range(len(rows)):
        temp = rows[i]
        products.append(temp)

    if len(products) > 0:
        products.sort(key=lambda x: 0)
    
    connection.commit()
    connection.close()
    return products

def insert_cart_products(cookies,products):
    random.seed(42)
    for i in range(100):
        
        p=random.choice(products)
        print("http://127.0.0.1:5000/cart/{}".format(p[0]))
        r=requests.post("http://127.0.0.1:5000/cart/{}".format(p[0]),cookies=cookies)
        
        if r.status_code==200:
            print(r)
            print("inserted product")
        else:
            print("failed to insert")
        
        

def insert_user(username, password):
    connection = sqlite3.connect("auth.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    connection.commit()
    
def login(username, password):
    session=requests.Session()
    payload={
        "username":username,
        "password": password
    }
    r=session.post("http://127.0.0.1:5000/login", data=payload)
    if r.status_code==200:
        "Logged in successfully"
        return session.cookies
    else:
        exit
        
    
    
    
def main():
    username="test123"
    password="test123"
    insert_user(username, password)
    cookies=login(username,password)
    products=get_products()
    insert_cart_products(cookies,products)
    

if __name__ == "__main__":
    main()
