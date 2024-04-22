from tour_shared.schema import parse_validation_error


def test_parse_nested():
    nested_validation_error = {
        'w': ['root -> w'],
        'x': ['root -> x'],
        'y': {
            'a': ['root -> y -> a'],
            'b': ['root -> y -> b']
        },
        'z': {
            'a': {
                'a': ['root -> z -> a -> a'],
                'b': {
                    'a': ['root -> z -> a -> b -> a']
                }
            },
            'b': ['root -> z -> b']
        }
    }
    result = parse_validation_error(nested_validation_error, parent_keys=["root"])
    assert result['root.w'] == 'root -> w'
    assert result['root.x'] == 'root -> x'
    assert result['root.y.a'] == 'root -> y -> a'
    assert result['root.y.b'] == 'root -> y -> b'
    assert result['root.z.a.a'] == 'root -> z -> a -> a'
    assert result['root.z.a.b.a'] == 'root -> z -> a -> b -> a'
    assert result['root.z.b'] == 'root -> z -> b'
