from fastapi import FastAPI, HTTPException
from customer_model import CustomerInfo

app = FastAPI(title="sim card provision apis")

@app.post('/info-validation')
def validate_customer_info(customer_info: CustomerInfo):
    """
    Get customer data and validate it with a cleaner manual approach.
    """
    customer_info_dict = customer_info.model_dump()
    required_fields = {"f_name", "l_name", "city", "plan_type", "national_code"}
    
    
    for field in required_fields:
        if not customer_info_dict.get(field):
            print("bad request for field ",field)
            raise HTTPException(status_code=400, detail="Invalid customer info: Missing field")

   
    national_code = customer_info_dict.get("national_code")
    plan_type = customer_info_dict.get("plan_type")
    print(f'reccied :::: {customer_info_dict}')
    if len(national_code) != 10:
        return {"isValidCustomer": False, "message":"national code is invalid"}

    if plan_type not in ("D", "E"):
        return {"isValidCustomer": False, "message":"plan type undifined"}
    
    return {"isValidCustomer": True}


@app.post('/customer-info')
def store_customer_info(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    customer_info_dict = customer_info.model_dump()

    pass
    
    return {"isValidCustomer": True}
        


@app.post('/bill-calculation')
def calculate_bill(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    customer_info_dict = customer_info.model_dump()

    pass
    
    return {"isValidCustomer": True}
        

@app.post('/store-bill')
def store_bill(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    customer_info_dict = customer_info.model_dump()

    pass
    
    return {"isValidCustomer": True}
        



# {
#   "status": 200,
#   "headers": {
#     "date": "Tue, 16 Sep 2025 22:31:36 GMT",
#     "content-length": "24",
#     "server": "uvicorn",
#     "content-type": "application/json"
#   },
#   "body": {
#     "isValidCustomer": true
#   },
#   "reason": "OK",
#   "document": null
# }