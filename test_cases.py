# AI USAGE CITATION:
# Used AI assistance to help design the DEBUG printing logic inside run_pretty_test,
# including formatting of assignment buckets and routes for readability during testing.
# AI was also used to suggest how to structure expected-failure tests to ensure invalid
# scenarios raise clear, informative exceptions. All test logic and assertions were
# written and verified manually.

from scenario import parse_scenario
from scheduler import (
    assign_round_robin,
    order_in_given,
    order_nearest,
    improve_order_2swap,
    build_route,
)
from simulator import simulate

def build_ordering_func(ordering):
    ordering = ordering.lower()
    if ordering == "given":
        return lambda depot, ds, g: order_in_given(ds)
    if ordering == "nearest":
        return lambda depot, ds, g: order_nearest(depot, ds, g)
    if ordering == "nearest_2swap":
        def f(depot, ds, g):
            base = order_nearest(depot, ds, g)
            return improve_order_2swap(depot, base, g)
        return f
    raise ValueError(f"Unknown ordering: {ordering}")

def summarize_text(summary):
    """
    Convert summary in clear txt format.
    """
    lines = []
    lines.append("=== Simulation Summary ===\n")

    lines.append(f"Total deliveries: {summary['total_deliveries']}\n")

    # Courier times
    lines.append("Courier times:")
    for i, t in enumerate(summary["courier_times"], 1):
        lines.append(f"  Courier_{i}: {t}")
    lines.append("")

    # Completed deliveries
    lines.append("Courier completed deliveries:")
    for i, bucket in enumerate(summary["courier_completed"], 1):
        lines.append(f"  Courier_{i}:")
        if not bucket:
            lines.append("    (none)")
        else:
            for delivery_dict, time_done in bucket:
                dest = delivery_dict["dest"]
                lines.append(f"    - {dest} at t={time_done}")
    lines.append("")

    lines.append(f"Max delivery time (makespan): {summary['max_delivery_time']}")
    lines.append("")

    return "\n".join(lines)


def run_pretty_test(scenario_path, ordering):
    print(f"\n================= TEST RUN =================")
    print(f"Scenario: {scenario_path}")
    print(f"Ordering: {ordering}\n")

    graph, depot, deliveries, k = parse_scenario(scenario_path)
    from scenario import print_map_overview
    print_map_overview(graph, depot, deliveries)

    # assign
    buckets = assign_round_robin(deliveries, k)

    '''
    print("\n[DEBUG] Assignment buckets:")
    for i, b in enumerate(buckets, 1):
        print(f"  Courier_{i}: {[d['dest'] for d in b]}")
    '''

    # order deliveries
    ordering_func = build_ordering_func(ordering)

    # build routes
    routes = []
    for bucket in buckets:
        if not bucket:
            routes.append([depot])
        else:
            ordered = ordering_func(depot, bucket, graph)
            route = build_route(graph, depot, ordered)
            routes.append(route)
     
    '''
    print("\n[DEBUG] Routes:")
    for i, r in enumerate(routes, 1):
        print(f"  Courier_{i}: {r}")
    '''

    # simulate to see movements
    summary = simulate(graph, depot, routes, buckets, verbose=True)

    # correctness checks
    assert summary["total_deliveries"] == len(deliveries)
    for t in summary["courier_times"]:
        assert t >= 0

    # bring out txt summary
    txt = summarize_text(summary)
    print(txt)

    print("===========================================\n")

def run_expected_failure(scenario_path):
    print("\n================= EDGE CASE =================")
    print(f"Scenario: {scenario_path}")
    print("Expecting: ValueError due to invalid destination\n")
    try:
        parse_scenario(scenario_path)
        print("-> FAIL (expected an error, but parse_scenario succeeded)")
    except ValueError as e:
        print(f"-> PASS (caught expected error): {e}")
    print("=============================================\n")


if __name__ == "__main__":
    run_pretty_test("scenario.txt", "nearest")
    run_pretty_test("scenario_ucla.txt", "nearest_2swap")
    run_pretty_test("scenario_edge_unreachable.txt", "nearest")


