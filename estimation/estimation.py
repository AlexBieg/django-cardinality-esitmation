from typing import Tuple, Type
from estimation import models

def lte_histogram_selectivity(value, histogram):
    lt_buckets = sum(bucket <= value for bucket in histogram)

    return lt_buckets / len(histogram)

def get_model_from_table(table_name: str) -> Type['models.EstimationModel']:
    words = table_name.split('_')
    model_name = ''.join(word.title() for word in words)

    return getattr(models, model_name)

def get_stats_from_table(table_name) -> Tuple['models.PgTableStats', dict[str, 'models.PgColumnStats']]:
    table_stats = models.PgTableStats.objects.get(relname=table_name)
    column_stats = models.PgColumnStats.objects.filter(tablename=table_name).in_bulk()

    return table_stats, column_stats


def estimate_seq_scan(queryset, table, filter):
    model = get_model_from_table(table)
    table_stats, column_stats = get_stats_from_table(table)

    if not filter:
        return table_stats.row_count


    django_filters = queryset._has_filters()

    for f in django_filters.children:
        lhs = f.lhs
        rhs = f.rhs

        filter_model = get_model_from_table(lhs.alias)

        if filter_model == model:
            sel = lte_histogram_selectivity(rhs, column_stats[lhs.field.attname].histogram_bounds)
            est_rows = table_stats.row_count * sel
            print(sel)


    return 1



NODE_TYPE_ESTIMATION = {
    'Seq Scan': estimate_seq_scan,
}

def estimate_plan(plan, queryset):
    try:
        return NODE_TYPE_ESTIMATION[plan['node_type']](queryset, plan['table'], plan['filter'])
    except KeyError as exc:
        return float('inf')
