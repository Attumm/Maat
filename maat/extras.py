from .maat import maat_scale, Invalid

def validate_args(validation_dic, fail_is_none=False, custom_exception=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) > 0:
                kwargs.update(zip(func.__code__.co_varnames, args))
            try:
                cleaned_kwargs = maat_scale(kwargs, validation_dic)
            except Invalid as e:
                if fail_is_none:
                    return None
                elif custom_exception is not None:
                    raise custom_exception
                else:
                    raise
            return func(**cleaned_kwargs)
        return wrapper
    return decorator

