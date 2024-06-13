from datetime import datetime

def my_view(request):
    date_string = request.data.get('date_field')  # Assuming you're using DRF's request object
    # Parse the date string into a datetime.date object
    date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
    
    # Save the date_object to the database
    # ...
# for saving string sent via api for datefield 