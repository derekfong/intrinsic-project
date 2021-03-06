from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from Main.models import Course, ClassList, UploadUserList, UploadClassList, Setting
from Instructor.models import Activity, Announcement, Slide
from Student.models import Submission
from Gradebook.models import Grade, GradeComment
from models import UserProfile
import xlrd, xlwt

## This page adds more features and overrides built in admin interface

class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
	

# below shows you all the additiona apps installed (Instructor, Main, Sites and Student app)
# this enables you to upload files or view list of users, classes that are available, etc...
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
		(None, {'fields': ['department', 'class_number', 'class_name', 'semester', 'year', 'section']})
	]
	list_filter= ['department', 'semester', 'year']
	search_fields = ['department']
	list_display=('class_number', 'department', 'semester', 'year', 'section')
	
class ClassListAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['uid', 'cid', 'is_instructor', 'is_ta']})
	]
	list_filter=['uid', 'cid']
	search_fields = ['uid']
	list_display=('uid','cid',)
	actions = ['enroll_students']

class ActivityAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['cid', 'activity_name', 'out_of', 'worth', 'due_date', 'status', 'description', 'description_doc']})
	]
	list_filter=['cid']
	search_fields=['cid']
	list_display=('cid','activity_name', 'due_date', 'status')
	
class AnnouncementAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['uid', 'cid', 'title', 'content', 'date_posted', 'send_email', 'was_updated', 'updated_by', 'updated_on']})
	]
	list_filter=['cid', 'uid']
	search_filter=['cid', 'uid']
	list_display=('uid','cid', 'title', 'date_posted')

class SubmissionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['aid', 'uid', 'submit_number', 'file_path']})
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

class UploadClassListAdmin(admin.ModelAdmin):
    fieldsets = [
		(None, {'fields': ['cid', 'upload_date', 'file_path']})
	]
    list_display = ('cid', 'upload_date', 'is_enrolled')
    actions = ['enroll_students']
    
    def enroll_students(self, request, queryset):
		for obj in queryset:
			class_list = UploadClassList.objects.get(id=obj.id)
			xls_file = class_list.file_path
			excel_book = xlrd.open_workbook(file_contents=xls_file.read())
			sheet = excel_book.sheet_by_index(0)
			num_of_rows = range(1,sheet.nrows)
			
			for row in num_of_rows:
				sfu_id = int(sheet.cell_value(row,3))
				user = UserProfile.objects.get(sfu_id=sfu_id)
				new_class_list = ClassList(uid=user, cid=class_list.cid)
				new_class_list.save()
			class_list.is_enrolled = True
			class_list.save()
		self.message_user(request, "%s class list(s) enrolled successfully" % len(queryset))
    enroll_students.short_description = "Enroll students into class from Excel file"

class SlideAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['cid', 'title', 'uploaded_on', 'file_path']})
	]
	list_filter=['cid']
	search_fields=['cid']
	list_display = ('cid', 'title')
	
class SettingAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['uid', 'email_announcement', 'email_activity']})
	]
	list_display = ('uid', 'email_announcement', 'email_activity')
	
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ClassList, ClassListAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(UploadUserList, UploadUserListAdmin)
admin.site.register(UploadClassList, UploadClassListAdmin)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Setting, SettingAdmin)
