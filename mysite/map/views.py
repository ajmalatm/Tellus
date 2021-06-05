from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import json
import requests
import xmltodict
from django.core import serializers as ser
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.


def masterTree(combinedTreeMaster,rootTree,groupTree):
        if(len(rootTree)>0):
            curroot = rootTree[len(rootTree)-1]
            if curroot not in combinedTreeMaster:
                combinedTreeMaster[curroot]={'layers':{},'groups':{}}
            combinedTreeMaster[curroot]['layers'] = groupTree[curroot]['layers'] if (curroot in groupTree) else []
            rootTree.pop()
            masterTree(combinedTreeMaster[curroot]['groups'], rootTree,groupTree)
        return combinedTreeMaster

def getRootTree(group,rootTree,dbGroups):
    group = dbGroups.get(group=group)
    if (group.parent_group is not None):
        rootTree.append(group.parent_group.group)
        getRootTree(group.parent_group,rootTree,dbGroups)
    return rootTree






class load_layers(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
        layerCollection = {}

        layers = Layer.objects.filter(visibility=True).order_by('-group__index','index').all()
        groupTree = {}
        combinedTreeMaster = {}
        for item in layers:
            if(item.group.group not in groupTree):
                groupTree[item.group.group]={'layers':[],'count':0}
            ly=json.loads((ser.serialize('json', [item, ])))
            URL = settings.SSL+"://"+settings.GEOSERVER_USERNAME+":"+settings.GEOSERVER_PASSWORD+"@"+settings.GEOSERVER_PATH+"/wfs?request=GetFeature&typeName=" + item.layer_service + "&version=1.1.0&resultType=hits"
            r = requests.get(url=URL)


            # print('-----------------',r.content)
            # o = xmltodict.parse(r.content)
            # out = (json.dumps(o))
            # ly[0]['count'] = ((json.loads(out))['wfs:FeatureCollection']['@numberOfFeatures'])
            ly[0]['count'] ="10"
            ly[0]['style']=None
            ly[0]['popuptemplate']={}
            titlelist=[]
            labellist=[]
            template = {}
            attributes={}
            for field in item.layer_field_set.values():
                fieldname=field['field']
                display_name=field['display_name'] if (field['display_name'] is not None) else field['field']
                if(field['show_in_popup']):
                    attributes[fieldname]={'title': display_name}
                if (field['popup_title']):
                    titlelist.append(fieldname)
                if (field['show_as_label']):
                    labellist.append(field['field'])
            print(labellist)
            template['title']=titlelist
            template['attributes'] = attributes
            ly[0]['popuptemplate']=template
            ly[0]['label']=labellist

            try:
                ly[0]['style'] = json.loads((ser.serialize('json', [item.layer_style,],fields=('colorfill','colorstrk','width','icon'))))[0]['fields'] if  json.loads((ser.serialize('json', [item.layer_style, ]))) is not None else None
            except:
                pass

            groupTree[item.group.group]['layers'].append(ly)
            # p=requests.get(url='http://admin:geoserver@localhost:8080/geoservernew/rest/styles/burg.sld')
            # oo = xmltodict.parse(p.content)
            # oo=(oo['StyledLayerDescriptor']['NamedLayer']['UserStyle']['FeatureTypeStyle']['Rule']['PointSymbolizer']['Graphic'])
            # size=oo['Size']['ogc:Literal'] if 'ogc:Literal' in oo['Size'] else oo['Size']
            # fill=oo['Mark']['Fill']['CssParameter']['#text'] if '#text' in oo['Mark']['Fill']['CssParameter'] else oo['Mark']['Fill']['CssParameter']['ogc:Literal']
            # # print(size,fill)



        dbGroups = Layergroup.objects.all()
        for group in groupTree.keys():
            rootTree = [group]
            getRootTree(group,rootTree,dbGroups)
            root=rootTree[len(rootTree)-1]
            groupTree[group]['root']=root
            parent=rootTree[0] if len(rootTree)>0 else None
            groupTree[group]['parent']=parent
            if(root not in combinedTreeMaster):
                combinedTreeMaster[root]={'layers':{},'groups':{}}
            if(group in combinedTreeMaster):
                combinedTreeMaster[group]['layers']=groupTree[group]['layers']
            else:
                masterTree(combinedTreeMaster,rootTree,groupTree)




        # layers = LayerSerializer((Layer.objects.filter(visibility=True).order_by('index')), many=True)
        # groups = Layergroup.objects.filter(visibility=True, layer__isnull=False).distinct().order_by('index')

        base_maps = BasemapSerializer((Basemap.objects.filter(visibility=True).order_by('index')), many=True)
        layerCollection['Basemap'] = []
        for map in base_maps.data:
            layerCollection['Basemap'].append(map)

        # for group in groups:
        #     layerCollection[group.group] = []
        # for layer in layers.data:
        #     key = groups.get(pk=layer['group']).group
        #     layer['url']='http://admin:geoserver@localhost:8080/geoservernew/'+layer['layer_service'].split(':')[0]+'/ows?service=WFS&version=1.0.0&request=GetFeature&typeName='+layer['layer_service']+'&outputFormat=application%2Fjson'
        #
        #     #layer['url'] = 'http://admin:geoserver@localhost:8080/geoservernew/' + layer['layer_service'].split(':')[0] + '/wms?service=WMS&version=1.1.0&request=GetMap&layers=' + layer['layer_service'] + '&bbox=' + layer['bbox'] + '&width=1700&height=700&srs=' + layer['crs'] + '&styles=&format=application/openlayers'
        #     layerCollection[key].append(layer)
        combinedTreeMaster['Basemap']=layerCollection['Basemap']
        return Response(combinedTreeMaster)


class map_configuration(APIView):
    def get(self, request):
        #config = ser.serialize('json', Map_Config.objects.all())
        config1 = {}
        con = Map_Config.objects.first()
        if (con is not None):
            config1['zoom'] = con.zoom;
            config1['base_filter'] = []
            config1['base_filter_layer'] = con.base_filter.layer_service;
            fields = (Layer_Field.objects.filter(layer=con.base_filter))
            for f in fields:
                config1['base_filter'].append(f.field)
        #config =MapConfigurationSerializer(Map_Config.objects.all(), many=True)
        return Response(config1)
