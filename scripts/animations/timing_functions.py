def linear_animation(start_value, end_value, current_time):
    return start_value + (end_value - start_value) * current_time


def ease_out_animation(start_value, end_value, current_time):
    return start_value + (end_value - start_value) * (1 - (1 - current_time) ** 2)


def ease_in_animation(start_value, end_value, current_time):
    return start_value + (end_value - start_value) * current_time ** 2


def ease_in_out_animation(start_value, end_value, current_time):
    if current_time < 0.5:
        return start_value + (end_value - start_value) * (2 * current_time) ** 2 / 2
    else:
        return start_value + (end_value - start_value) * (1 - (-2 * current_time + 2) ** 2 / 2)


def cubic_bezier_animation(start_value, end_value, current_time, p0, p1, p2, p3):
    return start_value + (end_value - start_value) * (1 - current_time) ** 3 * p0 + 3 * (1 - current_time) ** 2 *\
        current_time * p1 + 3 * (1 - current_time) * current_time ** 2 * p2 + current_time ** 3 * p3

if __name__ == "__main__":
    for i in range(100):
        print(ease_in_animation(-100, 300, i / 100))
