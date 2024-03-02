import math
import copy

def once(func):
    def wrapper(target):
        if wrapper.called:
            raise TypeError("Effect is depleted.")
        wrapper.called = True
        func(target)
    wrapper.called = False
    return wrapper

def calling_function_decorator(function, times):
    @once
    def decorator(target):
        for _ in range(times):
            function(target)
    return decorator

class Potion:

    def __hash__(self):
        hash_value = 0
        for effect_name, intensity in self.intensity.items():
            hash_value ^= hash((effect_name, intensity))
        return hash_value

    def round_intensity(self,to_return,effect_name):
         to_return.intensity[effect_name] = math.floor(to_return.intensity[effect_name]) if  to_return.intensity[effect_name] <= int(to_return.intensity[effect_name]) +0.5 else math.ceil(to_return.intensity[effect_name])

    def is_depleted(self):
         is_depleted_var = True
         for effect_name,effect in self.effects.items():
            function = getattr(self, effect_name)
            try:
                function(None)               
            except TypeError:
                is_depleted_var = True
                continue
            finally:
                setattr(self, effect_name, calling_function_decorator(effect, self.intensity[effect_name]))
                return False
         return is_depleted_var
    
    @staticmethod
    def already_used(target):
        raise TypeError("Potion is now part of something bigger than itself.")
    
    def __init__(self,effects, duration):
        self.effects = copy.copy(effects)
        self.was_used = False
        self.intensity = {}
        for effect_name in self.effects:
            self.intensity[effect_name] = 1
        for effect_name,effect in effects.items():
             setattr(self, effect_name, calling_function_decorator(effect, self.intensity[effect_name]))
             self.effects[effect_name] = effect
        self.duration = duration

    def __add__(self, other):
        if self.is_depleted() or other.is_depleted():
            raise TypeError("Potion is depleted.")
        if self.was_used == True or other.was_used == True:
            raise TypeError("Potion is now part of something bigger than itself.")
        to_return = Potion(self.effects, max(self.duration, other.duration)) 
        for effect_name,effect in to_return.effects.items():
            to_return.intensity[effect_name]=self.intensity[effect_name]
            setattr(to_return, effect_name, calling_function_decorator(effect, to_return.intensity[effect_name]))
        for effect_name,effect in other.effects.items():
            if effect_name in to_return.effects:
                to_return.intensity[effect_name] += 1       
                setattr(to_return, effect_name, calling_function_decorator(effect, to_return.intensity[effect_name]))
            else:
                to_return.intensity[effect_name] = other.intensity[effect_name]   
                setattr(to_return, effect_name, calling_function_decorator(effect, to_return.intensity[effect_name]))
                to_return.effects[effect_name] = effect
        for effect_name in self.effects:
            setattr(self, effect_name, self.already_used)
        for effect_name in other.effects:
            setattr(other, effect_name, other.already_used)
        self.was_used = other.was_used = True
        return to_return
    
    def __mul__(self, value):
        if self.is_depleted():
            raise TypeError("Potion is depleted.")
        if self.was_used == True:
            raise TypeError("Potion is now part of something bigger than itself.")
        if value >= 0 and value <= 1:
            to_return = Potion(self.effects, self.duration)
            for effect_name in to_return.effects:
                to_return.intensity[effect_name] = self.intensity[effect_name]
            for effect_name,effect in to_return.effects.items():
                to_return.intensity[effect_name] *= value
                self.round_intensity(to_return,effect_name)
                setattr(to_return, effect_name, calling_function_decorator(effect, to_return.intensity[effect_name]))
               #  to_return.intensity[effect_name] = math.floor(to_return.intensity[effect_name]) if  to_return.intensity[effect_name] <= 0.5 else math.ceil(to_return.intensity[effect_name])              
            for effect_name in self.effects:
                setattr(self, effect_name, self.already_used)
            self.was_used = True
            return to_return
        to_return = Potion(self.effects, self.duration)
        for effect_name in to_return.effects:
            to_return.intensity[effect_name] = self.intensity[effect_name]
        for effect_name in to_return.effects:
            to_return.intensity[effect_name] *= value
        for effect_name,effect in to_return.effects.items():
             setattr(to_return, effect_name, calling_function_decorator(effect, to_return.intensity[effect_name]))
        for effect_name in self.effects:
            setattr(self, effect_name, self.already_used)
        self.was_used = True
        return to_return
    
    def __sub__(self, other):
        if self.is_depleted() or other.is_depleted():
            raise TypeError("Potion is depleted.")
        if self.was_used == True or other.was_used == True:
            raise TypeError("Potion is now part of something bigger than itself.")
        to_return = Potion(self.effects, self.duration)
        for effect_name,effect in to_return.effects.items():
            to_return.intensity[effect_name] = self.intensity[effect_name]
            setattr(to_return, effect_name, calling_function_decorator(effect,to_return.intensity[effect_name]))
        for effect_name in other.effects:
            if effect_name not in to_return.effects:
                raise TypeError("Error")
        for effect_name, effect in other.effects.items():
            if to_return.intensity[effect_name] > other.intensity[effect_name]:
                to_return.intensity[effect_name] -= other.intensity[effect_name]
                setattr(to_return, effect_name, calling_function_decorator(effect, to_return.intensity[effect_name]))
            else:
                delattr(to_return, effect_name)
                del to_return.effects[effect_name]
                del to_return.intensity[effect_name]
        for effect_name in self.effects:
            setattr(self, effect_name, self.already_used)
        for effect_name in other.effects:
            setattr(other, effect_name, other.already_used)
        self.was_used = other.was_used = True
        return to_return

    def __truediv__(self, value):
        if self.is_depleted():
            raise TypeError("Potion is depleted.")
        if self.was_used == True:
            raise TypeError("Potion is now part of something bigger than itself.")
        copy_potion=Potion(self.effects,self.duration)
        for effect_name in self.intensity:
            copy_potion.intensity[effect_name] = self.intensity[effect_name]
        for effect_name,effect in copy_potion.effects.items():
            copy_potion.intensity[effect_name] /= value
            self.round_intensity(copy_potion,effect_name)
            #copy.intensity[effect_name] = math.floor(copy.intensity[effect_name]) if  copy.intensity[effect_name] <= 0.5 else math.ceil(copy.intensity[effect_name])
            setattr(copy_potion,effect_name, calling_function_decorator(effect, copy_potion.intensity[effect_name]))        
        potion_list=[]
        for _ in range(value):
            copy=Potion(copy_potion.effects,copy_potion.duration)
            for effect_name in copy_potion.intensity:
                copy.intensity[effect_name] = copy_potion.intensity[effect_name]
            for effect_name,effect in copy_potion.effects.items():
                setattr(copy,effect_name, calling_function_decorator(effect, copy_potion.intensity[effect_name]))
            potion_list.append(copy)
        for effect_name in self.effects:
            setattr(self, effect_name, self.already_used)
        self.was_used = True
        return tuple(potion_list)
 
    def __eq__(self,other):
        if self.is_depleted() or other.is_depleted():
            raise TypeError("Potion is depleted.")
        if self.was_used == True or other.was_used == True:
            raise TypeError("Potion is now part of something bigger than itself.")
        for effect_name in self.effects:
            if effect_name not in other.effects:
                return False
        for effect_name in self.effects:
            if self.intensity[effect_name] != other.intensity[effect_name]:
                return False
        return True
    
    def __gt__(self,other):
        if self.is_depleted() or other.is_depleted():
            raise TypeError("Potion is depleted.")
        if self.was_used == True or other.was_used == True:
            raise TypeError("Potion is now part of something bigger than itself.")
        sum_of_self = 0
        for effect_name in self.intensity:
            sum_of_self+=self.intensity[effect_name]
        sum_of_other = 0
        for effect_name in other.intensity:
            sum_of_other += other.intensity[effect_name]
        return sum_of_self > sum_of_other
        

def sorting_potions(potion):
        name = potion[0]
        sum_of_potion_name = 0
        for letter in name:
            sum_of_potion_name += ord(letter)
        return sum_of_potion_name


class ГоспожатаПоХимия:
    def __init__(self):
        self.used_potions = []
        self.targets_copies = {}
        self.targets_buffed_copies = {}

    def apply(self, target, potion):
        if potion.duration == 0:
            return
        if potion.is_depleted():
            raise TypeError("Potion is depleted.")
        if potion.was_used:
            raise TypeError("Potion is now part of something bigger than itself.")
        sorted_potions = sorted(potion.effects.items(), key=sorting_potions, reverse=True)
        potion.effects = dict(sorted_potions)
        if target not in self.targets_buffed_copies.values():
            self.targets_copies[potion] = copy.copy(target)
        else:
            for potion_loop in self.used_potions:
                potion_loop.was_used = False
                if self.targets_buffed_copies[potion_loop] == target:
                    self.targets_copies[potion] = copy.copy(self.targets_copies[potion_loop])
                potion_loop.was_used = True
        self.used_potions.append(potion)
        for effect_name in potion.effects:
            function = getattr(potion, effect_name)
            try:
                function(target)
            except TypeError:
                continue
        for potion_iter in self.used_potions:
            potion_iter.was_used = False
        self.targets_buffed_copies[potion] = target
        potion.was_used = True
        for potion_iter in self.used_potions:
            potion_iter.was_used = True
    
    def tick(self):
        for potion in self.used_potions:
            potion.duration -= 1
            if potion.duration == 0:
                self.targets_buffed_copies[potion].__dict__ = vars(self.targets_copies[potion])
                for potion_inner in self.used_potions:
                    potion_inner.was_used = False
                    potion.was_used = False
                    if potion_inner == potion or potion_inner.duration <= 0 or self.targets_buffed_copies[potion] != self.targets_buffed_copies[potion_inner]:
                        potion_inner.was_used = True
                        potion.was_used = True
                        continue
                    potion_inner.was_used = True
                    potion.was_used = True
                    copy = Potion(potion_inner.effects,potion_inner.duration)
                    for effect_name,effect in  copy.effects.items():
                         copy.intensity[effect_name] = potion_inner.intensity[effect_name]
                         setattr(copy, effect_name, calling_function_decorator(effect, copy.intensity[effect_name]))
                    for effect_name in  copy.effects:
                        function = getattr(copy, effect_name)
                        function(self.targets_buffed_copies[potion])