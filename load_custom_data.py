import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medcompare_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from medicines.models import Manufacturer, Medicine, Formula

try:
    with open('datadump.json', 'r') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading dump: {e}")
    exit(1)

# Groups
manuf_group, _ = Group.objects.get_or_create(name='Manufacturers')

# 1. Load users
print("Loading users...")
for item in data:
    if item['model'] == 'auth.user':
        fields = item['fields']
        # username might be natural key if dumped with --natural-primary
        # but --natural-primary outputs dict/list pk sometimes.
        pk = item['pk']
        
        # In natural primary for auth.User, pk is the username itself. 
        username = pk[0] if isinstance(pk, list) else (fields.get('username') or pk)
        if isinstance(username, list): 
            username = username[0]
            
        print(username)

        u, created = User.objects.get_or_create(username=username, defaults={
            'email': fields['email'],
            'first_name': fields['first_name'],
            'last_name': fields['last_name'],
            'is_staff': fields['is_staff'],
            'is_active': fields['is_active'],
            'is_superuser': fields['is_superuser'],
            'password': fields['password'],
        })
        if not created:
            u.password = fields['password']
            u.save()

# 2. Extract manufacturer mapping (User ID -> Manufacturer)
# Wait, natural-foreign uses username for User FK
print("Loading manufacturers...")
for item in data:
    if item['model'] == 'medicines.manufacturer':
        fields = item['fields']
        user_key = fields['user'][0] if isinstance(fields['user'], list) else fields['user']
        user = User.objects.filter(username=user_key).first()
        if user:
            u.groups.add(manuf_group)
            m, _ = Manufacturer.objects.get_or_create(
                user=user, 
                defaults={
                    'name': fields['name'],
                    'address': fields['address']
                }
            )

# 3. Load medicines
print("Loading medicines...")
for item in data:
    if item['model'] == 'medicines.medicine':
        fields = item['fields']
        manuf_name = fields['manufacturer'][0] if isinstance(fields['manufacturer'], list) else fields['manufacturer']
        if isinstance(manuf_name, int):
            # fallback if it's integer ID
            manuf = Manufacturer.objects.filter(id=manuf_name).first()
        else:
            manuf = Manufacturer.objects.filter(user__username=manuf_name).first() or Manufacturer.objects.filter(name=manuf_name).first()
            
        if manuf:
            med, created = Medicine.objects.get_or_create(
                name=fields['name'],
                manufacturer=manuf,
                defaults={
                    'price': fields['price'],
                    'formula': fields['formula'],
                    'dosage': fields['dosage'],
                    'rating': fields['rating'],
                    'is_paid': fields['is_paid'],
                    'created_at': fields['created_at'],
                }
            )

print("Data loaded successfully!")
