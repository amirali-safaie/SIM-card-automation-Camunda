## SIM Card Activation Workflow (Camunda 8 + FastAPI)
### This project demonstrates a SIM card activation process using Camunda 8 as the workflow engine and FastAPI as the backend service.
### It simulates how a telecom company activates SIM cards through an automated business process including CRM, validation, activation, billing

### tools :
* docker or podman
* python3.10+
* Fastapi
* Cammunda8

**Camunda** 8 for process orchestration (.bpmn workflows)

**FastAPI** for implementing REST APIs used in each workflow step

**Docker Compose** for running the full Camunda 8 stack locally

---
### The process includes:

- Customer information validation  
- National ID (NA) and OTP verification  
- SIM card assignment and activation  
- Billing and payment simulation  
- Email notifications to customer and IT team  
- Simple in-memory mock database 

--- 
### how to run :

first of all clone the project after of installing requirements do as blow :
change the docker compose file of cammunda to include your Fastapi dockerfile
run the docker compose (by docker or podman)     
`sudo docker compose up -d`

your apis will expose to `localhost:5000`  
you can see, and test them in `http://localhost:5000/docs`

---
then you can import and run flow and monitor them in operate and optimize and ...
here is the list of services:

Operate: http://localhost:8081  
Tasklist: http://localhost:8082  
Optimize: http://localhost:8083  
Identity: http://localhost:8084  
Web Modeler http://localhost:8070  
Elasticsearch: http://localhost:9200  
Keycloak is used to manage users, and can be accessed with the user admin and password admin:  
Keycloak: http://localhost:18080/auth/

#### list of some of endpoints:

| Endpoint                 | Method | Description                       |
|--------------------------|--------|-----------------------------------|
| `/info-validation`       | POST   | Validate customer info            |
| `/customer-info`         | POST   | Store customer info               |
| `/sim-card`              | POST   | Assign SIM card                   |
| `/sim-card-activation`   | POST   | Activate SIM card                 |
| `/bill-calculation`      | POST   | Calculate billing amount          |
| `/billing-system-update` | POST   | Save billing info                 |
| `/payment`               | POST   | Simulate customer payment         |
| `/customer-notice`       | POST   | Send confirmation/rejection email |
| `/IT-notice`             | POST   | Notify IT about errors            |
| `/NA-validation`         | POST   | Validate national code            |
| `/OTP`                   | POST   | Send OTP to customer              |
| `/OTP-validation`        | POST   | Validate OTP                      |
| `/shahkar`               | POST   | Check eligibility for new SIM     |  

----
👨‍💻 Authors:  
Amirali Safaie, Fatemeh khavari  
SIM Card Activation Process – Camunda 8 + FastAPI
