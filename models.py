# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AkaName(models.Model):
    id = models.IntegerField(primary_key=True)
    person_id = models.IntegerField()
    name = models.CharField(max_length=-1, blank=True, null=True)
    imdb_index = models.CharField(max_length=3, blank=True, null=True)
    name_pcode_cf = models.CharField(max_length=11, blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=11, blank=True, null=True)
    surname_pcode = models.CharField(max_length=11, blank=True, null=True)
    md5sum = models.CharField(max_length=65, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aka_name'


class AkaTitle(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=-1, blank=True, null=True)
    imdb_index = models.CharField(max_length=4, blank=True, null=True)
    kind_id = models.IntegerField()
    production_year = models.IntegerField(blank=True, null=True)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)
    episode_of_id = models.IntegerField(blank=True, null=True)
    season_nr = models.IntegerField(blank=True, null=True)
    episode_nr = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=72, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aka_title'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CastInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    person_id = models.IntegerField()
    movie_id = models.IntegerField()
    person_role_id = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=-1, blank=True, null=True)
    nr_order = models.IntegerField(blank=True, null=True)
    role_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cast_info'


class CharName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1)
    imdb_index = models.CharField(max_length=2, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    surname_pcode = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'char_name'


class CompCastType(models.Model):
    id = models.IntegerField(primary_key=True)
    kind = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'comp_cast_type'


class CompanyName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1)
    country_code = models.CharField(max_length=6, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    name_pcode_sf = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_name'


class CompanyType(models.Model):
    id = models.IntegerField(primary_key=True)
    kind = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_type'


class CompleteCast(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField(blank=True, null=True)
    subject_id = models.IntegerField()
    status_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'complete_cast'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InfoType(models.Model):
    id = models.IntegerField(primary_key=True)
    info = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'info_type'


class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=-1)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keyword'


class KindType(models.Model):
    id = models.IntegerField(primary_key=True)
    kind = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kind_type'


class LinkType(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'link_type'


class MovieCompanies(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField()
    company_id = models.IntegerField()
    company_type_id = models.IntegerField()
    note = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_companies'


class MovieInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField()
    info_type_id = models.IntegerField()
    info = models.CharField(max_length=-1)
    note = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_info'


class MovieInfoIdx(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField()
    info_type_id = models.IntegerField()
    info = models.CharField(max_length=-1)
    note = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_info_idx'


class MovieKeyword(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField()
    keyword_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'movie_keyword'


class MovieLink(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField()
    linked_movie_id = models.IntegerField()
    link_type_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'movie_link'


class Name(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1)
    imdb_index = models.CharField(max_length=9, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    name_pcode_cf = models.CharField(max_length=5, blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    surname_pcode = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'name'


class PersonInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    person_id = models.IntegerField()
    info_type_id = models.IntegerField()
    info = models.CharField(max_length=-1)
    note = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person_info'


class RoleType(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'role_type'


class Title(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=-1)
    imdb_index = models.CharField(max_length=5, blank=True, null=True)
    kind_id = models.IntegerField()
    production_year = models.IntegerField(blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)
    episode_of_id = models.IntegerField(blank=True, null=True)
    season_nr = models.IntegerField(blank=True, null=True)
    episode_nr = models.IntegerField(blank=True, null=True)
    series_years = models.CharField(max_length=49, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'title'
