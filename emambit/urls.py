
from django.contrib import admin
from django.urls import path
from home.views import * 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title='EMAMBIT Admin Panel'
admin.site.site_header="EMAMBIT"
admin.site.index_title='Welcome to  Admin Panel'




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view),
    path('login/',login_view),
    path('logout/',logout_view),
    

    path('add-company/',addClientCompany_view),
    path('manage-company/',manageClientCompany_view),
    path('update-company/<id>/',UpdateClientCompany_view),
    path('delete-company/<id>/',DeleteClientCompany_view),

    # path('view-pdf/<id>/',viewPdf.as_view()),
    path('download-pdf/<id>/',Download_report_view),
    path('download-order-report/<id>/',DownloadOrder_view),
    path('view-order-report/<id>/',ViewOrder_view),


    path('punch-in/',PunchIn_view),
    path('punch-out/',PunchOut_view),

    path('assign-engineer/',assignEngineer_view),
    path('assigned-works/',assignedWork_view),
    path('update-assigned-work/<id>/',UpdateAssignedWork_view),
    path('delete-assigned-work/<id>',DeleteAssignedWork_view),



    path('add-engineer/',addEngineer_view),
    path('manage-engineer/',manageEngineer_view),
    path('update-engineer/<id>/',UpdateEngineer_view),
    path('delete-engineer/<id>/',DeleteEngineer_view),


    path('add-manager/',addManager_view),
    path('our-managers/',ourManagers_view),
    path('delete-manager/<id>/',deleteManager_view),
    path('update-manager/<id>/',updateManager_view),



    path('manage-orders/',manageOrders_view),
    path('create-orders/',createOrders_view),
    path('update-orders/<id>/',UpdatePurchaseCompany_view),
    path('delete-orders/<id>/',DeletePurchaseCompany_view),
    path('delete-purchase-order/<id>/',DeletePurchaseOrder_view),
    path('project-lists/',projectList_view),




    path('add-report/<id>/',addReport_view),
    path('project-compeletion/<id>',ProjectCompletion_view),
    path('report-preview/<id>/',reportPreview_view),


    path('user-dashboard/',userDashboard_view),
    path('user-profile/',userProfile_view),



    path('reimbursement/',reimbursement_view),
    path('add-reimbursement/',addReimbursement_view),
    path('approve-reimbursement/<id>/',ApproveReimbursement),


    path('add-vendors/',AddPurchaseCompany_view),
    path('manage-vendors/',ShowPurchaseCompany_view),



    path('user-attendance/',UserAttendance_view),
    path('view-attendance/<id>/',ViewAttendance_view),
    path('download-attendance/<id>/',ViewAttendance_view),
    path('view-advance/',ViewAdvance_view),
    path('delete-advance/<id>/',DeleteAdvance_view),
    path('reimbursement-details/<id>/',ReimbursementDetails_view),
    path('delete-reimbursement/<id>/',DeleteReimbursement_view),
    path('clear-reimbursement/<id>/',ClearReimbursement_view),
    path('excel-attendance/<month_no>/',attendance_to_download),
    path('download-advance/<cur_month>/',downloadAdvance),
    path('page-not-found',ForZeroFor),
    
    path('equipment-page/',equipment_view),
    path('delete-equipment/',delete_equipment),
 ]






if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()