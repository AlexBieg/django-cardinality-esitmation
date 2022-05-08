from collections import deque
import pprint
from django.db import connection


def parse_plan(plan, depth=0):
    data = {
        'node_type': plan['Node Type'],
        'plan_rows': plan['Plan Rows'],
        'actual_rows': plan['Actual Rows'],
        'relation_name': plan.get('Relation Name', 'NO RELATION'),
        'sub_plans': [parse_plan(sub_plan, depth=depth+1) for sub_plan in plan.get('Plans', [])],
    }

    return data

def cardinality_estimation_wrapper(execute, sql, params, many, context):
    explain_sql = f'EXPLAIN (FORMAT JSON, ANALYZE) {sql}'

    execute(explain_sql, params, many, context)
    explain_json = context['cursor'].fetchone()
    parsed_plan = parse_plan(explain_json[0][0]['Plan'])

    print()
    pprint.pprint(explain_json[0][0]['Plan'])

    return execute(sql, params, many, context)


def install_cardinality_estimation_wrapper(conn=None, **kwargs):
    if cardinality_estimation_wrapper not in connection.execute_wrappers:
        conn.execute_wrappers.append(cardinality_estimation_wrapper)
