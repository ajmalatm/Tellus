from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from colorfield.fields import ColorField
from django.db.models import Max

import requests
from django.conf import settings
from django.contrib.gis.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

def layer_service():
    LAYERS=[]
    URL = settings.SSL+"://"+settings.GEOSERVER_USERNAME+":"+settings.GEOSERVER_PASSWORD+"@"+settings.GEOSERVER_PATH+"/rest/layers.json"
    PARAMS = {}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    for layer in data['layers']['layer']:
        if(layer['name'].split(':')[0]=='tellus'):
            print(layer['name'])
            LAYERS.append((layer['name'],layer['name'].split(':')[1]+':'+layer['name'].split(':')[0]))
    LAYERS=tuple(LAYERS)
    return LAYERS

def group_index():
    index=Layergroup.objects.aggregate(Max('index')).get('index__max')
    if index is None:
        return 1
    return index+1


def layer_index():
    index=Layer.objects.aggregate(Max('index')).get('index__max')
    if index is None:
        return 1
    return index+1


def basemap_index():
    index=Basemap.objects.aggregate(Max('index')).get('index__max')
    if index is None:
        return 1
    return index+1


class Layergroup(models.Model):
    parent_group = models.ForeignKey("self", on_delete=models.PROTECT,null=True,blank=True)
    group = models.CharField(max_length=200)
    visibility = models.BooleanField(default=True)
    index=models.PositiveSmallIntegerField(default=group_index)

    def __str__(self):  # __unicode__ for Python
        return self.group
    class Meta:
        verbose_name = "Layer Group"

class Layer(models.Model):
    group = models.ForeignKey(Layergroup, on_delete=models.PROTECT)
    layer_service = models.CharField(max_length=200,choices=layer_service(),unique=True)
    layer_title = models.CharField(max_length=200,verbose_name='Layer Title')
    popup=models.BooleanField()
    opacity=IntegerRangeField(min_value=0, max_value=100,default=100)
    visibility=models.BooleanField(default=True)
    enable = models.BooleanField(default=False)
    service_type = models.CharField(max_length=200,choices=(('wfs','wfs'),('wms','wms')))
    index=models.PositiveSmallIntegerField(default=layer_index)
    bbox=models.CharField(max_length=200,blank=True,null=True)
    crs=models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        URL = settings.SSL+"://"+settings.GEOSERVER_USERNAME+":"+settings.GEOSERVER_PASSWORD+"@"+settings.GEOSERVER_PATH+"/rest/layers/"+self.layer_service+".json"
        r = requests.get(url=URL)
        data = r.json()
        newurl=(data['layer']['resource']['href'])
        newurl=newurl.replace('//','//admin:geoserver@')
        r = requests.get(url=newurl)
        data = r.json()
        bbox=(data['featureType']['latLonBoundingBox'])
        self.bbox = str(bbox['minx'])+","+str(bbox['miny'])+","+str(bbox['maxx'])+","+str(bbox['maxy'])
        self.crs=bbox['crs']
        super(Layer, self).save(*args, **kwargs)

    def __str__(self):  # __unicode__ for Python
        return self.layer_title
    class Meta:
        verbose_name = "Layer configuration"


class Layer_Style(models.Model):
    layer = models.OneToOneField(Layer, on_delete=models.PROTECT)
    colorfill = ColorField(db_column='colorFill', max_length=15, blank=True, null=True)  # Field name made lowercase.
    colorstrk = ColorField(db_column='colorStrk', max_length=15, blank=True, null=True)  # Field name made lowercase.
    width = models.FloatField()
    icon = models.ImageField(null=True,blank=True)
    style=models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Layer styling"

class Layer_Field(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    field = models.CharField(max_length=30, blank=True)
    display_name = models.CharField(max_length=30, blank=True,null=True)
    popup_title = models.BooleanField(default=False)
    show_in_popup=models.BooleanField(default=True)
    show_as_label=models.BooleanField(default=False)
    show_in_details=models.BooleanField(default=False)

    def __str__(self):  # __unicode__ for Python
        return self.field
    class Meta:
        verbose_name = "Layer Field configuration"

@receiver(post_save, sender=Layer)
def create_or_update_layer_field(sender, instance, created, **kwargs):
    URL = settings.SSL+"://"+settings.GEOSERVER_USERNAME+":"+settings.GEOSERVER_PASSWORD+"@"+settings.GEOSERVER_PATH+"/" + instance.layer_service.split(':')[0] + "/ows?service=WFS&version=1.0.0&request=DescribeFeatureType&typeName=" + instance.layer_service + "&outputFormat=application%2Fjson"
    r = requests.get(url=URL)
    data = r.json()
    properties = (data['featureTypes'][0]['properties'])
    if created:
        for field in properties:
            layerfield=Layer_Field.objects.create(layer=instance,field=field['name'])
            layerfield.save()
    else:
        current_fields=Layer_Field.objects.all().values_list('field', flat=True)
        removable_list=current_fields
        addable_list=properties
        for curfield in current_fields:
            for field in properties:
                if(field['name']==curfield):
                    removable_list=removable_list.exclude(field=curfield)
                    addable_list.remove(field)
                    break
                else:
                    continue  # only executed if the inner loop did NOT break
                break
        for field in removable_list:
            Layer_Field.objects.filter(field=field,layer=instance).delete()
        for field in addable_list:
            layerfield=Layer_Field.objects.create(layer=instance,field=field['name'])
            layerfield.save()

class Basemap(models.Model):
    layer_title = models.CharField(max_length=30,choices=(('OSM','OSM'),('DRONE','DRONE'),('SATELLITE','SATELLITE')),unique=True)
    url = models.CharField(max_length=250)
    visibility = models.BooleanField(default=True)
    opacity=IntegerRangeField(min_value=0, max_value=100,default=100)
    index = models.PositiveSmallIntegerField(default=basemap_index)

    def __str__(self):  # __unicode__ for Python
        return self.layer_title

    class Meta:
        verbose_name = "Basemap"

class Map_Config(models.Model):
    user=models.OneToOneField(User, on_delete=models.PROTECT)
    zoom = IntegerRangeField(min_value=1, max_value=25,default=5)
    default_basemap= models.ForeignKey(Basemap, on_delete=models.PROTECT)
    base_filter = models.ForeignKey(Layer, on_delete=models.PROTECT)

    def __str__(self):  # __unicode__ for Python
        return self.default_basemap.layer_title

    class Meta:
        verbose_name="Map Configuration"


from django.contrib.auth.models import User



class advancesearch_distinct_list(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,model_name,field_name,data_type):
        current_model = None
        for model in apps.get_models():
            if (model.__name__ == model_name):
                current_model = model
        field_value_list = []
        if(request.user.is_superuser):
            field_value_list = current_model.objects.filter().order_by(field_name).values_list(field_name, flat=True).distinct()
        elif(request.user.user_extension.functional_body.id==1):#LSGI
            field_value_list = current_model.objects.filter().order_by(field_name).values_list(field_name, flat=True).distinct()
        if(data_type=='ForeignKey'):
            #print(dir(current_model._meta.get_field(field_name)))
            model=current_model._meta.get_field(field_name).related_model
            lst=model.objects.filter(id__in=field_value_list).all()
            field_value_list= [it.__str__() for it in lst]
        else:
            field_value_list = [str(x) for x in field_value_list]
        return Response(field_value_list)

class advancesearch_result(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        obj=data['obj']
        # data={
        # "parent_model":"Property",
        # "obj":[{"attribute":"age","op":"__gt","value":"10","model_name":"Member_Details","join_op":null},
        #      {"attribute":"new_pro_id","op":"__gt","value":"10","model_name":"Property","join_op":"or"},
        #      {"attribute":"consumer_no","op":"","value":"123","model_name":"Property_Other_Details","join_op":"or"},
        #      {"attribute": "new_pro_id", "op": "__lt", "value": "13", "model_name": "Property","join_op": "or"}]
        # }

        # iterate through all model until parent model match with model
        current_model = None
        parent_model=data['parent_model']
        for model in apps.get_models():
            if (model.__name__ == parent_model):
                current_model=model
        data_list=current_model.objects.none()
        for item in obj:
            condition = {}
            is_not_equal=False
            if(item['op']=='equal' or item['op']=='='):
                item['op']=''
            elif(item['op']=='notequal' or item['op']=='!='):
                item['op'] = ''
                is_not_equal=True
            condition[item['attribute'] + item['op']] = item['value']
            data_list_temp = set([])
            parent_model_field = (parent_model.lower()) + "_id"
            if(item['model_name']!=item['parent_model']):
                for rel_model in (current_model._meta.related_objects):
                    if (rel_model.related_model.__name__ == item['model_name']):
                        if(is_not_equal):
                            data=rel_model.related_model.objects.filter(~Q(**condition)).all()
                            #data_list_temp=(rel_model.related_model.objects.filter(**condition,property__localbody__id=1).values_list(parent_model_field,flat=True).distinct())
                            data_list_temp = (rel_model.related_model.objects.filter(~Q(**condition)).values_list(parent_model_field, flat=True).distinct())
                        else:
                            data = rel_model.related_model.objects.filter(**condition).all()
                            # data_list_temp=(rel_model.related_model.objects.filter(**condition,property__localbody__id=1).values_list(parent_model_field,flat=True).distinct())
                            data_list_temp = (rel_model.related_model.objects.filter(**condition).values_list(parent_model_field,flat=True).distinct())

                        # for i in data:
                        #     data_list_temp.add(getattr(i,(parent_model).lower()).id)
            else:
                if(is_not_equal):
                    data=current_model.objects.filter(~Q(**condition)).all()
                    data_list_temp = current_model.objects.filter(~Q(**condition)).values_list('id',flat=True).distinct()
                else:
                    data = current_model.objects.filter(**condition).all()
                    data_list_temp = current_model.objects.filter(**condition).values_list('id', flat=True).distinct()

                # data_list_temp=current_model.objects.filter(**condition,localbody__id=1).values_list('id',flat=True).distinct()
                # # for i in data:
                #     data_list_temp.add(i.id)
            if (item['join_op']=='and'):
                data_list=data_list.intersection(data_list_temp)
            elif (item['join_op'] == 'or'):
                data_list=data_list.union(data_list_temp)
            elif (item['join_op']==None):
                data_list=data_list_temp
        return Response(data_list)

