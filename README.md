
# Offline E-Commerce

Offline E-Commerce, local shops are now in your phone

Some points to consider
- This application is based on microservices architecture, means SELLER and BUYER code can work independently and hence they both have different database
- In upcoming deployment, Product database will be access through only API



## Demo


[Video Demo](https://youtu.be/6jAYiVFLnwM)
## Authors

- [@sidd6p](https://github.com/sidd6p)
- [@siddp6](https://github.com/siddp6) (my account but on another laptop)
## Directory stracture
    C:.
    │   .gitignore
    │   LICENSE
    │   README.md
    │   
    ├───BUYER
    │   │   .flaskenv
    │   │   requirements.txt
    │   │   run.py
    │   │   
    │   └───files
    │       │   .env
    │       │   config.py
    │       │   forms.py
    │       │   models.py
    │       │   utils.py
    │       │   __init__.py
    │       │
    │       ├───databases
    │       │       buyer.db
    │       │
    │       ├───routes
    │       │       orders.py
    │       │       user.py
    │       │
    │       └───templates
    │           │   accounts.html
    │           │   buyer-home.html
    │           │   create-buyer.html
    │           │   layout.html
    │           │   login.html
    │           │   show-products.html
    │           │
    │           └───includes
    │                   meta.html
    │                   nav.html
    │
    ├───DATABASE_PROD
    │       product.db
    │
    └───SELLER
        │   .flaskenv
        │   requirements.txt
        │   run.py
        │
        └───files
            │   .env
            │   config.py
            │   forms.py
            │   models.py
            │   utils.py
            │   __init__.py
            │
            ├───databases
            │       seller.db
            │
            ├───routes
            │       products.py
            │       user.py
            │
            └───templates
                │   accounts.html
                │   create-shop.html
                │   layout.html
                │   login.html
                │   my-buyers.html
                │   orders.html
                │   seller-home.html
                │   upload-product.html
                │
                └───includes
                        meta.html
                        nav.html
## Run Locally

- [Deployment Video](https://youtu.be/AL4ydKZyoLo)


Clone the project

```bash
  git clone https://github.com/sidd6p/offline-e-commerce.git
```

### BUYER
Go to the BUYER directory

```bash
  cd BUYER
```

Install dependencies

```bash
  pip install -r requirements.txt
```

run the project

```bash
  flask run 
```

##### BUYER account can be access at http://127.0.0.1:5000/



### SELLER
Go to the SELLER directory

```bash
  cd SELLER
```

Install dependencies

```bash
  pip install -r requirements.txt
```

run the project

```bash
  flask run 
```


##### SELLER account can be access at http://127.0.0.1:8000/

## Feature

### GENERAL
- User Login and Registration
- See status of order
    - Accept
    - Cancelled
    - Out_for_delivery
- Smart Product Search

### BUYER
- Buy Product
- Add to Cart or Wishlist
- Bulk order all products in Cart or Wishlist
- Transfer products from Cart to Wishlist or vice-versa
- Post-order actions
    - Cancell order
    - Delivered
- Get History
    - Delivery products
    - Cancelled

### SELLER
- Upload products
- Update order status
   - Accept
   - Out_for_delivery
   - Cancelled
## Upcoming Feature

### GENERAL
- Forget Password
- Update Account

### BUYER
- Get Delivery boy/girl details
- Add instruction for the order/Delivery
- Set the order quantity
- Get SELLER location on map

### SELLER
- Provide Delivery details

## Environment Variables

To run this project, you will need to add the following environment variables

#### SELLER\files\\.env

```
PRODUCT_DATABASE=YOUR_RELATIVE_PATH_TO_Offline_E_Commerce_FOLDER\DATABASE_PROD\product.db
CONNECT_STRING=YOUR_AZURE_BLOB_CONNECTION_STRING
CONTAINER_NAME=YOUR_BLOB_CONTAINER_NAME
SECRET_KEY=YOUR_SECRET_KEY
SELLER_DATABASE=sqlite:///databases/seller.db
```


#### BUYER\files\\.env

```
PRODUCT_DATABASE=YOUR_RELATIVE_PATH_TO_Offline_E_Commerce_FOLDER\DATABASE_PROD\product.db
CONNECT_STRING=YOUR_AZURE_BLOB_CONNECTION_STRING
CONTAINER_NAME=YOUR_BLOB_CONTAINER_NAME
SECRET_KEY=YOUR_SECRET_KEY
SELLER_DATABASE=sqlite:///databases/buyer.db
```
