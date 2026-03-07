import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medcompare_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from medicines.models import Manufacturer, Medicine

with open('datadump.json', 'r') as f:
    data = json.load(f)

# 1. Load users
print("Loading users...")
for item in data:
    if item['model'] == 'auth.user':
        fields = item['fields']
        username = fields.get('username')
        if isinstance(username, list): 
            username = username[0]
            
        u, created = User.objects.get_or_create(username=username, defaults={
            'email': fields.get('email', ''),
            'first_name': fields.get('first_name', ''),
            'last_name': fields.get('last_name', ''),
            'is_staff': fields.get('is_staff', False),
            'is_active': fields.get('is_active', True),
            'is_superuser': fields.get('is_superuser', False),
            'password': fields.get('password', ''),
        })
        if not created:
            u.password = fields.get('password', u.password)
            u.save()

# 2. Manufacturers
print("Loading manufacturers...")
manuf_map = {}
for item in data:
    if item['model'] == 'medicines.manufacturer':
        pk = item['pk']
        fields = item['fields']
        user_val = fields.get('user')
        
        user_obj = None
        if user_val is not None:
            user_key = user_val[0] if isinstance(user_val, list) else user_val
            user_obj = User.objects.filter(username=user_key).first()
            
        m, _ = Manufacturer.objects.get_or_create(
            name=fields['name'],
            defaults={
                'user': user_obj,
                'address': fields.get('address', '')
            }
        )
        # Store mapping from dumped pk to real object
        manuf_map[pk] = m

# 3. Medicines
print("Loading medicines...")
for item in data:
    if item['model'] == 'medicines.medicine':
        fields = item['fields']
        manuf_id = fields.get('manufacturer')
        
        if isinstance(manuf_id, list):
            manuf_id = manuf_id[0]
            
        manuf_obj = manuf_map.get(manuf_id) or Manufacturer.objects.filter(id=manuf_id).first()
            
        if manuf_obj:
            med, created = Medicine.objects.get_or_create(
                name=fields['name'],
                manufacturer=manuf_obj,
                defaults={
                    'description': fields.get('description', ''),
                    'price': fields.get('price', 0),
                    'formula': fields.get('formula', ''),
                    'dosage': fields.get('dosage', ''),
                    'rating': fields.get('rating', 0),
                    'is_paid': fields.get('is_paid', True),
                    'created_at': fields.get('created_at'),
                }
            )

print(f"Data loaded safely! {Medicine.objects.count()} medicines now exist in PostgreSQL!")
