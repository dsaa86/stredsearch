def removeBlankParams(keys_to_delete: list, params_dict: dict) -> dict:
        for key in keys_to_delete:
            del params_dict[key]

        return params_dict
def processFilters(params_dict: dict) -> dict:
    keys_to_delete = []

    # " " indicates a param not used in this search on the
    # part of the user.
    for key, value in params_dict.items():
        if value == " ":
            keys_to_delete.append(key)

        # Stack Exchange expects semi-colon delimited list
        if key in ["tagged", "ids"]:
            params_dict[key] = value.replace(",", ";")

    params_dict = removeBlankParams(keys_to_delete, params_dict)

    return params_dict