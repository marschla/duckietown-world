# coding=utf-8
import argparse
import json
import os
import sys

from .misc import draw_static
from duckietown_world.world_duckietown import DuckietownMap
from duckietown_world.world_duckietown.map_loading import list_maps, load_gym_map

__all__ = [
    'draw_maps_main',
]


def draw_maps_main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="output dir", default='out-draw_maps')
    parsed = parser.parse_args(args)

    output = parsed.output

    map_names = list_maps()
    print(map_names)

    for map_name in map_names:
        duckietown_map = load_gym_map(map_name)
        out = os.path.join(output, map_name)

        draw_map(out, duckietown_map)

        y = duckietown_map.as_json_dict()
        fn = os.path.join(out, 'map.json')
        with open(fn, 'w') as f:
            f.write(json.dumps(y, indent=4))
        print('written to %s' % fn)


def draw_map(output, duckietown_map):
    if not os.path.exists(output):
        os.makedirs(output)
    assert isinstance(duckietown_map, DuckietownMap)

    draw_static(duckietown_map, output_dir=output, pixel_size=(640, 640), area=None)


if __name__ == '__main__':
    draw_maps_main()
