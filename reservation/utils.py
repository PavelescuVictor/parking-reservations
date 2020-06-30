import datetime


def date_intervals_overlap(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2
    start1 = start1.replace(tzinfo=None)
    start2 = start2.replace(tzinfo=None)
    end1 = end1.replace(tzinfo=None)
    end2 = end2.replace(tzinfo=None)
    return (start1 <= start2 <= end1) or (start2 <= start1 <= end2)
