# ============================================================================ #
# Copyright (c) 2022 - 2023 NVIDIA Corporation & Affiliates.                   #
# All rights reserved.                                                         #
#                                                                              #
# This source code and the accompanying materials are made available under     #
# the terms of the Apache License 2.0 which accompanies this distribution.     #
# ============================================================================ #


import cudaq

cudaq.set_target('nvidia')

@cudaq.kernel(jit=True)
def sample_kernel(n_qubits: int):

    reg  = cudaq.qvector(n_qubits)
   
    h(reg[0])

    for qubit in range(n_qubits-1):
        x.ctrl(reg[qubit], reg[qubit+1])

    mz(reg)    




#[Begin Time]

import timeit

code_to_time = 'cudaq.sample(sample_kernel, qubit_count, shots_count=1000000 )'
qubit_count = 25

cudaq.set_target('qpp-cpu')
print('CPU time')
print( timeit.timeit(stmt = code_to_time, globals=globals(), number = 1))

cudaq.set_target('nvidia')
print('GPU time')
print( timeit.timeit(stmt = code_to_time, globals=globals(), number = 1))

# CPU Time
# 27.57462245109491
# GPU Time
# 0.7732861610129476


#[End Time]










