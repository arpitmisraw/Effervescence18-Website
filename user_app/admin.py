from django.contrib import admin
from .models import RegularUser, Event, File
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Name"),
        smart_str(u"College"),
        smart_str(u"Gender"),
        smart_str(u"Phone"),
        smart_str(u"fb_id"),
        smart_str(u"referral"),
        smart_str(u"total_points"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.name),
            smart_str(obj.college),
            smart_str(obj.gender),
            smart_str(obj.phone),
            smart_str(obj.fb_id),
            smart_str(obj.referral),
            smart_str(obj.total_points),
        ])
    return response
export_csv.short_description = u"Export CSV"

def export_csv_user(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Username"),
        smart_str(u"Email"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.username),
            smart_str(obj.email),
        ])
    return response
export_csv.short_description = u"Export CSV"

class UserAdmin(admin.ModelAdmin):
    actions = [export_csv_user]

class MyModelAdmin(admin.ModelAdmin):
    actions = [export_csv]

admin.site.register(RegularUser,MyModelAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Event)
admin.site.register(File)

