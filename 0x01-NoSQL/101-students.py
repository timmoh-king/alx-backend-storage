#!/usr/bin/env python3

"""
    a Python function that returns all students sorted by average score:
    Prototype: def top_students(mongo_collection):
    mongo_collection will be the pymongo collection object
    The top must be ordered
    The average score must be part of each item returns with key = avgScore
"""

def top_students(mongo_collection):
    """returns all students sorted by average score:"""
    db.mongo_collection.aggregate([
        {
            '$project': {
                'name': 1,
                'averageScore': {'$avg': '$topics.score'}
                }
            },
        {'$sort': {'avarageScore': -1}}
        ])
