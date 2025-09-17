from fastapi import FastAPI, HTTPException
from customer_model import CustomerInfo
import random

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
    
    random_num = random.randint(0,2)

    if random_num < 2:
        return {"message": "stored"}
    else:
        raise HTTPException(status_code=500, detail="unable to store data")
        


@app.post('/bill-calculation')
def calculate_bill(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    customer_info_dict = customer_info.model_dump()

    pass
    
    return {"isValidCustomer": True}
        

@app.post('/user-exist')
def check_customer_existing(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    random_num = random.randint(0,2)

    if random_num < 2:
        return {"savedCustomer": False}
    else:
        return {"savedCustomer": True}
        

#...................................................... sim card provision
@app.post('/sim-card')
def assign_sim_card(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    random_num = random.randint(0,2)
    print(f'>>>>>>>>>>>>>>>>>>. { random_num}')
    if random_num < 2:
        return {"assigned": True}
    else:
        raise HTTPException(status_code=400, detail="unable to assign a sim card")

        


# {
#   "status": 200,
#   "headers": {
#     "date": "Wed, 17 Sep 2025 07:30:47 GMT",
#     "content-length": "23",
#     "server": "uvicorn",
#     "content-type": "application/json"
#   },
#   "body": {
#     "savedCustomer": false
#   },
#   "reason": "OK",
#   "document": null
# }