from fastapi import FastAPI, HTTPException
from customer_model import (
    CustomerInfo, 
    PhoneNumber, 
    BillingRequest, 
    BillingInfo, 
    EmailInfo,
    BaseCustomerInfo
)
from database.db import customer_data
import random
import smtplib
from email.message import EmailMessage


app = FastAPI(title="sim card provision apis")


@app.post('/shahkar')
def check_shahkar(customer_info: BaseCustomerInfo):
    """
    check that this natinal code is able to get number or not 
    """
    customer_info_dict = customer_info.model_dump()
    national_code = customer_info_dict.get("national_code")
    
    phone_number_counter = 0
    for customer in customer_data:
        if customer[0] == national_code:
            phone_number_counter += 1 

    if phone_number_counter >= 10:
        return {"can_buy": False, "message":"too much phone_number for this person"}
    
    return {"can_buy":True}

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

    print("here is working at all")
    if not billing_dict.get("bill_id") or not billing_dict.get("total"):
        raise HTTPException(status_code=400, detail="Missing billing data")

    return {
        "message": "saved",
    }


        
#...................................................................send email


@app.post('/customer-notice')
def send_email_to_customer(mail_info: EmailInfo):
    """
    send rejection or confirmation email to customer
    """
    mail_info_dict = mail_info.model_dump()

    msg = EmailMessage()
    if mail_info_dict.get("email_type") == "confirmation":
        msg["Subject"] = "buy confirmation"
    msg["Subject"] = "buy rejection"
    msg["From"] = "amirali.safa2004@gmail.com"
    msg["To"] = "amirali.safie@gmail.com"
    msg.set_content("Hello, this is a test email sent from MTN to announce you")


    smtp_server = "smtp.gmail.com"
    smtp_port = 587


    email = "amirali.safa2004@gmail.com"
    password = "tjzh oyvr wrhl cxqe" 
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(email, password)
            server.send_message(msg)
        return{"message":"email sent"}
    except Exception as e:
        print("Error sending email:", e)
        raise HTTPException(status_code=400, detail="unable to activate sim card")

@app.post('/IT-notice')
def send_email_to_IT(customer_info: CustomerInfo):
    """
    aware IT team of some problem
    """
    return{"message":"email sent"}





# {
#   "phone_number": null,
#   "national_code": null,
#   "total": 109000,
#   "plan_type": null,
#   "bill_id": "BILL-6616"
# }