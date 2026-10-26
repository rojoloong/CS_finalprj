# AI USAGE CITATION:
# Used AI assistance to help outline a simple text-based interactive menu
# for user input (scenario selection and ordering strategy). All control
# flow, function calls, and error handling were written manually.

import sys
from scenario import parse_scenario, print_map_overview
from scheduler import (
    assign_round_robin,
    order_in_given,
    order_nearest,
    improve_order_2swap,
    build_route,
)
from simulator import simulate

def choose_ordering_strategy(name):
    """
    Map a strategy name string to a function.
    Returns f(depot, deliveries, graph) -> ordered_deliveries.
    """
    lname = name.lower()

    if lname == "given":
        return lambda depot, ds, graph: order_in_given(ds)

    if lname == "nearest":
        return lambda depot, ds, graph: order_nearest(depot, ds, graph)

    if lname == "nearest_2swap":
        def strategy(depot, ds, graph):
            base = order_nearest(depot, ds, graph)
            return improve_order_2swap(depot, base, graph)
        return strategy

    raise ValueError(f"Unknown ordering strategy: {name}")


def choose_ordering_strategy(name):
    """
    Map a strategy name string to a function.
    Returns f(depot, deliveries, graph) -> ordered_deliveries.
    """
    lname = name.lower()

    if lname == "given":
        return lambda depot, ds, graph: order_in_given(ds)

    if lname == "nearest":
        return lambda depot, ds, graph: order_nearest(depot, ds, graph)

    if lname in {"nearest_2swap", "nearest+2s"}:
        def strategy(depot, ds, graph):
            base = order_nearest(depot, ds, graph)
            return improve_order_2swap(depot, base, graph)
        return strategy

    raise ValueError(f"Unknown ordering strategy: {name}")


def run_once(scenario_path, ordering_name, verbose=True):
    """
    Load a scenario, run the scheduling + simulation pipeline, and print a summary.
    """
    graph, depot, deliveries, k = parse_scenario(scenario_path)

    print(f"\n=== Scenario: {scenario_path} ===")
    print(f"Depot: {depot}")
    print(f"Deliveries: {[d['dest'] for d in deliveries]}")
    print(f"Couriers: {k}\n")

    print_map_overview(graph, depot, deliveries)
    print()

    # assign deliveries to couriers
    buckets = assign_round_robin(deliveries, k)

    # choose ordering strategy
    ordering_strategy = choose_ordering_strategy(ordering_name)
    courier_routes = []

    for i, bucket in enumerate(buckets):
        if not bucket:
            route = [depot]
        else:
            ordered = ordering_strategy(depot, bucket, graph)
            route = build_route(graph, depot, ordered)
        courier_routes.append(route)

    # simulate
    summary = simulate(graph, depot, courier_routes, buckets, verbose=verbose)

    # summary print
    print("\nSummary:")
    print(f"  Total deliveries completed: {summary['total_deliveries']}")
    for idx, t in enumerate(summary["courier_times"]):
        count = len(summary["courier_completed"][idx])
        print(f"  Courier_{idx+1}: time={t}, deliveries={count}")
    print(f"  Max delivery completion time: {summary['max_delivery_time']}")
    print("===")

    return summary

def interactive_menu():
    """
    Simple text UI: lets the user repeatedly choose scenario + strategy.
    """
    print("CourierGraph: Multi-Agent Routing and Scheduling Simulator")
    print("----------------------------------------------------------")
    print("Run format (non-interactive): python main.py <scenario> <ordering>")
    print("Ordering options: given, nearest, nearest_2swap\n")

    while True:
        scenario_path = input("Enter scenario file (or 'q' to quit): ").strip()
        if scenario_path.lower() in {"q", "quit", "exit"}:
            print("Exiting.")
            break

        ordering_name = input("Ordering strategy [given / nearest / nearest_2swap]: ").strip()
        if not ordering_name:
            ordering_name = "nearest_2swap"

        try:
            run_once(scenario_path, ordering_name, verbose=True)
        except Exception as e:
            print(f"[ERROR] {e}")

        again = input("\nRun another scenario? [y/n]: ").strip().lower()
        if again not in {"y", "yes"}:
            print("Goodbye.")
            break

def main():
    # If called with args -> non-interactive 
    if len(sys.argv) >= 3:
        scenario_path = sys.argv[1]
        ordering_name = sys.argv[2]
        run_once(scenario_path, ordering_name, verbose=True)
    else:
        # No args -> launch simple text UI for interaction 
        interactive_menu()