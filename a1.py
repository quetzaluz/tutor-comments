'''
Created on Mar 14, 2020

@author: Sabinas
'''
from abc import ABC, abstractmethod
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
        return self._medicine.rateType #calling parent class method
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
        return f'{self.getMed} \n{self.qtyDispensed}mg dispensed at {self._dosage}mg {self._frequencyPerDay} times per day for {self._duration} days'



#clinic class
class Clinic:
    def __init__(self):
        self._medicationList = {}
        
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
        for key in sorted(self._medicationList.keys()): #sort via key
            print(self._medicationList[key])
            
            
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
        return f'ID No: {self._visitID} {self._visitDate} @{self._patientWeight}kg Total: ${self._totalCost} Company: {self._companyRef}'
        
class PrivateVisit(Visit):
    def __init__(self, visitDate, patientWeight):
        super().__init__(visitDate, patientWeight)
        
    def getRatePerPrescriptionItem(self):
        rate = 0.1
        return rate
        
    def __str__(self):
        return f'ID No: {self._visitID} {self._visitDate} @{self._patientWeight}kg Total: ${self._totalCost}'
    
def main():
    

    #construct the medicines
    m1 = Medication('CP12', 'Chloro-6 pheniramine-X', 0.08, 4.0, 3)
    m3 = Medication('DM01', 'Dex-2 trimethorphan-0', 0.25, 15.0, 2)
    m2 = Medication('LH03', 'Lyso-X Hydrochloride', 1.00, 10.0, 1)
    alm1 = AgeLimitedMedication("ZE01", "Zoledra-Enic1", 0.08, 4.0, 4, 16)

    p1 = PrescribedItem(10, 3, 5, m3)
    p2 = PrescribedItem(4, 3, 5, alm1)



    cv1 = CorporateVisit('27 March 2020', 65.5, 'C0123')
    pv1 = PrivateVisit("28 March 2020", 65.5)
    cv1.addPrescribedItem(p1)
    cv1.addPrescribedItem(p2)
    #to add money
    
    cv1.setTotalCost((p1.qtyDispensed * cv1.getRatePerPrescriptionItem(p1.getMedRate)) + (p2.qtyDispensed * cv1.getRatePerPrescriptionItem(p2.getMedRate)))
    
    print(p1.qtyDispensed *cv1.getRatePerPrescriptionItem(p1.getMedRate))
    print(p2.qtyDispensed * cv1.getRatePerPrescriptionItem(p2.getMedRate))
    
    pv1.addPrescribedItem(p1)
    pv1.addPrescribedItem(p2)
    
    print(cv1)
    cv1.prescribedItemListStr()

    
    print(pv1)
    pv1.prescribedItemListStr()
    
main()
