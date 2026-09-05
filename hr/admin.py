from django.contrib import admin

from hr.models import Department, Employee, Designation

# Register your models here.
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)

