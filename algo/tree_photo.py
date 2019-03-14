import math
import random

def degree(radians, offset=0):
    degrees = math.degrees(radians) + offset
    return '%.1f' % degrees

def wrap_angles(angles, fov):
    for angle in angles:
        yield angle

    for angle in angles:
        if angle + math.pi > fov:
            break

        yield angle + 2 * math.pi

def calc_max_number_of_trees(trees, field_of_view):
    if not trees or field_of_view <= 0:
        return 0

    if field_of_view >= 2 * math.pi:
        return len(trees)

    angles = (math.atan2(y, x) for x, y in trees)
    angles = list(sorted(angles))
    print [degree(angle, 180) for angle in angles]
    print [degree(angle, 180) for angle in wrap_angles(angles, field_of_view)]
    angles1 = wrap_angles(angles, field_of_view)
    angles2 = wrap_angles(angles, field_of_view)

    max_number = 0
    start_index = 0
    start_angle = angles1.next()
    for end_index, end_angle in enumerate(angles2):
        print '-' * 40
        while end_angle - start_angle > field_of_view:
            print '[X]', start_index, end_index, degree(end_angle - start_angle)
            start_index += 1
            start_angle = angles1.next()

        number = end_index - start_index + 1
        print '[V]', start_index, end_index, degree(end_angle - start_angle), '|',
        print number, max_number, '[NEW]' if number > max_number else '[N/A]'
        max_number = max(max_number, number)

    return max_number

def get_angle(angles, index):
    return angles[index] if index < len(angles) else angles[index - len(angles)] + 2 * math.pi

def calc2(trees, field_of_view):
    if not trees or field_of_view <= 0:
        return 0

    if field_of_view >= 2 * math.pi:
        return len(trees)

    angles = (math.atan2(y, x) for x, y in trees)
    angles = list(sorted(angles))
    print [degree(angle, 180) for angle in angles]

    max_number = 0
    end_index = 0
    end_angle = get_angle(angles, end_index)
    for start_index, start_angle in enumerate(angles):
        print '-' * 40
        while end_angle - start_angle <= field_of_view:
            number = end_index - start_index + 1
            print '[V]', start_index, end_index, degree(end_angle - start_angle), '|',
            print number, max_number, '[NEW]' if number > max_number else '[N/A]'
            max_number = max(max_number, number)
            end_index += 1
            end_angle = get_angle(angles, end_index)

        print '[X]', start_index, end_index, degree(end_angle - start_angle)

    return max_number

def calc3(trees, field_of_view):
    if not trees or field_of_view <= 0:
        return 0

    if field_of_view >= 2 * math.pi:
        return len(trees)

    angles = (math.atan2(y, x) for x, y in trees)
    angles = list(sorted(angles))
    print [degree(angle, 180) for angle in angles]

    max_number = 0
    start_index = 0
    start_angle = angles[start_index]
    end_index = 0
    end_angle = angles[end_index]
    while start_index < len(angles):
        if end_angle - start_angle <= field_of_view:
            number = end_index - start_index + 1
            print '[V]', start_index, end_index, degree(end_angle - start_angle), '|',
            print number, '->' if number > max_number else '..', max_number
            max_number = max(max_number, number)
            end_index += 1
            end_angle = get_angle(angles, end_index)
        else:
            print '[X]', start_index, end_index, degree(end_angle - start_angle)
            start_index += 1
            start_angle = get_angle(angles, start_index)

    return max_number

def foo(n, fov_degree):
    trees = [(random.randint(-100, 100), random.randint(-100, 100)) for _ in xrange(n)]
    fov = math.radians(fov_degree)
    print trees
    print '=' * 40
    n1 = calc_max_number_of_trees(trees, fov)
    print '=' * 40
    n2 = calc2(trees, fov)
    print '=' * 40
    n3 = calc3(trees, fov)
    print n1, n2, n3
