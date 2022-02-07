
# Offline E-Commerce

Offline E-Commerce, local shops are now in your phone

BUYER: http://buyer-home-offline-e-commerce.eastus.cloudapp.azure.com/


SELLER:http://buyer-home-offline-e-commerce.eastus.cloudapp.azure.com/



## Azure Services

1. Azure SQL Server
- Used to store product details, orders details, wishlist and cart details.
2. Azure Blobs
- Used Azure storage container to store images
- This include seller shop image/logo and products images
- Images are accessed throught the connection string
3. Azure VM
- Two VM used, both having ubuntu image
- One VM for Buyer, this handle all opertaion related to buyers
- One VM for Seller, this deals with all sellerrelated operations
- VMs also act as storage platform for information of seller and buyer

#### Using Two VMs and seperated DB for products and order makes product information and orders details available incase if seller or buyer server goes down. If seller server will go down, then still buyer will be able to access all functionality as normal and same privilage for seller also. __This whole project is based on microservice architecture, so keeping different database for different microservice, and future updates include FastApi for accessing Azure SQL Server__ 
## Authors

- [@sidd6p](https://github.com/sidd6p)
- [@siddp6](https://github.com/siddp6) (my account but on another laptop)
## Directory stracture
    Offline E-Commerce
    │   .gitignore
    │   LICENSE
    │   README.md
    │
    ├───BUYER
    │   │   .flaskenv
    │   │   db-offline-e-commerce
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
    └───SELLER
        │   .flaskenv
        │   db-offline-e-commerce
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
            ├───static
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
- Buy Product with quantity specification
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
## Demo


[BUYER's Interface](http://buyer-home-offline-e-commerce.eastus.cloudapp.azure.com/)


[SELLER's Interface](http://buyer-home-offline-e-commerce.eastus.cloudapp.azure.com/)

[Video Demo](https://youtu.be/6jAYiVFLnwM)
## Upcoming Feature

### GENERAL
- Forget Password
- Update Account

### BUYER
- Get Delivery boy/girl details
- Add instruction for the order/Delivery
- Get SELLER location on map

### SELLER
- Provide Delivery details

## Environment Variables

To run this project locally, you will need to add the following environment variables

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

## Deployment

Buyer Interface and Seller Interface are Deployed seperately to keep low Coupling.

Both are deployed in Azure VM with ```nginx```, ```gunicorn``` and ```supervisor```.


## Tech Stack

**Client:** HTML, CSS, Bootstrap 4

**Server:** Flask, Jinja2

**Deployment** Azure VM

**Database** Azure SQL Server, Sqlite3

**VCS** Git Bash (GitHub)

