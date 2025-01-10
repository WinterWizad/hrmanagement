from django.shortcuts import render,HttpResponse,get_object_or_404, redirect
from .models import Employee,Department
from datetime import datetime
from django.db.models import Q,Sum,Avg


def index(request):
    total_employees = Employee.objects.count()
    total_salaries = Employee.objects.aggregate(Sum('salary'))['salary__sum'] or 0
    average_salary = Employee.objects.aggregate(Avg('salary'))['salary__avg'] or 0
    departments = Department.objects.all()
    employees_by_department = {dept.name: Employee.objects.filter(dept=dept).count() for dept in departments}

    context = {
        'total_employees': total_employees,
        'total_salaries': total_salaries,
        'average_salary': average_salary,
        'employees_by_department': employees_by_department,
    }
    return render(request, "index.html", context)
def allemp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request,"allemp.html",context)
def removeemp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("Employee not found")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request,"removeemp.html",context)
def addemp(request):
    if request.method == 'POST':
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      salary = int(request.POST['salary'])
      bonus = int(request.POST['bonus'])
      phone = int(request.POST['phone'])
      dept = int(request.POST['dept'])
      role = int(request.POST['role'])
      emp = Employee(first_name=first_name,last_name=last_name,salary=salary,bonus=bonus,phone=phone,dept_id=dept,role_id=role,hire_date=datetime.now())
      emp.save()
      return HttpResponse('employee add sucessfully')
    elif request.method == 'GET':
       return render(request,'addemp.html')
    else:
        return render(request,"addemp.html")
def filteremp(request):
    if request.method == "POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)
        context = {
            'emps': emps
        }
        return render(request,'allemp.html',context)
    elif request.method == "GET":
        return render(request,'filteremp.html')
    else:
        return HttpResponse("Errror occur")

