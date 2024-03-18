from home.managers import *
from django.contrib.auth.models import AbstractUser
from django.db import models

# Your existing code for other models, if any

# User's of Em Ambati
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    user_phone = models.CharField(max_length=50,unique=True)
    user_address=models.CharField(max_length=50)
    user_gender=models.CharField(max_length=50)
    user_status=models.CharField(max_length=100,null=True,blank=True,default='Engineer')
    total_cost=models.IntegerField(default=0,null=True,blank=True)
    visible_password=models.CharField(max_length=254,null=True,blank=True)
    attendance_status=models.CharField(max_length=250,null=True,blank=True,default="A")






    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
        return self.first_name + self.last_name

    # You can keep the manager here or import it from managers.py
    objects = CustomUserManager()



# Required Tables for Other Data

    
class AddTravelBy(models.Model):
    travel_by=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.travel_by

class AddUnit(models.Model):
    unit=models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.unit




 #Client Company Info
class ClientCompanyInfo(models.Model):
    company_name=models.CharField(max_length=200)
    company_phone=models.CharField(max_length=20)
    contact_person=models.CharField(max_length=250)
    company_email=models.CharField(max_length=254)
    company_gst=models.CharField(max_length=50)
    company_address=models.CharField(max_length=254)
    timestampt=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self) -> str:
        return self.company_name






# Assign Engineer 
class AssignEngineer(models.Model):
    company_name=models.ForeignKey(ClientCompanyInfo,on_delete=models.CASCADE)
    manager_name=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='manager_assignments',default=None)
    engineer_one=models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True,blank=True,related_name='engineer_one_assignments')
    engineer_two=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True, related_name='engineer_two_assignments')
    engineer_three=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True, related_name='engineer_three_assignments')
    visit_purpose=models.CharField(max_length=254)
    machine_type=models.CharField(max_length=254)
    leave_date=models.CharField(max_length=254)
    reach_date=models.CharField(max_length=254)
    travel_by=models.ForeignKey(AddTravelBy,on_delete=models.CASCADE)
    timestampt=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    ending_date=models.CharField(max_length=100,null=True,blank=True,default='Work on Progress')
    work_status=models.CharField(max_length=100,blank=True,null=True,default='Doing')
    project_link=models.CharField(max_length=1000,null=True,blank=True)
    download_link=models.CharField(max_length=254,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.company_name}--{self.visit_purpose}'

class AddReport(models.Model):
    project_name=models.ForeignKey(AssignEngineer,on_delete=models.CASCADE)
    engineer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    day_count=models.PositiveIntegerField()
    report_date=models.DateField()
    starting_time=models.TimeField()
    ending_time=models.CharField(max_length=15)
    total_hours=models.CharField(max_length=100)
    description=models.CharField(max_length=254 , null=True,blank=True)





class ProjectImage(models.Model):
    image = models.ImageField(upload_to='project_photos')
class ProjectCompletion(models.Model):
    project = models.OneToOneField(AssignEngineer, on_delete=models.CASCADE)
    project_description = models.CharField(max_length=500, null=True, blank=True)
    customer_remark = models.CharField(max_length=1000, null=True, blank=True)
    project_status = models.CharField(max_length=150, default='doing')
    project_images = models.ManyToManyField('ProjectImage')



# reimbursement

class AttachmentImages(models.Model):
    images=models.ImageField(upload_to='attachment_images')
class Reimbursement(models.Model):
    engineer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    company=models.ForeignKey(ClientCompanyInfo,on_delete=models.CASCADE)
    visit_purpose=models.CharField(max_length=250)
    manager_name=models.CharField(max_length=250)
    department=models.CharField(max_length=250)
    date=models.DateField()
    work_description=models.CharField(max_length=254)
    category=models.CharField(max_length=254)
    reimbursement_value=models.IntegerField(null=True,blank=True)
    advance=models.IntegerField(null=True,blank=True)
    cost=models.PositiveIntegerField(null=True,blank=True)
    attachment_images = models.ManyToManyField('AttachmentImages')
    reimbursement_status=models.CharField(max_length=254 ,null=True,blank=True,default='Pending')





#
class AddPurchaseComapny(models.Model):
    purchase_name=models.CharField(max_length=254)
    purchase_phone=models.CharField(max_length=254)
    purchase_person=models.CharField(max_length=254)
    purchase_email=models.CharField(max_length=254)
    purchase_gst=models.CharField(max_length=254)
    purchase_address=models.CharField(max_length=254)
    timestampt=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self) -> str:
        return self.purchase_name
    


# 
class PurchaseOrder(models.Model):
    purchase_company=models.ForeignKey(AddPurchaseComapny,on_delete=models.CASCADE)
    order_date=models.CharField(max_length=254,null=True,blank=True)
    order_no=models.CharField(max_length=254,null=True,blank=True)
    quotation_no=models.PositiveIntegerField()
    refrence=models.CharField(max_length=254,null=True,blank=True)
    project_description=models.CharField(max_length=24,null=True,blank=True)
    terms_condition=models.CharField(max_length=254,null=True,blank=True)
    order_description=models.CharField(max_length=254,null=True,blank=True)
    rate=models.FloatField()
    quantity=models.FloatField()
    unit=models.CharField(max_length=200,null=True,blank=True)
    subtotal=models.FloatField()
    discount=models.FloatField()
    gst_percent=models.FloatField()
    gst_amount=models.FloatField()
    final_amount=models.FloatField()

    

class UserAttendance(models.Model):
    engineer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    punchin_country=models.CharField(max_length=254,null=True,blank=True)
    punchin_state=models.CharField(max_length=254,null=True,blank=True)
    punchin_location=models.CharField(max_length=500,null=True,blank=True)
    punchin_postcode=models.CharField(max_length=100,null=True,blank=True)
    attendance_date=models.CharField(max_length=254,null=True,blank=True)
    punchin_time=models.CharField(max_length=200,null=True,blank=True)
    punchout_country=models.CharField(max_length=254,null=True,blank=True)
    punchout_state=models.CharField(max_length=254,null=True,blank=True)
    punchout_location=models.CharField(max_length=500,null=True,blank=True)
    punchout_postcode=models.CharField(max_length=100,null=True,blank=True)
    punchout_time=models.CharField(max_length=200,null=True,blank=True)
    total_hours=models.CharField(max_length=200,default='0.00')
    punch_status=models.CharField(max_length=20,default='Absent' , null=True,blank=True)

    class Meta:
        unique_together =('attendance_date','engineer')


class AdvanceMoney(models.Model):
    project_name=models.ForeignKey(AssignEngineer,on_delete=models.CASCADE)
    engineer_name=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    advance_amount=models.IntegerField(null=True,blank=True)
    