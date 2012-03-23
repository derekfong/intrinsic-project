from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from Main.models import Course, ClassList, UploadUserList
from Instructor.models import Activity, Announcement
from Student.models import Submission
from Gradebook.models import Grade, GradeComment
from models import UserProfile
import xlrd, xlwt

class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
	
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
		(None, {'fields': ['faculty', 'department', 'class_number', 'class_name', 'semester', 'year', 'section']})
	]
	list_filter= ['faculty', 'department', 'semester', 'year']
	search_fields = ['department']
	list_display=('class_number', 'department', 'faculty', 'semester', 'year', 'section')
	
class ClassListAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['uid', 'cid', 'is_instructor', 'is_ta']})
	]
	list_filter=['uid', 'cid']
	search_fields = ['uid']
	list_display=('uid','cid',)

class ActivityAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['cid', 'activity_name', 'out_of', 'worth', 'due_date', 'status']})
	]
	list_filter=['cid']
	search_fields=['cid']
	list_display=('cid','activity_name', 'due_date', 'status')
	
class AnnouncementAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['uid', 'cid', 'title', 'content', 'date_posted']})
	]
	list_filter=['cid', 'uid']
	search_filter=['cid', 'uid']
	list_display=('uid','cid', 'title', 'date_posted')

class SubmissionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['aid', 'uid', 'submit_date', 'submit_number', 'file_path']})
	]
	list_filter=['aid', 'uid']
	search_fields=['aid', 'uid']
	list_display=('aid', 'uid', 'submit_number')

class GradeInline(admin.StackedInline):
	model = GradeComment
	fk_name = 'gid'

class GradeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Enter Grade', {'fields': ['aid', 'uid', 'mark']})
	]
	list_filter=['aid', 'uid']
	search_fields=['aid', 'uid']
	inlines = [GradeInline, ]
	list_display=('aid', 'uid', 'mark')
	
class UploadUserListAdmin(admin.ModelAdmin):
    fieldsets = [
		(None, {'fields': ['file_name', 'upload_date', 'file_path']})
	]
    list_display = ('file_name', 'upload_date', 'is_imported')
    actions = ['import_users']
    
    def import_users(self, request, queryset):
		for obj in queryset:
			user_list = UploadUserList.objects.get(id=obj.id)
			xls_file = user_list.file_path
			excel_book = xlrd.open_workbook(file_contents=xls_file.read())
			sheet = excel_book.sheet_by_index(0)
			num_of_rows = range(1,sheet.nrows)
    
			for row in num_of_rows:
				username = sheet.cell_value(row,0)
				password = sheet.cell_value(row,1)
				first_name = sheet.cell_value(row,2)
				last_name = sheet.cell_value(row,3)
				sfu_id = int(sheet.cell_value(row,4))
				email = username + "@sfu.ca"
				new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
				new_user.set_password(password)
				new_user.save()
				user_profile = UserProfile(user=new_user, sfu_id=sfu_id)
				user_profile.save()
			user_list.is_imported = True
			user_list.save()
		self.message_user(request, "%s user list(s) imported successfully" % len(queryset))
    import_users.short_description = "Import users from Excel file"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ClassList, ClassListAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(UploadUserList, UploadUserListAdmin)
