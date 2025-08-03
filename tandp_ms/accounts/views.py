from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')

def admin_login(request):
    return render(request, 'accounts/admin_login.html')
def student_login(request):
    return render(request, 'accounts/student_login.html')

def about(request):
    return render(request, 'accounts/about.html')

def contact(request):
    message_sent = False
    if request.method == 'POST':
        message_sent = True
    return render(request, 'accounts/contact.html', {'message_sent': message_sent})

def team_view(request):
    team_members = [
        {"sno": 1, "name": "Mr. C. Y. Balu", "designation": "Head – Corporate Relations", "mobile": "9900944775", "email": "balucy@srit.ac.in"},
        {"sno": 2, "name": "Dr. S Bhargava Reddy", "designation": "Training & Placement Officer", "mobile": "9515811111", "email": "tpo@srit.ac.in"},
        {"sno": 3, "name": "Dr. D Anil Kumar", "designation": "Alumni Relations Officer & Verbal Trainer", "mobile": "9791265918", "email": "alumni@srit.ac.in"},
        {"sno": 4, "name": "Dr. G. Hemanth Kumar Yadav", "designation": "Industry Relations Officer & Technical Trainer", "mobile": "9848169943", "email": "iiicell@srit.ac.in"},
        {"sno": 5, "name": "Mr. S Moin Ahmed", "designation": "Associate TPO & Coordinator – MEC", "mobile": "8328220829", "email": "atpo@srit.ac.in"},
        {"sno": 6, "name": "Mrs. T A Swathi", "designation": "Coordinator – Civil", "mobile": "8074669931", "email": "swathi.civ@srit.ac.in"},
        {"sno": 7, "name": "Mr. Y. Sathish Kumar", "designation": "Coordinator – EEE", "mobile": "8309918031", "email": "sathishkumar.eee@srit.ac.in"},
        {"sno": 8, "name": "Mr. D. Sreekanth Reddy", "designation": "Coordinator – ECE", "mobile": "9963917078", "email": "sreekanthreddy.ece@srit.ac.in"},
        {"sno": 9, "name": "Mr. K Kondanna", "designation": "Coordinator – CSD & Technical Trainer (Global Certifications)", "mobile": "9985502062", "email": "kondanna.cse@srit.ac.in"},
        {"sno": 10, "name": "Dr. D. Rajesh Babu", "designation": "Coordinator – CSE & CSM", "mobile": "9966982288", "email": "rajeshbabud.cse@srit.ac.in"},
        {"sno": 11, "name": "Mr. M Prabhakar", "designation": "Aptitude & Reasoning Trainer", "mobile": "9441553074", "email": "prabhakar.hs@srit.ac.in"},
        {"sno": 12, "name": "Mr. V Naveen Kumar", "designation": "Clerk – AIRP", "mobile": "9398023404", "email": "clerk.tpcell@srit.ac.in"},
    ]
    return render(request, 'accounts/team.html', {'team_members': team_members})
