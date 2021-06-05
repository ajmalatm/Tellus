from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Create your views here.
from django.db.models import Count

def home(response):
    if(response.user.is_superuser):
        return render(response,'tellus/index.html',{})
    else:
        return render(response, 'tellus/propertysearch.html', {})

def dashboard(response):
    return render(response,'tellus/dashboard.html',{})

def propsearch(response):
    return render(response,'tellus/propertysearch.html',{})

class get_Dashboard_Data(APIView):
    def get(self, request):
        totalbuidings=0
        tax_paid_buildings=0
        tax_notpaid_buildings = 0
        total_tax_collected=0
        dashboard={'usageGroup':{},'totalBuildings':0,'tax_paid_buildings':0,'tax_notpaid_buildings':0,'total_tax_collected':0,'wardwise':{}}
        for ward in Ward.objects.all():
            #local body must be considered
            dashboard['wardwise'][ward.ward_no]={'ward_name':'','buidings':0,'collectedamt':0,'pending':0,'total':0}
        for usage in Building_Usage.objects.all():
            count=usage.formsix_set.count()
            dashboard['usageGroup'][usage.bldg_usage]=count
            totalbuidings+=count
            for b in usage.formsix_set.all():
                dashboard['wardwise'][b.ward_no]['ward_name'] = b.ward_nm
                #building can be categorised based on usage here
                dashboard['wardwise'][b.ward_no]['buidings'] += 1
                if(b.tax_details_set.exists()):
                    if(b.tax_details_set.filter(taxpaid_yr=date.today().year).exists()):
                        amt=(b.tax_details_set.get(taxpaid_yr=date.today().year).tax_amnt)
                        dashboard['wardwise'][b.ward_no]['collectedamt']+=amt
                        tax_paid_buildings+=1
                        total_tax_collected+=amt
                    else:
                        dashboard['wardwise'][b.ward_no]['pending']+=1
                        tax_notpaid_buildings += 1
                else:
                    dashboard['wardwise'][b.ward_no]['pending'] += 1
                    tax_notpaid_buildings+=1
        dashboard['totalBuildings']=totalbuidings
        dashboard['tax_paid_buildings'] = tax_paid_buildings
        dashboard['tax_notpaid_buildings'] = tax_notpaid_buildings
        dashboard['total_tax_collected']=total_tax_collected
        return Response(dashboard)


def get_Tax_Info(id):
    try:
        property = Formsix.objects.get(id=id)
        baserate = 10
        reduction = 0;
        reduction_percentage = 0;
        addition = 0;
        addition_percentage = 0;
        basic_propertytax = property.get_total_area * baserate
        if (property.bldg_zone == 'Zone 2'):
            reduction += (basic_propertytax * 10) / 100
            reduction_percentage += 10
        elif (property.bldg_zone == 'Zone 3'):
            reduction += (basic_propertytax * 20) / 100
            reduction_percentage += 20
        if (property.rd_width.road_type_category == 2):
            reduction += (basic_propertytax * 10) / 100;
            reduction_percentage += 10
        elif (property.rd_width.road_type_category == 1):
            reduction += (basic_propertytax * 20) / 100
            reduction_percentage += 20
        elif (property.rd_width.road_type_category == 4):
            addition += (basic_propertytax * 20) / 100
            addition_percentage += 20
        if (property.centrl_ac == '1'):
            addition += (basic_propertytax * 10) / 100
            addition_percentage += 10
        propertytax = basic_propertytax - reduction + addition
        # {'property': property.new_pro_id, 'basic_tax': basic_propertytax, 'reduction%': reduction_percentage,
        #  'reduction': reduction, 'addition%': addition_percentage, 'addition': addition, 'tax': propertytax})
        return (
            {'property': property.new_pro_id, 'basic_tax': basic_propertytax, 'reduction%': reduction_percentage,
             'addition%': addition_percentage, 'tax': propertytax})
    except:
        return None

class get_PropertyTax(APIView):
    def get(self, request,id):
        try:
            result=get_Tax_Info(id)
            if(result is not None):
                return Response(result)
            else:
                return Response({})
        except:
            return Response({})

class get_property(APIView):
    def post(self, request):
        print(request.data)
        keywords = (request.data).keys()
        #qs = [Q(new_pro_id=request.data[keyword]) | Q(old_pro_id=request.data[keyword]) for keyword in keywords]
        qs=None
        property_data={}
        if('new_pro_id' in keywords):
            qs = [Q(new_pro_id=request.data['new_pro_id'])]
        elif ('old_pro_id' in keywords):
            qs = [Q(old_pro_id=request.data['old_pro_id'])]
        if(qs is not None):
            query = qs.pop()
            for q in qs:
                query |= q
            property = Formsix.objects.filter(ward_no=request.data['ward_no']).filter(query)
            propobj=property.first()
            if(propobj is not None):
                bldg_satus_values = dict(BLDGSTATUS)
                yes_no_values = dict(YESNO)
                owner=OwnerSerializer(propobj.owner_details_set.all(),many=True)
                property=PropertySerializer(propobj)
                property_data=property.data
                property_data['centrl_ac'] =yes_no_values[property_data['centrl_ac']]
                property_data['bldg_zone']=propobj.bldg_zone.bldg_zone
                property_data['bldg_usage'] = propobj.bldg_usage.bldg_usage
                property_data['bldg_stats']=bldg_satus_values[property_data['bldg_stats']]
                property_data['owner']=owner.data
                property_data['tax_details'] = get_Tax_Info(property_data['id'])
        return Response(property_data)
        #serializer = SnippetSerializer(data=request.data)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
