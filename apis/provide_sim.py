from fastapi import FastAPI, HTTPException
from customer_model import CustomerInfo, PhoneNumber, BillingRequest, BillingInfo
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
    print(f'.........{random_num}')
    if random_num < 2:
        return {"phone_number": "09392890534"}
    else:
        raise HTTPException(status_code=400, detail="unable to assign a sim card")

        
@app.post('/sim-card-activation')
def activate_sim_card(phone_number_info: PhoneNumber):
    """
    activate sim card and phone number
    """
    phone_number_info_dict = phone_number_info.model_dump()
    print(f'.................{phone_number_info_dict.get("phone_number")}')
    random_num = random.randint(0,2)
    if random_num < 2:
        return {"activate": True, "phone_number":phone_number_info_dict.get("phone_number")}
    else:
        raise HTTPException(status_code=400, detail="unable to activate sim card")

        
# ...................................................... billing system 

@app.post("/bill-calculation")
def calculate_bill(request: BillingRequest):
    """
    Calculating total bill based on the plan type.
    """
    base_price = 150000 if request.plan_type == "D" else 100000
    tax = int(base_price * 0.09)
    total = base_price + tax

    return {
        "message": "Billing calculated",
        "national_code": request.national_code,
        "phone_number": request.phone_number,
        "plan_type": request.plan_type,
        "bill_id": f"BILL-{random.randint(1000, 9999)}",
        "total": total
    }




@app.post('/billing-system-update')
def update_billing_system(billing_info: BillingInfo):
    """
    Update billing system with the calculated bill.
    """
    billing_dict = billing_info.model_dump()
    
    if not billing_dict.get("bill_id") or not billing_dict.get("total"):
        raise HTTPException(status_code=400, detail="Missing billing data")

    return {
        "message": "Billing updated",
        "bill_id": billing_dict.get("bill_id"),
        "phone_number" : billing_dict.get("phone_number"),
        "total" : billing_dict.get("total")
    }


        


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