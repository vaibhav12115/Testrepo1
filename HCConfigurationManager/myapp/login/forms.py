#files.py
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateTimeWidget
from datetime import datetime
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    OPTIONS = (
        ("op1", "op1"),
        ("op2", "op2"),
    )
    privileges = forms.MultipleChoiceField(
        choices=OPTIONS,  # this is optional
        widget=forms.CheckboxSelectMultiple)

    #access_rights_number=forms.IntegerField(required=True,label="Access rights", help_text="ENTER one of the following numbers<br /> 1: OnDemand feeds access; <br />"
     #                                                          "2: Grid access; <br />"
      #                                                         "3: Referral access; <br />"
       #                                                        "12: OnDemand feeds & Grid access; <br />"
        #                                                       "13: OnDemand feeds & Referral access; <br />"
         #                                                      "23: Grid & Referral access; <br />"
          #                                                     "123: All access; <br />"
    #                                )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        #if 'access_rights_number' in self.cleaned_data:
         #   if self.cleaned_data['access_rights_number'] != 1 and self.cleaned_data['access_rights_number'] != 2 and self.cleaned_data['access_rights_number'] != 3 and self.cleaned_data['access_rights_number'] != 12 and self.cleaned_data['access_rights_number'] != 13 and self.cleaned_data['access_rights_number'] != 23 and self.cleaned_data['access_rights_number'] != 123:
          #      raise forms.ValidationError(_("Enter a valid access rights number"))
        if 'email' in self.cleaned_data:
            if "helpchat" not in self.cleaned_data['email']:
                raise forms.ValidationError(_("Enter a valid helpchat email"))
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class AddCardForm(forms.Form):
    card_title = forms.CharField(required=True,label='CARD TITLE: ', max_length=100)
    deeplink = forms.CharField(required=True, label='CARD LINK: ', max_length=150)
    cta_text = forms.CharField(required=True, label='CARD CTA: ', max_length=30)
    link = forms.CharField(required=True, label='CTA LINK: ', max_length=150)
    card_sub_title = forms.CharField(required=True, label='CARD SUBTITLE: ', max_length=75,help_text="Accepted Format Example: 2016-06-29 07:26:09")
    dateTimeOptions = {
        'format': 'yyyy-mm-dd hh:ii:ss',
        'autoclose': True,
        'showMeridian': True
    }
    card_start_date = forms.DateTimeField(widget=DateTimeWidget(attrs={'id':"dtid1"},options = dateTimeOptions), required=True,
                                          label='START DATE: ')
    #card_start_date=forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datepicker'}),required=True, label='START DATE: ',help_text="Accepted Format Example: 2016-06-29 07:26:09")
    card_expiry_date = forms.DateTimeField(widget=DateTimeWidget(attrs={'id':"dtid2"},options = dateTimeOptions),
                                           required=True, label='END DATE: ')
    #card_start_date = forms.CharField(required=True, label='START DATE: ')
    #card_expiry_date = forms.CharField(required=True, label='END DATE: ')
    card_image= forms.CharField(required=True, label='CARD IMAGE: ', max_length=150)
    priority= forms.IntegerField(required=True, label='PRIORITY: ')
    card_icon =forms.CharField(required=True, label='CARD ICON: ', max_length=150)

    def clean(self):
        if 'priority' in self.cleaned_data:
            if self.cleaned_data['priority'] <0:
                raise forms.ValidationError(_("Priority must be >=0"))
        if 'card_start_date' in self.cleaned_data and 'card_expiry_date' in self.cleaned_data:
            if self.cleaned_data['card_expiry_date'] < self.cleaned_data['card_start_date']:
                raise forms.ValidationError(_("Start date must be atleast equal to end date"))
        return self.cleaned_data

class ModifyCardForm_cardtitle(forms.Form):
    card_title = forms.ChoiceField(label='CARD TITLE:')

class ModifyCardForm(forms.Form):
    OPTIONS = (
        ("op1", "active"),
        ("op2", "inactive"),
    )
    #card_title = forms.ChoiceField(label='CARD TITLE:')
    #card_title = forms.CharField(required=True,label='CARD TITLE: ', max_length=100)
    deeplink = forms.CharField(required=True, label='CARD LINK: ', max_length=150)
    cta_text = forms.CharField(required=True, label='CARD CTA: ', max_length=30)
    link = forms.CharField(required=True, label='CTA LINK: ', max_length=150)
    card_sub_title = forms.CharField(required=True, label='CARD SUBTITLE: ', max_length=75,help_text="Accepted Format Example: 2016-06-29 07:26:09")
    dateTimeOptions = {
        'format': 'yyyy-mm-dd hh:ii:ss',
        'autoclose': True,
        'showMeridian': True
    }
    card_start_date = forms.DateTimeField(widget=DateTimeWidget(attrs={'id':"dtid1"},options = dateTimeOptions), required=True,
                                          label='START DATE: '
                                          )
    card_expiry_date = forms.DateTimeField(widget=DateTimeWidget(attrs={'id':"dtid2"},options = dateTimeOptions),
                                           required=True, label='END DATE: ')
    card_image= forms.CharField(required=True, label='CARD IMAGE: ', max_length=150)
    priority= forms.IntegerField(required=True, label='PRIORITY: ')
    card_icon =forms.CharField(required=True, label='CARD ICON: ', max_length=150)
    card_status = forms.ChoiceField(label='CARD STATUS:',choices=OPTIONS)
    def clean(self):
        if 'priority' in self.cleaned_data:
            if self.cleaned_data['priority'] <0:
                raise forms.ValidationError(_("Priority must be >=0"))
        if 'card_start_date' in self.cleaned_data and 'card_expiry_date' in self.cleaned_data:
            if self.cleaned_data['card_expiry_date'] < self.cleaned_data['card_start_date']:
                raise forms.ValidationError(_("Start date must be atleast equal to end date"))
        return self.cleaned_data

class ReferralConfigForm_name(forms.Form):
    attribute_name = forms.ChoiceField(label='Referral Name:')

class ReferralConfigForm_value(forms.Form):
    attribute_value = forms.CharField(label='Current Value:', max_length=30)
