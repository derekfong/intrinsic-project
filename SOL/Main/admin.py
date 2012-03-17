from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from Main.models import Course, ClassList
from models import UserProfile

class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    #max_num = 1
	#raw_id_fields = ("sfu_id",)
	
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        ('User Information', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
		('Additional Information', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name')}
        ),
    )
    inlines = [
		ProfileInline,
	]

class CourseAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['faculty', 'department', 'class_number', 'class_name', 'semester', 'year']})
	]
	list_display=('class_number', 'department', 'faculty', 'semester', 'year',)
	
class ClassListAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['uid', 'cid', 'is_instructor', 'is_ta']})
	]
	list_display=('uid','cid',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ClassList, ClassListAdmin)