from http.client import HTTPResponse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from hr.models import Department
from hr.models import Designation
from hr.models import Employee
from hr.models import Leave


# Create your views here.
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            if Employee.objects.filter(user=user).exists():
                return redirect("employee_dashboard")
            return redirect("dashboard")
        return render(request,"login.html",{"error": "Invalid username or password"})
    return render(request, "login.html")




@login_required
@never_cache
def dashboard(request):
    return render(request,"dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
@never_cache
def employee_list(request):
    employees=(Employee.objects.select_related("department","designation")
               .filter(status=True))
    return render(request,"employee_list.html",{"employees":employees})
@login_required
@never_cache
def employee_create(request):

    departments = Department.objects.all()
    designations = Designation.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        department_id = request.POST.get("department")
        designation_id = request.POST.get("designation")

        joining_date = request.POST.get("joining_date")
        employment_type = request.POST.get("employment_type")
        salary = request.POST.get("salary")
        address = request.POST.get("address")

        status = request.POST.get("status") == "on"
        if Employee.objects.filter(email=email).exists():
            messages.error(
                request,
                "Employee with this email already exists."
            )
            return redirect("employee_create")

        # Create Django User
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=name
        )

        # Disable password until employee creates one
        user.set_unusable_password()
        user.save()

        # Create Employee
        employee = Employee.objects.create(
            user=user,
            employee_id=employee_id,
            name=name,
            email=email,
            phone=phone,
            department_id=department_id,
            designation_id=designation_id,
            joining_date=joining_date,
            employment_type=employment_type,
            salary=salary,
            address=address,
            status=status
        )

        # Generate password setup token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Password setup URL
        setup_link = request.build_absolute_uri(
            reverse(
                "set_password",
                kwargs={
                    "uidb64": uid,
                    "token": token
                }
            )
        )

        # Send email
        send_mail(
            subject="CrewConnect - Set Your Password",
            message=f"""
Hello {name},

Your CrewConnect employee account has been created.

Please click the link below to create your password:

{setup_link}

After setting your password, you can log in to CrewConnect.

Regards,
CrewConnect HR
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return redirect("employee_list")

    return render(
        request,
        "employee_add_update.html",
        {
            "departments": departments,
            "designations": designations,
            "employment_types": Employee.EMPLOYMENT_TYPES,
            "is_update": False,
        }
    )

@login_required
@never_cache
def employee_update(request, id):


    employee = get_object_or_404(Employee,id=id )


    departments = Department.objects.all()
    designations = Designation.objects.all()


    if request.method == "POST":


        employee.employee_id = request.POST.get("employee_id")
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")


        employee.department_id = request.POST.get("department")
        employee.designation_id = request.POST.get("designation")


        employee.joining_date = request.POST.get("joining_date")
        employee.employment_type = request.POST.get("employment_type")
        employee.salary = request.POST.get("salary")
        employee.address = request.POST.get("address")


        employee.status = request.POST.get("status") == "on"


        employee.save()


        return redirect(
            "employee_list"
        )


    return render(
        request,
        "employee_add_update.html",
        {
            "employee": employee,
            "departments": departments,
            "designations": designations,
            "employment_types": Employee.EMPLOYMENT_TYPES,
            "is_update": True,
        }
    )
@login_required
@never_cache
def employee_delete(request, id):
    employee = get_object_or_404(
        Employee,
        id=id
    )
    employee.status = not employee.status
    employee.save()
    return redirect("employee_list")



@login_required
def leave_approve(request):


   # Check whether logged-in user is an employee
   if Employee.objects.filter(user=request.user).exists():
       return redirect("employee_dashboard")


   leaves = Leave.objects.select_related(
       "employee",
       "employee__department",
       "employee__designation"
   ).order_by("-applied_date")


   return render(
       request,
       "leave_approval.html",
       {
           "leaves": leaves,
           "is_employee": False,
       }
   )


def leave_action(request, id):

    leave = get_object_or_404(Leave, id=id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            leave.status = 'Approved'

        elif action == 'reject':
            leave.status = 'Rejected'

        leave.save()

    return redirect('leave_calendar')
@login_required
def leave_calendar(request):

    # HR can see all leaves
    leaves = Leave.objects.all().order_by("start_date")

    return render(
        request,
        "leave_calendar.html",
        {
            "leaves": leaves
        }
    )

@login_required
def department_list(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    departments = Department.objects.all().order_by("name")

    return render(
        request,
        "department_list.html",
        {
            "departments": departments
        }
    )

@login_required
def department_create(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            Department.objects.create(
                name=name
            )

            return redirect("department_list")

    return render(
        request,
        "department_form.html"
    )

@login_required
def department_update(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    department = Department.objects.get(id=id)

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            department.name = name
            department.save()

            return redirect("department_list")

    return render(
        request,
        "department_form.html",
        {
            "department": department
        }
    )

@login_required
def department_delete(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    department = Department.objects.get(id=id)

    if request.method == "POST":

        try:

            department.delete()

        except ProtectedError:

            return render(
                request,
                "department_list.html",
                {
                    "departments": Department.objects.all(),
                    "error": "This department cannot be deleted because employees are assigned to it."
                }
            )

        return redirect("department_list")

    return render(
        request,
        "department_confirm_delete.html",
        {
            "department": department
        }
    )

@login_required
def designation_list(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    designations = Designation.objects.all().order_by("name")

    return render(
        request,
        "designation_list.html",
        {
            "designations": designations
        }
    )

@login_required
def designation_create(request):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            Designation.objects.create(
                name=name
            )

            return redirect("designation_list")

    return render(
        request,
        "designation_form.html"
    )

@login_required
def designation_update(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    designation = Designation.objects.get(id=id)

    if request.method == "POST":

        name = request.POST.get("name")

        if name:

            designation.name = name
            designation.save()

            return redirect("designation_list")

    return render(
        request,
        "designation_form.html",
        {
            "designation": designation
        }
    )

@login_required
def designation_delete(request, id):

    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")

    designation = Designation.objects.get(id=id)

    if request.method == "POST":

        try:

            designation.delete()

        except ProtectedError:

            return render(
                request,
                "designation_list.html",
                {
                    "designations": Designation.objects.all(),
                    "error": "This designation cannot be deleted because employees are assigned to it."
                }
            )

        return redirect("designation_list")

    return render(
        request,
        "designation_confirm_delete.html",
        {
            "designation": designation
        }
    )

@login_required
def settings_view(request):

    return render(
        request,
        "settings.html"
    )


@login_required
def update_profile(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email

        request.user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("settings")

    return render(
        request,
        "update_profile.html"
    )


@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get(
            "current_password"
        )

        new_password = request.POST.get(
            "new_password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )


        if not request.user.check_password(
            current_password
        ):

            messages.error(
                request,
                "Current password is incorrect."
            )

            return redirect("change_password")


        if new_password != confirm_password:

            messages.error(
                request,
                "New passwords do not match."
            )

            return redirect("change_password")


        if len(new_password) < 8:

            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

            return redirect("change_password")


        request.user.set_password(
            new_password
        )

        request.user.save()


        update_session_auth_hash(
            request,
            request.user
        )


        messages.success(
            request,
            "Password changed successfully."
        )

        return redirect("settings")


    return render(
        request,
        "change_password.html"
    )


@login_required
def logout_view(request):

    if request.method == "POST":

        logout(request)

        return redirect("/")

    return render(
        request,
        "logout.html"
    )