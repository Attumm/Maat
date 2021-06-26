from .validations import registered_functions
from .transformations import registered_transformation
from .exceptions import Invalid

NESTED = "nested"
TYPELIST = "list"
VALIDATOR = "type"
OPTIONAL = "optional"
NULLABLE = "null_able"
TYPEASOARR = "aso_array"
SKIPFAILED = "skip_failed"
TYPELISTDICTS = "list_dicts"
DEFAULT = "default"
EMPTYLIST = "empty_list"
TRANSFORM = "transform"
PRETRANSFORM = "pre_transform"

special_arguments = {VALIDATOR, NESTED, TYPELIST, TYPEASOARR, SKIPFAILED, NULLABLE, OPTIONAL, DEFAULT, PRETRANSFORM,
                     TRANSFORM, TYPELISTDICTS, EMPTYLIST}


def get_validation_func(item):
    try:
        return registered_functions[item[VALIDATOR]]
    except KeyError:
        raise Invalid(f"{item.get(VALIDATOR)} is not registered as type")


def get_validation_args(item):
    return {k: v for k, v, in item.items() if k not in special_arguments}


def get_transformation_func(item, type_transformation):
    """Check if transformation is set. If set try to find it in registerd transformation.
    If transformation is misspelled or sit or throw an exception"""
    transformation = item.get(type_transformation)
    if transformation is None:
        return lambda x: x
    try:
        return registered_transformation[transformation]
    except KeyError:
        raise Invalid(f"{transformation} is not registered as transformation")


def keys_equality(input_dict, counter_dict):
    try:
        return set(input_dict) <= set(counter_dict)
    except (TypeError, AttributeError):
        return False


def find_missing_keys(input_dict, counter_dict):
    try:
        found_keys = ", ".join(set(input_dict) - set(counter_dict))
        return f"{found_keys} :expected keys: {', '.join(counter_dict.keys())}"
    except (TypeError, AttributeError):
        raise Invalid(f"{input_dict} not a dictionary but is of type {type(input_dict).__name__}")


def scale(input_dict, counter_dict):

    if not keys_equality(input_dict, counter_dict):
        raise Invalid(f"invalid keys: {find_missing_keys(input_dict, counter_dict)}")

    validated_items = {}
    for key, item in counter_dict.items():

        try:
            val = input_dict[key]
        except KeyError:
            if DEFAULT in item:
                validated_items[key] = item[DEFAULT]
                continue
            elif item.get(OPTIONAL):
                continue
            else:
                raise Invalid(f'key:"{key}" is not set')

        # # if the value is None, check for default value or check if it was required
        if val is None and item.get(NULLABLE):
            validated_items[key] = None
            continue

        try:
            validation_func = registered_functions[item[VALIDATOR]]
        except KeyError:
            raise Invalid(f"{item.get(VALIDATOR)} is not registered as type")

        validation_args = {k: v for k, v, in item.items() if k not in special_arguments}

        pre_transformation = get_transformation_func(item, PRETRANSFORM)
        post_transformation = get_transformation_func(item, TRANSFORM)

        # the validation can be done on top level, life is good
        if NESTED not in item:
            validated_items[key] = post_transformation(validation_func(key=key, val=pre_transformation(val), **validation_args))

        elif TYPELIST in item:
            validated_items[key] = item.get(EMPTYLIST, []) if len(val) == 0 else []

            for nested_item in val:
                # within a list a item should be skipable
                try:
                    validated_items[key].append(post_transformation(validation_func(key=key, val=pre_transformation(nested_item), **validation_args)))
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        # the item is nested with a list of dictionary items
        elif TYPELISTDICTS in item:

            validation_func(key=key, val=val, **validation_args)
            validated_items[key] = []
            for nested_item in val:
                try:
                    validated_items[key].append(post_transformation(scale(pre_transformation(nested_item), counter_dict[key][NESTED])))
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        # the item is nested. we have to start over to do the same the one level deeper
        elif not item.get(TYPEASOARR, False):
            validated_items[key] = post_transformation(scale(pre_transformation(input_dict[key]), counter_dict[key][NESTED]))

        # the item is a "associative array" dictionary e.g keys are numerical indexes
        else:
            validation_func(key=key, val=val, **validation_args)

            for nested_key, nested_val in val.items():
                # make sure dictionary is present.
                if key not in validated_items:
                    validated_items[key] = {}
                if nested_key not in validated_items[key]:
                    validated_items[key][nested_key] = {}

                validated_items[key][nested_key] = scale(nested_val, counter_dict[key][NESTED])

    return validated_items


def validate(input_dict, counter_dict):

    if not keys_equality(input_dict, counter_dict):
        raise Invalid(f"invalid keys: {find_missing_keys(input_dict, counter_dict)}")

    validated_items = {}
    for key, item in counter_dict.items():
        try:
            val = input_dict[key]
        except KeyError:
            if DEFAULT in item:
                validated_items[key] = item[DEFAULT]
                continue
            elif item.get(OPTIONAL):
                continue
            else:
                raise Invalid(f'key:"{key}" is not set')

        # # if the value is None, check for default value or check if it was required
        if val is None and item.get(NULLABLE):
            validated_items[key] = None
            continue

        try:
            validation_func = registered_functions[item[VALIDATOR]]
        except KeyError:
            raise Invalid(f"{item.get(VALIDATOR)} is not registered as type")

        validation_args = {k: v for k, v, in item.items() if k not in special_arguments}

        # the validation can be done on top level, life is good
        if NESTED not in item:
            validated_items[key] = validation_func(key=key, val=val, **validation_args)

        elif TYPELIST in item:
            validated_items[key] = item.get(EMPTYLIST, []) if len(val) == 0 else []

            for nested_item in val:
                # within a list a item should be skipable
                try:
                    validated_items[key].append(validation_func(key=key, val=nested_item, **validation_args))
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        # the item is nested with a list of dictionary items
        elif TYPELISTDICTS in item:

            validation_func(key=key, val=val, **validation_args)
            validated_items[key] = []
            for nested_item in val:
                try:
                    validated_items[key].append(validate(nested_item, counter_dict[key][NESTED]))
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        # the item is nested. we have to start over to do the same the one level deeper
        elif not item.get(TYPEASOARR, False):
            validated_items[key] = validate(input_dict[key], counter_dict[key][NESTED])

        # the item is a "associative array" dictionary e.g keys are numerical indexes
        else:
            validation_func(key=key, val=val, **validation_args)

            for nested_key, nested_val in val.items():
                # make sure dictionary is present.
                if key not in validated_items:
                    validated_items[key] = {}
                if nested_key not in validated_items[key]:
                    validated_items[key][nested_key] = {}

                validated_items[key][nested_key] = validate(nested_val, counter_dict[key][NESTED])

    return validated_items
