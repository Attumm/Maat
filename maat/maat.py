from .validations import types
from .transformations import registered_transformation
from .exceptions import Invalid

NESTED = "nested"
OPTIONAL = "optional"
NULLABLE = "nullable"
DEFAULT = "default"
EMPTYLIST = "empty_list"
TRANSFORM = "transform"
PRETRANSFORM = "pre_transform"
SKIPFAILED = "skip_failed"

TYPE = "type"
TYPELIST = "list"
TYPEDICT = "dict"
TYPEASOARR = "aso_array"
TYPELISTDICTS = "list_dicts"

special_arguments = {NESTED, TYPELIST, TYPEASOARR, SKIPFAILED, NULLABLE, OPTIONAL, DEFAULT, PRETRANSFORM,
                     TRANSFORM, TYPELISTDICTS, EMPTYLIST, TYPEDICT, TYPE}


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


def scale(input_dict, counter_dict):  # noqa:C901

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

        # if the value is None check if value is allowed to be None
        if val is None and item.get(NULLABLE):
            validated_items[key] = None
            continue

        try:
            validation_func = types[item[TYPE]]
        except KeyError:
            raise Invalid(f"{item.get(TYPE)} is not registered as type")

        pre_transformation = get_transformation_func(item, PRETRANSFORM)
        post_transformation = get_transformation_func(item, TRANSFORM)

        # the validation can be done on top level, life is good
        if NESTED not in item:
            validated_items[key] = post_transformation(validation_func(key=key, val=pre_transformation(val), **item))
            continue

        type_ = item["type"]
        if type_ == TYPEDICT:
            validation_func(key=key, val=val, **item)
            validated_items[key] = post_transformation(scale(pre_transformation(input_dict[key]), counter_dict[key][NESTED]))

        elif type_ == TYPELIST:
            validation_func(key=key, val=val, **item)
            validated_items[key] = item.get(EMPTYLIST, []) if len(val) == 0 else []

            try:
                validation_func = types[item[NESTED][TYPE]]
            except KeyError:
                raise Invalid(f"{item[NESTED].get(TYPE)} is not registered as type")

            for nested_item in val:
                try:
                    validated_items[key].append(post_transformation(validation_func(key=key, val=pre_transformation(nested_item), **item[NESTED])))
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        elif type_ == TYPELISTDICTS:
            validation_func(key=key, val=val, **item)
            validated_items[key] = []
            for nested_item in val:
                try:
                    validated_items[key].append(post_transformation(scale(pre_transformation(nested_item), counter_dict[key][NESTED])))
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        elif type_ == TYPEASOARR:
            validation_func(key=key, val=val, **item)

            for nested_key, nested_val in val.items():
                # TODO this could be nicer
                if key not in validated_items:
                    validated_items[key] = {}
                if nested_key not in validated_items[key]:
                    validated_items[key][nested_key] = {}

                validated_items[key][nested_key] = validate(nested_val, counter_dict[key][NESTED])

        else:
            raise Invalid(f"type {type_} can't handle nested structures, use {TYPEASOARR}, {TYPELISTDICTS}, {TYPEDICT} instead")

    return validated_items


def validate(input_dict, counter_dict):  # noqa:C901

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

        # if the value is None check if value is allowed to be None
        if val is None and item.get(NULLABLE):
            validated_items[key] = None
            continue

        try:
            validation_func = types[item[TYPE]]
        except KeyError:
            raise Invalid(f"{item.get(TYPE)} is not registered as type")

        # the validation can be done on top level, life is good
        if NESTED not in item:
            validated_items[key] = validation_func(key=key, val=val, **item)
            continue

        type_ = item["type"]
        if type_ == TYPEDICT:
            validation_func(key=key, val=val, **item)
            validated_items[key] = validate(input_dict[key], counter_dict[key][NESTED])

        elif type_ == TYPELIST:
            validation_func(key=key, val=val, **item)
            validated_items[key] = item.get(EMPTYLIST, []) if len(val) == 0 else []

            try:
                validation_func = types[item[NESTED][TYPE]]
            except KeyError:
                raise Invalid(f"{item[NESTED].get(TYPE)} is not registered as type")

            for nested_item in val:
                try:
                    validated_items[key].append(validation_func(key=key, val=nested_item, **item[NESTED]))  # ADD test item nested
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        elif type_ == TYPELISTDICTS:
            validation_func(key=key, val=val, **item)
            validated_items[key] = []
            for nested_item in val:
                try:
                    validated_items[key].append(validate(nested_item, counter_dict[key][NESTED]))
                except Invalid:
                    if not item.get(SKIPFAILED):
                        raise

        elif type_ == TYPEASOARR:
            validation_func(key=key, val=val, **item)

            for nested_key, nested_val in val.items():
                # TODO this could be nicer
                if key not in validated_items:
                    validated_items[key] = {}
                if nested_key not in validated_items[key]:
                    validated_items[key][nested_key] = {}

                validated_items[key][nested_key] = validate(nested_val, counter_dict[key][NESTED])

        else:
            raise Invalid(f"type {type_} can't handle nested structures, use {TYPEASOARR}, {TYPELISTDICTS}, {TYPEDICT} instead")

    return validated_items
