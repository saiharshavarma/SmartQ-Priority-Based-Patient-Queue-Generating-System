def medDepart(str = 'Good'):
    ans = ''
    if 'heart'.lower() in str.lower():
       ans = 'Cardiology' 
    elif 'pregnant'.lower() in str.lower() or str.lower() == 'pregnancy'.lower():
        ans = 'Obstetrics'
    elif 'skin'.lower() in str.lower():
        ans = 'Dermatology'
    elif 'child'.lower() in str.lower():
        ans = 'Pediatrics'
    elif 'reproduction'.lower() in str.lower() or 'period'.lower() in str.lower() or'periods'.lower() in str.lower():
        ans = 'Gynecology'
    elif 'bone'.lower() in str.lower() or 'fracture'.lower() in str.lower():
        ans = 'Orthopedics'
    elif 'kidney'.lower() in str.lower() or 'urine'.lower() in str.lower():
        ans = 'Nephrology'
    elif 'eye'.lower() in str.lower():
        ans = 'Ophthalmology'
    elif 'brain'.lower() in str.lower():
        ans = 'Neurology'
    elif 'cancer'.lower() in str.lower():
        ans = 'Oncology'
    else:
        ans = 'General Surgery'
    return ans