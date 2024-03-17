def detectUser(user):
    if user.role_id == 1:
        redirect_url = 'account/EmpDashboard.html'
        return redirect_url
    elif user.role_id == 2:
        redirect_url = 'account/AdmDashboard.html'
        return redirect_url
    elif user.role_id == 3:
        redirect_url = 'account/SADashboard.html'
        return redirect_url
    elif user.role_id == None  :
        print("now user detected")