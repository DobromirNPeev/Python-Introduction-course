import math


class Candy:

    def __init__(self, mass, uranium):
        self.mass = mass
        self.uranium = uranium
    
    def get_uranium_quantity(self):
        return self.uranium*self.mass
    
    def get_mass(self):
        return self.mass
    
    def __gt__(self, other):
        return self.mass > other.mass
    

class Person:

    def __init__(self, position):
        self.set_position(position)

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position    


class Kid(Person):

    CRITICAL_URANIUM_DOSE = 20

    def __init__(self, position, initiative):
        super().__init__(position)
        self.initiative = initiative
        self.basket = []
        self.visited_hosts = set()

    def get_initiative(self):
        return self.initiative
    
    def add_candy(self, candy):
        self.basket.append(candy)

    def is_critical(self):
        sum = 0
        for candy in self.basket:
            sum += candy.get_uranium_quantity()
        return sum > self.CRITICAL_URANIUM_DOSE

    def __lt__(self, other):
        return self.initiative < other.initiative        

    def _sort_hosts(self, host):
        dist = math.sqrt((self.position[0] - host.position[0]) ** 2 + (self.position[1] - host.position[1]) ** 2)
        return dist, host.position[0], host.position[1]
    
    def _go_to_door(self, hosts):
        unvisited_hosts = [host for host in hosts if host not in self.visited_hosts]
        if not unvisited_hosts:
            return False
        unvisited_hosts.sort(key=lambda host: self._sort_hosts(host))
        selected_host = unvisited_hosts[0]
        self.visited_hosts.add(selected_host)
        self.position=selected_host.position
        selected_host.visiting_kids.append(self)


class Host(Person):

    def __init__(self, position, candies):
        super().__init__(position)
        self.basket = []
        self.visiting_kids = []
        for candy in candies:
            self.basket.append(Candy(candy[0], candy[1]))

    def remove_candy(self, func):
        if not self.basket:
            return None
        candy_to_remove = func(self.basket)
        self.basket = [candy for candy in self.basket if candy is not candy_to_remove]
        return candy_to_remove
    
    def _give_candy(self):
        self.visiting_kids.sort(reverse = True)
        for kid in self.visiting_kids:
            candy = self.remove_candy(func=lambda basket:sorted(basket)[0])
            if candy is not None:
                kid.basket.append(candy)
        self.visiting_kids.clear()


class FluxCapacitor:

    def __init__(self, participants):
        self.participants = participants
        self.kids = []
        self.hosts = []
        for person in participants:
            if isinstance(person, Kid):
                self.kids.append(person)
            elif isinstance(person, Host):
                self.hosts.append(person)
    
    def get_victim(self):
        kids_with_critical_mass = set()
        while True:
            for kid in self.kids:
                kid._go_to_door(self.hosts)
            for host in self.hosts:
                host._give_candy()
            for kid in self.kids:
                if kid.is_critical():
                    kids_with_critical_mass.add(kid)
            if kids_with_critical_mass:
                return kids_with_critical_mass
            all_kids_visited_all_hosts = True
            for kid in self.kids:
                if not kid.visited_hosts == set(self.hosts):
                    all_kids_visited_all_hosts = False
                    break
            if all_kids_visited_all_hosts:
                return None