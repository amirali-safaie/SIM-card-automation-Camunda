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
from database.db import customer_data,bills
import random
import smtplib
from email.message import EmailMessage
from datetime import datetime
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
    required_fields = {"f_name", "l_name", "city", "plan_type"}
    
    
    for field in required_fields:
        if not customer_info_dict.get(field):
            print("bad request for field ",field)
            raise HTTPException(status_code=400, detail=f"Invalid customer info: Missing or empty field '{field}'")
   
    plan_type = customer_info_dict.get("plan_type")
    print(f'reccied :::: {customer_info_dict}')

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
    print(f'new database is : \n {customer_data}')
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
    Calculate bill and create bill object with customer info and creation timestamp.
    """
    
    bill = {
        "national_code": request.national_code,
        "phone_number": request.phone_number,
        "plan_type": request.plan_type,
        "total": 0,
        "created_at": datetime.now()
    }
    
    return {
        "message": "Billing calculated",
        "national_code": bill.get("national_code"),
        "phone_number": bill.get("phone_number"),
        "plan_type":bill.get("plan_type"),
        "total": bill.get("total"),
        "created_at": bill.get("created_at")
    }

@app.post('/billing-system-update')
def update_billing_system(billing_info: BillingInfo):
    """
    Update billing system by storing bill in array using same pattern as customer info.
    """
    billing_info_dict = billing_info.model_dump()
    national_code = billing_info_dict.get("national_code")
    phone_number = billing_info_dict.get("phone_number")
    plan_type = billing_info_dict.get("plan_type")
    total = billing_info_dict.get("total")
    created_at = billing_info_dict.get("created_at")
    
    bills.append([national_code, phone_number, plan_type, total, created_at])
    print(f'new database is : \n {bills}')
    
    return {"message": "Billinf system updated"}

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

from datetime import datetime

@app.post('/customer-notice')
def send_email_to_customer(mail_info: EmailInfo):
    """
    send rejection or confirmation email to customer
    """
    mail_info_dict = mail_info.model_dump()
    email = mail_info_dict.get("email")

    msg = EmailMessage()
    if mail_info_dict.get("email_type") == "confirmation":
        msg["Subject"] = "✓ SIM Card Activation Successful - MTN Irancell"
    else:
        msg["Subject"] = "SIM Card Activation Update - MTN Irancell"
    msg["From"] = "amirali.safa2004@gmail.com"
    msg["To"] = email

    national_code = mail_info_dict.get("national_code", "N/A")

    phone_number = mail_info_dict.get("phone_number", "N/A")

    if mail_info_dict.get("email_type") == "confirmation":
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 40px 30px; text-align: center;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">MTN Irancell</h1>
                                    <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 14px;">Your Trusted Mobile Network</p>
                                </td>
                            </tr>
                            
                            <!-- Success Icon -->
                            <tr>
                                <td style="padding: 40px 30px 20px; text-align: center;">
                                    <div style="width: 80px; height: 80px; background-color: #4CAF50; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                                        <span style="color: white; font-size: 48px; line-height: 80px;">✓</span>
                                    </div>
                                </td>
                            </tr>
                            
                            <!-- Content -->
                            <tr>
                                <td style="padding: 0 30px 30px;">
                                    <h2 style="color: #333333; font-size: 24px; margin: 0 0 20px 0; text-align: center;">Activation Successful!</h2>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                        Dear Valued Customer,
                                    </p>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                        We're pleased to inform you that your SIM card has been <strong style="color: #4CAF50;">successfully activated</strong>.
                                    </p>
                                    
                                    <!-- Info Box -->
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa; border-radius: 6px; margin: 20px 0;">
                                        <tr>
                                            <td style="padding: 20px;">
                                                <p style="margin: 0; color: #666666; font-size: 14px;">
                                                    <strong style="color: #333333;">Customer ID:</strong> {national_code}
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 20px;">
                                                <p style="margin: 0; color: #666666; font-size: 14px;">
                                                    <strong style="color: #333333;">Customer phone number:</strong> {phone_number}
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 20px 0;">
                                        You can now enjoy our premium mobile services, high-speed data, and nationwide coverage.
                                    </p>
                                    
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 20px 0 30px 0;">
                                        Thank you for choosing MTN Irancell. We're committed to providing you with the best mobile experience.
                                    </p>
                                    
                                    
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                    <p style="margin: 0 0 10px 0; color: #999999; font-size: 14px;">
                                        Need help? Contact our support team
                                    </p>
                                    <p style="margin: 0 0 15px 0; color: #666666; font-size: 14px;">
                                        📞 Call: 0000-000-0000 | 📧 Email: simActivationTeam@mtnirancell.com
                                    </p>
                                    <p style="margin: 15px 0 0 0; color: #999999; font-size: 12px;">
                                        © 2025 MTN Irancell. All rights reserved.<br>
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        text_content = f"Dear customer {national_code} with the phone number {phone_number}, your SIM card has been activated successfully. Thank you for choosing MTN Irancell."
    else:  
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 40px 30px; text-align: center;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">MTN Irancell</h1>
                                    <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 14px;">Your Trusted Mobile Network</p>
                                </td>
                            </tr>
                            
                            <!-- Info Icon -->
                            <tr>
                                <td style="padding: 40px 30px 20px; text-align: center;">
                                    <div style="width: 80px; height: 80px; background-color: #FF9800; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                                        <span style="color: white; font-size: 48px; line-height: 80px;">ℹ</span>
                                    </div>
                                </td>
                            </tr>
                            
                            <!-- Content -->
                            <tr>
                                <td style="padding: 0 30px 30px;">
                                    <h2 style="color: #333333; font-size: 24px; margin: 0 0 20px 0; text-align: center;">Activation Request Update</h2>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                        Dear Valued Customer,
                                    </p>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                        We regret to inform you that we were unable to process your SIM card activation request at this time.
                                    </p>
                                    
                                    <!-- Info Box -->
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #fff3e0; border-left: 4px solid #FF9800; border-radius: 6px; margin: 20px 0;">
                                        <tr>
                                            <td style="padding: 20px;">
                                                <p style="margin: 0 0 10px 0; color: #333333; font-size: 14px; font-weight: bold;">
                                                    Customer ID: {national_code}
                                                </p>
                                                <p style="margin: 0; color: #666666; font-size: 14px; line-height: 1.5;">
                                                    This may be due to incomplete documentation, verification issues, or other requirements that need to be addressed.
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 20px 0;">
                                        <strong>What to do next:</strong>
                                    </p>
                                    <ul style="color: #666666; font-size: 15px; line-height: 1.8; margin: 0 0 20px 20px; padding: 0;">
                                        <li>Contact our support team for detailed information</li>
                                        <li>Ensure all required documents are complete and valid</li>
                                    </ul>
                                    
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 20px 0 30px 0;">
                                        We apologize for any inconvenience and look forward to serving you soon.
                                    </p>
                                    
                                    <!-- CTA Button -->
                                    <div style="text-align: center; margin: 30px 0;">
                                        <a href="#" style="display: inline-block; background-color: #FF9800; color: #ffffff; text-decoration: none; padding: 14px 40px; border-radius: 6px; font-weight: bold; font-size: 16px;">Contact Support</a>
                                    </div>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                    <p style="margin: 0 0 10px 0; color: #999999; font-size: 14px;">
                                        Need immediate assistance?
                                    </p>
                                    <p style="margin: 0 0 15px 0; color: #666666; font-size: 14px;">
                                        📞 Call: 0000-000-0000 | 📧 Email: simActivationTeam@mtnirancell.com
                                    </p>
                                    <p style="margin: 15px 0 0 0; color: #999999; font-size: 12px;">
                                        © 2025 MTN Irancell. All rights reserved.<br>
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        text_content = f"Dear customer {national_code} with the phone number {phone_number}, we regret to inform you that your SIM card activation request has been rejected. Please contact our support team for more information."

    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype='html')

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    email_sender = "amirali.safa2004@gmail.com"
    password = "tjzh oyvr wrhl cxqe" 
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_sender, password)
            server.send_message(msg)
        return {"message": "email sent"}
    except Exception as e:
        print("Error sending email:", e)
        raise HTTPException(status_code=400, detail="unable to send email")


@app.post('/IT-notice')
def send_email_to_IT(customer_info: CustomerInfo):
    """
    aware IT team of some problem
    """
    customer_info_dict = customer_info.model_dump()
    
    msg = EmailMessage()
    msg["Subject"] = "⚠️ SIM Activation Process Alert - Review Required"
    msg["From"] = "amirali.safa2004@gmail.com"
    msg["To"] = "ftmekhvri@gmail.com"
    
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="650" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); padding: 30px; text-align: left;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="width: 60px; vertical-align: middle;">
                                            <div style="width: 50px; height: 50px; background-color: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                                <span style="color: white; font-size: 32px; line-height: 50px;">⚠</span>
                                            </div>
                                        </td>
                                        <td style="vertical-align: middle; padding-left: 15px;">
                                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: bold;">System Alert</h1>
                                            <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.9); font-size: 14px;">SIM Activation Process - Action Required</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Alert Badge -->
                        <tr>
                            <td style="padding: 0;">
                                <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px 30px;">
                                    <p style="margin: 0; color: #856404; font-size: 14px; font-weight: bold;">
                                        🔔 Priority: Medium | Category: SIM Activation
                                    </p>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 30px;">
                                <h2 style="color: #333333; font-size: 20px; margin: 0 0 20px 0;">Hello IT Team,</h2>
                                
                                <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                    An issue has been detected during the SIM card activation process that requires your attention.
                                </p>
                                
                                <!-- Issue Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #fff5f5; border: 2px solid #feb2b2; border-radius: 8px; margin: 25px 0;">
                                    <tr>
                                        <td style="padding: 25px;">
                                            <h3 style="margin: 0 0 15px 0; color: #c53030; font-size: 18px;">⚠️ Process Error Detected</h3>
                                            <p style="margin: 0; color: #742a2a; font-size: 15px; line-height: 1.6; font-weight: 500;">
                                                There is a problem in the SIM activation code process. Please check and review the system immediately.
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Customer Details -->
                                <h3 style="color: #333333; font-size: 18px; margin: 25px 0 15px 0;">📋 Related Customer Information</h3>
                                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa; border-radius: 6px; border: 1px solid #e0e0e0;">
                                    <tr>
                                        <td style="padding: 20px;">
                                            <table width="100%" cellpadding="8" cellspacing="0">
                                                
                                                <tr>
                                                    <td style="color: #666666; font-size: 14px; padding: 8px 0; border-top: 1px solid #e0e0e0;">
                                                        <strong style="color: #333333;">Timestamp:</strong>
                                                    </td>
                                                    <td style="color: #333333; font-size: 14px; padding: 8px 0; border-top: 1px solid #e0e0e0; font-family: 'Courier New', monospace;">
                                                        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Action Items -->
                                <h3 style="color: #333333; font-size: 18px; margin: 25px 0 15px 0;">✅ Recommended Actions</h3>
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 0 0 25px 0;">
                                    <tr>
                                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background-color: #007bff; color: white; text-align: center; line-height: 28px; border-radius: 50%; font-size: 14px; font-weight: bold; margin-right: 12px;">1</span>
                                            <span style="color: #666666; font-size: 15px; line-height: 1.6;">Review the SIM activation code generation process</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background-color: #007bff; color: white; text-align: center; line-height: 28px; border-radius: 50%; font-size: 14px; font-weight: bold; margin-right: 12px;">2</span>
                                            <span style="color: #666666; font-size: 15px; line-height: 1.6;">Check system logs for any errors or anomalies</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background-color: #007bff; color: white; text-align: center; line-height: 28px; border-radius: 50%; font-size: 14px; font-weight: bold; margin-right: 12px;">3</span>
                                            <span style="color: #666666; font-size: 15px; line-height: 1.6;">Verify database connectivity and data integrity</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 12px 0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background-color: #007bff; color: white; text-align: center; line-height: 28px; border-radius: 50%; font-size: 14px; font-weight: bold; margin-right: 12px;">4</span>
                                            <span style="color: #666666; font-size: 15px; line-height: 1.6;">Monitor the system for any recurring issues</span>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="color: #666666; font-size: 15px; line-height: 1.6; margin: 25px 0 0 0;">
                                    Please investigate this matter at your earliest convenience and update the incident tracking system once resolved.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 25px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="margin: 0 0 10px 0; color: #666666; font-size: 13px;">
                                    This is an automated system notification from MTN Irancell SIM Activation Service
                                </p>
                                <p style="margin: 0; color: #999999; font-size: 12px;">
                                    © 2025 MTN Irancell IT Department | Internal Use Only
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    text_content = f"""
    SYSTEM ALERT: SIM Activation Process Error
    
    Hello IT Team,
    
    An issue has been detected during the SIM card activation process that requires your attention.
    
    PROCESS ERROR DETECTED:
    There is a problem in the SIM activation code process. Please check and review the system immediately.
    
    - Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    RECOMMENDED ACTIONS:
    1. Review the SIM activation code generation process
    2. Check system logs for any errors or anomalies
    3. Verify database connectivity and data integrity
    4. Monitor the system for any recurring issues
    
    Please investigate this matter at your earliest convenience.
    
    ---
    This is an automated system notification from MTN Irancell SIM Activation Service
    """
    
    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype='html')
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    email_sender = "amirali.safa2004@gmail.com"
    password = "tjzh oyvr wrhl cxqe"
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_sender, password)
            server.send_message(msg)
        return {"message": "IT notification email sent"}
    except Exception as e:
        print("Error sending IT notification:", e)
        raise HTTPException(status_code=400, detail="unable to send IT notification")



#CEM..............................................

OTP_code_generated:str = "2347"

@app.post('/NA-validation')
def validate_NA(national_code: NA):
    """
    get national code and check it to be valid
    """
    national_code_dict = national_code.model_dump()
    
    if not national_code_dict.get("national_code"):
        raise HTTPException(status_code=400, detail="NA code isn't correct ")
    
    national_code = national_code_dict.get("national_code")
    if len(national_code) != 10:
        raise HTTPException(status_code=400, detail="NA code isn't correct ")

    
    return {"isValid": True}


@app.post('/OTP')
def send_OTP(customer_email: Email):
    """
    get email and send OTP
    """
    customer_email_dict = customer_email.model_dump()
    des_email = customer_email_dict.get("email")
    global OTP_code_generated
    OTP_code_generated = str(random.randint(1000,9999))

    msg = EmailMessage()
    msg["Subject"] = "🔐 Your OTP Code - MTN Irancell"
    msg["From"] = "amirali.safa2004@gmail.com"
    msg["To"] = des_email
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 40px 30px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">MTN Irancell</h1>
                                <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 14px;">Your Trusted Mobile Network</p>
                            </td>
                        </tr>
                        
                        <!-- Lock Icon -->
                        <tr>
                            <td style="padding: 40px 30px 20px; text-align: center;">
                                <div style="width: 80px; height: 80px; background-color: #2196F3; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                                    <span style="color: white; font-size: 48px; line-height: 80px;">🔐</span>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 0 30px 30px;">
                                <h2 style="color: #333333; font-size: 24px; margin: 0 0 20px 0; text-align: center;">Verification Code</h2>
                                <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0; text-align: center;">
                                    Please use the following One-Time Password (OTP) to complete your verification:
                                </p>
                                
                                <!-- OTP Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 30px; display: inline-block;">
                                                <p style="margin: 0 0 10px 0; color: rgba(255,255,255,0.9); font-size: 14px; font-weight: 600; letter-spacing: 1px;">YOUR OTP CODE</p>
                                                <p style="margin: 0; color: #ffffff; font-size: 48px; font-weight: bold; letter-spacing: 8px; font-family: 'Courier New', monospace;">{OTP_code_generated}</p>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Warning Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #fff3e0; border-left: 4px solid #FF9800; border-radius: 6px; margin: 30px 0;">
                                    <tr>
                                        <td style="padding: 20px;">
                                            <p style="margin: 0 0 10px 0; color: #333333; font-size: 14px; font-weight: bold;">
                                                ⏱️ Important Security Notice:
                                            </p>
                                            <ul style="margin: 0; padding-left: 20px; color: #666666; font-size: 14px; line-height: 1.6;">
                                                <li>This code is valid for 5 minutes</li>
                                            </ul>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="color: #666666; font-size: 15px; line-height: 1.6; margin: 25px 0 0 0; text-align: center;">
                                    If you didn't request this code, please ignore this email or contact our support team immediately.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="margin: 0 0 10px 0; color: #999999; font-size: 14px;">
                                    Need help? Contact our support team
                                </p>
                                <p style="margin: 0 0 15px 0; color: #666666; font-size: 14px;">
                                    📞 Call: 0000-000-0000 | 📧 Email: simActivationTeam@mtnirancell.com
                                </p>
                                <p style="margin: 15px 0 0 0; color: #999999; font-size: 12px;">
                                    © 2025 MTN Irancell. All rights reserved.<br>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    text_content = f"Your OTP code is: {OTP_code_generated}. This code is valid for 10 minutes. Never share this code with anyone."
    
    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype='html')

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    email = "amirali.safa2004@gmail.com"
    password = "tjzh oyvr wrhl cxqe" 
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
        return {"message": "email sent"}
    except Exception as e:
        print("Error sending email:", e)
        raise HTTPException(status_code=500)



@app.post('/OTP-validation')
def check_OTP(OTP_code: OTPModel):
    """
    get otp and validate it 
    """

    OTP_code_dict = OTP_code.model_dump()
    code = OTP_code_dict.get("OTP_code")
    
    if code == OTP_code_generated:
        return {"validOTP": True, "message":"code is valid"}
    
    return {"validOTP": False, "message":"code is not valid"} 



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


