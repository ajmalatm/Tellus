from django.db import models
from django.contrib.gis.db import models
import datetime

Floors = [
    ('1', 'Floor 1'),
    ('2', 'Floor 2'),
    ('3', 'Floor 3'),
    ('4', 'Floor 4'),
    ('5', 'Floor 5'),
    ('6', 'Floor 6'),
    ('7', 'Floor 7'),
    ('8', 'Floor 8'),
    ('9', 'Floor 9'),
    ('10', 'Floor 10'),
    ('11', 'Floor 11'),
    ('12', 'Floor 12'),
    ('13', 'Floor 13'),
    ('14', 'Floor 14'),
    ('15', 'Floor 15'),
    ('16', 'Floor 16'),
    ('17', 'Floor 17'),
    ('18', 'Floor 18'),
    ('19', 'Floor 19'),
    ('20', 'Floor 20'),
    ('21', 'Floor 21'),
    ('22', 'Floor 22'),
    ('23', 'Floor 23'),
    ('24', 'Floor 24'),
    ('25', 'Floor 25'),
]


BLDGSTATUS = [
    ('1', 'Owned'),
    ('2', 'Rented'),
]

YESNO = [
    ('1', 'yes'),
    ('2', 'no'),
]

class District1(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    gid = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=28, blank=True, null=True)
    state = models.CharField(max_length=24, blank=True, null=True)
    st_cen_cd = models.IntegerField(blank=True, null=True)
    dt_cen_cd = models.IntegerField(blank=True, null=True)
    censuscode = models.FloatField(blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.district

    class Meta:
        db_table = 'district1'
        verbose_name_plural = "District"


class Localbody(models.Model):
    id = models.BigAutoField(primary_key=True)
    district =  models.ForeignKey(District1,on_delete=models.CASCADE)
    localbody_id = models.CharField(max_length=50,unique=True)
    localbody = models.CharField(max_length=50)

    def __str__(self):  # __unicode__ for Python
        return self.localbody

    class Meta:
        verbose_name_plural = "Localbody"
        unique_together = ('district', 'localbody',)


class Villages_Localbody(models.Model):
    id = models.AutoField(primary_key=True)
    localbody = models.ForeignKey(Localbody,on_delete=models.CASCADE)
    village_nm = models.CharField(unique=True, max_length=30, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.village_nm

    class Meta:
        verbose_name_plural = "Villages"


class Ward(models.Model):
    id = models.AutoField(primary_key=True)
    localbody = models.ForeignKey(Localbody,on_delete=models.CASCADE)
    ward_no = models.IntegerField()
    ward_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.ward_name

    class Meta:
        verbose_name_plural = "Ward"

class Postoffice(models.Model):
    id = models.BigAutoField(primary_key=True)
    postoffice = models.CharField(max_length=250)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.postoffice

    class Meta:
        verbose_name_plural = "Postoffice"
#
class Postoffice_Localbody(models.Model):
    id = models.BigAutoField(primary_key=True)
    postoffice = models.ForeignKey(Postoffice,on_delete=models.CASCADE)
    localbody =  models.ForeignKey(Localbody,on_delete=models.CASCADE)

    def __str__(self):  # __unicode__ for Python
        return self.postoffice+"-"+self.localbody

    class Meta:
        verbose_name_plural = "Postoffice_Localbody"



class Building_Usage(models.Model):
    id = models.BigAutoField(primary_key=True)
    bldg_usage = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.bldg_usage

    class Meta:
        verbose_name_plural = "Building Usage"


class Building_Zone(models.Model):
    id = models.AutoField(primary_key=True)
    bldg_zone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.bldg_zone

    class Meta:
        verbose_name_plural = "Zone"




class Floor_Type(models.Model):
    id = models.AutoField(primary_key=True)
    floor_type = models.CharField(max_length=50, blank=True, null=True)
    floor_type_ml = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.floor_type

    class Meta:
        verbose_name_plural = "Floor Type"



# def ward_list():
#     WARDS=[]
#     for ward in Ward.objects.all():
#         WARDS.append((ward.ward_no,ward.ward_no))
#     WARDS=tuple(WARDS)
#     return WARDS

class Road_Type(models.Model):
    id = models.AutoField(primary_key=True)
    road_type_category=models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4)],blank=True, null=True)
    road_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.road_type

    class Meta:
        verbose_name_plural = "Road Type"

class Formsix(models.Model):
    id = models.AutoField(primary_key=True)
    bldg_stats = models.CharField(max_length=20, choices=BLDGSTATUS,default='1')
    any_institute = models.CharField(max_length=22, choices=YESNO,default='1')
    bldg_usage = models.ForeignKey(Building_Usage,on_delete=models.CASCADE)
    bldg_zone = models.ForeignKey(Building_Zone,on_delete=models.CASCADE)
    centrl_ac = models.CharField(max_length=22, choices=YESNO,default='1')
    district = models.CharField(max_length=10, blank=True, null=True)
    cellar_area = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    flr_grnd = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    higher_floor_gt=models.CharField(max_length=22, choices=YESNO,default='2')
    other_flr_type=models.CharField(max_length=22, choices=YESNO,default='1')
    near_rd = models.CharField(max_length=81, blank=True, null=True)
    new_pro_id = models.CharField(max_length=25, unique=True)
    noofyears = models.IntegerField(blank=True, null=True)
    old_pro_id = models.CharField(max_length=24,unique=True, blank=True, null=True)
    place_nm = models.CharField(max_length=48, blank=True, null=True)
    postoffice = models.CharField(max_length=23, blank=True, null=True)
    rd_typ = models.CharField(max_length=9, blank=True, null=True)
    rd_width = models.ForeignKey(Road_Type,on_delete=models.CASCADE)
    roof_concrete = models.CharField(max_length=22, choices=YESNO,default='1')
    roof_concrete_per = models.IntegerField(default=100)
    roof_other = models.CharField(max_length=22, choices=YESNO,default='2')
    roof_other_per = models.IntegerField(default=0)
    unique_id = models.CharField(max_length=24, blank=True, null=True)
    ward_nm = models.CharField(max_length=24, blank=True, null=True)
    ward_no_id = models.ForeignKey(Ward,on_delete=models.CASCADE,related_name='newward')
    ward_no = models.IntegerField(blank=True, null=True)
    old_ward_nm = models.CharField(max_length=24, blank=True, null=True)
    old_ward_no_id = models.ForeignKey(Ward,on_delete=models.CASCADE,related_name='oldward')
    old_ward_no = models.IntegerField(blank=True, null=True)
    year_const = models.IntegerField(default=2020)
    state = models.CharField(max_length=32, blank=True, null=True)
    lsgd = models.ForeignKey(Localbody,on_delete=models.CASCADE)
    structural_change = models.CharField(max_length=22, choices=YESNO, default='2')
    country = models.CharField(max_length=32, blank=True, null=True)
    geom = models.PointField(srid=4326, blank=True, null=True)

    @property
    def get_total_area(self):
        floors=(self.floor_prop_area_set.all())
        base = self.cellar_area+self.flr_grnd
        total =base+(sum([floor.floor_area for floor in floors]))
        return total

    def save(self, *args, **kwargs):
        new_ward=Ward.objects.get(id=self.ward_no_id.id)
        old_ward = Ward.objects.get(id=self.old_ward_no_id.id)
        self.ward_no = new_ward.ward_no
        self.old_ward_no=old_ward.ward_no
        self.ward_nm = new_ward.ward_name
        self.old_ward_nm = old_ward.ward_name
        self.district=self.lsgd.district.district
        super(Formsix, self).save(*args, **kwargs)

    def __str__(self):  # __unicode__ for Python
        return self.new_pro_id

    class Meta:
        verbose_name_plural = "Property"




class Floor_Prop_Area(models.Model):
    proprty = models.ForeignKey(Formsix,on_delete=models.CASCADE)
    floor_no = models.CharField(max_length=33,choices=Floors,default='1')
    floor_area=models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.floor_no

    class Meta:
        verbose_name_plural = "Floor Area"
        unique_together = ('proprty', 'floor_no',)

class Establishment(models.Model):
    proprty = models.OneToOneField(Formsix, on_delete=models.CASCADE)
    estb_email = models.CharField(max_length=30, blank=True, null=True)
    estb_l_phn = models.CharField(max_length=11, blank=True, null=True)
    estb_mob = models.CharField(max_length=11, blank=True, null=True)
    estb_nm = models.CharField(max_length=78, blank=True, null=True)
    estb_pin = models.CharField(max_length=4, blank=True, null=True)
    estb_post = models.CharField(max_length=30, blank=True, null=True)
    estb_typ = models.CharField(max_length=50, blank=True, null=True)
    estb_yr = models.IntegerField(blank=True, null=True)
    inchrg_nm = models.CharField(max_length=53, blank=True, null=True)
    inchrg_pst = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.estb_nm

    class Meta:
        verbose_name_plural = "Establishment"


class Owner_Details(models.Model):
    proprty = models.ForeignKey(Formsix,on_delete=models.CASCADE)
    ownr_email = models.CharField(max_length=33, blank=True, null=True)
    ownr_house = models.CharField(max_length=77, blank=True, null=True)
    ownr_l_phn = models.CharField(max_length=13, blank=True, null=True)
    ownr_mob = models.CharField(max_length=13, blank=True, null=True)
    ownr_nm = models.CharField(max_length=125, blank=True, null=True)
    ownr_occup = models.CharField(max_length=27, blank=True, null=True)
    ownr_pin = models.CharField(max_length=14, blank=True, null=True)
    ownr_place = models.CharField(max_length=47, blank=True, null=True)
    ownr_post = models.CharField(max_length=30, blank=True, null=True)
    ownr_surno = models.CharField(max_length=37, blank=True, null=True)
    ownr_vlage = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.ownr_nm

    class Meta:
        verbose_name_plural = "Owner Details"

class Tenent_Details(models.Model):
    proprty = models.ForeignKey(Formsix, on_delete=models.CASCADE)
    tnt_email = models.CharField(max_length=36, blank=True, null=True)
    tnt_hsname = models.CharField(max_length=57, blank=True, null=True)
    tnt_l_phn = models.CharField(max_length=12, blank=True, null=True)
    tnt_mob = models.CharField(max_length=12, blank=True, null=True)
    tnt_native = models.CharField(max_length=30, blank=True, null=True)
    tnt_nm = models.CharField(max_length=99, blank=True, null=True)
    tnt_pincod = models.CharField(max_length=6, blank=True, null=True)
    tnt_place = models.CharField(max_length=30, blank=True, null=True)
    tnt_pstoff = models.CharField(max_length=32, blank=True, null=True)
    tnt_sur_no = models.CharField(max_length=21, blank=True, null=True)
    tnt_vilage = models.CharField(max_length=30, blank=True, null=True)
    rent_amnt = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.tnt_nm

    class Meta:
        verbose_name_plural = "Tenent Details"

class Tax_Details(models.Model):
    proprty = models.ForeignKey(Formsix, on_delete=models.CASCADE)
    tax_bil_no = models.CharField(max_length=35, blank=True, null=True)
    taxpaid_dt = models.DateField()
    taxpaid_yr = models.IntegerField(blank=True, null=True)
    tax_amnt = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    asses_no = models.IntegerField(blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.tax_bil_no

    class Meta:
        verbose_name_plural = "Tax Details"
        unique_together = ('proprty', 'taxpaid_yr',)



class Roof_Type(models.Model):
    id = models.AutoField(primary_key=True)
    roof_type = models.CharField(max_length=50, blank=True, null=True)
    roof_type_ml = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python
        return self.roof_type

    class Meta:
        verbose_name_plural = "Roof Type"

