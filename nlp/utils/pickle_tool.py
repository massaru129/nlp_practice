# -*- coding: utf-8 -*-

__author__ = "masaru"

try:
    import cPickle as pickle
except:
    import pickle


def dump_object(object, filename):
    with open(filename, "w") as f:
        pickle.dump(object, f)


def load_object(filename):
    try:
        with open(filename, "r") as f:
            object = pickle.load(f)
        return object
    except IOError:
        return None