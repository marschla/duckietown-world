# coding=utf-8
from __future__ import unicode_literals
import json

import oyaml as yaml
from comptests import comptest, run_module_tests

from duckietown_serialization_ds1 import Serializable
from duckietown_serialization_ds1 import GenericData


class MyClass(Serializable):
    def __init__(self, x, y):
        self.x = x
        self.y = y


@comptest
def ser1():
    ob = MyClass(0, MyClass(1, {'a': 'b'}))
    d = ob.as_json_dict()
    d_json = json.dumps(d, indent=4)
    print(d_json)
    d_yaml = yaml.safe_dump(d, default_flow_style=False)
    print(d_yaml)

    d2_json = json.loads(d_json)
    d2_yaml = yaml.load(d_yaml)

    ob1 = Serializable.from_json_dict(d2_json)

    assert isinstance(ob1.y, MyClass), ob1
    ob2 = Serializable.from_json_dict(d2_yaml)
    assert isinstance(ob2.y, MyClass), ob2

    print(ob2)
    ob2_json = json.dumps(ob2.as_json_dict(), indent=4)
    print(ob2_json)


@comptest
def ser2():
    class MyClass2(Serializable):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    Serializable.registered.pop('MyClass2')
    ob = MyClass2(0, MyClass2(1, {'a': 'b'}))
    d = ob.as_json_dict()
    d_json = json.dumps(d, indent=4)
    print(d_json)
    d_yaml = yaml.safe_dump(d, default_flow_style=False)
    print(d_yaml)

    d2_json = json.loads(d_json)
    d2_yaml = yaml.load(d_yaml)

    ob1 = Serializable.from_json_dict(d2_json)
    print(ob1)
    ob2 = Serializable.from_json_dict(d2_yaml)
    print(ob2)

    ob2.y.x

    ob2_json = json.dumps(ob2.as_json_dict(), indent=4)
    print(ob2_json)


def try_serialization(ob):
    d = ob.as_json_dict()
    d_json = json.dumps(d, indent=4)
    print(d_json)
    d_yaml = yaml.safe_dump(d, default_flow_style=False)
    print(d_yaml)

    d2_json = json.loads(d_json)
    d2_yaml = yaml.load(d_yaml)

    ob1 = Serializable.from_json_dict(d2_json)
    print(ob1)
    ob2 = Serializable.from_json_dict(d2_yaml)
    print(ob2)

    ob2_json = json.dumps(ob2.as_json_dict(), indent=4)
    print(ob2_json)
    return ob2


@comptest
def ser3():
    class MyBase(Serializable):
        def __init__(self, a):
            self.a = a

        def params_to_json_dict(self):
            return dict(a=self.a)

    class MyDer(MyBase):
        def __init__(self, x, y, *args, **kwargs):
            self.x = x
            self.y = y
            MyBase.__init__(self, *args, **kwargs)

        def params_to_json_dict(self):
            return dict(x=self.x, y=self.y)

    # Serializable.registered.pop('MyClass2')
    ob = MyDer(1, 2, 3)
    ob2 = try_serialization(ob)


@comptest
def ser4():
    ob = GenericData(b'ijdeijdiej', 'image/jpg')
    ob2 = try_serialization(ob)


if __name__ == '__main__':
    run_module_tests()
