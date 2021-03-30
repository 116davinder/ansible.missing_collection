from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    try:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    try:
                        _return.append(camel_dict_to_snake_dict(_app))
                    except AttributeError:
                        _return.append(_app)
        else:
            for _app in iterator[resource_field]:
                try:
                    _return.append(camel_dict_to_snake_dict(_app))
                except AttributeError:
                    _return.append(_app)
        return _return
    except KeyError:
        return _return


# used in aws pinpoint module
def aws_response_nested_list_parser(paginate: bool, iterator, resource_field: str, nested_resource_field: str) -> list:
    _return = []
    try:
        if paginate:
            for response in iterator:
                for _app in response[resource_field][nested_resource_field]:
                    try:
                        _return.append(camel_dict_to_snake_dict(_app))
                    except AttributeError:
                        _return.append(_app)
        else:
            for _app in iterator[resource_field][nested_resource_field]:
                try:
                    _return.append(camel_dict_to_snake_dict(_app))
                except AttributeError:
                    _return.append(_app)
        return _return
    except KeyError:
        return _return
