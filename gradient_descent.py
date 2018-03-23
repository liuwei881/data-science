# coding=utf-8

import random


def sum_of_squares(v):
    """给一个向量, 输出一个实数"""
    return sum(v_i ** 2 for v_i in v)


def difference_quotient(f, x, h):
    """求导数"""
    return (f(x + h) - f(x)) / h


def partial_difference_quotient(f, v, i, h):
    """compute the ith partial difference quotient of f at v"""
    w = [v_j + (h if j == i else 0) for j, v_j in enumerate(v)]
    return (f(w) - f(v)) / h


def estimate_gradient(f, v, h=0.00001):
    return [partial_difference_quotient(f, v, i, h) for i, _ in enumerate(v)]


def step(v, direction, step_size):
    """move step_size in the direction from v"""
    return [
        v_i +
        step_size *
        direction_i for v_i,
        direction_i in zip(
            v,
            direction)]


def sum_of_squares_gradient(v):
    return [2 * v_i for v_i in v]


v = [random.randint(-10, 10) for i in range(3)]
tolerance = 0.0000001
while True:
    gradient = sum_of_squares_gradient(v)
    next_v = step(v, gradient, -0.01)
    if distance(next_v, v) < tolerance:
        break
    v = next_v

step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]


def safe(f):
    """return a new function that's the same as f,
    except that it outputs infinity whenever f produces an error"""
    def safe_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return float('inf')
    return safe_f


def minimize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
    """use gradient descent to find theta that minimizes target function"""
    step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    theta = theta_0
    target_fn = safe(target_fn)
    value = target_fn(theta)
    # 设定theta为初始值 # target_fn的安全版 # 我们试图最小化的值
    while True:
        gradient = gradient_fn(theta)
        next_thetas = [step(theta, gradient, -step_size)
                       for step_size in step_sizes]
        next_theta = min(next_thetas, key=target_fn)
        next_value = target_fn(next_theta)
        # 当“收敛”时停止
        if abs(value - next_value) < tolerance:
            return theta
        else:
            theta, value = next_theta, next_value


def negate(f):
    """return a function that for any input x returns -f(x)"""
    return lambda *args, **kwargs: -f(*args, **kwargs)


def negate_all(f):
    """the same when f returns a list of numbers"""
    return lambda *args, **kwargs: [-y for y in f(*args, **kwargs)]


def maximize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
    return minimize_batch(
        negate(target_fn),
        negate_all(gradient_fn),
        theta_0,
        tolerance)


def in_random_order(data):
    """generator that returns the elements of data in random order"""
    indexes = [i for i, _ in enumerate(
        data)]  # 生成索引列表 random.shuffle(indexes) # 随机打乱数据
    for i in indexes:  # 返回序列中的数据
        yield data[i]


def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
    data = zip(x, y)
    theta = theta_0
    alpha = alpha_0
    min_theta, min_value = None, float("inf")
    iterations_with_no_improvement = 0
    # 如果循环超过100次仍无改进，停止
    while iterations_with_no_improvement < 100:
        # 初始值猜测
        # 初始步长
        # 迄今为止的最小值
        value = sum( target_fn(x_i, y_i, theta) for x_i, y_i in data )
        if value < min_value:
        # 如果找到新的最小值，记住它
        # 并返回到最初的步长
            min_theta, min_value = theta, value iterations_with_no_improvement = 0 alpha = alpha_0
        else:
        # 尝试缩小步长，否则没有改进 iterations_with_no_improvement += 1 alpha *= 0.9
        # 在每个数据点上向梯度方向前进一步
            for x_i, y_i in in_random_order(data):
                 gradient_i = gradient_fn(x_i, y_i, theta)
                 theta = vector_subtract(theta, scalar_multiply(alpha, gradient_i))
    return min_theta


def maximize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
    return minimize_stochastic(negate(target_fn), negate_all(gradient_fn), x, y, theta_0, alpha_0)
