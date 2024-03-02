def  logic_mixin_factory(mass, mass_attr_name, material, material_attr_name, float_method_name):


    class LogicMixin:
         
         def is_a_witch(self):
              if hasattr(self, mass_attr_name) and  mass == getattr(self, mass_attr_name):
                    return "Burn her!"
              if hasattr(self, material_attr_name) and getattr(self, material_attr_name) == material:
                    return "Burn her!"
              if hasattr(self, float_method_name):
                    return "Burn her!"
              return "No, but it's a pity, cuz she looks like a witch!"
         
    return LogicMixin     