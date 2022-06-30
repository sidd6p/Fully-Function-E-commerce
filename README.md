> This project was done under [Microsoft FutureReady Internship](https://futurereadytalent.in/index)

> And happy to share the successful completeion [Certificate](https://drive.google.com/file/d/1nmqpH-OxWeHMWf2qg5Th9DWoy6zqi-_4/view?usp=sharing)

# Offline E-Commerce

Offline E-Commerce, local shops are now in your phone

BUYER: http://buyer-home-offline-e-commerce.eastus.cloudapp.azure.com/


SELLER:http://seller-home-offline-e-commerce.eastus.cloudapp.azure.com/


## Author

- [@sidd6p](https://github.com/sidd6p)
- [@siddp6](https://github.com/siddp6) (my account but on another laptop)

## Demo


[BUYER's Interface](http://buyer-home-offline-e-commerce.eastus.cloudapp.azure.com/)


[SELLER's Interface](http://seller-home-offline-e-commerce.eastus.cloudapp.azure.com/)

[Video Demo](https://youtu.be/LgmkuKQBBxAM)


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
- Buy Product with quantity specification from seller in their locality
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
- Email Notification updates

### BUYER
- Get Delivery boy/girl details
- Add instruction for the order/Delivery
- Get SELLER location on map

### SELLER
- Provide Delivery details
- Update products details


## Environment Variables

To run this project locally, you will need to add the following environment variables

#### SELLER\files\\.env

```
CONTAINER_NAME=AZURE_BLOB_CONTAINER_NAME
SECRET_KEY=aFGESRjykgcdfDSafdIUJHNaeqpxn539GHyw3232533gdrtdhtyfd28erhdfaoih2472saf8
SELLER_DATABASE=sqlite:///databases/seller.db
CONNECT_STRING=AZURE_SQL_SERVER_CONNETCION_STRING
PRODUCT_SERVER=AZURE_SQL_SERVER
PRODUCT_DATABASE=AZURE_SQL_DATABASE
PRODUCT_USER=AZURE_SQL_SERVER_USERNAME
PRODUCT_PSWD={AZURE_SQL_SERVER_PASSWORD}
PRODUCT_DRIVER={ODBC Driver 17 for SQL Server}
```


#### BUYER\files\\.env

```
CONTAINER_NAME=AZURE_BLOB_CONTAINER_NAME
SECRET_KEY=aFGESRjykgcdfDSafdIUJHNaeqpxn539GHyw3232533gdrtdhtyfd28erhdfaoih2472saf8
SELLER_DATABASE=sqlite:///databases/seller.db
CONNECT_STRING=AZURE_SQL_SERVER_CONNETCION_STRING
PRODUCT_SERVER=AZURE_SQL_SERVER
PRODUCT_DATABASE=AZURE_SQL_DATABASE
PRODUCT_USER=AZURE_SQL_SERVER_USERNAME
PRODUCT_PSWD={AZURE_SQL_SERVER_PASSWORD}
PRODUCT_DRIVER={ODBC Driver 17 for SQL Server}

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


## Screen Shots

### Buyer

__Buyer Landing Page__

<img src="https://bl3301files.storage.live.com/y4mRLshLOtTB6s_8VBod25q30m8QnXNNepuk1I1wJaNBM4h2IQWxPP69E3XuQhgJ3O4m1q5LDqoFGmCHHeqe9ArE9Nz5r6hg-os09dY0GezS82zdm586twmstqnxNo9UlFSkPnJWYJeWkwFyXSPZnJsvTVrIq3TzXT_HYfEnjqi0Zu4n6WtabSO6q0_T9Tqc9mI?width=1002&height=1011&cropmode=none" width="auto" height="auto" />


__Buyer Account Page__

<img src="https://bl3301files.storage.live.com/y4mTiTvLn5N_Cy0y4p5ikmJWUK3FB27LlPAumWc9y6_0iPU4qZQXcGNVXRnO37ZghjURGY02e_x8kfWIsJ1GZMdSA2zteFQkTbgdEMMEIk2hf6IOHl5lLpBQ-h3z2XTGPawJw2zb1q2P8A8Z_AWVgxv9NLFaQf2aT3Pte3N7QfCDCByOYJEMRoXoREJZgtsSl7w?width=1024&height=539&cropmode=none" width="auto" height="auto" />

__Buyer Order Page__

<img src="https://bl3301files.storage.live.com/y4mdfsy9ji4QJ7ZyNKzSCkmIcGyhRPalDdtUBexWdZpVdLF5HyFiAuUaAfz5ISNd3qffwnB7_W7hfXWZZa00CpF3kyOfMsxB1qj_cjBARuIxoi1JJw8TM7o9y2I3nzbweQZSVbys2FONFPUfPpqd9pH7uVewK32kei6NXVwD-SIvJGVM0SKjXDjJjpKISqPTrPe?width=951&height=1008&cropmode=none" width="auto" height="auto" />


__Buyer Cart Page__

<img src="https://bl3301files.storage.live.com/y4mOT8ALZ9mA4bLubxP5IAw8IYHcRp9oSxOqiJXnb0aZHy4wEiWOBiFqUAiw0pMOEkPbn2PEFYzaPvcgGLac59O00Ah_tx9hTMHvOkS39RTGt1hjfnu8GI83SZa6jbqn66tAuGF8EijrxR4ogT-N1rLQfIIlRowgYFMJhxfaRMm1b0yxGyztEctrn8zZ5KzNCb7?width=1258&height=1080&cropmode=none" width="auto" height="auto" />


__Buyer Wish-list Page__

<img src="https://bl3301files.storage.live.com/y4mgR91pZkGCH-pzeQFHzNAYBQ-hZtkXEZc5XKHkDBdBsrRSIfL6S0vE8jD8jcz_nbbIfW7cJn-1RIw-914gBgqQcx7p5GugAR-q8L2MG6wLWjQTkyd2E1cOUeZFYgFoRBmAkBUQ-7qrK4qH-hHDpTPS2rfz8XyTLQ7HeXooAt1w7-KdjCvR4MOe5bb81qQcLIv?width=953&height=1015&cropmode=none" width="auto" height="auto" />


__Buyer History Page__

<img src="https://bl3301files.storage.live.com/y4mYAJsV7hUehS-eFfVYBafJjxO1KFZa0e_e8oZP445kuCn-TfemPzbNMgh1k3hX-2wCITrRPZqb2OK3KCSF8t-8LAMcSRNkq46Z879RHkadhiWtctLwetRMTV3V5BgNKv-MsunhFaJ5Wkiu9LOoM9FxhQ0YfVU_s28D9eTZYwjIExzAkzGePMgJvpQ-wwodR0Y?width=993&height=871&cropmode=none" width="auto" height="auto" />




### Seller

__Seller Landing Page__

<img src="https://bl3301files.storage.live.com/y4m7ooCYhPVMoSnaeZDwq0S06NU6MRJO_yRjSLVP8uH9jrJj2v9aN0RtSYEocpFu1Q2MA0wquFxLzwMtuyBluFsd3IPILxGcIPJF4sMdC0D0hAz8sJ9btLbat3em62JPytd5igP7coWDZyqpafXAvXGCwefGaHwwMOYMJD0Xjbk7Aqp63NNXAPkBCWZJZ-gLZN2?width=1024&height=601&cropmode=none" width="auto" height="auto" />


__Seller Product Page__

<img src="https://bl3301files.storage.live.com/y4m4ZVV8JSfO368HP9xhY4o2QGVv8CeCT4HJivD0CbttWgT28e13Rg9p_GaXJLTQwHma0i_aGvpeIeF3Dniuij4IoOOpReBb1kiqHFmkXyof0F18U4xs2sn1LJBG4ELaPtekWHZNG7nG1rPkRJ27_dsYQoK4Ep0gT27iPZIPVS6fiFOBeCeKt1S2JL7f0xv1Hns?width=1915&height=1080&cropmode=none" width="auto" height="auto" />


__Seller Product Upload Page__

<img src="https://bl3301files.storage.live.com/y4m9hGoT4LDFxEB_87Bo4fHheI0nds7HFYZ-oWJG6s7wC-q6U9VwvUqd4rx-SQ0Qqms4MAwvWZ8uMpNeJTOP07zHffL0FaBwFi5ky2xgMFJHIv5W0q6vtUpfC_2iGAEVqe-qAr2goA-3uxWU01uTjBcTEOJINzoHRI2ovSXaknx0VH6yZyPlHDivIpKxRu_G0xO?width=1915&height=1080&cropmode=none" width="auto" height="auto" />


__Seller Order Viewing__

<img src="https://bl3301files.storage.live.com/y4msM_xoPbzTGLumPh0d6oTKcRFqV3OuG76wVpx8fHMGS-QPhYmjneM4RyyrLBJBGfuotcdM95ywwciABqSBTakonF8ITSDKKmEY0ZBtxEyyY2yIHoJzUwZw4DJcmNsOFevAWuY3cEZxAEvsG1Xej33sSG7_e3Zm-lgg8ujZZJpy5zdkSmmEK70eUPYUOnwrLXi?width=1200&height=1010&cropmode=none" width="auto" height="auto" />


__Seller History Page__

<img src="https://bl3301files.storage.live.com/y4mbtzCI3M1vk_WJWkCMNKmdj4FthBs9JAk4StlMpWmMeca5hWN1-msVXQwgct4VOEXLOJJw0cQgTwdkI9Za4rGgWc9s1gGCNVFT2amgcewgL3pTbECHLv848TM0bdF3E9EyBzUYMCh7S7VVNnXNr5riFaDOeIeVBEBtvhdHBYR-JJq1IFQjDzX-naDZmSEzj02?width=1326&height=1080&cropmode=none" width="auto" height="auto" />

