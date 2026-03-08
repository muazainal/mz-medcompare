import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medcompare_project.settings')
django.setup()

from medicines.models import Manufacturer, Medicine
from django.db import transaction

data = [
  {"name":"Test Medicine","manufacturer":"Admin Pharma","formula":"TestFormula","dosage":"100mg","price":10.50,"rating":0.0},
  {"name":"Salbutamol","manufacturer":"Cipla","formula":"Salbutamol Sulfate","dosage":"Inhaler 100mcg","price":9.00,"rating":4.0},
  {"name":"Airomir","manufacturer":"3M Pharmaceuticals","formula":"Salbutamol Sulfate","dosage":"Inhaler 100mcg per puff","price":11.00,"rating":4.0},
  {"name":"Salamol","manufacturer":"Teva Pharmaceuticals","formula":"Salbutamol Sulfate","dosage":"Inhaler 100mcg per puff","price":10.00,"rating":4.0},

  {"name":"Losartan","manufacturer":"Viatris","formula":"Losartan Potassium","dosage":"Tablet 50mg, 100mg","price":17.00,"rating":4.0},
  {"name":"Losartan","manufacturer":"Sandoz","formula":"Losartan Potassium","dosage":"Tablet 50mg, 100mg","price":18.00,"rating":4.0},
  {"name":"Losartan","manufacturer":"Teva Pharmaceuticals","formula":"Losartan Potassium","dosage":"Tablet 25mg, 50mg, 100mg","price":18.00,"rating":4.0},

  {"name":"Azithromycin","manufacturer":"Viatris","formula":"Azithromycin","dosage":"Tablet 250mg, 500mg","price":19.00,"rating":4.0},
  {"name":"Azithromycin","manufacturer":"Sandoz","formula":"Azithromycin","dosage":"Tablet 250mg, 500mg","price":19.00,"rating":4.0},
  {"name":"Azithromycin","manufacturer":"Teva Pharmaceuticals","formula":"Azithromycin","dosage":"Tablet 250mg, 500mg","price":20.00,"rating":4.0},

  {"name":"Sildenafil","manufacturer":"Viatris","formula":"Sildenafil Citrate","dosage":"Tablet 50mg, 100mg","price":34.00,"rating":4.0},
  {"name":"Sildenafil","manufacturer":"Teva Pharmaceuticals","formula":"Sildenafil Citrate","dosage":"Tablet 25mg, 50mg, 100mg","price":35.00,"rating":4.0},
  {"name":"Cialis","manufacturer":"Eli Lilly","formula":"Tadalafil","dosage":"Tablet 10mg, 20mg","price":35.00,"rating":4.0},

  {"name":"Atorvastatin","manufacturer":"Viatris","formula":"Atorvastatin Calcium","dosage":"Tablet 20mg, 40mg","price":0.00,"rating":0.0},
  {"name":"Atorvastatin","manufacturer":"Sandoz","formula":"Atorvastatin Calcium","dosage":"Tablet 10mg, 20mg","price":19.00,"rating":4.0},
  {"name":"Atorvastatin","manufacturer":"Teva Pharmaceuticals","formula":"Atorvastatin Calcium","dosage":"Tablet 10mg, 20mg, 40mg","price":20.00,"rating":4.0},

  {"name":"Diclofenac","manufacturer":"Sandoz","formula":"Diclofenac Sodium","dosage":"Tablet 50mg","price":9.00,"rating":4.0},
  {"name":"Diclofenac","manufacturer":"Viatris","formula":"Diclofenac Sodium","dosage":"Tablet 50mg, 100mg","price":10.00,"rating":4.0},
  {"name":"Diclofenac","manufacturer":"Teva Pharmaceuticals","formula":"Diclofenac Sodium","dosage":"Tablet 50mg, 75mg","price":10.00,"rating":4.0},
  {"name":"Cataflam","manufacturer":"Novartis","formula":"Diclofenac Potassium","dosage":"Tablet 50mg","price":14.00,"rating":4.0},

  {"name":"Rosuvastatin","manufacturer":"Viatris","formula":"Rosuvastatin Calcium","dosage":"Tablet 10mg, 20mg","price":17.00,"rating":4.0},
  {"name":"Rosuvastatin","manufacturer":"Sandoz","formula":"Rosuvastatin Calcium","dosage":"Tablet 5mg, 10mg, 20mg","price":17.00,"rating":4.0},
  {"name":"Rosuvastatin","manufacturer":"Teva Pharmaceuticals","formula":"Rosuvastatin Calcium","dosage":"Tablet 5mg, 10mg, 20mg","price":18.00,"rating":4.0},

  {"name":"Amlodipine","manufacturer":"Viatris","formula":"Amlodipine Besylate","dosage":"Tablet 5mg, 10mg","price":10.00,"rating":4.0},
  {"name":"Amlodipine","manufacturer":"Sandoz","formula":"Amlodipine Besylate","dosage":"Tablet 5mg, 10mg","price":11.00,"rating":4.0},
  {"name":"Amlodipine","manufacturer":"Teva Pharmaceuticals","formula":"Amlodipine Besylate","dosage":"Tablet 2.5mg, 5mg, 10mg","price":10.00,"rating":4.0},
  {"name":"Istin","manufacturer":"Pfizer","formula":"Amlodipine Besylate","dosage":"Tablet 5mg, 10mg","price":14.00,"rating":4.0},

  {"name":"Paracetamol","manufacturer":"Sandoz","formula":"Paracetamol","dosage":"Tablet 500mg","price":3.00,"rating":4.0},
  {"name":"Paracetamol","manufacturer":"Teva Pharmaceuticals","formula":"Paracetamol","dosage":"Tablet 500mg","price":3.00,"rating":4.0},
  {"name":"Calpol","manufacturer":"Johnson & Johnson","formula":"Paracetamol","dosage":"Oral suspension 120mg/5ml, 250mg/5ml","price":5.00,"rating":4.0},
  {"name":"Tylenol","manufacturer":"Johnson & Johnson","formula":"Paracetamol","dosage":"Tablet 325mg, 500mg, 650mg","price":6.00,"rating":4.0},
  {"name":"Panadol","manufacturer":"GSK","formula":"Paracetamol","dosage":"Tablet 500mg / Syrup 120mg/5ml","price":5.00,"rating":5.0},

  {"name":"Voltaren","manufacturer":"Novartis","formula":"Diclofenac","dosage":"Tablet 50mg, 75mg, 100mg","price":15.00,"rating":4.0},
  {"name":"Viagra","manufacturer":"Pfizer","formula":"Sildenafil Citrate","dosage":"Tablet 25mg, 50mg, 100mg","price":50.00,"rating":5.0},
  {"name":"Lipitor","manufacturer":"Pfizer","formula":"Atorvastatin Calcium","dosage":"Tablet 10mg, 20mg, 40mg, 80mg","price":25.00,"rating":5.0},
  {"name":"Zithromax","manufacturer":"Pfizer","formula":"Azithromycin","dosage":"Tablet 250mg, 500mg","price":25.00,"rating":4.0},

  {"name":"Xolair","manufacturer":"Novartis","formula":"Omalizumab","dosage":"Injection 150mg, 300mg","price":1300.00,"rating":4.0},
  {"name":"Tasigna","manufacturer":"Novartis","formula":"Nilotinib","dosage":"Capsule 150mg, 200mg","price":1800.00,"rating":4.0},
  {"name":"Exjade","manufacturer":"Novartis","formula":"Deferasirox","dosage":"Tablet 125mg, 250mg, 500mg","price":1600.00,"rating":4.0},
  {"name":"Gleevec","manufacturer":"Novartis","formula":"Imatinib","dosage":"Tablet 100mg, 400mg","price":1800.00,"rating":5.0},
  {"name":"Diovan","manufacturer":"Novartis","formula":"Valsartan","dosage":"Tablet 80mg, 160mg, 320mg","price":25.00,"rating":4.0},

  {"name":"Cozaar","manufacturer":"Merck","formula":"Losartan","dosage":"Tablet 25mg, 50mg, 100mg","price":20.00,"rating":4.0},
  {"name":"Propecia","manufacturer":"Merck","formula":"Finasteride","dosage":"Tablet 1mg","price":30.00,"rating":4.0},
  {"name":"Gardasil","manufacturer":"Merck","formula":"HPV Vaccine","dosage":"Injection 0.5ml","price":150.00,"rating":5.0},
  {"name":"Januvia","manufacturer":"Merck","formula":"Sitagliptin","dosage":"Tablet 25mg, 50mg, 100mg","price":45.00,"rating":4.0},
  {"name":"Keytruda","manufacturer":"Merck","formula":"Pembrolizumab","dosage":"Injection 100mg/4ml","price":2200.00,"rating":5.0},

  {"name":"Allegra","manufacturer":"Sanofi","formula":"Fexofenadine","dosage":"Tablet 120mg, 180mg","price":20.00,"rating":4.0},
  {"name":"Plavix","manufacturer":"Sanofi","formula":"Clopidogrel","dosage":"Tablet 75mg","price":35.00,"rating":5.0},
  {"name":"Dupixent","manufacturer":"Sanofi","formula":"Dupilumab","dosage":"Injection 200mg, 300mg","price":1500.00,"rating":5.0},
  {"name":"Lantus","manufacturer":"Sanofi","formula":"Insulin Glargine","dosage":"Injection 100 units/ml","price":60.00,"rating":5.0},

  {"name":"Ventolin","manufacturer":"GSK","formula":"Salbutamol Sulfate","dosage":"Inhaler 100mcg","price":12.00,"rating":5.0},
  {"name":"Augmentin","manufacturer":"GSK","formula":"Amoxicillin + Clavulanate","dosage":"Tablet 375mg, 625mg","price":25.00,"rating":4.0},

  {"name":"Tagrisso","manufacturer":"AstraZeneca","formula":"Osimertinib","dosage":"Tablet 40mg, 80mg","price":2000.00,"rating":5.0},
  {"name":"Nexium","manufacturer":"AstraZeneca","formula":"Esomeprazole","dosage":"Capsule 20mg, 40mg","price":25.00,"rating":4.0},
  {"name":"Crestor","manufacturer":"AstraZeneca","formula":"Rosuvastatin Calcium","dosage":"Tablet 5mg, 10mg, 20mg, 40mg","price":20.00,"rating":5.0},

  {"name":"Tamiflu","manufacturer":"Roche","formula":"Oseltamivir","dosage":"Capsule 30mg, 45mg, 75mg","price":35.00,"rating":4.0},
  {"name":"Herceptin","manufacturer":"Roche","formula":"Trastuzumab","dosage":"Injection 150mg","price":1500.00,"rating":5.0},
  {"name":"Avastin","manufacturer":"Roche","formula":"Bevacizumab","dosage":"Injection 100mg/4ml","price":1200.00,"rating":5.0},

  {"name":"Risperdal","manufacturer":"Johnson & Johnson","formula":"Risperidone","dosage":"Tablet 0.5mg–4mg","price":40.00,"rating":4.0},
  {"name":"Xarelto","manufacturer":"Johnson & Johnson","formula":"Rivaroxaban","dosage":"Tablet 2.5mg, 10mg, 15mg, 20mg","price":60.00,"rating":4.0},
  {"name":"Imbruvica","manufacturer":"Johnson & Johnson","formula":"Ibrutinib","dosage":"Tablet 140mg","price":2500.00,"rating":4.0},
  {"name":"Stelara","manufacturer":"Johnson & Johnson","formula":"Ustekinumab","dosage":"Injection 45mg, 90mg","price":1800.00,"rating":4.0},

  {"name":"Norvasc","manufacturer":"Pfizer","formula":"Amlodipine Besylate","dosage":"Tablet 2.5mg, 5mg, 10mg","price":15.00,"rating":5.0},
  {"name":"Lyrica","manufacturer":"Pfizer","formula":"Pregabalin","dosage":"Capsule 25mg–300mg","price":45.00,"rating":4.0}
]

added_count = 0
with transaction.atomic():
    for item in data:
        manuf, _ = Manufacturer.objects.get_or_create(name=item['manufacturer'])
        
        med, created = Medicine.objects.get_or_create(
            name=item['name'],
            manufacturer=manuf,
            dosage=item['dosage'], # including dosage as part of uniqueness
            defaults={
                'formula': item['formula'],
                'price': item['price'],
                'rating': item['rating'],
                'is_paid': True
            }
        )
        if created:
            added_count += 1
        else:
            # Update fields if it already exists
            med.formula = item['formula']
            med.price = item['price']
            med.rating = item['rating']
            med.save()

print(f"Successfully added/updated {len(data)} medicines. ({added_count} new entries created.)")
