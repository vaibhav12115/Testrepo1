from django.shortcuts import render
#views.py
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from login.models import on_demand_feeds, on_demand_feeds_cta,UserProfile
from login.connections import getconnection
from login.connection_fm import get_connection_fm
from login.connection_ref import get_connection_ref
from login.roleprivilege_query import common_query
@csrf_protect
def register(request):
    """
    register a new user and assign privileges to access of functionalities
    :param request:
    :return:
    """
    if request.method == 'POST':
        db_conn = getconnection()
        c=db_conn.cursor()

        row = c.execute("""SELECT privilege_name from privileges where is_visible=%s""", (1,))
        rows = c.fetchall()

        lstChoices = ()
        i = 0
        lstChoices = list(lstChoices)
        while i < row:
            lstChoices.insert(i, (rows[i][0], rows[i][0]))
            i = i + 1

        lstChoices.insert(i, ("All", "All"))
        lstChoices = tuple(lstChoices)
        form = RegistrationForm(request.POST)
        form.fields['privileges'].choices = lstChoices
        if form.is_valid():

            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],

            )
            privileges=form.cleaned_data['privileges']
            profile = UserProfile(user=user,privileges=privileges)
            profile.save()

            rolename="role_"+user.username
            from datetime import datetime
            if "All" not in profile.privileges:
                db_conn = getconnection()
                c = db_conn.cursor()
                c.execute("""INSERT INTO roles (role_name,created_at)
                VALUES (%s, %s)""",
                          (rolename, datetime.now()))
                roleidrow=c.execute("""SELECT id from roles where role_name=%s""",(rolename,))
                roleidrows=c.fetchall()
                finalroleid=roleidrows[0][0]

                if "OnDemand Feeds" in profile.privileges:
                    common_query("OnDemand Feeds",finalroleid)
                if "Android Grid" in profile.privileges:
                    common_query("Android Grid",finalroleid)
                if "iOS Grid" in profile.privileges:
                    common_query("iOS Grid",finalroleid)
                if "Referral" in profile.privileges:
                    common_query("Referral",finalroleid)
                db_conn.commit()
                db_conn.close()

            return HttpResponseRedirect('/register/success/')
    else:
        db_conn = getconnection()
        c = db_conn.cursor()

        row = c.execute("""SELECT privilege_name from privileges where is_visible=%s""",(1,))
        rows = c.fetchall()

        lstChoices = ()
        i = 0
        lstChoices = list(lstChoices)
        while i < row:
            lstChoices.insert(i, (rows[i][0], rows[i][0]))
            i = i + 1

        lstChoices.insert(i,("All","All"))
        lstChoices = tuple(lstChoices)
        form = RegistrationForm()
        form.fields['privileges'].choices = lstChoices
    variables = RequestContext(request, {
    'form': form,
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

@login_required
@csrf_protect
def Addcard(request):
    """
    Functionality to add a new On Demand card and update to feeds and cta tables accordingly
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "OnDemand Feeds" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    elif request.method == 'POST':
        form = AddCardForm(request.POST)
        #print "hello"
        if form.is_valid():
            one=request.POST.get('card_title', '')
            two = request.POST.get('deeplink', '')
            three = request.POST.get('cta_text', '')
            four = request.POST.get('link', '')
            five = request.POST.get('card_sub_title', '')
            six = request.POST.get('card_start_date', '')
            seven = request.POST.get('card_expiry_date', '')
            eight = request.POST.get('card_image', '')
            nine = request.POST.get('priority', '')
            ten = request.POST.get('card_icon', '')
            db_conn=get_connection_fm()
            c = db_conn.cursor()

            cardobj = on_demand_feeds(card_title=one, deeplink=two, card_sub_title=five, card_start_date=six,
                                      card_expiry_date=seven, card_image=eight, priority=nine, card_icon=ten,
                                      card_category=0,
                                      is_processed=0, created_at=datetime.now(), card_status=1
                                      )
            #cardobj.save()
            c.execute("""INSERT INTO on_demand_feeds (card_title, deeplink, card_sub_title,card_start_date,
                             card_expiry_date,card_image,priority,card_icon, card_category,
                             is_processed, created_at,card_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (one,two,five,six,seven,eight,nine,ten,0,0,datetime.now(),1))


            ctaobj = on_demand_feeds_cta(feed_id=c.lastrowid, link=four, cta_text=three, created_at=datetime.now(),
                                         status=0, display_order=0)
            #ctaobj.save()

            c.execute("""INSERT INTO on_demand_feeds_cta (feed_id,link,cta_text,created_at,
                           status,display_order)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                      (c.lastrowid, four, three, datetime.now(),0, 0))
            db_conn.commit()

            db_conn.close()
            return HttpResponseRedirect('/home/')
    else:
        form = AddCardForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
    'Addcard.html',
    variables,
    )

@login_required
@csrf_protect
def Modifycarddetails(request):
    """
    Functionality to modify an OnDemand card for the selected specific card (card title) from modifycard functionality
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "OnDemand Feeds" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    elif request.method == 'POST':
        form0 = ModifyCardForm(request.POST)
        if form0.is_valid():
            one = request.session['Ctitle']
            two = request.POST.get('deeplink', '')
            three = request.POST.get('cta_text', '')
            four = request.POST.get('link', '')
            five = request.POST.get('card_sub_title', '')
            six = request.POST.get('card_start_date', '')
            seven = request.POST.get('card_expiry_date', '')
            eight = request.POST.get('card_image', '')
            nine = request.POST.get('priority', '')
            ten = request.POST.get('card_icon', '')
            eleven=request.POST.get('card_status','')

            db_conn=get_connection_fm()
            c = db_conn.cursor()

            if eleven=="op1":
                cardstatval=1
            else:
                cardstatval=0

            c.execute("""UPDATE on_demand_feeds SET deeplink=%s, card_sub_title=%s,card_start_date=%s,
                            card_expiry_date=%s,card_image=%s,priority=%s,card_icon=%s, card_category=%s,
                           is_processed=%s, created_at=%s,card_status=%s
                          WHERE card_title=%s""",
                  (two, five, six, seven, eight, nine, ten, 0, 0, datetime.now(), cardstatval,one))


            c.execute("""UPDATE on_demand_feeds_cta SET link=%s,cta_text=%s,created_at=%s,
                          status=%s,display_order=%s
                         WHERE feed_id=%s""",
                   (four, three, datetime.now(), 0, 0,request.session['Fid']))
            db_conn.commit()

            db_conn.close()
            return HttpResponseRedirect('/home/')
    else:
        db_conn = get_connection_fm()
        c = db_conn.cursor()

        request.session['Ctitle'] = request.GET.get('card_title', '')

        rowcarddetails=c.execute("""SELECT deeplink, card_sub_title,card_start_date,
                          card_expiry_date,card_image,priority,card_icon, card_category,
                          is_processed, created_at,card_status from on_demand_feeds
                          WHERE card_title=%s""", (request.session['Ctitle'],))
        rowcarddetailsrows=c.fetchall()
        deeplink_val=rowcarddetailsrows[0][0]
        card_sub_title_val = rowcarddetailsrows[0][1]
        card_start_date_val = rowcarddetailsrows[0][2]
        card_expiry_date_val = rowcarddetailsrows[0][3]
        card_image_val = rowcarddetailsrows[0][4]
        priority_val = rowcarddetailsrows[0][5]
        card_icon_val = rowcarddetailsrows[0][6]
        card_category_val = rowcarddetailsrows[0][7]
        is_processed_val = rowcarddetailsrows[0][8]
        created_at_val = rowcarddetailsrows[0][9]
        card_status_val = rowcarddetailsrows[0][10]

        rowidid = c.execute("""SELECT id from on_demand_feeds WHERE card_title=%s""", (request.session['Ctitle'],))
        rowidrows = c.fetchall()

        request.session['Fid'] = rowidrows[0][0]

        rowcta = c.execute("""SELECT cta_text,link from on_demand_feeds_cta WHERE feed_id=%s""", (request.session['Fid'],))
        rowctarows = c.fetchall()

        cta_text_val=rowctarows[0][0]
        link_val=rowctarows[0][1]

        if card_status_val==1:
            card_status_option='op1'
        else:
            card_status_option='op2'

        form0 = ModifyCardForm(
                initial={'deeplink': deeplink_val, 'cta_text': cta_text_val, 'link': link_val,
                         'card_sub_title': card_sub_title_val, 'card_start_date': card_start_date_val,
                         'card_expiry_date': card_expiry_date_val, 'card_image': card_image_val,
                         'priority': priority_val, 'card_icon': card_icon_val,'card_status':card_status_option})

        db_conn.commit()
        db_conn.close()

    variables = RequestContext(request, {
        'form0': form0,
        'ctitle':request.session['Ctitle']

    })
    return render_to_response(
        'Modifycarddetails.html',
        variables,
    )

@login_required
@csrf_protect
def Modifycard(request):
    """
    Select the specific card which needs to be modified by card title
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "OnDemand Feeds" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    elif request.method == 'POST':
            return HttpResponseRedirect('/home/Modifycard/Modifycarddetails/')
    else:
        db_conn = get_connection_fm()
        c = db_conn.cursor()
        row=c.execute("""SELECT card_title, deeplink, card_sub_title,card_start_date,
                             card_expiry_date,card_image,priority,card_icon from on_demand_feeds""")
        rows = c.fetchall()

        lstChoices = ()
        i=0
        lstChoices=list(lstChoices)
        while i< row:
            lstChoices.insert(i,(rows[i][0],rows[i][0]))
            i=i+1
        lstChoices=tuple(lstChoices)
        form0=ModifyCardForm_cardtitle()
        form0.fields['card_title'].choices = lstChoices

        db_conn.commit()
        db_conn.close()

    variables = RequestContext(request, {
        'form0':form0

    })
    return render_to_response(
        'Modifycard.html',
        variables,
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def CardMenu(request):
    """
    Menu for adding/modifying a card
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "OnDemand Feeds" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    return render_to_response(
    'CardMenu.html',
    {  }
    )

@login_required
def AndroidGrid(request):
    """
    Grid functionality in progress...
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "Android Grid" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    return render_to_response(
    'AndroidGrid.html',
    {  }
    )

@login_required
def iOSGrid(request):
    """
    Grid functionality in progress
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "iOS Grid" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    return render_to_response(
    'iOSGrid.html',
    {  }
    )

@csrf_protect
@login_required
def ReferralConfig(request):
    """
    Select the referral attribute whose value needs to be changed
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "Referral" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    elif request.method == 'POST':
        return HttpResponseRedirect('/home/Modifycard/Modifycarddetails/')

    else:
        db_conn=get_connection_ref()
        c = db_conn.cursor()
        row = c.execute("""SELECT attribute_name from referral_config""")
        rows = c.fetchall()

        lstChoices = ()
        i = 0
        lstChoices = list(lstChoices)
        while i < row:
            lstChoices.insert(i, (rows[i][0], rows[i][0]))
            i = i + 1
        lstChoices = tuple(lstChoices)
        form0 = ReferralConfigForm_name()
        form0.fields['attribute_name'].choices = lstChoices

        db_conn.commit()
        db_conn.close()

    variables = RequestContext(request, {
    'form0': form0

})
    return render_to_response(
    'ReferralConfig.html',
    variables,
)

@login_required
@csrf_protect
def ReferralConfigVal(request):
    """
    Update the attribute value of selected attribute
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)
    if "Referral" not in profile.privileges and "All" not in profile.privileges:
        return HttpResponseRedirect('/AccessForbidden/')
    elif request.method == 'POST':
        form0 = ReferralConfigForm_value(request.POST)
        if form0.is_valid():
            one = request.session['refname']
            two = request.POST.get('attribute_value', '')

            request.session['ref_finalvalue']=two

            db_conn = get_connection_ref()
            c = db_conn.cursor()

            c.execute("""UPDATE referral_config SET attribute_value=%s
                          WHERE attribute_name=%s""",
                  (two,one))

            db_conn.commit()

            db_conn.close()

            import logging
            logger = logging.getLogger('myapp')
            hdlr = logging.FileHandler('/var/tmp/myapp.log')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            logger.addHandler(hdlr)
            logger.setLevel(logging.INFO)

            logger.info(request.session['refname'] + "\'s value was "+request.session['ref_initialvalue']+" and was changed to "
                        +request.session['ref_finalvalue']+" by "+request.user.username)

            return HttpResponseRedirect('/home/')
    else:
        db_conn = get_connection_ref()
        c = db_conn.cursor()

        request.session['refname'] = request.GET.get('attribute_name', '')

        rowrefdetails=c.execute("""SELECT attribute_value from referral_config
                          WHERE attribute_name=%s""", (request.session['refname'],))
        rowrefdetailsrows=c.fetchall()
        attribute_val=rowrefdetailsrows[0][0]

        request.session['ref_initialvalue'] = attribute_val

        form0 = ReferralConfigForm_value(
                initial={'attribute_value': request.session['ref_initialvalue']})

        db_conn.commit()
        db_conn.close()

    variables = RequestContext(request, {
        # 'form': form,
        'form0': form0,
        'refname':request.session['refname']

    })
    return render_to_response(
        'ReferralConfigVal.html',
        variables,
    )

@login_required
def AccessForbidden(request):
    """
    Denying access to pages whose privilege is not given to a particular user
    :param request:
    :return:
    """
    return render_to_response(
    'AccessForbidden.html',
    {  }
    )


@login_required
def home(request):
    """
    home page giving access to specific functionalities based on privileges
    :param request:
    :return:
    """
    profile = UserProfile.objects.get(user=request.user)

    ondemandfeeds=""
    androidgrid=""
    iosgrid=""
    referral=""
    if "OnDemand Feeds" in profile.privileges:
        ondemandfeeds="OnDemand Feeds"
    if "Android Grid" in profile.privileges:
        androidgrid = "Android Grid"
    if "iOS Grid" in profile.privileges:
        iosgrid = "iOS Grid"
    if "Referral" in profile.privileges:
        referral = "Referral"
    if "All" in profile.privileges:
        ondemandfeeds = "OnDemand Feeds"
        androidgrid = "Android Grid"
        iosgrid = "iOS Grid"
        referral = "Referral"
    return render_to_response(
    'home.html',
    { 'user': request.user,
      'ondemandfeeds': ondemandfeeds,
      'androidgrid' : androidgrid,
      'iosgrid' : iosgrid,
      'referral':referral
      }

    )