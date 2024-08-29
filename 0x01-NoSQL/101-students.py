#!/usr/bin/env python3
"""
This script defines a function to return all students
sorted by their average score in a MongoDB collection.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by their average score
    """
    students = mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ])

    return [student for student in students]
