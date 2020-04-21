from django.contrib import admin
from .models import List,links,instructors,assignments,announcements,studList,studRecords,questr,ques,attempt,resAccess
# Register your models here.
admin.site.register(List)
admin.site.register(links)
admin.site.register(instructors)
admin.site.register(assignments)
admin.site.register(announcements)
admin.site.register(studList)
admin.site.register(studRecords)
admin.site.register(questr)
admin.site.register(ques)
admin.site.register(attempt)
admin.site.register(resAccess)
