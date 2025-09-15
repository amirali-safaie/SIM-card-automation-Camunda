from fastapi import FastAPI, HTTPException
from customer_model import CustomerInfo

app = FastAPI(title="sim card provision apis")

@app.post('/info-validation')
def validate_customer_info(customer_info: CustomerInfo):
    """
    get customer data and validate it and return a result as bool
    """
    
    customer_info_dict = customer_info.model_dump()

    if not (customer_info_dict.get("f_name") and customer_info_dict.get("l_name") and customer_info_dict.get("city")):
        raise HTTPException(status_code=400, detail="Invalid customer info")


    if customer_info_dict.get("national_code"):
        if len(customer_info_dict.get("national_code")) != 10:
            raise HTTPException(status_code=400, detail="Invalid customer info")
    
    return {"success": True}
        


@app.post('/customer-info')
def store_customer_info(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    customer_info_dict = customer_info.model_dump()

    pass
    
    return {"success": True}
        


@app.post('/bill-calculation')
def calculate_bill(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    customer_info_dict = customer_info.model_dump()

    pass
    
    return {"success": True}
        

@app.post('/store-bill')
def store_bill(customer_info: CustomerInfo):
    """
    get customer data store it into db
    """
    
    customer_info_dict = customer_info.model_dump()

    pass
    
    return {"success": True}
        