from fastapi import FastAPI, HTTPException
from customer_model import (
    CustomerInfo, 
    PhoneNumber, 
    BillingRequest, 
    BillingInfo, 
    EmailInfo,
    BaseCustomerInfo,
    NA,
    Email,
    OTPModel,
    SimCardInfo
)
from database.db import customer_data
import random
import smtplib
from email.message import EmailMessage
import re
# pattern = r'^\d{10}$'
#     return bool(re.match(pattern, input_string))


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
    f_name = customer_info_dict.get("f_name")
    l_name = customer_info_dict.get("l_name")
    national_code = customer_info_dict.get("national_code")
    city = customer_info_dict.get("city")
    plan_type = customer_info_dict.get("plan_type")
    phone_number = customer_info_dict.get("phone_number")
    email = customer_info_dict.get("email")
    customer_data.append([national_code, f_name, l_name, city, plan_type, phone_number, email])
    
    return {"message":"stored"}
        


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

@app.post("/payment")
def pay_cost(sim_info: SimCardInfo):
    """
    simulate payment gateway
    """
    sim_info_dict = sim_info.model_dump()
    plan_type = sim_info_dict.get("plan_type")

    base_price = 150000 if plan_type == "D" else 100000
    tax = int(base_price * 0.09)
    total = base_price + tax

    return {
        "message": "payed",
        "plan_type": plan_type,
        "pay_id": f"BILL-{random.randint(1000, 9999)}",
        "total": total
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



#CEM..............................................

OTP_code_generated:str = "2347"
@app.post('/NA-validation')
def validate_NA(national_code: NA):
    """
    get national code and check it to be valid
    """
    national_code_dict = national_code.model_dump()
    
    if national_code_dict.get("national_code"):
        national_code = national_code_dict.get("national_code")
        if len(national_code) != 10:
            raise HTTPException(status_code=400, detail="NA code isnt correct ")

    
    return {"isValid": True}


@app.post('/OTP')
def send_OTP(customer_email: Email):
    """
    get email and send OTP
    """
    customer_email_dict = customer_email.model_dump()
    des_email = customer_email_dict.get("email")


    msg = EmailMessage()
    msg["Subject"] = "OTP code"
    msg["From"] = "amirali.safa2004@gmail.com"
    msg["To"] = des_email
    msg.set_content("this is your OTP code : "+OTP_code_generated)


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
        raise HTTPException(status_code=500)




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
        return {"canActive": False, "message":"too much phone_number for this person"}
    
    return {"canActive":True, "message":"user can buy another phone number"}


@app.post('/OTP-validation')
def check_OTP(OTP_code: OTPModel):
    """
    get otp and validate it 
    """
    OTP_code_dict = OTP_code.model_dump()
    code = OTP_code_dict.get("OTP_code")
    
    if code == OTP_code_generated:
        print("hello its here ")
        return {"validOTP": True, "message":"code is valid"}
    
    return {"validOTP": False, "message":"code is not valid"} 