import pprint
from django.db import connection
from estimation.estimation import estimate_plan


def parse_plan(plan, queryset, depth=0):
    sub_plans = [parse_plan(sub_plan, queryset, depth=depth + 1) for sub_plan in plan.get('Plans', [])]

    parsed_plan = {
        'node_type': plan.get('Node Type'),
        'table': plan.get('Relation Name', None),
        'filter': plan.get('Filter', None),
        'rows_estimate': plan.get('Plan Rows'),
        'rows_actual': plan.get('Actual Rows'),
        'sub_plans': sub_plans,
    }

    parsed_plan['rows_django_estimate'] = estimate_plan(parsed_plan, queryset)

    return parsed_plan

def cardinality_estimation_wrapper(queryset):
    def inner (execute, sql, params, many, context):
        # Pop the current wrappers so we can make queries without triggering it
        current_wrappers = connection.execute_wrappers
        connection.execute_wrappers = []

        execute(f"EXPLAIN (FORMAT JSON, ANALYZE) {sql}", params, many, context)
        explain_json = context['cursor'].fetchone()[0][0]['Plan']
        parsed_plan = parse_plan(explain_json, queryset)

        print()
        pprint.pprint(parsed_plan)

        # Add the wrappers back
        connection.execute_wrappers = current_wrappers

        return execute(sql, params, many, context)

    return inner
