import inspect
from django.db import connection, models
from django.contrib.postgres.fields import ArrayField

from estimation.query_wrapper_utils import cardinality_estimation_wrapper

CHAR_MATCHES = {'"': '"'}


def parse_pg_anyarray(val):
    """
    Postgres has a psuedo-type called anyarray. According to their documentation this cannot be used as a column type.
    It should only be used as a function param type. They didn't follow their rules. This function does it's best to
    parse the string we get back from a column of that type to a list.
    """
    # Remove the curly braces
    val = val[1:-1]

    ret = ['']

    open_stack = []

    prev_char = None

    for char in val:
        if open_stack and char in CHAR_MATCHES.keys() and CHAR_MATCHES[char] == open_stack[-1] and prev_char != '\\':
            open_stack.pop()
            continue

        if char in CHAR_MATCHES.values() and prev_char != '\\':
            open_stack.append(char)
            continue

        if char == ',' and not open_stack:
            ret.append('')
            continue

        ret[-1] = ret[-1] + char

        prev_char = char

    return ret


class AnyField(models.Field):
    pass


class AnyArrayField(ArrayField):
    def to_python(self, value):
        return super().to_python(value)

    def from_db_value(self, value, expression, connection):
        return parse_pg_anyarray(value) if value else None


"""
Postgres Specific Models. Let's us grab the table/column stats
"""
class PgColumnStats(models.Model):
    tablename = models.ForeignKey('PgTableStats', on_delete=models.CASCADE, db_column='tablename')
    attname = models.CharField(max_length=200, primary_key=True)
    null_frac = models.FloatField()
    n_distinct = models.FloatField()
    most_common_vals = AnyArrayField(base_field=models.CharField(max_length=200))
    most_common_freqs = ArrayField(base_field=models.FloatField())
    histogram_bounds = AnyArrayField(base_field=models.CharField(max_length=200))

    class Meta:
        db_table = 'pg_stats'
        managed = False


class PgTableStats(models.Model):
    relid = models.IntegerField()
    relname = models.CharField(max_length=200, primary_key=True)
    row_count = models.IntegerField(db_column='n_live_tup')

    class Meta:
        db_table = 'pg_stat_all_tables'
        managed = False


"""
Estimation Utils
"""
def for_all_methods(decorator):
    def decorate(cls):
        for name, fn in inspect.getmembers(cls, inspect.isfunction):
            if not name.startswith('__'):
                setattr(cls, name, decorator(fn))
        return cls
    return decorate

def execute_decorator(func):
    def wrapper(self, *args, **kwargs):
        with connection.execute_wrapper(cardinality_estimation_wrapper(self)):
            return func(self, *args, **kwargs)

    return wrapper


@for_all_methods(execute_decorator)
class EstimationQuerySet(models.QuerySet):
    pass

class EstimationModel(models.Model):
    objects = EstimationQuerySet.as_manager()

    class Meta:
        abstract = True

"""
IMDB models
"""
class AkaName(EstimationModel):
    person = models.ForeignKey('Name', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, blank=True, null=True)
    imdb_index = models.CharField(max_length=3, blank=True, null=True)
    name_pcode_cf = models.CharField(max_length=11, blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=11, blank=True, null=True)
    surname_pcode = models.CharField(max_length=11, blank=True, null=True)
    md5sum = models.CharField(max_length=65, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'aka_name'


class AkaTitle(EstimationModel):
    movie = models.ForeignKey('Title', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True, null=True)
    imdb_index = models.CharField(max_length=4, blank=True, null=True)
    kind = models.ForeignKey('KindType', on_delete=models.CASCADE)
    production_year = models.IntegerField(blank=True, null=True)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)
    episode_of_id = models.IntegerField(blank=True, null=True)
    season_nr = models.IntegerField(blank=True, null=True)
    episode_nr = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=72, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'aka_title'


class CastInfo(EstimationModel):
    person = models.ForeignKey('Name', on_delete=models.CASCADE)
    movie = models.ForeignKey('Title', on_delete=models.CASCADE)
    person_role = models.ForeignKey('CharName', on_delete=models.CASCADE)
    note = models.CharField(max_length=1000, blank=True, null=True)
    nr_order = models.IntegerField(blank=True, null=True)
    role = models.ForeignKey('RoleType', on_delete=models.CASCADE)

    class Meta(EstimationModel.Meta):
        db_table = 'cast_info'


class CharName(EstimationModel):
    name = models.CharField(max_length=1000)
    imdb_index = models.CharField(max_length=2, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    surname_pcode = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'char_name'


class CompCastType(EstimationModel):
    kind = models.CharField(max_length=32)

    class Meta(EstimationModel.Meta):
        db_table = 'comp_cast_type'


class CompanyName(EstimationModel):
    name = models.CharField(max_length=1000)
    country_code = models.CharField(max_length=6, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    name_pcode_sf = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'company_name'


class CompanyType(EstimationModel):
    kind = models.CharField(max_length=32, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'company_type'


class CompleteCast(EstimationModel):
    movie = models.ForeignKey('Title', on_delete=models.CASCADE)
    subject_id = models.IntegerField()
    status_id = models.IntegerField()

    class Meta(EstimationModel.Meta):
        db_table = 'complete_cast'


class InfoType(EstimationModel):
    info = models.CharField(max_length=32)

    class Meta(EstimationModel.Meta):
        db_table = 'info_type'


class Keyword(EstimationModel):
    keyword = models.CharField(max_length=1000)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'keyword'


class KindType(EstimationModel):
    kind = models.CharField(max_length=15, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'kind_type'


class LinkType(EstimationModel):
    link = models.CharField(max_length=32)

    class Meta(EstimationModel.Meta):
        db_table = 'link_type'


class MovieCompanies(EstimationModel):
    movie = models.ForeignKey('Title', on_delete=models.CASCADE)
    company = models.ForeignKey('CompanyName', on_delete=models.CASCADE)
    company_type = models.ForeignKey('CompanyType', on_delete=models.CASCADE)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'movie_companies'


class MovieInfo(EstimationModel):
    movie = models.ForeignKey('Title', on_delete=models.CASCADE)
    info_type = models.ForeignKey('InfoType', on_delete=models.CASCADE)
    info = models.CharField(max_length=1000)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'movie_info'


class MovieInfoIdx(EstimationModel):
    movie = models.ForeignKey('Title', on_delete=models.CASCADE)
    info_type = models.ForeignKey('InfoType', on_delete=models.CASCADE)
    info = models.CharField(max_length=1000)
    note = models.CharField(max_length=1, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'movie_info_idx'


class MovieKeyword(EstimationModel):
    movie = models.ForeignKey('Title', on_delete=models.CASCADE)
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE)

    class Meta(EstimationModel.Meta):
        db_table = 'movie_keyword'


class MovieLink(EstimationModel):
    movie = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='movies')
    linked_movie = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='linked_movies')
    link_type = models.ForeignKey('LinkType', on_delete=models.CASCADE)

    class Meta(EstimationModel.Meta):
        db_table = 'movie_link'


class Name(EstimationModel):
    name = models.CharField(max_length=1000)
    imdb_index = models.CharField(max_length=9, blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    name_pcode_cf = models.CharField(max_length=5, blank=True, null=True)
    name_pcode_nf = models.CharField(max_length=5, blank=True, null=True)
    surname_pcode = models.CharField(max_length=5, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'name'


class PersonInfo(EstimationModel):
    person = models.ForeignKey('Name', on_delete=models.CASCADE)
    info_type = models.ForeignKey('InfoType', on_delete=models.CASCADE)
    info = models.CharField(max_length=1000)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'person_info'


class RoleType(EstimationModel):
    role = models.CharField(max_length=32)

    class Meta(EstimationModel.Meta):
        db_table = 'role_type'


class Title(EstimationModel):
    title = models.CharField(max_length=1000)
    imdb_index = models.CharField(max_length=5, blank=True, null=True)
    kind = models.ForeignKey('KindType', on_delete=models.CASCADE)
    production_year = models.IntegerField(blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    phonetic_code = models.CharField(max_length=5, blank=True, null=True)
    episode_of_id = models.IntegerField(blank=True, null=True)
    season_nr = models.IntegerField(blank=True, null=True)
    episode_nr = models.IntegerField(blank=True, null=True)
    series_years = models.CharField(max_length=49, blank=True, null=True)
    md5sum = models.CharField(max_length=32, blank=True, null=True)

    class Meta(EstimationModel.Meta):
        db_table = 'title'
