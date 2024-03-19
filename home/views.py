from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login, logout,authenticate
from home.models import *
from django.contrib import messages
from datetime import *
from django.core.mail import send_mail,EmailMultiAlternatives
from django.db.models import Sum , Count
import time,datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Count
import pandas as pd
import os




# home_function
# @login_required(login_url='/login')
# def equipment_view(request):
#     equipment_object=AssignEngineer.objects.all()

#     equipment_data=[]
#     for i in equipment_object:
#         if i.equipment is not None and i.equipment !='':
#             equipment_data.append(i)
        

#     return render(request,'equipment-page.html',{'equipment_data':equipment_data})

@login_required(login_url='/login')
def equipment_view(request):
    equipment_object=AssignEngineer.objects.all()

        
    equipment_data=[]
    for i in equipment_object:
        if i.equipment is not None and i.equipment !='':
            equipment_data.append(i)

    recived_equipment=[]
    for j in equipment_object:
        if j.recived_equipment is not None and j.equipment !='':
            equipment_data.append(j)

    return render(request,'equipment-page.html',{'equipment_data':equipment_data,'recived_equipment':recived_equipment})

# home_function
@login_required(login_url='/login')
def delete_equipment(request):
   
    if request.method=="POST":
        id_to_get=request.POST.get('recive_id')
        recive=request.POST.get('recive')
        recive_date=datetime.datetime.now().strftime('%d-%m-%Y')
        data_to_save=AssignEngineer.objects.get(id=id_to_get)
        data_to_save.recived_equipment=recive
        data_to_save.recived_date=recive_date
        data_to_save.save()
        messages.error(request,'Recived Succesfully')
        return redirect('/equipment-page')
    else:
        messages.error(request,'Something Went Wrong')
        return redirect('/equipment-page')

# home_function
@login_required(login_url='/login')
def home_view(request):
    all_company=ClientCompanyInfo.objects.all().order_by('-id')
    all_company_length=len(all_company)
    recent_customers=ClientCompanyInfo.objects.all().order_by('-id')[0:2]
    total_project=AssignEngineer.objects.all().order_by('-id')
    total_project_length=len(total_project)
    recent_projects=total_project[0:4]
    purchase_orders=PurchaseOrder.objects.all()
    total_staff=CustomUser.objects.all().exclude(is_staff=True)
    total_staff=len(total_staff)

    total_reimbursement = CustomUser.objects.exclude(is_staff=True).aggregate(total_cost_sum=Sum('total_cost'))
    total_cost=total_reimbursement['total_cost_sum']

    return render(request,'index.html',{'total_staff':total_staff,'all_company':recent_customers,'total_project':recent_projects,'purchase_orders':purchase_orders,'total_cost':total_cost,"all_company_length":all_company_length,'total_project_length':total_project_length})

def ForZeroFor(request):
    return render(request,'404.html')
def ForZeroFor(request,exception):
    return render(request,'404.html',status=404)

def login_view(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            if user.is_authenticated and user.is_superuser:
                print('super user he')
                login(request,user)
                messages.success(request,'Welcome to Emambit')
                return redirect('/')
            else:
                print('else men aa gaya')
                login(request,user)
                return redirect('/user-dashboard')
        else:
            messages.error(request,'Wrong Crediential')

            return redirect('/login')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request,"Log out Successfully..")
    return redirect('/login')

# CLient  Company Start
@login_required(login_url='/login')
def addClientCompany_view(request):
    if request.method == "POST" :
        company_name=request.POST.get('company_name')
        company_phone=request.POST.get('company_phone')
        contact_person=request.POST.get('contact_person')
        company_email=request.POST.get('company_email')
        company_gst=request.POST.get('company_gst')
        company_address=request.POST.get('company_address')
        if ClientCompanyInfo.objects.filter(company_name=company_name).exists():
            messages.error(request,'This Company is Alredy Existing In Database e')
            return redirect('/add-company')
        try:

            company_data=ClientCompanyInfo(company_name=company_name,company_phone=company_phone,contact_person=contact_person,company_email=company_email,company_gst=company_gst,company_address=company_address)
            company_data.save()
            print('Company Created successfully of ',company_name)
            messages.success(request,'Company Created Successfully')
            return redirect('/manage-company')
        except Exception as e:
            print('Company Created successfully ')
            messages.error(request,'Something Went Wrong | Please Try Again')
            return redirect('/add-company')
    return render(request,'add-company.html')


# manage company
@login_required(login_url='/login')
def manageClientCompany_view(request):
    companydata=ClientCompanyInfo.objects.all()

    p = Paginator(companydata, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'our-company.html',{"data":page_obj})

# update comoany
@login_required(login_url='/login')
def UpdateClientCompany_view(request,id):
    data_to_update=ClientCompanyInfo.objects.get(id=id)
    if request.method=="POST":
        company_name=request.POST.get('company_name')
        company_phone=request.POST.get('company_phone')
        contact_person=request.POST.get('contact_person')
        company_email=request.POST.get('company_email')
        company_gst=request.POST.get('company_gst')
        company_address=request.POST.get('company_address')
        data_to_update.company_name=company_name
        data_to_update.company_phone=company_phone
        data_to_update.contact_person=contact_person
        data_to_update.company_email=company_email
        data_to_update.company_gst=company_gst
        data_to_update.company_address=company_address
        try:

            data_to_update.save()
            messages.success(request,f'{company_name} Updated Successfully !')
            return redirect('/manage-company')
        except:
            messages.error(request,'Something Went Wrong')
            return redirect('/manage-company')
    return render(request,'update-company.html',{"data_to_update":data_to_update})
# delete
@login_required(login_url='/login')
def DeleteClientCompany_view(request,id):
    try:
        client_to_delete=ClientCompanyInfo.objects.get(id=id)
        client_name=client_to_delete.company_name
        client_to_delete.delete()
        messages.success(request,f'{client_name} Deleted SuccessFully !')
        return redirect('/manage-company')
    except:
        messages.error(request,'Something Went Wrong Tray Again')
        return redirect('/manage-company')

# Client Company End



@login_required(login_url='/login')
def manageOrders_view(request):
    purchase_data=PurchaseOrder.objects.all().order_by('-id')
    p = Paginator(purchase_data, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'orders.html',{'purchase_data':page_obj})



@login_required(login_url='/login')
def createOrders_view(request):
    last_id=0
    try:
        last_order=PurchaseOrder.objects.all().order_by('-id')
        last_id=last_order[0].id+1
    except:
        last_id=1
    company_data=AddPurchaseComapny.objects.all()
    current_company={}
    units=AddUnit.objects.all()
    year=datetime.datetime.now().year
    if request.GET.get('select_company'):
        current_company=AddPurchaseComapny.objects.get(purchase_name=request.GET.get('select_company'))
    if request.method=="POST":
        try:
            gate_company=AddPurchaseComapny.objects.get(purchase_name=request.POST.get('gated_company'))
            order_date=request.POST.get('order_date')
            order_no=request.POST.get('order_no')
            quotation_no=request.POST.get('quotation_no')
            refrence=request.POST.get('refrence')
            project_description=request.POST.get('project_description')
            terms_condition=request.POST.get('terms_condition')
            order_description=request.POST.get('order_description')
            rate=request.POST.get('rate')
            quantity=request.POST.get('quantity')
            unit=request.POST.get('unit')
            subtotal=request.POST.get('subtotal')
            discount=request.POST.get('discount')
            gst_percent=request.POST.get('gst_percent')
            gst_amount=request.POST.get('gst_amount')
            final_amount=request.POST.get('final_amount')
            order_to_save=PurchaseOrder(purchase_company=gate_company,order_date=order_date,order_no=order_no,quotation_no=quotation_no,refrence=refrence,project_description=project_description,terms_condition=terms_condition,order_description=order_description,rate=rate,quantity=quantity,unit=unit,subtotal=subtotal,discount=discount,gst_percent=gst_percent,gst_amount=gst_amount,final_amount=final_amount,)

            order_to_save.save()
            messages.success(request,'Order Created Successfully')
            return redirect('/manage-orders')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong Please Try Again')
            return redirect('/create-orders')
    return render(request,'create-order.html',{'company_data':company_data,'current_company':current_company,"last_id":last_id,'year':year,'units':units})
def DownloadOrder_view(request,id):
    try:
        data=PurchaseOrder.objects.get(id=id)
        return render(request,'view-purchase-order.html',{"data":data})
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/manage-orders')
def ViewOrder_view(request,id):
    try:

        data=PurchaseOrder.objects.get(id=id)
        return render(request,'view-purchase-order.html',{"data":data})
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/manage-orders')

def DeletePurchaseOrder_view(request,id):
    try:

        order_to_delete=PurchaseOrder.objects.get(id=id)
        order_to_delete.delete()
        messages.success(request,'Purchase Order Deleted Successfully')
        return redirect('/manage-orders')
    except:
        messages.error(request,'Opps ! Something Went Wrong')
        return redirect('/manage-orders')





# Engineer Views Start
@login_required(login_url='/login')
def addEngineer_view(request):
    if request.method=="POST":
        user_name=request.POST.get('engineer_name')
        user_phone=request.POST.get('engineer_phone')
        email=request.POST.get('engineer_email')
        user_gender=request.POST.get('engineer_gender')
        user_address=request.POST.get('engineer_address')
        password=request.POST.get('engineer_password')
        if CustomUser.objects.filter(first_name=user_name).exists():
            messages.error(request,'User Name Already Exist | Choose A Unique Name')
            return redirect('/add-engineer')
        if CustomUser.objects.filter(email=email ).exists():
            messages.error(request,'user already registerd with this email')
            return redirect('/add-engineer')
        if CustomUser.objects.filter(user_phone=user_phone ).exists():
            messages.error(request,'user already registerd with this Phone')
            return redirect('/add-engineer')
        try:
            user_data=CustomUser(email=email,first_name=user_name,user_phone=user_phone,user_gender=user_gender,user_address=user_address,visible_password=password)
            user_data.set_password(password)
            user_data.save()
            messages.success(request,'Engineer Added Successfully')
            return redirect('/manage-engineer')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong Please Try Again ')
            return redirect('/add-engineer')
    return render(request,'add-engineer.html')

# manage engineer
@login_required(login_url='/login')
def manageEngineer_view(request):
    engineers=CustomUser.objects.filter(user_status="Engineer").order_by('-id')
    p = Paginator(engineers, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'our-engineer.html',{'data':page_obj})
# update engineer

@login_required(login_url='/login')
def UpdateEngineer_view(request,id):
    engineer_to_update=CustomUser.objects.get(id=id)
    if request.method=="POST":
        user_name=request.POST.get('engineer_name')
        user_phone=request.POST.get('engineer_phone')
        email=request.POST.get('engineer_email')
        user_gender=request.POST.get('engineer_gender')
        user_address=request.POST.get('engineer_address')
        password=request.POST.get('engineer_password')

        try:
            engineer_to_update.first_name=user_name
            engineer_to_update.user_phone=user_phone
            engineer_to_update.email=email
            engineer_to_update.user_gender=user_gender
            engineer_to_update.user_address=user_address
            engineer_to_update.set_password(password)
            engineer_to_update.save()
            messages.success(request,'Engieer Updated Successfully')
            print('updated')
            return redirect('/manage-engineer')
        except Exception as e:
            print(e,'not updated')
            messages.error(request,'Something Went Wrong Please Try Again , Or Use Admin Panel')
            return redirect(f'/update-engineer/{id}')
    return render(request,'update-engineer.html',{"engineer_to_update":engineer_to_update})


@login_required(login_url='/login')
def DeleteEngineer_view(request,id):
    try:

        engineer_to_delete=CustomUser.objects.get(id=id)
        engineer_name=engineer_to_delete.first_name
        engineer_to_delete.delete()
        messages.success(request,f'{engineer_name}  Deleted Successfully')
        return redirect('/manage-engineer')
    except:
        messages.success(request,'Something Went Wrong')
        return redirect('/manage-engineer')

# engineer Views End







# manager view starts <==================>

@login_required(login_url='/login')
def addManager_view(request):
    if request.method=="POST":
        user_name=request.POST.get('manager_name')
        user_phone=request.POST.get('manager_phone')
        email=request.POST.get('manager_email')
        user_gender=request.POST.get('manager_gender')
        user_address=request.POST.get('manager_address')
        password=request.POST.get('manager_password')
        if CustomUser.objects.filter(first_name=user_name).exists():
            messages.error(request,'User Name Already Exist | Choose A Unique Name')
            return redirect('/add-manager')
        if CustomUser.objects.filter(email=email ).exists():
            messages.error(request,'user already registerd with this email')
            return redirect('/add-manager')
        if CustomUser.objects.filter(user_phone=user_phone ).exists():
            messages.error(request,'user already registerd with this Phone')
            return redirect('/add-manager')
        try:
            user_data=CustomUser(email=email,first_name=user_name,user_phone=user_phone,user_gender=user_gender,user_address=user_address,visible_password=password,user_status="Manager")
            user_data.set_password(password)
            user_data.save()
            messages.success(request,'Manager Added Successfully')
            return redirect('/our-managers')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong Please Try Again ')
            return redirect('/add-manager')

    return render(request,'add-manager.html')


@login_required(login_url='/login')
def ourManagers_view(request):
    engineers=CustomUser.objects.filter(user_status="Manager").order_by('-id')
    p = Paginator(engineers, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'our-manager.html',{'data':page_obj})

@login_required(login_url='/login')
def updateManager_view(request,id):
    manager_to_update=CustomUser.objects.get(id=id)
    if request.method=="POST":
        manager_name=request.POST.get('manager_name')
        manager_phone=request.POST.get('manager_phone')
        manager_email=request.POST.get('manager_email')
        manager_gender=request.POST.get('manager_gender')
        manager_address=request.POST.get('manager_address')
        manager_pasword=request.POST.get('manager_password')
        print(manager_name,manager_email,manager_phone)
        try:
            manager_to_update.email=manager_email
            manager_to_update.first_name=manager_name
            manager_to_update.user_phone=manager_phone
            manager_to_update.user_gender=manager_gender
            manager_to_update.user_address=manager_address
            manager_to_update.visible_password=manager_pasword
            manager_to_update.set_password(manager_pasword)
            manager_to_update.save()
            messages.success(request,'Manager Updated Successfully')
            return redirect('/our-managers')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong Please Try Again ')
            return redirect(f'/update-manager/{id}')


    return render(request,'update-manager.html',{'manager_to_update':manager_to_update})

@login_required(login_url='/login')
def deleteManager_view(request,id):
    manager_to_delete=CustomUser.objects.filter(id=id)[0]
    try:
        manager_to_delete.delete()
        messages.success(request,'Manager Deleted Successfully')
        return redirect('/our-managers')
    except:
        messages.error(request,'OOPS! Something Went Wrong')
        return redirect('/our-managers')







# manager view ends <==================>










# assign engineer view

@login_required(login_url='/login')
def assignEngineer_view(request):
    advance_engineers=CustomUser.objects.all().exclude(is_staff=True)
    if request.method=="POST":
        try:
            company=ClientCompanyInfo.objects.get(company_name=request.POST.get('company'))
            manager_name=CustomUser.objects.get(first_name=request.POST.get('manager_name'))
            engineer_one=CustomUser.objects.filter(first_name=request.POST.get('engineer_one'))
            engineer_two=CustomUser.objects.filter(first_name=request.POST.get('engineer_two'))
            engineer_three=CustomUser.objects.filter(first_name=request.POST.get('engineer_three'))


            visit_purpose=request.POST.get('visit_purpose')
            machine_type=request.POST.get('machine_type')
            leave_date=request.POST.get('leave_date')
            reach_date=request.POST.get('reach_date')
            equipment = request.POST.get('equipment')
            travel_by=AddTravelBy.objects.get(travel_by=request.POST.get('travel'))
            assign_data=AssignEngineer(
            company_name=company,
            manager_name=manager_name,
            visit_purpose=visit_purpose,
            machine_type=machine_type,
            leave_date=leave_date,
            reach_date=reach_date,
            travel_by=travel_by,
            equipment=equipment
            )
            if len(engineer_one) != 0:
                assign_data.engineer_one=engineer_one[0]
            if len(engineer_two) !=0:
                assign_data.engineer_two=engineer_two[0]
            if len(engineer_three) !=0:
                assign_data.engineer_three=engineer_three[0]


            assign_data.save()
            data_to_advance=AssignEngineer.objects.get(company_name=company,manager_name=manager_name,
            visit_purpose=visit_purpose,machine_type=machine_type, leave_date=leave_date,reach_date=reach_date,
            travel_by=travel_by)
            try:
                try:
                    advance_manager=request.POST.get('advance_manager')
                    manager_money=request.POST.get('manager_money')
                    ad_manager=CustomUser.objects.filter(first_name=advance_manager)
                    if len(ad_manager) !=0:
                        manager_to_save=AdvanceMoney(project_name=data_to_advance,engineer_name=ad_manager[0],advance_amount=manager_money)
                        manager_to_save.save()
                    else:
                        pass
                except:
                    pass
                try:
                    advance_engineerone=request.POST.get('advance_engineerone')
                    advance_money1=request.POST.get('advance_money1')
                    eng_one=CustomUser.objects.filter(first_name=advance_engineerone)
                    if len(eng_one) !=0:
                        engineer_one_to_save=AdvanceMoney(project_name=data_to_advance,engineer_name=eng_one[0],advance_amount=advance_money1)
                        engineer_one_to_save.save()
                    else:
                        pass

                except:
                    pass
                try:

                    advance_engineertwo=request.POST.get('advance_engineertwo')
                    advance_money2=request.POST.get('advance_money2')
                    eng_two=CustomUser.objects.filter(first_name=advance_engineertwo)
                    if len(eng_two) !=0:
                        engineer_two_to_save=AdvanceMoney(project_name=data_to_advance,engineer_name=eng_two[0],advance_amount=advance_money2)
                        engineer_two_to_save.save()
                    else:
                        pass
                except:
                    pass
                try:
                    advance_engineerthree=request.POST.get('advance_engineerthree')
                    advance_money3=request.POST.get('advance_money3')
                    eng_three=CustomUser.objects.filter(first_name=advance_engineerthree)
                    if len(eng_three) !=0:
                        eng_three_to_save=AdvanceMoney(project_name=data_to_advance,engineer_name=eng_three[0],advance_money=advance_money3)
                        eng_three_to_save.save()
                    else:
                        pass
                except:
                    pass
            except:
                pass
                # set your email inplace of emambit email here and remove this comment
            subject, from_email, to = "Engineer Assigned", "webrdevo@gmail.com", assign_data.company_name.company_email
            text_content = "hi"
            html_content = f"<h1>We Assigned Our Engineers To Your Project</h1><br><p> <strong> Manager Name : <b>{assign_data.manager_name.first_name}</b></a></strong><br><strong> Engineer Phone : {assign_data.manager_name.user_phone}/</a></strong> <br><strong> Engineer Email : {assign_data.manager_name.email}</strong></strong><br><strong> Expected Reach Date : {assign_data.reach_date}</a></strong</p>"
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request,'Project Assigned successfully')
            return redirect('/assigned-works/')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong | Please Try Again')
            return redirect('/assign-engineer')
    travel_by_data=AddTravelBy.objects.all()
    companydata=ClientCompanyInfo.objects.all()
    engineers=CustomUser.objects.filter(user_status="Engineer").order_by('-id')
    managers=CustomUser.objects.filter(user_status="Manager").order_by('-id')
    return render (request,'assign-engineer.html',{'engineers':engineers,'companydata':companydata,'travel_by_data':travel_by_data,'managers':managers,'advance_engineers':advance_engineers})


@login_required(login_url='/login')
def assignedWork_view(request):
    assigned_data=AssignEngineer.objects.all().order_by('-id')
    companydata=ClientCompanyInfo.objects.all().order_by('-id')
    p = Paginator(assigned_data, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'assigned-works.html',{'assigned_data':page_obj})


@login_required(login_url='/login')
def UpdateAssignedWork_view(request,id):
    data_to_update=AssignEngineer.objects.get(id=id)
    if request.method=="POST":
        try:
            company=ClientCompanyInfo.objects.get(company_name=request.POST.get('company'))
            manager_name=CustomUser.objects.get(first_name=request.POST.get('manager_name'))
            engineer_one=CustomUser.objects.filter(first_name=request.POST.get('engineer_one'))
            engineer_two=CustomUser.objects.filter(first_name=request.POST.get('engineer_two'))
            engineer_three=CustomUser.objects.filter(first_name=request.POST.get('engineer_three'))
            visit_purpose=request.POST.get('visit_purpose')
            machine_type=request.POST.get('machine_type')
            leave_date=request.POST.get('leave_date')
            reach_date=request.POST.get('reach_date')
            travel_by=AddTravelBy.objects.get(travel_by=request.POST.get('travel'))
            print(company,manager_name,engineer_one,engineer_two,engineer_three,visit_purpose,machine_type,leave_date,reach_date,travel_by)
            data_to_update.company_name=company
            data_to_update.manager_name=manager_name
            data_to_update.visit_purpose=visit_purpose
            data_to_update.machine_type=machine_type
            data_to_update.leave_date=leave_date
            data_to_update.reach_date=reach_date
            travel_by=travel_by
            if len(engineer_one) != 0:
                data_to_update.engineer_one=engineer_one[0]
            if len(engineer_two) !=0:
                data_to_update.engineer_two=engineer_two[0]
            if len(engineer_three) !=0:
                data_to_update.engineer_three=engineer_three[0]
            data_to_update.save()
            messages.success(request,'Information Updated Successfully')
            return redirect('/assigned-works')

        except Exception as e:
            print(e,'was error')
            messages.error(request,'Something Went Wrong !')
            return redirect(f'/update-assigned-work/{id}')
    travel_by_data=AddTravelBy.objects.all()
    companydata=ClientCompanyInfo.objects.all()
    engineers=CustomUser.objects.filter(user_status="Engineer")
    managers=CustomUser.objects.filter(user_status='Manager')
    return render(request,'update-assign-engineer.html',{'data_to_update':data_to_update,'companydata':companydata,'travel_by_data':travel_by_data,'managers':managers,'engineers':engineers })



@login_required(login_url='/login')
def DeleteAssignedWork_view(request,id):
    try:
        data_to_delete=AssignEngineer.objects.get(id=id)
        data_to_delete.delete()
        messages.success(request,'Assigned Work Deleted Successfully')
        return redirect('/assigned-works/')
    except:
        messages.error(request,'Something Went Wrogn Please Try Again')
        return redirect('Something Went Wrong')



# Project Lists
@login_required(login_url='/login')
def projectList_view(request):
    project_info=AssignEngineer.objects.all().order_by('-id')
    doing_data=AssignEngineer.objects.filter(work_status="Doing").order_by('-id')
    done_data=AssignEngineer.objects.filter(work_status="Done").order_by('-id')
    pending_data=AssignEngineer.objects.filter(work_status="Pending").order_by('-id')
    all_engineers=CustomUser.objects.all().order_by('-id')
    all_company=ClientCompanyInfo.objects.all().order_by('-id')
    if request.GET.get('get_engineer'):
        current_engineer=CustomUser.objects.filter(first_name__icontains=request.GET.get('get_engineer'))[0]
        print(current_engineer ,'is current engineer')
        project_info=AssignEngineer.objects.filter(engineer_name = current_engineer)
        doing_data=AssignEngineer.objects.filter(engineer_name = current_engineer)
        done_data=AssignEngineer.objects.filter(engineer_name = current_engineer)
        pending_data=AssignEngineer.objects.filter(engineer_name = current_engineer)
        print(project_info)
    if request.GET.get('get_company'):
        current_company=ClientCompanyInfo.objects.filter(company_name__icontains=request.GET.get('get_company'))[0]
        project_info=AssignEngineer.objects.filter(company_name = current_company)
        done_data=AssignEngineer.objects.filter(company_name = current_company)
        doing_data=AssignEngineer.objects.filter(company_name = current_company)
        pending_data=AssignEngineer.objects.filter(company_name = current_company)
    return render(request,'project-list.html',{"data":project_info,'all_engineers':all_engineers,'all_company':all_company,'doing_data':doing_data,'done_data':done_data,'pending_data':pending_data})






# Purchase Company
@login_required(login_url='/login')
def AddPurchaseCompany_view(request):
    if request.method=="POST":
        purchase_company_name=request.POST.get('purchase_company_name')
        purchase_company_phone=request.POST.get('purchase_company_phone')
        purchase_contact_person=request.POST.get('purchase_contact_person')
        purchase_company_email=request.POST.get('purchase_company_email')
        purchase_company_gst=request.POST.get('purchase_company_gst')
        purchase_company_address=request.POST.get('purchase_company_address')
        purchase_company_data=AddPurchaseComapny(purchase_name=purchase_company_name,purchase_phone=purchase_company_phone,purchase_person=purchase_contact_person,purchase_email=purchase_company_email,purchase_gst=purchase_company_gst,purchase_address=purchase_company_address)
        try:
            purchase_company_data.save()
            messages.success(request,'Company Added Successfully')
            return redirect('/manage-vendors')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong | Try Again')
            return redirect('add-vendors')
    return render(request,'add-purchase-company.html')
@login_required(login_url='/login')
def ShowPurchaseCompany_view(request):
    data=AddPurchaseComapny.objects.all()
    p = Paginator(data, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'purchase-company.html',{'data':page_obj})

@login_required(login_url='/login')
def UpdatePurchaseCompany_view(request,id):
    vendor_to_update=AddPurchaseComapny.objects.get(id=id)
    if request.method=="POST":
        purchase_company_name=request.POST.get('purchase_company_name')
        purchase_company_phone=request.POST.get('purchase_company_phone')
        purchase_contact_person=request.POST.get('purchase_contact_person')
        purchase_company_email=request.POST.get('purchase_company_email')
        purchase_company_gst=request.POST.get('purchase_company_gst')
        purchase_company_address=request.POST.get('purchase_company_address')
        vendor_to_update.purchase_name=purchase_company_name
        vendor_to_update.purchase_phone=purchase_company_phone
        vendor_to_update.purchase_person=purchase_contact_person
        vendor_to_update.purchase_email=purchase_company_email
        vendor_to_update.purchase_gst=purchase_company_gst
        vendor_to_update.purchase_address=purchase_company_address
        try:
            vendor_to_update.save()
            messages.success(request,'Company Updated Successfully')
            return redirect('/manage-vendors')
        except:
            messages.error(request,'Something Went Wrong')
            return redirect('/manage-vendors')
    return render(request,'update-purchase-company.html',{'vendor_data':vendor_to_update})

def DeletePurchaseCompany_view(request,id):
    vendor_to_delete=AddPurchaseComapny.objects.get(id=id)
    try:

        vendor_to_delete.delete()
        messages.success(request,'Deleted Successfully')
        return redirect('/manage-vendors')
    except:
        vendor_to_delete.delete()
        messages.success(request,'Deleted Successfully')
        return redirect('/manage-vendors')




@login_required(login_url='/login')
def userDashboard_view(request):
    projects_data = AssignEngineer.objects.filter(
    Q(manager_name=request.user) | Q(engineer_one=request.user) | Q(engineer_two=request.user) | Q(engineer_three=request.user)
)
    done_count = projects_data.filter(work_status="Done").count()
    doing_count = projects_data.filter(work_status="Doing").count()
    my_reimbursement_cost_sum = Reimbursement.objects.filter(engineer=request.user).aggregate(total_cost=Sum('cost'))

    reimbursement_cost = my_reimbursement_cost_sum.get('total_cost', 0)
    return render(request, 'user-dashboard.html', {
        'projects_data': projects_data,
        'done_count': done_count,
        'doing_count': doing_count,
        'reimbursement_cost':reimbursement_cost
    })




@login_required(login_url='/login')
def addReport_view(request,id):
    try:

        data_to_report=AssignEngineer.objects.get(id=id)
        if data_to_report.work_status != "Doing":
            messages.error('Final Report Already Submited')
            return redirect('user-dashboard')
        if request.method=="POST":
            project_name=data_to_report
            engineer=request.user
            day_count=request.POST.get('day_count')
            visit_date=request.POST.get('visit_date')
            starting_time=request.POST.get('starting_time')
            ending_time=request.POST.get('ending_time')
            total_hours=request.POST.get('total_hours')
            total_hours=str(total_hours)
            description=request.POST.get('description')
            report_to_save=AddReport(project_name=project_name,engineer=engineer,day_count=day_count,report_date=visit_date,starting_time=starting_time,ending_time=ending_time,total_hours=total_hours,description=description)
            try:
                report_to_save.save()
                messages.success(request,'Reported Added Successfulyy')
                return redirect('/user-dashboard')
            except Exception as e:
                print(e)
                messages.error(request,'Something Went Wrong')
                return redirect(f'/add-report/{id}')
        reported_data=AddReport.objects.filter(project_name=data_to_report)
        return render(request,'add-report.html',{'data_to_report':data_to_report,'reported_data':reported_data})
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/user-dashboard')


def ProjectCompletion_view(request, id):
    if request.method == "POST":
        try:
            project_name = AssignEngineer.objects.get(id=id)
            project_description = request.POST.get('project_description')
            project_images = request.FILES.getlist('project_image')
            project_to_save = ProjectCompletion(project=project_name, project_description=project_description)
            project_to_save.save()
            for image in project_images:
                project_to_save.project_images.create(image=image)
                project_to_save.save()
            data_to_report = AssignEngineer.objects.get(id=id)
            ended_date=datetime.datetime.now().date()
            todended_date=ended_date.strftime('%d %m %Y')
            todended_date=str(todended_date).replace(' ','-')
            print(todended_date,'was today ending date')
            data_to_report.ending_date=todended_date
            compelete_project = ProjectCompletion.objects.get(project=data_to_report)
            data_to_report.work_status = 'Pending'
            data_to_report.project_link = f'https://emambit.pythonanywhere.com/report-preview/{compelete_project.id}/'
            data_to_report.download_link = f'https://emambit.pythonanywhere.com/download-pdf/{compelete_project.id}/'
            data_to_report.save()
            subject, from_email, to = "Project Completed", "webrdevo@gmail.com", data_to_report.company_name.company_email
            text_content = "Hi, we have completed your project."
            html_content = f"<p><h1>Hi, we have completed your project.</h1><br>Please check and give your remarks <strong><a href='https://emambit.pythonanywhere.com/report-preview/{compelete_project.id}/'>Click Here To Check Your Report</a></strong> message.</p>"
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request,'Final Report Submited Successfully')
            return redirect('/user-dashboard')
        except Exception as e:
            messages.error(request,'Something Went Wrong')
            return redirect(f'/add-report/{id}')

    return redirect('/user-dashboard')






def reportPreview_view(request,id):
    if request.method=="POST":
        customer_remark=request.POST.get('customer_remark')
        project_to_update=ProjectCompletion.objects.get(id=id)
        project_to_update.customer_remark=customer_remark
        status_to_update=project_to_update.project
        try:
            project_to_update.save()
            status_to_update.work_status="Done"
            status_to_update.project_link=f'https://emambit.pythonanywhere.com/report-preview/{id}/'
            status_to_update.save()
            messages.success(request,'Thank You !  Have a Great Day')
            return redirect(f'/report-preview/{id}')
        except:
            messages.error(request,'Something Went Wrong Please Try Again')
            return redirect(f'/report-preview/{id}')
    compeleted_project=ProjectCompletion.objects.get(id=id)
    project_images = compeleted_project.project_images.all()
    project_report_data=AddReport.objects.filter(project_name=compeleted_project.project)
    return render(request,'preview.html',{"compeleted_project":compeleted_project,'project_report_data':project_report_data,"project_images":project_images})
@login_required(login_url='/login')
def Download_report_view(request,id):
    compeleted_project=ProjectCompletion.objects.get(id=id)
    project_images = compeleted_project.project_images.all()
    project_report_data=AddReport.objects.filter(project_name=compeleted_project.project)
    return render(request,'preview.html',{"compeleted_project":compeleted_project,'project_report_data':project_report_data,"project_images":project_images})


@login_required(login_url='/login')
def UserAttendance_view(request):
    try:

        cur_month=datetime.datetime.now().month
        # cur_month-=1
        if cur_month < 10:
            cur_month='0' + str(cur_month)
        cur_month=str(cur_month)
        today=datetime.datetime.now().date()
        today=today.strftime('%d %m %Y')
        formated_today=str(today).replace(' ','-')
        attendance_data={}
        abc_data=[]
        try:
            attendance_data=UserAttendance.objects.get(engineer=request.user,attendance_date=formated_today)
        except:
            pass
        cur_year=datetime.datetime.now().year
        cur_year=str(cur_year)
        cur_year='-'+cur_year
        all_a_data=UserAttendance.objects.filter(engineer=request.user).order_by('-id')


        for ij in all_a_data:
            if ij.attendance_date[3:]==cur_month+cur_year:
                abc_data.append({
                    'Date':ij.attendance_date,
                    'PunchIn':ij.punchin_time,
                    'PunchOut':ij.punchout_time,
                    "Production":ij.total_hours,
                    "Location":ij.punchin_location,
                })

            else:
                pass
        date_to_gate=cur_month+cur_year
        total_attendance=UserAttendance.objects.all().order_by('-id')
        g_data=UserAttendance.objects.filter(attendance_date__endswith=date_to_gate)

        engineer_occurrences = g_data.values('engineer').annotate(total_occurrences=Count('engineer'))
        all_engineer=CustomUser.objects.all().exclude(is_staff=True)

        return render(request,'user-attendance.html',{'attendance_data':attendance_data,'total_attendance':total_attendance,'engineer_occurrences':engineer_occurrences,'all_engineer':all_engineer,'abc_data':abc_data})
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/')

def ViewAttendance_view(request,id):
    eng_to_get=CustomUser.objects.get(id=id)
    particular_attendance=UserAttendance.objects.filter(engineer=eng_to_get)
    return render(request,'view-attendance.html',{'particular_attendance':particular_attendance,'eng_to_get':eng_to_get})
def PunchIn_view(request):
    print('hello world')
    if request.method == "POST":
        print('it was a post request')
        current_engineer=request.user

        print(current_engineer,'this was current engineer')
        punchin_country=request.POST.get('punchin_country')
        punchin_state=request.POST.get('punchin_state')
        punchin_location=request.POST.get('punchin_location')
        punchin_postcode=request.POST.get('punchin_postcode')
        attendance_date = request.POST.get('attendance_date')
        print('was date',attendance_date)
        punchin_time=request.POST.get('punchin_time')
        current_engineer.attendance_status="P"
        current_engineer.save()
        try:

            attendance_to_save=UserAttendance(engineer=current_engineer,punchin_country=punchin_country,punchin_state=punchin_state,punchin_location=punchin_location,punchin_postcode=punchin_postcode,attendance_date=attendance_date,punchin_time=punchin_time,punch_status="In")
            attendance_to_save.save()
            messages.success(request,'Attendance Marked Successfully')
            return redirect('/user-attendance')
        except Exception as e:
            print('was else date',attendance_date)
            print(e,'was error  ')
            messages.error(request,'Something Went Wrong !')
    messages.error(request,'Something Went Wrong  ')
    return redirect('/user-attendance')

def PunchOut_view(request):
    if request.method == "POST":

        punchout_country=request.POST.get('punchout_country')
        punchout_state=request.POST.get('punchout_state')
        punchout_location=request.POST.get('punchout_location')
        punchout_postcode=request.POST.get('punchout_postcode')
        punchout_time=request.POST.get('punchout_time')
        attendance_date=request.POST.get('attendance_date')
        print(attendance_date,'its date')
        total_hours=request.POST.get('total_hours')
        punchout_data=UserAttendance.objects.get(engineer=request.user,attendance_date__icontains=attendance_date)
        if punchout_data.punch_status=="Out":
            messages.error(request,'Already Punch Out')
            return redirect('/user-attendance')
        punchout_data.punchout_country=punchout_country
        punchout_data.punchout_state=punchout_state
        punchout_data.punchout_location=punchout_location
        punchout_data.punchout_postcode=punchout_postcode
        punchout_data.punchout_time=punchout_time
        punchout_data.total_hours=total_hours
        punchout_data.punch_status="Out"
        punchout_data.save()
        current_engineer=request.user
        current_engineer.attendance_status="A"
        current_engineer.save()

        messages.success(request,'Punch Out Successfully')
        return redirect('/user-attendance')
    return redirect('/user-attendance')





@login_required(login_url='/login')
def reimbursement_view(request):
    total_user=CustomUser.objects.all().exclude(is_staff=True)
    total_cost=Reimbursement.objects.all()
    pending_data=Reimbursement.objects.filter(reimbursement_status="Pending")
    approved_data=Reimbursement.objects.filter(reimbursement_status="Approved")
    if request.GET.get('get_engineer'):
        cur=CustomUser.objects.get(first_name=request.GET.get('get_engineer'))
        total_cost=Reimbursement.objects.filter(engineer=cur)
    return render(request,'user-reimbursement.html',{"total_cost":total_cost,'pending_data':pending_data,"approved_data":approved_data,'total_user':total_user})

@login_required(login_url='/login')
def addReimbursement_view(request):
    try:

        reimbursement_data=ClientCompanyInfo.objects.all()
        old_data=Reimbursement.objects.filter(engineer=request.user)
        total_cost = old_data.aggregate(total_cost=Sum('cost'))['total_cost']

        if request.method=="POST":
            engineer=CustomUser.objects.get(first_name=request.POST.get('engineer'))
            company=ClientCompanyInfo.objects.get(company_name=request.POST.get('company'))
            visit_purpose=request.POST.get('visit_purpose')
            manager_name=request.POST.get('manager_name')
            department=request.POST.get('department')
            date=request.POST.get('date')
            work_description=request.POST.get('work_description')
            category=request.POST.get('category')
            reimbursement_value=request.POST.get('reimbursement_value')
            advance=request.POST.get('advance')
            cost=request.POST.get('cost')
            reimbursement_images=request.FILES.getlist('attachment')
            print(len(reimbursement_images),'is length of imagess')
            try:
                data=Reimbursement(engineer=engineer,company=company,visit_purpose=visit_purpose,manager_name=manager_name,department=department,date=date,work_description=work_description,category=category,reimbursement_value=reimbursement_value,advance=advance,cost=cost)
                data.save()
                for im in reimbursement_images:
                    print(im,'geted images')
                    data.attachment_images.create(images=im)
                data.save

                messages.success(request,'Reimbursement Added Successfully')
                return redirect('/add-reimbursement')

            except  Exception as e:
                print(e)
                messages.error(request,'something went wrong')
                return redirect('/add-reimbursement')
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/user-dashboard')

    return render(request,'add-reimbursement.html',{"reimbursement_data":reimbursement_data,'old_data':old_data,'total_cost':total_cost})

@login_required(login_url='/login')
def ApproveReimbursement(request,id):
    if  request.user.is_superuser:
        print('hello world')
        data_to_approve=Reimbursement.objects.get(id=id)
        current_engineer=data_to_approve.engineer.email
        data_to_approve.reimbursement_status="Approved"
        data_to_approve.save()
        cost=data_to_approve.cost
        total_cost_to_add=CustomUser.objects.get(email=current_engineer)
        total_cost_to_add.total_cost+=cost
        total_cost_to_add.save()
        messages.success(request,'Reimbursement Approved Successfully')
        return redirect('/reimbursement')
    else:
        return redirect('/page-not-found')

@login_required(login_url='/login')
def ReimbursementDetails_view(request,id):
    try:

        data_to_view=Reimbursement.objects.get(id=id)
        attachments=data_to_view.attachment_images.all()
        if request.method=="POST":
            cost=request.POST.get('cost')
            reimbursement_value=request.POST.get('reimbursement_value')
            advance=request.POST.get('advance')
            data_to_save=Reimbursement.objects.get(id=id)
            try:
                data_to_save.cost=cost
                data_to_save.reimbursement_value=reimbursement_value
                data_to_save.advance=advance
                data_to_save.reimbursement_status='Approved'
                data_to_save.save()
                messages.success(request,'Reimbursement Approved Successfully')
                return redirect (f'/reimbursement')
            except Exception as e:
                print(e,'was error')
                messages.error(request,'Opps ! Something Went Wrong ')
                return redirect (f'/reimbursement-details/{id}')
        return render(request,'reimbursement-details.html',{'data_to_view':data_to_view,"attachments":attachments})
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/reimbursement')

@login_required(login_url='/login')
def ClearReimbursement_view(request,id):
    data_to_clear=Reimbursement.objects.get(id=id)
    try:
        data_to_clear.delete()
        messages.success(request,'Amount Cleard Successfully')
        return redirect('/reimbursement')
    except:
        messages.error(request,'Something Went Wrong Please Try Again')
        return redirect('/reimbursement')

@login_required(login_url='/login')
def DeleteReimbursement_view(request,id):
    data_to_delete=Reimbursement.objects.get(id=id)
    try:
        data_to_delete.delete()
        messages.success(request,'Delete Successfully')
        return redirect('/add-reimbursement')
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/add-reimbursement')


@login_required(login_url='/login')
def userProfile_view(request):
    user_data=CustomUser.objects.get(email=request.user.email)
    return render(request,'user-profile.html',{"user_data":user_data})

def ViewAdvance_view(request):
    advance_data=AdvanceMoney.objects.all()
    if request.GET.get('get_user'):
        try:
            cur_user=CustomUser.objects.get(first_name=request.GET.get('get_user'))
            advance_data=AdvanceMoney.objects.filter(engineer_name=cur_user)
        except:
            messages.error(request,'User Not Found')
            return redirect('/view-advance')
    p = Paginator(advance_data, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    all_engineers=CustomUser.objects.all().exclude(is_staff=True)
    return render(request,'view-advance.html',{'advance_data':page_obj,'all_engineers':all_engineers})

def DeleteAdvance_view(request,id):

    try:

        advance_to_delete=AdvanceMoney.objects.get(id=id)
        advance_to_delete.delete()
        messages.success(request,'Advance Deleted Successfully')
        return redirect('/view-advance')
    except:
        messages.error(request,'Something Went Wrong')
        return redirect('/view-advance')







@login_required(login_url='/login')
def attendance_to_download(request,month_no):
    try:
        data_to_excel = UserAttendance.objects.all()
        # print(month_no,'was month number')
        cur_year=datetime.datetime.now().year
        if int(month_no) == 12:
            cur_year-=1
        cur_year=str(cur_year)
        cur_year='-'+cur_year
        filtered_data = []
        for d in data_to_excel:
            if d.attendance_date[3:] == month_no+cur_year:
                filtered_data.append({
                    'engineer': d.engineer.first_name,
                    'attendance_date': d.attendance_date,
                    'punchin_country': d.punchin_country,
                    'punchout_country': d.punchout_country,
                    'punchin_location': d.punchin_location,
                    'punchout_location': d.punchout_location,
                    'punchin_time': d.punchin_time,
                    'punhcout_time': d.punchout_time,  # Fixed typo punhcout_time to punchout_time
                    'total_hours': d.total_hours,
                })
        # print(filtered_data,'f')
        # Convert filtered data to DataFrame
        if len(filtered_data) == 0:
            print('data ni mila')
            messages.error(request,'No Data Found')
            return redirect('/user-attendance')
        df = pd.DataFrame(filtered_data)

        # Write data to Excel file
        excel_filename = 'attendance_record.xlsx'
        excel_filepath = os.path.join(os.getcwd(), excel_filename)

        with pd.ExcelWriter(excel_filepath, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        # Read the file content
        with open(excel_filepath, 'rb') as file:
            file_content = file.read()

        # Delete the file
        os.remove(excel_filepath)

        # Serve file for download
        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(excel_filename)

        # Return file response
        return response
    except Exception as e:
        print(e)
        messages.error(request,'Opps! Something Went Wrong')
        return redirect('/user-attendance')



@login_required(login_url='/login')
def downloadAdvance(request,cur_month):
    try:
        cur_year=datetime.datetime.now().year
        if int(cur_month) == 12:
            cur_year-=1
        cur_year=str(cur_year)
        cur_year=cur_year+'-'
        data_to_excel = AdvanceMoney.objects.all()
        filtered_data = []
        for d in data_to_excel:

            if d.project_name.leave_date[0 :7] == cur_year+cur_month:
                filtered_data.append({
                    'engineer': d.engineer_name.first_name,
                    'company_name':d.project_name.company_name.company_name,
                    'date': d.project_name.leave_date,
                    'address':d.project_name.company_name.company_address,
                    'amount':d.advance_amount
                })
        if len(filtered_data) == 0:

            messages.error(request,'No Data Found')
            return redirect('/view-advance')
        # Convert filtered data to DataFrame
        df = pd.DataFrame(filtered_data)

        # Write data to Excel file
        excel_filename = 'advance_record.xlsx'
        excel_filepath = os.path.join(os.getcwd(), excel_filename)

        with pd.ExcelWriter(excel_filepath, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        # Read the file content
        with open(excel_filepath, 'rb') as file:
            file_content = file.read()

        # Delete the file
        os.remove(excel_filepath)

        # Serve file for download
        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(excel_filename)

        # Return file response
        return response
    except Exception as e:
        print(e)
        messages.error(request,'Opps! Something Went Wrong')
        return redirect('/view-advance')