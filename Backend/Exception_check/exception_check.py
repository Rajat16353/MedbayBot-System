def check_fields_post_message(request_json):
    try:
        fields = ['name', 'age', 'gender', 'text']
        for field in fields:
            if field not in request_json.keys():
                raise Exception(field)
        return True
    except Exception as ex:
        return {'error': "Key error: '{}' key not found in the request".format(ex)}


def check_fields_disease_info(request_json):
    try:
        if "disease_name" not in request_json.keys():
            raise Exception('disease_name')
        return True
    except Exception as ex:
        return {"error": "Key error: '{}' key not found in the request".format(ex)}
