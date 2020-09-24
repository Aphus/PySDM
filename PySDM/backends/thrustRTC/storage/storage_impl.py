"""
Created at 02.06.2020
"""

from ..conf import trtc
from PySDM.backends.thrustRTC.nice_thrust import nice_thrust
from PySDM.backends.thrustRTC.conf import NICE_THRUST_FLAGS


def thrust(obj):
    if isinstance(obj, list):
        result = [thrust(o) for o in obj]
    elif hasattr(obj, 'data'):
        result = obj.data
    elif isinstance(obj, float):
        result = trtc.DVDouble(obj)
    elif isinstance(obj, int):
        result = trtc.DVInt64(obj)
    else:
        raise ValueError(f"Cannot upload {obj} to device.")
    return result


@nice_thrust(**NICE_THRUST_FLAGS)
def add(output, addend):
    trtc.Transform_Binary(thrust(addend), thrust(output), thrust(output), trtc.Plus())


__row_modulo_body = trtc.For(['output', 'divisor', 'length'], "i", '''
        int d = i / length;
        output[i] %= divisor[d];
    ''')


@nice_thrust(**NICE_THRUST_FLAGS)
def row_modulo(output, divisor):
    __row_modulo_body.launch_n(len(output), thrust([output, divisor, output.shape[1]]))


__floor_body = trtc.For(['arr'], "i", '''
        if (arr[i] >= 0) {
            arr[i] = (long) arr[i];
        }
        else {
            auto old = arr[i];
            arr[i] = (long) arr[i];
            if (old != arr[i]) {
                arr[i] -= 1;
            }
        }
    ''')


@nice_thrust(**NICE_THRUST_FLAGS)
def floor(output):
    __floor_body.launch_n(len(output), thrust([output]))


__floor_out_of_place_body = trtc.For(['output', 'input_data'], "i", '''
        if (input_data[i] >= 0) {
            output[i] = (long) input_data[i];
        }
        else {
            output[i] = (long) input_data[i];
            if (input_data[i] != output[i]) {
                output[i] -= 1;
            }
        }
    ''')


@nice_thrust(**NICE_THRUST_FLAGS)
def floor_out_of_place(output, input_data):
    __floor_out_of_place_body.launch_n(len(output), thrust([output, input_data]))


__multiply_elementwise_body = trtc.For(['output', 'multiplier'], "i", '''
        output[i] *= multiplier[i];
    ''')

__multiply_body = trtc.For(['output', 'multiplier'], "i", '''
        output[i] *= multiplier;
    ''')


@nice_thrust(**NICE_THRUST_FLAGS)
def multiply(output, multiplier):
    if hasattr(multiplier, 'data'):
        loop = __multiply_elementwise_body
    else:
        loop = __multiply_body
    loop.launch_n(len(output), thrust([output, multiplier]))


__multiply_out_of_place_elementwise_body = trtc.For(['output', 'multiplicand', 'multiplier'], "i", '''
        output[i] = multiplicand[i] * multiplier[i];
    ''')

__multiply_out_of_place_body = trtc.For(['output', 'multiplicand', 'multiplier'], "i", '''
        output[i] = multiplicand[i] * multiplier;
    ''')


@nice_thrust(**NICE_THRUST_FLAGS)
def multiply_out_of_place(output, multiplicand, multiplier):
    if hasattr(multiplier, 'data'):
        loop = __multiply_out_of_place_elementwise_body
    elif isinstance(multiplier, float):
        loop = __multiply_out_of_place_body
    else:
        raise NotImplementedError()
    loop.launch_n(len(output), thrust([output, multiplicand, multiplier]))


__power_body = trtc.For(['output', 'exponent'], "i", '''
        output[i] = pow(output[i], exponent);
    ''')


@nice_thrust(**NICE_THRUST_FLAGS)
def power(output, exponent: int):
    if exponent == 1:
        return
    __power_body.launch_n(len(output), thrust([output, float(exponent)]))


__subtract_body = trtc.For(['output', 'subtrahend'], 'i', '''
        output[i] -= subtrahend[i];
    ''')


@nice_thrust(**NICE_THRUST_FLAGS)
def subtract(output, subtrahend):
    __subtract_body.launch_n(len(output), thrust([output, subtrahend]))
