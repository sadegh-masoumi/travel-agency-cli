"""
CLI Program
"""
import json

# Models


class City:
    id: int
    name: str
    cities = {}

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        # in memory store objects
        self.cities[id] = self


class Road:
    id: int
    name: str
    from_: int
    to: int
    through: list
    speed_limit: int
    length: int
    bi_directional: int

    roads = {}

    def __init__(
        self, id, name, from_, to, through, speed_limit, length, bi_directional
    ):
        self.id = id
        self.name = name
        self.from_ = from_
        self.to = to
        self.through = [from_] + through + [to]
        self.speed_limit = speed_limit
        self.length = length
        self.bi_directional = bi_directional
        # in memory store objects
        self.roads[id] = self


# Start CLI


def menu() -> int:
    while True:
        try:
            print("Main Menu - Select an action:")
            print("1. Help")
            print("2. Add")
            print("3. Delete")
            print("4. Path")
            print("5. Exit")
            action = int(input(""))
            if action not in [num for num in range(1, 6)]:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1 for more info.")

    return action


def help_() -> None:
    """
    this function print help of CLI program
    """
    print("Select a number from shown menu and enter. For example 1 is for help.")


def add(model=None):
    if model is None:
        print("Select model:")
        print("1. City")
        print("2. Road")
        action = int(input())
        model = "City" if action == 1 else "Road"

    data_for_fields = {}
    if model == "City":
        for key in City.__annotations__.keys():
            print(f"{key}=?")
        for key in City.__annotations__.keys():
            data_for_fields[key] = Road.__annotations__[key](input())
        City(**data_for_fields)

    elif model == "Road":
        for key in Road.__annotations__.keys():
            if key.endswith("_"):
                print(f"{key[:-1]}=?")
            else:
                print(f"{key}=?")

        for key in Road.__annotations__.keys():
            data = input()
            if key == "through":
                data_for_fields[key] = json.loads(data)
            else:
                data_for_fields[key] = Road.__annotations__[key](data)
        Road(**data_for_fields)
    else:
        print("invalid input")
        return

    print(f"{model} with id={data_for_fields['id']} added!")
    print("Select your next action:")
    print(f"1. Add another {model}")
    print("2. Main Menu")
    action = int(input())
    if action == 1:
        add(model=model)
    elif action == 2:
        return
    else:
        print("invalid Input")


def delete():
    print("Select model:")
    print("1. City")
    print("2. Road")
    action = int(input())
    if action == 1:
        id = int(input())
        removed_value = City.cities.pop(id, None)
        model = "City"
    else:
        id = int(input())
        removed_value = Road.roads.pop(id, None)
        model = "Road"

    if removed_value is None:
        print(f"{model} with id {id} not found!")
    else:
        print(f"{model}:{id} deleted!")


def format_time(time_: int):
    day = time_ // 1440
    hour = ((time_ % 1440) // 60)
    minute = time_ % 60

    return "%02d:%02d:%02d" % (day, hour, minute)


def path():
    source, destination = map(int, input().split(":"))
    roads = []
    for road in Road.roads.values():
        through = road.through
        if source in through and destination in through:
            if road.bi_directional or through.index(source) < through.index(
                destination
            ):
                time = (road.length / road.speed_limit) * 60
                roads.append((road, time))

    roads.sort(key=lambda item: item[1])
    for road, time in roads:
        formatted_time = format_time(time)
        from_city_name = City.cities[source].name
        to_city_name = City.cities[destination].name
        print(
            f"{from_city_name}:{to_city_name} via Road {road.name}: Takes {formatted_time}"
        )


def exit_():
    exit(0)


actions_map = {1: help_, 2: add, 3: delete, 4: path, 5: exit_}


def main():
    """
    entrypoint function
    """
    #  show menu and get action from user
    action = menu()

    actions_map[action]()

    main()


main()
