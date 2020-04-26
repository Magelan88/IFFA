from faker import Faker
import numpy as np
import re


class DecisionEngine():
    def __init__(self):
        self.path = []
    
    def __call__(self, record):
        self.R = record
        #self.path += "\n".join([ f"{k:17s}: {v}"  for k,v in record.items()]) + "\n\n"        
    
    def notEligible(self):
        decision = "We are sorry, you are not eligible for any aid"
        return self.path, decision
    
    
class MaltaDecisionEngine(DecisionEngine):
    
    Malta_Lists = {"ListA":{
                    "Hairdesser", 
                    "Photographer",
                    "Eventmanager",
                    "Waiter/Waitress",
                    },
               "ListB":{
                    "Plumer",
                    "Carpenter",
                    "Butcher",                   
                    }              
              }        
    
    def __call__(self, record):
        #self.R = record
        #self.path = "\n".join([ f"{k:17s}: {v}"  for k,v in record.items()]) + "\n"
        super(MaltaDecisionEngine, self).__call__(record)        
        return self.D1_Taxid()
    
    def D1_Taxid(self):
        decision = self.R["taxedInCountry"]        
        self.path.append(f"Do you have a Maltesian Tax ID? -> {decision}")
        
        if decision:
            return self.D2_MainActivityImpacted()
        else:
            return self.notEligible()       
    
    def D2_MainActivityImpacted(self):
        decision = self.R["covidReductionPct"] > 30.0        
        self.path.append(f"Is your main activity impacted (reduction > 30%)? -> {decision}")
        if decision:
            return self.D3_ActivitySector()
        else:
            return self.notEligible()       
        
    def D3_ActivitySector(self):
        try:
            decision = [ l for l,ct in Malta_Lists.items() if self.R["business"] in ct ][0]
        except:
            decision = "Other"            
        self.path.append(f"What list does your occupation fall under? -> {decision}")        
        if decision == "ListA":
            return self.D4_ListA_PartTime()
        elif decision == "ListB":
            return self.D4_ListB_PartTime()
        else:
            return self.notEligible()        
        
    def D4_ListA_PartTime(self):
        decision = self.R["full_time"]        
        self.path.append("Are you working full time? -> {decision}")        
        if decision:
            return self.A1_Eligible(800)
        else:
            return self.A1_Eligible(500)
 

    def D5_Gozo_Postalcode(self):
        decision = self.R["zipCode"].startswith("8")
        self.path.append(f"Do you live on Gozo (zip code check)? -> {decision}")
        if decision:
            return self.A1_Eligible(320)            
        else:
            return self.D6_ListB_PartTime()
                
    def D6_ListB_PartTime(self):
        decision = self.R["full_time"] 
        self.path.append(f"Are you working full time? -> {decision}")
        if decision:
            return self.A1_Eligible(160)
        else:
            return self.A1_Eligible(100)    
    
    def A1_Eligible(self, amount):
        decision = f"You are eligible to {amount}€ per month\n--> it is being transfered to your account: {self.R['IBAN']}"
        return self.path, decision
    
    
class IrelandDecisionEngine(DecisionEngine):
    def __call__(self, record):
        super(IrelandDecisionEngine, self).__call__(record)        
        return self.D1_Taxid()
    
    
    def D1_Taxid(self):
        decision = self.R["taxedInCountry"]        
        self.path.append(f"Do you have a Ireland Tax ID? -> {decision}")
        
        if decision:
            return self.D2_EmployableAge()
        else:
            return self.notEligible()
        
    def D2_EmployableAge(self):
        decision = (self.R["age"]) >= 18 & (self.R["age"]) <= 66
        self.path.append(f"* Are you between 18 and 66 years old? -> {decision}")
        
        if decision:
            return self.D3_EligibilityCriteria()
        else:
            return self.notEligible()
        
    def D3_EligibilityCriteria(self):        
        if self.R["studentStatus"]:
            return self.A1_Eligible(100*4)
        elif self.R["layedOffCorona"]:
            return self.A1_Eligible(350*4)
        elif self.R["employees"] == 0:
            return self.A1_Eligible(350*4)
        else:
            return self.notEligible()
        
    def A1_Eligible(self, amount):
        decision = f"You are eligible to {amount}€ per month\n--> it is being transfered to your account: {self.R['IBAN']}"
        return self.path, decision  