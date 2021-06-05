from django.contrib import admin

from django.contrib.auth.models import User
from .models import *
from django_admin_listfilter_dropdown.filters import (DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from admin_auto_filters.filters import AutocompleteFilter


class LayerFilter(AutocompleteFilter):
    title = 'Layer' # display title
    field_name = 'layer'
# Register your models here.

class LayerGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'index',)
    list_editable = ('index',)
    ordering=['index',]

admin.site.register(Layergroup,LayerGroupAdmin)


class LayerAdmin(admin.ModelAdmin):
    search_fields = ['layer_title']
    list_display = ('group', 'layer_service', 'layer_title', 'popup', 'opacity', 'enable', 'service_type','index',)
    list_editable=('layer_service', 'layer_title', 'popup', 'opacity', 'enable', 'service_type','index',)
    list_filter = (('group',DropdownFilter),('layer_title',DropdownFilter),('popup'))

admin.site.register(Layer,LayerAdmin)

class Layer_FiledAdmin(admin.ModelAdmin):
    list_display = ('layer', 'field', 'display_name', 'popup_title', 'show_in_popup', 'show_as_label', 'show_in_details')
    list_editable=('display_name', 'popup_title', 'show_in_popup', 'show_as_label', 'show_in_details')
    list_filter = [LayerFilter]
    search_fields = ['field','display_name']
    #list_filter = (('layer', DropdownFilter),('a_choicefield', ChoiceDropdownFilter))



admin.site.register(Layer_Field,Layer_FiledAdmin)


class Layer_StyleAdmin(admin.ModelAdmin):
    # def get_queryset(self, request):
    #     qs = super(Layer_StyleAdmin, self).get_queryset(request)
    #     print(qs)
    #     return qs.filter(layer__service_type='wfs')
    def render_change_form(self, request, context, *args, **kwargs):
        context["adminform"].form.fields["layer"].queryset = Layer.objects.filter(service_type='wfs')
        return super(Layer_StyleAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )

admin.site.register(Layer_Style,Layer_StyleAdmin)



admin.site.register(Map_Config)
admin.site.register(Basemap)
# Register your models here.
