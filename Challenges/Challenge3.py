import secret
import inspect


#4MI0600262

def methodify():
    fn="4MI0600262"
    interesting_methods =[]
    module_attributes=dir(secret)
    for attr in module_attributes:
        if inspect.isclass(attr):
            nested_classes = [name for name, obj in inspect.getmembers(attr) if inspect.isclass(obj)]
            module_attributes.extend(nested_classes)

    for attr in module_attributes:
        if len(attr)==1 and callable(attr) and "clue" in attr and (attr.isupper() or attr.isdigit()):
            if hasattr(attr, '__name__') and attr.__name__  in fn:
                try:
                    attr()
                except TypeError as data:
                    if data=="Опаааааа, тука има нещо нередно.":
                        interesting_methods.append(attr)
                        continue
                try:
                    attr()
                except BaseException:
                    interesting_methods.append(attr)
                    continue
                if attr(2)==4 and attr(1)==0:
                    interesting_methods.append(attr)
                    continue
                elif attr("Java ","Sucks") == "Java sucks":
                    interesting_methods.append(attr)
                    continue
                elif isinstance(attr,staticmethod):
                    interesting_methods.append(attr)
                    continue
    return tuple(interesting_methods)
