from typing import get_type_hints

# def strict_types(f: callable):
#     def type_checker(*args, **kwargs):
#         hints = get_type_hints(f)
#
#         all_args = kwargs.copy()
#         all_args.update(dict(zip(f.__code__.co_varnames, args)))
#
#         for key in all_args:
#             if key in hints:
#                 if type(all_args[key]) != hints[key]:
#                     raise Exception('Type of {} is {} and not {}'.format(key, type(all_args[key]), hints[key]))
#
#         res = f(*args, **kwargs)
#
#         if type(res) == hints['return']:
#             return res
#         else:
#             raise Exception('Type of result is {} and not {}'.format(type(res), hints['return']))
#
#     return type_checker

def strict_types(f: callable):
    return f
