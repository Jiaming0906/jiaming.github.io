import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from filters import render_object, render_event

try:
    from config import FILES, GLOBALS
except ImportError:
    print('ERROR: config.py not found. Copy config.example.py to config.py and edit the settings.')
    exit(1)

env = Environment(loader=FileSystemLoader('templates'),
                  autoescape=select_autoescape(),
                  lstrip_blocks=True,
                  trim_blocks=True)

env.filters['game_object'] = render_object
env.filters['game_event'] = render_event
env.globals.update(GLOBALS)

templates = {
    'home': env.get_template('pages/index.html'),
    'gamelog': env.get_template('pages/gamelog.html'),
}

rounds = []

for title, match_file, winners in FILES:
    rounds.append({
        'title': title,
        'winners': winners,
        'path': match_file,
        'games': json.load(Path(match_file, 'matches.json').open()),
    })

home = templates['home'].render(Path=Path, groups=rounds)

with open('static/index.html', mode='w', encoding='utf-8') as f:
    f.write(home)

for game_round in rounds:
    for match in game_round['games']:
        file = Path(game_round['path'], match['file']).with_suffix('.json')

        try:
            data = json.load(file.open())
        except OSError:
            print('Cannot find ' + str(file))
            continue

        path = Path('static', game_round['path'], match['file']).with_suffix('.html')
        html = templates['gamelog'].render(**data, winners=game_round['winners'])

        path.parent.mkdir(parents=True, exist_ok=True)
        path.open('w', encoding='utf-8').write(html)
