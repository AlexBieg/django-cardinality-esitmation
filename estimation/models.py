from django.db import models


class AkaName(models.Model):
    person_id = models.ForeignKey('Name', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, blank=True, null=True)
    imdb_index = models.CharField(max_length=3, blank=True, null=True)
    name_pcode_cf = models.CharField(max_length=11, blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=11, blank=True, null=True)
    surname_pcode = models.CharField(max_length=11, blank=True, null=True)
    md5sum = models.CharField(max_length=65, blank=True, null=True)

    class Meta:
        db_table = 'aka_name'


class AkaTitle(models.Model):
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True, null=True)
    imdb_index = models.CharField(max_length=4, blank=True, null=True)
    kind_id = models.ForeignKey('KindType', on_delete=models.CASCADE)
    production_year = models.IntegerField(blank=True, null=True)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)
    episode_of_id = models.IntegerField(blank=True, null=True)
    season_nr = models.IntegerField(blank=True, null=True)
    episode_nr = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=72, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'aka_title'


class CastInfo(models.Model):
    person_id = models.ForeignKey('Name', on_delete=models.CASCADE)
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE)
    person_role_id = models.ForeignKey('CharName', on_delete=models.CASCADE)
    note = models.CharField(max_length=1000, blank=True, null=True)
    nr_order = models.IntegerField(blank=True, null=True)
    role_id = models.ForeignKey('RoleType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cast_info'


class CharName(models.Model):
    name = models.CharField(max_length=1000)
    imdb_index = models.CharField(max_length=2, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    surname_pcode = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'char_name'


class CompCastType(models.Model):
    kind = models.CharField(max_length=32)

    class Meta:
        db_table = 'comp_cast_type'


class CompanyName(models.Model):
    name = models.CharField(max_length=1000)
    country_code = models.CharField(max_length=6, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    name_pcode_sf = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'company_name'


class CompanyType(models.Model):
    kind = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'company_type'


class CompleteCast(models.Model):
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE)
    subject_id = models.IntegerField()
    status_id = models.IntegerField()

    class Meta:
        db_table = 'complete_cast'


class InfoType(models.Model):
    info = models.CharField(max_length=32)

    class Meta:
        db_table = 'info_type'


class Keyword(models.Model):
    keyword = models.CharField(max_length=1000)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        db_table = 'keyword'


class KindType(models.Model):
    kind = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'kind_type'


class LinkType(models.Model):
    link = models.CharField(max_length=32)

    class Meta:
        db_table = 'link_type'


class MovieCompanies(models.Model):
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE)
    company_id = models.ForeignKey('CompanyName', on_delete=models.CASCADE)
    company_type_id = models.ForeignKey('CompanyType', on_delete=models.CASCADE)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'movie_companies'


class MovieInfo(models.Model):
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE)
    info_type_id = models.ForeignKey('InfoType', on_delete=models.CASCADE)
    info = models.CharField(max_length=1000)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'movie_info'


class MovieInfoIdx(models.Model):
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE)
    info_type_id = models.ForeignKey('InfoType', on_delete=models.CASCADE)
    info = models.CharField(max_length=1000)
    note = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'movie_info_idx'


class MovieKeyword(models.Model):
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE)
    keyword_id = models.ForeignKey('Keyword', on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_keyword'


class MovieLink(models.Model):
    movie_id = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='movies')
    linked_movie_id = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='linked_movies')
    link_type_id = models.ForeignKey('LinkType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_link'


class Name(models.Model):
    name = models.CharField(max_length=1000)
    imdb_index = models.CharField(max_length=9, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    name_pcode_cf = models.CharField(max_length=5, blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    surname_pcode = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'name'


class PersonInfo(models.Model):
    person_id = models.ForeignKey('Name', on_delete=models.CASCADE)
    info_type_id = models.ForeignKey('InfoType', on_delete=models.CASCADE)
    info = models.CharField(max_length=1000)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'person_info'


class RoleType(models.Model):
    role = models.CharField(max_length=32)

    class Meta:
        db_table = 'role_type'


class Title(models.Model):
    title = models.CharField(max_length=1000)
    imdb_index = models.CharField(max_length=5, blank=True, null=True)
    kind_id = models.ForeignKey('KindType', on_delete=models.CASCADE)
    production_year = models.IntegerField(blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)
    episode_of_id = models.IntegerField(blank=True, null=True)
    season_nr = models.IntegerField(blank=True, null=True)
    episode_nr = models.IntegerField(blank=True, null=True)
    series_years = models.CharField(max_length=49, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'title'
