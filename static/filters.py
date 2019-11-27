def row(key, value):
    return '<strong>{}:</strong> {}'.format(key, value)


def object_names(objects):
    return ', '.join(obj['name'] for obj in objects)


def render_object(obj):
    if isinstance(obj, bool):
        return obj

    if isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float):
        return str(obj)

    obj = {k: v for k, v in obj.items() if v is not None}

    if 'type' not in obj:
        return obj['name']

    tooltip = [row(obj['name'], obj['type'])]

    if 'health' in obj:
        tooltip.append(row('Health', obj['health']))

    if 'hunger' in obj:
        tooltip.append(row('Hunger', obj['hunger']))

    if 'damage' in obj:
        tooltip.append(row('Damage', obj['damage']))

    if 'max_dmg' in obj and 'max_dmg' in obj:
        tooltip.append(row('Damage', '{} - {}'.format(obj['min_dmg'], obj['max_dmg'])))

    if 'shots_left' in obj:
        tooltip.append(row('Shots', obj['shots_left']))

    if 'food_value' in obj:
        tooltip.append(row('Food Value', obj['food_value']))

    if 'medicine_value' in obj:
        tooltip.append(row('Medicine Value', obj['medicine_value']))

    if 'inventory' in obj:
        tooltip.append(row('Inventory', object_names(obj['inventory'])))

    if 'objects' in obj:
        tooltip.append(row('Objects', object_names(obj['objects'])))

    if 'owner' in obj:
        tooltip.append(row('Owner', obj['owner']['name']))

    if 'place' in obj:
        tooltip.append(row('Place', obj['place']['name']))

    tooltip_text = '<br>'.join(tooltip)
    return '<span data-toggle="tooltip" title="{}" class="game-object">{}</span>'.format(tooltip_text, obj['name'])


def icon(name):
    return '<i class="fa fa-{}"></i>'.format(name)


def render_event(event):
    event_type = event[0]
    params = map(render_object, event[1:])

    if event_type == 'MOVE':
        return '{} moved from {} to {}'.format(*params)

    if event_type == 'TOOK':
        return '{} picked up {}'.format(*params)

    if event_type == 'ATE':
        return '{} ate {}'.format(*params)

    if event_type == 'ATTACK':
        return '{} {} attacked {} for <strong>{}</strong> damage'.format(icon('crosshairs'), *params)

    if event_type == 'LOAD':
        tribute, weapon, ammo, success = params
        if success:
            return '{} loaded {} with {}'.format(tribute, weapon, ammo)
        else:
            return '{} <strong class="text-danger">cannot</strong> load {} with {}'.format(tribute, weapon, ammo)

    if event_type == 'INPUT_ERROR':
        return '{} {} raised exception: <span class="text-danger">{}</span>'.format(icon('warning'), *params)

    if event_type == 'SPAWNED':
        return '{} {} <strong>spawned</strong>'.format(icon('heart'), *params)

    if event_type == 'STARVED':
        return '{} {} <strong>starved</strong> to death'.format(icon('times'), *params)

    if event_type == 'KILLED':
        return '{} {} <strong>killed</strong> {}'.format(icon('times'), *params)

    if event_type == 'SURVIVED':
        return '{} <strong class="text-success">{} survived</strong>'.format(icon('trophy'), *params)

    return ''
