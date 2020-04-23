# coding=utf-8
from .ser1 import *


def jobs_comptests(context):
    # instantiation
    # from comptests import jobs_registrar
    from comptests.registrar import jobs_registrar_simple
    jobs_registrar_simple(context)
