"""Campus shuttle timetable and fleet tracker.

Logs passenger counts per trip, works out average loads, flags under-used
routes and syncs the fleet data to ``fleet.json``.
"""
import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10


def get_route(route_id):
    """Return the route record, or raise ValueError if it does not exist."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")
    return routes[route_id]


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and return the list of log lines.

    Raises ValueError for an unknown route or a count that is not a
    non-negative whole number.
    """
    route = get_route(route_id)
    if (isinstance(passenger_count, bool)
            or not isinstance(passenger_count, int)
            or passenger_count < 0):
        raise ValueError(f"Invalid passenger count: {passenger_count!r}")
    if logs is None:
        logs = []
    route["trips"].append(passenger_count)
    logs.append(
        f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Delete a route; raises ValueError if it does not exist."""
    get_route(route_id)
    del routes[route_id]


def average_load(route_id):
    """Return the mean passengers per trip; ValueError if no trips logged."""
    trips = get_route(route_id)["trips"]
    if not trips:
        raise ValueError(f"No trips logged for {route_id}")
    return sum(trips) / len(trips)


def underused_routes():
    """Return the ids of routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id, route in routes.items():
        if route["trips"] and average_load(route_id) < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver(route_id):
    """Pick a driver at random for an existing route."""
    get_route(route_id)
    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return secrets.choice(drivers)


def sync_fleet_data(file="fleet.json"):
    """Write the current fleet data to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(routes, handle)


def main():
    """Run the demo: log trips, report loads, sync data, remove a route."""
    sample_trips = [("R1", 32), ("R1", 28), ("R2", 4), ("R2", -6),
                    ("R3", "full")]
    for route_id, count in sample_trips:
        try:
            add_trip_log(route_id, count)
        except ValueError as err:
            print("Rejected trip:", err)
    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    for label, lookup in (
            (f"Trips on {choice}", lambda: get_route(choice)["trips"]),
            ("R3 average", lambda: average_load("R3"))):
        try:
            print(label + ":", lookup())
        except ValueError as err:
            print(err)


if __name__ == "__main__":
    main()
