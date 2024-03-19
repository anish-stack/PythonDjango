from django.contrib import admin

from django.contrib import admin
from home.models import *

# required tables

admin.site.register((AddTravelBy,AddUnit))


admin.site.register(CustomUser)






#Client company info
class AdminClientCompanyInfo(admin.ModelAdmin):
    list_display=('id','company_name','company_phone','contact_person','company_email','company_gst','company_address')
admin.site.register(ClientCompanyInfo,AdminClientCompanyInfo)

class AdminAddReport(admin.ModelAdmin):
    list_display=('id','project_name','engineer','report_date','day_count','starting_time','ending_time','total_hours','description')
admin.site.register(AddReport,AdminAddReport)




# Assign Engineer
class AdminAssignEngineer(admin.ModelAdmin):
    list_display=('id','company_name','manager_name','engineer_one','engineer_two','engineer_three','visit_purpose','machine_type','leave_date','reach_date','travel_by','equipment','work_status','project_link','download_link','recived_equipment','recived_date')
admin.site.register(AssignEngineer,AdminAssignEngineer)



class AdminProjectCompeletion(admin.ModelAdmin):
    list_display=('id','project','project_description','customer_remark','project_status')
admin.site.register(ProjectCompletion,AdminProjectCompeletion)
admin.site.register(ProjectImage)


# Create Project
# class AdminCreateProject(admin.ModelAdmin):
#     list_display=('id','project_title','client_name','machine_type','project_rate','project_email','project_email','project_phone','project_description','project_address','project_status')
# admin.site.register(CreateProject,AdminCreateProject)



#  Purchase Company
class AdminPurchaseCompany(admin.ModelAdmin):
    list_display=('id','purchase_name','purchase_person','purchase_phone','purchase_email','purchase_gst','purchase_address')
admin.site.register(AddPurchaseComapny,AdminPurchaseCompany)

class AdminVisiblePassword(admin.ModelAdmin):
    list_display=('id','user','password')





class AdminImbursement(admin.ModelAdmin):
    list_display=('id','engineer','company','visit_purpose','manager_name','department','date','work_description','category','reimbursement_value','advance','cost','reimbursement_status')
admin.site.register(Reimbursement,AdminImbursement)
admin.site.register(AttachmentImages)

class AdminPurchaseOrder(admin.ModelAdmin):
    list_display=('id','purchase_company','order_date','order_no','quotation_no','refrence','project_description','terms_condition','order_description','rate','quantity','unit','subtotal','discount','gst_percent','gst_amount','final_amount')
admin.site.register(PurchaseOrder,AdminPurchaseOrder)


class AdminUserAttendance(admin.ModelAdmin):
    list_display=('id','engineer','punchin_country','punchin_state','punchin_location','punchin_postcode','attendance_date','punchin_time','punchout_country','punchout_state','punchout_location','punchout_postcode','punchout_time','total_hours','punch_status')
admin.site.register(UserAttendance,AdminUserAttendance)

class AdminAdvanceMoney(admin.ModelAdmin):
    list_display=('id','project_name','engineer_name','advance_amount')
admin.site.register(AdvanceMoney,AdminAdvanceMoney)
