'''
Created on Mar 14, 2020

@author: Sabinas
'''
from abc import ABC, abstractmethod
from datetime import datetime
#Medication Class

class Medication():
    def __init__(self, code, name, maxDose, doseLimit, rate):
        #instance attributes
        self._code = code
        self._name = name 
        self._maximumDosageAllowedPerKg = maxDose
        self._dosageLimit = doseLimit
        self._rateType = rate
        
        
        #getters and setter methods
    
    @property
    def getCode(self):
        return self._code
    
    @property
    def name(self):
        return self._name
    
    @property
    def maxDose(self):
        return self._maximumDosageAllowedPerKg
    
    def setMaxDose(self, newMax):
        self._maximumDosageAllowedPerKg = newMax
    
    @property
    def dosageLimit(self):
        return self._dosageLimit
    
    @dosageLimit.setter
    def dosageLimit(self, newLimit):
        self._dosageLimit = newLimit
        
    @property
    def rateType(self):
        return self._rateType
    
    def recommendedDosage(self, weight, age):
        self._weight = weight
        self._age = age
        if (self._weight * self.maxDose) <= self._dosageLimit:
            if (self._age <= 12):
                return (self._weight * self.maxDose / 2)
            else:
                return (self._weight * self.maxDose)
        
    def compareStrength(self, anotherMed):
        if self._dosageLimit == anotherMed._dosageLimit:
            return 0
        
        if self._dosageLimit < anotherMed._dosageLimit:
            return 1

        if self._dosageLimit > anotherMed._dosageLimit:
            return -1


    def __str__(self):
        return f'{self._code} {self._name}    Max dose/kg: {self._maximumDosageAllowedPerKg}mg Dose Limit: {self._dosageLimit}mg Rate Type: {self._rateType}'
    

#prescription class
class PrescribedItem():
    def __init__(self, dose, freq, duration, med):
        self._dosage = dose
        self._frequencyPerDay = freq
        self._duration = duration
        self._medicine = med
        
        
    @property
    def getMed(self):
        return self._medicine
    
    @property
    def getMedRate(self):
        return self._medicine.rateType #calling from obj med class
    @property
    def medCode(self):
        return self._medicine.getCode
    
    @property
    def getDosage(self):
        return self._dosage
    
    @property
    def getDuration(self):
        return self._duration
    
    @property
    def getFrequency(self):
        return self._frequencyPerDay
    
    @property
    def qtyDispensed(self):
        qty = self._dosage * (self._frequencyPerDay * self._duration)
        return qty
    
    @property
    def dosageStrength(self):
        return self._dosage / self._medicine.dosageLimit
        

    def __str__(self):
        return f'{self.getMed} \n\t{self.qtyDispensed}mg dispensed at {self._dosage}mg {self._frequencyPerDay} times per day for {self._duration} days'



#clinic class
class Clinic():
    def __init__(self):
        self._medicationList = {}
        self._patientList = {}
        
    def searchMedicationByCode(self, code):
        if code in self._medicationList.keys():
            return True
        else:
            return False
            

    def addMedication(self, medication):
        if medication in self._medicationList.values():
            print(f'Medication: {medication.getCode} already added.')
        else:
            self._medicationList[medication.getCode] = medication
            
    def medicationStr(self):
        print(f'Medication List: {len(self._medicationList)}')
        for key in sorted(self._medicationList.keys()): #sort via key
            print(self._medicationList[key])
            
    def searchPatient(self, patientID):
        if patientID in self._patientList.keys():
            return patientID
        else:
            return None
        
    def addPatient(self, patient):
        if patient in self._patientList.values():
            print(f'Patient: {patient.patientID} already added.')
            return False
        else:
            self._patientList[patient.patientID] = patient
            return True
        
    def removePatient(self, patient):
        if patient in self._patientList.keys():
            print(f'Patient: {patient.patientID} deleted.')
            self._patientList.pop(patient)
        else:
            return None
        
    def patientStr(self):
        print(f'\nPatient List: {len(self._patientList)}')
        for key in sorted(self._patientList.keys()):
            print(self._patientList[key])
            
    def __str__(self):
        return f'Medication List: {len(self._medicationList)}\n {self.medicationStr()}\n\nPatient List: {len(self._patientList)}\n{self.patientStr()}'
            
#subclass of Medication
class AgeLimitedMedication(Medication):
    def __init__(self, code, name, maxDose, doseLimit, rate, minimumAge):
        super().__init__(code, name, maxDose, doseLimit, rate)
        self._minAge = minimumAge
    @property 
    def minimumAge(self):
        return self._minAge
    
    @minimumAge.setter 
    def minimumAge(self, newMinimumAge):
        self._minAge = newMinimumAge
        
    #overriding of recommendedDosage def
    def recommendedDosage(self, weight, age):
        self._weight = weight
        self._age = age
        if self._age < self.minimumAge:
            return 0
        elif (self._weight * self.maxDose) <= self._dosageLimit:
            if (self._age <= 12):
                return (self._weight * self.maxDose / 2)
            else:
                return (self._weight * self.maxDose)
    
    def __str__(self):
        return f'{self._code} {self._name}    Max dose/kg: {self._maximumDosageAllowedPerKg}mg Dose Limit: {self._dosageLimit}mg Rate Type: {self._rateType} Minimum Age: {self._minAge}'
        

#abstract visit class
class Visit(ABC):
    _consultRate = 35
    nextID = 1
    def __init__(self, visitDate, patientWeight):
        self._visitDate = visitDate
        self._patientWeight = patientWeight
        self._prescribedItemList = []
        self._totalCost = 0
        self._visitID = Visit.nextID
        Visit.nextID += 1
        
    #classmethod
    @classmethod
    def getConsultRate(cls):
        return cls._consultRate
    
    @classmethod
    def setConsultRate(cls, amt):
        cls._consultRate = amt
        
    @property
    def visitID(self):
        return self._visitID
    @property
    def visitDate(self):
        return self._visitDate
    @property
    def patientWeight(self):
        return self._patientWeight
    @property
    def totalCost(self):
        return self._totalCost

    def setTotalCost(self, amt):
        self._totalCost = amt
    
    def searchPrescribedItem(self, med):
        if med in self._prescribedItemList:
            return med
        else:
            return False 
    
    def addPrescribedItem(self, med):
        if med in self._prescribedItemList:
            return False
        else:
            self._prescribedItemList.append(med)
            return True
    
    def removePrescribedItem(self, med):
        if med in self._prescribedItemList:
            self._prescribedItemList.remove(med)
            return True 
        else:
            return False 
    
    def getPrecriptionCost(self, med):
        return med.qtyDispensed * (self.getRatePerPrescriptionItem(med.getMedRate) * med.getMedRate)
        
    def prescribedItemListStr(self):
        for p in self._prescribedItemList:
            print(p)
            
    @abstractmethod 
    def getRatePerPrescriptionItem(self):
        pass
    
#subclass of Visit
class CorporateVisit(Visit):
    _consultRate = 20
    _companyRef = 'none'
    def __init__(self, visitDate, patientWeight, companyRef):
        super().__init__(visitDate, patientWeight)
        self._visitDate = visitDate
        self._patientWeight = patientWeight
        self._companyRef = companyRef
    
    
    def getRatePerPrescriptionItem(self, rateType):
        rate = 0.1
        if rateType >= 4:
            rate = 0.075
        return rate
        
    def __str__(self):
        return f'ID No: {self._visitID} {self.visitDate.strftime("%a, %d %b %Y")} @{self._patientWeight}kg Total: ${self._totalCost:.2f} Company: {self._companyRef}\n'
        
class PrivateVisit(Visit):
        
    def getRatePerPrescriptionItem(self):
        rate = 0.1
        return rate
        
    def __str__(self):
        return f'ID No: {self._visitID} {self.visitDate.strftime("%a, %d %b %Y")} @{self._patientWeight}kg Total: ${self._totalCost:.2f}'

class ClinicException (Exception):
    pass
    
    
class Patient():
    def __init__(self, pID, dob, weight):
        self._visitList = []
        self._patientID = pID
        self._weight = weight
        self._today_date = datetime.now()
        self._dateofBirth = dob #to pass datetime obj
        #exception is raised here.
        if self._dateofBirth > self._today_date:
            raise ClinicException("Birth date {} should not be later than today {}".format(dob.strftime("%d %b %Y"), self._today_date.strftime("%d %b %Y")))
        
        if self._weight <= 0:
            raise ClinicException("Invalid weight {}kg!".format(self.weight))
    #getter
    @property
    def patientID(self):
        return self._patientID
    
    @property
    def dateOfBirth(self):
        return self._dateofBirth
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter 
    def weight(self, newWeight):
        if newWeight <= 0:
            raise ClinicException("Invalid weight {}kg!".format(newWeight))
        else:
            self._weight = newWeight
            
            
    def visitList(self, fromDate, toDate):
        self._fromDate = None 
        self._toDate = None 
        if self._fromDate is None and self._toDate is None:
            for x in self._visitList:
                if self._visitList[x].visitDate() <= self._toDate:
                    print(x)
        elif self._fromDate is not None and self._toDate is None:
            for x in self._visitList:
                if self._visitList[x].visitDate() >= self._fromDate:
                    print(x)
        else:
            for x in self._visitList:
                if self._visitList[x].visitDate() >= self._fromDate and self._visitList[x].visitDate() <= self._toDate:
                    print(x)
                    
    def addVisit(self, visit):
#         self._lastVisit = self._visitList[-1].visitDate
#         self._diff = self._lastVisit - visit.visitDate
#         if len(self._visitList) >= 4 and self._diff.days <= 7:
#             raise ClinicException("This is the fourth visit in a week block")
#         else:
            self._visitList.append(visit)
        
    def __str__(self):
        return f'\n{self._patientID} Date of Birth: {self._dateofBirth.strftime("%d %b %Y")} {self._weight}kg\n Visits: {len(self._visitList)}\n'
        for x in self._visitList:
            return self._visitList[x].prescribedItemListStr()

def main():
    

    #construct the medicines
    m1 = Medication('CP12', 'Chloro-6 pheniramine-X', 0.08, 4.0, 3)
    m3 = Medication('DM01', 'Dex-2 trimethorphan-0', 0.25, 15.0, 2)
    m2 = Medication('LH03', 'Lyso-X Hydrochloride', 1.00, 10.0, 1)
    alm1 = AgeLimitedMedication("ZE01", "Zoledra-Enic1", 0.08, 4.0, 4, 16)

    p1 = PrescribedItem(10, 3, 5, m3)
    p2 = PrescribedItem(4, 3, 5, alm1)

    cv1Date = datetime(2020, 1, 20)
    pv1Date = datetime(2020, 3, 20)
    cv1 = CorporateVisit(cv1Date, 65.5, 'C0123')
    pv1 = PrivateVisit(pv1Date, 65.5)
    cv1.addPrescribedItem(p1)
    cv1.addPrescribedItem(p2)
    pv1.addPrescribedItem(p1)
    pv1.addPrescribedItem(p2)
    
    #to add money
    cv1.setTotalCost(cv1.getPrecriptionCost(p1) + cv1.getPrecriptionCost(p2) + cv1.getConsultRate())
    pv1.setTotalCost((p1.qtyDispensed * (pv1.getRatePerPrescriptionItem() * p1.getMedRate)) + (p2.qtyDispensed * (pv1.getRatePerPrescriptionItem() * p2.getMedRate)) + pv1.getConsultRate())
    
#     print(cv1)
#     cv1.prescribedItemListStr()
#  
#     print(pv1)
#     pv1.prescribedItemListStr()

    p1Date = datetime(2004, 3, 26)
    p2Date = datetime(1993, 3, 26)
    p3Date = datetime(2010, 4, 12)
    p4Date = datetime(2012, 12, 25)
    patient1 = Patient("T0002", p1Date, 48.4)
    patient2 = Patient("T0001", p2Date, 65.5)
    patient3 = Patient("T0003", p3Date, 36.3)
    patient4 = Patient("T0004", p4Date, 41.8)
    
    #adding the visits into Patient class
    patient2.addVisit(cv1)
    patient2.addVisit(pv1)
    
    #opening Clinic Medication List & patient List
    clinicMedList = Clinic()
    clinicPatientList = Clinic()
    
    clinicMedList.addMedication(m1)
    clinicMedList.addMedication(m2)
    clinicMedList.addMedication(m3)
    clinicMedList.addMedication(alm1)
    
    clinicPatientList.addPatient(patient1)
    clinicPatientList.addPatient(patient2)
    clinicPatientList.addPatient(patient3)
    clinicPatientList.addPatient(patient4)
    
    clinicMedList.medicationStr()
    clinicPatientList.patientStr()
    
main()