# coding=utf-8
from __future__ import unicode_literals

import copy

import six
from contracts import contract, check_isinstance

from duckietown_serialization_ds1 import Serializable
from duckietown_world.seqs import SampledSequence, UndefinedAtTime
from duckietown_world.svg_drawing import draw_axes
from .rectangular_area import RectangularArea
from .transforms import Transform

__all__ = [
    'PlacedObject',
    'SpatialRelation',
    'GroundTruth',
]


class SpatialRelation(Serializable):

    @contract(a='seq(str|unicode)', b='seq(str|unicode)')
    def __init__(self, a, transform, b):
        check_isinstance(transform, (Transform, SampledSequence))
        self.a = tuple(a)
        self.transform = transform
        self.b = tuple(b)

    def filter_all(self, f):
        return SpatialRelation(self.a, f(self.transform), self.b)

    @classmethod
    def params_from_json_dict(cls, d):
        a = d.pop('a', [])
        b = d.pop('b')
        transform = d.pop('transform')
        return dict(a=a, b=b, transform=transform)

    def params_to_json_dict(self):
        res = {}
        if self.a:
            res['a'] = list(self.a)
        res['b'] = self.b
        res['transform'] = self.transform
        return res


class GroundTruth(SpatialRelation):
    def params_to_json_dict(self):
        return {}


class PlacedObject(Serializable):
    def __init__(self, children=None, spatial_relations=None):
        children = children or {}
        spatial_relations = spatial_relations or {}

        self.children = children

        for k, v in list(spatial_relations.items()):
            from .transforms import Transform
            if isinstance(v, Transform):
                if k in self.children:
                    sr = GroundTruth(a=(), b=(k,), transform=v)
                    spatial_relations[k] = sr
                else:
                    msg = 'What is the "%s" referring to?' % k
                    raise ValueError(msg)

        self.spatial_relations = spatial_relations

        if not spatial_relations:
            for child in self.children:
                from duckietown_world import SE2Transform
                sr = GroundTruth(a=(), b=(child,), transform=SE2Transform.identity())
                self.spatial_relations[child] = sr

    def filter_all(self, f):
        x = copy.copy(self)
        children = {}
        spatial_relations = {}

        no_child = []
        for child_name, child in list(x.children.items()):
            try:
                child2 = f(child.filter_all(f))
            except UndefinedAtTime:
                no_child.append(child_name)
            else:
                children[child_name] = child2

        for sr_name, sr in list(x.spatial_relations.items()):
            if sr.b and sr.b[0] in no_child:
                pass
            else:
                try:
                    sr2 = f(sr.filter_all(f))
                except UndefinedAtTime:
                    pass
                else:
                    spatial_relations[sr_name] = sr2
        x.children = children
        x.spatial_relations = spatial_relations
        return x

    def get_object_from_fqn(self, fqn):
        if fqn == ():
            return self
        first, rest = fqn[0], fqn[1:]
        if first in self.children:
            return self.children[first].get_object_from_fqn(rest)
        else:
            msg = 'Cannot find child %s in %s' % (first, list(self.children))
            raise KeyError(msg)

    def params_to_json_dict(self):
        res = {}

        if self.children:
            res['children'] = self.children
        if self.spatial_relations:
            res['spatial_relations'] = self.spatial_relations

        return res

    def set_object(self, name, ob, **transforms):
        check_isinstance(name, six.string_types)
        assert self is not ob
        self.children[name] = ob
        type2klass = {
            'ground_truth': GroundTruth
        }
        for k, v in transforms.items():
            klass = type2klass[k]
            st = klass(a=(), b=(name,), transform=v)
            i = len(self.spatial_relations)
            self.spatial_relations[i] = st

    # @abstractmethod
    def draw_svg(self, drawing, g):
        draw_axes(drawing, g)

    def get_drawing_children(self):
        return sorted(self.children)

    def extent_points(self):
        return [(0.0, 0.1), (0.1, 0.0)]

    def get_footprint(self):
        return RectangularArea([-0.1, -0.1], [0.1, 0.1])
