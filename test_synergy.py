import sys, types
# Provide minimal stubs for external modules
sys.modules['requests'] = types.ModuleType('requests')
sys.modules['PIL'] = types.ModuleType('PIL')
sys.modules['PIL.Image'] = types.ModuleType('PIL.Image')
sys.modules['matplotlib'] = types.ModuleType('matplotlib')
sys.modules['matplotlib.pyplot'] = types.ModuleType('matplotlib.pyplot')
sys.modules['numpy'] = types.ModuleType('numpy')
sys.modules['mpl_toolkits'] = types.ModuleType('mpl_toolkits')
mpl_toolkits_mod = types.ModuleType('mpl_toolkits.mplot3d')
mpl_toolkits_mod.Axes3D = object
sys.modules['mpl_toolkits.mplot3d'] = mpl_toolkits_mod

from MTGDeck import MagicDeck


def test_synergy_matrix():
    deck = MagicDeck('test')
    # Provide a small synergy dataset without hitting the network
    deck.synergy_data = {
        'Zombie': {'Zombie': 1.0, 'Wizard': 0.75},
        'Wizard': {'Zombie': 0.75, 'Wizard': 1.0}
    }
    deck.cards = [
        {
            'name': 'Card A',
            'type_line': 'Creature — Zombie',
            'cmc': 1,
            'count': 1,
            'url': '',
            'power': '1',
            'toughness': '1',
            'keywords': []
        },
        {
            'name': 'Card B',
            'type_line': 'Creature — Zombie Wizard',
            'cmc': 2,
            'count': 1,
            'url': '',
            'power': '2',
            'toughness': '2',
            'keywords': []
        }
    ]
    matrix, names = deck.compute_synergy_matrix()
    assert names == ['Card A', 'Card B']
    assert abs(matrix[0][1] - 0.875) < 1e-6
    assert matrix[0][0] == 1
