def linear_animation(start_value: float, end_value: float, current_time: float) -> float:
    return start_value + (end_value - start_value) * current_time


def ease_out_animation(start_value: float, end_value: float, current_time: float) -> float:
    return start_value + (end_value - start_value) * (1 - (1 - current_time) ** 2)


def ease_in_animation(start_value: float, end_value: float, current_time: float) -> float:
    return start_value + (end_value - start_value) * current_time ** 2


def ease_in_out_animation(start_value: float, end_value: float, current_time: float) -> float:
    if current_time < 0.5:
        return start_value + (end_value - start_value) * (2 * current_time) ** 2 / 2
    else:
        return start_value + (end_value - start_value) * (1 - (-2 * current_time + 2) ** 2 / 2)


def cubic_bezier_animation(start_value: float, end_value: float, current_time: float, p0: float, p1: float,
                           p2: float, p3: float) -> float:
    NotImplementedError("Cubic Bezier animation is not implemented yet.")


if __name__ == "__main__":
    # Test the functions
    for i in range(100):
        print(ease_in_animation(-100, 300, i / 100))
