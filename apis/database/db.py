from datetime import datetime

customer_data = [
    # Ali Rezaei - 5 phone numbers
    ["1234567890", "Ali", "Rezaei", "Tehran", "D", "09123456789", "ali.rezaei@example.com"],
    ["1234567890", "Ali", "Rezaei", "Tehran", "D", "09123456790", "ali.rezaei@example.com"],
    ["1234567890", "Ali", "Rezaei", "Tehran", "D", "09123456791", "ali.rezaei@example.com"],
    ["1234567890", "Ali", "Rezaei", "Tehran", "D", "09123456792", "ali.rezaei@example.com"],
    ["1234567890", "Ali", "Rezaei", "Tehran", "D", "09123456793", "ali.rezaei@example.com"],

    # Sara Mohammadi – 10 phone numbers
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234560", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234561", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234562", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234563", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234564", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234565", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234566", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234567", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234568", "sara.mohammadi@example.com"],
    ["0987654321", "Sara", "Mohammadi", "Shiraz", "E", "09351234569", "sara.mohammadi@example.com"],

    # Hossein Nouri – 4 phone numbers
    ["5544332211", "Hossein", "Nouri", "Mashhad", "D", "09353334450", "hossein.nouri@example.com"],
    ["5544332211", "Hossein", "Nouri", "Mashhad", "D", "09353334451", "hossein.nouri@example.com"],
    ["5544332211", "Hossein", "Nouri", "Mashhad", "D", "09353334452", "hossein.nouri@example.com"],
    ["5544332211", "Hossein", "Nouri", "Mashhad", "D", "09353334453", "hossein.nouri@example.com"],

    # Unique individuals
    ["6677889900", "Fatemeh", "Ahmadi", "Tabriz", "E", "09148887766", "fatemeh.ahmadi@example.com"],
    ["3344556677", "Zahra", "Jafari", "Kerman", "D", "09381234567", "zahra.jafari@example.com"],
    ["7766554433", "Mehdi", "Shahbazi", "Qom", "E", "09121239876", "mehdi.shahbazi@example.com"],
    ["8899001122", "Niloofar", "Ghasemi", "Karaj", "D", "09201234567", "niloofar.ghasemi@example.com"],
    ["2233445566", "Omid", "Rahimi", "Yazd", "E", "09441234567", "omid.rahimi@example.com"],
    ["4455667788", "Amir", "Tavakoli", "Bandar Abbas", "D", "09229997766", "amir.tavakoli@example.com"]
]

bills = [
    ["1234567890", "09123456789", "D", 0, datetime(2025, 10, 1, 10, 30)],
    ["0987654321", "09234567890", "E", 0, datetime(2025, 10, 2, 14, 45)],
    ["1122334455", "09345678901", "D", 0, datetime(2025, 10, 3, 9, 15)]
]
