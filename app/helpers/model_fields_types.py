def model_fields_types(model):
    dict = {}

    fields = model._meta.fields
    for field in fields:
        dict[field.name] = field.get_internal_type()

    return dict
