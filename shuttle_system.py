import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10

def get_route(route_id):
    if route_id not in routes:
        raise ValueError("Unknown route: %s" % route_id)
    return routes[route_id]

def add_trip_log(route_id, passenger_count, logs=[]):
    route = get_route(route_id)
    if (isinstance(passenger_count, bool)
            or not isinstance(passenger_count, int)
            or passenger_count < 0):
        raise ValueError("Invalid passenger count: %r" % (passenger_count,))
    route["trips"].append(passenger_count)
    logs.append("%s: %s carried %s" % (datetime.now(), route_id, passenger_count))
    return logs

def remove_route(route_id):
    get_route(route_id)
    del routes[route_id]

def average_load(route_id):
    trips = get_route(route_id)["trips"]
    return sum(trips) / len(trips)

def underused_routes():
    flagged = []
    for r in routes:
        if routes[r]["trips"] and average_load(r) < MIN_CAPACITY:
            flagged.append(r)
    return flagged

def assignDriver(route_id):
    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return secrets.choice(drivers)

def sync_fleet_data(file="fleet.json"):
    global routes
    f = open(file, "w")
    f.write(json.dumps(routes))
    f.close()
    f = open(file)
    routes = json.loads(f.read())

def main():
    sample_trips = [("R1", 32), ("R1", 28), ("R2", 4), ("R2", -6),
                    ("R3", "full")]
    for route_id, count in sample_trips:
        try:
            add_trip_log(route_id, count)
        except ValueError as err:
            print("Rejected trip:", err)
    print("Driver for R1:", assignDriver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    print("Trips on", choice, ":", get_route(choice)["trips"])
    print("R3 average:", average_load("R3"))

main()
