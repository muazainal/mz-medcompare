from django.shortcuts import render, get_object_or_404
from .models import Medicine


# HOME PAGE
# This function runs when someone visits "/"
# It fetches all Medicine objects from the database
def home(request):

    # Query the database table for Medicine
    # Equivalent SQL: SELECT * FROM medicines_medicine;
    medicines = Medicine.objects.all()

    # Render means:
    # 1. Take this template file
    # 2. Insert data into it
    # 3. Return HTML to the browser
    return render(request,
                  'medicines/medicines_list.html',
                  {
                      # This dictionary sends data into template
                      # Inside template we can use: {% for med in medicines %}
                      'medicines': medicines
                  })


# DETAIL PAGE
# This runs when someone visits: /medicine/1/
def medicine_detail(request, pk):

    # Get medicine by primary key (id)
    # If not found → show 404 error
    medicine = get_object_or_404(Medicine, pk=pk)

    return render(request,
                  'medicines/medicine_detail.html',
                  {
                      'medicine': medicine
                  })