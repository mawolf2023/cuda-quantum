# ============================================================================ #
# Copyright (c) 2022 - 2023 NVIDIA Corporation & Affiliates.                   #
# All rights reserved.                                                         #
#                                                                              #
# This source code and the accompanying materials are made available under     #
# the terms of the Apache License 2.0 which accompanies this distribution.     #
# ============================================================================ #

#[Begin Observe1]

import cudaq
from cudaq import spin

cudaq.set_target('nvidia')

operator = spin.z(0)
print(operator)

@cudaq.kernel(jit=True)
def observe_kernel():

    reg  = cudaq.qvector(1)

    h(reg[0])

# [1+0j] Z

#[End Observe1]

#[Begin Observe2]

observe_results = cudaq.observe(observe_kernel, operator)
print(observe_results.expectation())

# 0.0

#[End Observe2]


#[Begin Observe3]

observe_results = cudaq.observe(observe_kernel, operator, shots_count = 1000)

print(observe_results.expectation())

# 0.026000000000000023

#[End Observe3]










