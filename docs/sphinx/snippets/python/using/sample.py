# ============================================================================ #
# Copyright (c) 2022 - 2023 NVIDIA Corporation & Affiliates.                   #
# All rights reserved.                                                         #
#                                                                              #
# This source code and the accompanying materials are made available under     #
# the terms of the Apache License 2.0 which accompanies this distribution.     #
# ============================================================================ #

#[Begin Sample1]

import cudaq

cudaq.set_target('nvidia')

@cudaq.kernel(jit=True)
def sample_kernel(n_qubits: int):

    reg  = cudaq.qvector(n_qubits)
   
    h(reg[0])

    for qubit in range(n_qubits-1):
        x.ctrl(reg[qubit], reg[qubit+1])

    mz(reg)    


qubit_count = 2
results = cudaq.sample(sample_kernel, qubit_count)
results.dump()

#{ 00:512 11:488 }

#[End Sample1] 


#[Begin Sample2]

results = cudaq.sample(sample_kernel, qubit_count, shots_count=10000)
results.dump()

#{ 00:5033 11:4967 }

#[End Sample2]


#[Begin Sample3]

print(results.most_probable())
print(results.probability(results.most_probable()))

# 00
# 0.5033

#[End Sample3]










