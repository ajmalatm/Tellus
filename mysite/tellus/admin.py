from django.contrib import admin
from .models import *

from leaflet.admin import LeafletGeoAdmin
# Register your models here.

#
admin.site.register(Building_Usage)
admin.site.register(Building_Zone)
admin.site.register(Road_Type)

#admin.site.register(District1)
admin.site.register(Localbody)

admin.site.register(Villages_Localbody)
admin.site.register(Postoffice)
admin.site.register(Postoffice_Localbody)
admin.site.register(Ward)

admin.site.register(Establishment)
admin.site.register(Owner_Details)
admin.site.register(Tenent_Details)
admin.site.register(Tax_Details)

#emp_count = models.IntegerField(blank=True, null=True)
#'estb_nm','estb_yr','estb_post','estb_pin','estb_l_phn','estb_mob','estb_email',
#'ownr_nm','ownr_house','ownr_place','ownr_post','ownr_pin','ownr_surno','ownr_vlage','ownr_l_phn','ownr_mob','ownr_email'





#admin.site.register(Floor_Prop_Area)

from django import forms
class MyForm(forms.ModelForm):
    class Meta:
        model = Floor_Prop_Area
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        #self.fields['status'].widget = forms.RadioSelect(choices=self.fields['status'].choices)

class Floor_Prop_AreaInline(admin.TabularInline):
    model = Floor_Prop_Area
    form = MyForm

class Tax_Inline(admin.TabularInline):
    model = Tax_Details
    max=1


class Owner_Inline(admin.TabularInline):
    model = Owner_Details
    max=1
class FormsixAdmin(LeafletGeoAdmin):
    list_display = ('lsgd','bldg_usage', 'new_pro_id', 'ward_no', 'ward_nm', 'get_total_area')
    fields = ('lsgd', 'ward_no_id', 'old_ward_no_id', 'new_pro_id', 'old_pro_id','cellar_area', 'flr_grnd', 'bldg_stats', 'bldg_zone', 'near_rd', 'rd_width',
        'year_const', 'centrl_ac','bldg_usage', 'structural_change', 'geom')
    inlines = [Floor_Prop_AreaInline,Tax_Inline,Owner_Inline]
    def save_model(self, request, obj, form, change):
        obj.save()
        # for user in User.objects.all():
        #     obj.attendance_set.create(user=user, status='')
             # you should consider a null field or a possible choice for "Undecided"

admin.site.register(Formsix, FormsixAdmin)