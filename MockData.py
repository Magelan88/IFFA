from faker import Faker
import numpy as np
import re

companyTypes={
    "Hairdesser",
    "IT Consultant",
    "Photographer",
    "Eventmanager",
    "Waiter/Waitress",
    "Plumer",
    "Carpenter",
    "Butcher",
}


def fake_Tax(TaxID, AidDemand=5000):
    fake = Faker(locale="en_IE")    
    r ={       
       "name": fake.name(),
       "VATID": TaxID,
       "age": np.random.randint(15, 88),
       "address": fake.address().replace("\n", ', '),
       "citizen": np.random.rand() < 0.9,
       "workInCountry": np.random.rand() < 0.95,
       "taxedInCountry": np.random.rand() < 0.95,
       "full_time" : np.random.rand() < 0.7,
       "studentStatus" : np.random.rand() < 0.9,
       "layedOffCorona" : np.random.rand() < 0.4,
       "businessName": fake.company(),
       "business": np.random.choice( list(companyTypes)),
       "founded": 2020 - int(np.random.exponential(7)),
       "employees": int(np.random.exponential(2)),
       "annualTurnover": np.round(int(np.random.exponential(100_000)) + np.random.normal(10_000, 20_000), 2),
       "covidReductionPct": np.round(np.random.normal(0.5,0.1), 3)*10**2,
       "aidDemand": AidDemand,
       "IBAN": fake.iban()
        
    }
    
    r["zipCode"] = re.findall( "\d{4,5}", r["address"])[-1]    
    return r