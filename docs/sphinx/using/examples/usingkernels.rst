Using Quantum Kernels
-------------------

Sampling
+++++++++++++++++++++++++++++++++++++++++

The `cudaq.sample` function is used to produce a sample of bitstring measurements corresponding to the distribution defined by the quantum state of a kernel.The example below illustrates the construction and sampling of a Bell State kernel. The kernel and any required kernel parameters are the only inputs required for `cudaq.sample`. The dump method prints the dictionary containing the bitstrings and their results.



.. code-block:: python
   N = 2


   @cudaq.kernel
   def bell_state_kernel(qubits: int):
       reg = cudaq.qvector(qubits)
       h(reg[0])
       x.ctrl(reg[0], reg[1])


   results = cudaq.sample(bell_state_kernel, N)
   results.dump()

By default, `cudaq.sample()` produces 1000 samples. This can be changed by specifying the number of shots: `cudaq.sample(kernel, shots_count = 5000)`.


Processing Sample Results
+++++++++++++++++++++++++++++++++++++++++
The results of a `cudaq.sample()` call are stored in a `SampleResult` object which can be processed in a number of helpful ways. The examples below show some of the helpful tools for obtaining the most important results from a sample. For a full description of `SampleResult` methods, see the API guide here (link).


.. code-block:: python
   
   #Outputs the full sample dictionary
   results.dump()

   #{11:487, 00:513}
   
   #Provides the count of the specified bitstring
   results.count(‘11’)

   #487

   #Provides the probability of a specified bitstring
   results.probability(‘11’)

   #0.487

   #Provides the most probable bitstring
   results.most_probable()

   #00


Mid-circuit Measurement and Conditional Logic
+++++++++++++++++++++++++++++++++++++++++


Kernels can be constructed such that measurements control the application of additional operations. The example below starts with a kernel consisting of a single  Hadamard gate acting on qubit 0. Then, qubit 0 is measured using `mz(q[0])`. If the result (`b0`) is 1, a Hadamard gate is performed on qubit 1.  The kernel concludes with a measurement of qubit 1.



.. code-block:: python
 
   @cudaq.kernel
   def kernel():
       q = cudaq.qvector(2)
       h(q[0])
       b0 = mz(q[0])
       if b0:
           h(q[1])
       mz(q[1])


   counts = cudaq.sample(kernel, shots_count=1000)
   counts.dump()

   #{ 
   #  __global__ : { 1:256 0:744 }
   #   b0 : { 1:481 0:519 }
   #}

The `dump` command produces counts for the mid-circuit measurements (b0) and the global register. Notice that the b0 results are a 50/50 split, while the global (qubit 1) measurements are 25/75, an expected result if the Hadamard was applied to qubit 1 with 50% probability.  


Expectation Values (Observe)
+++++++++++++++++++++++++++++++++++++++++

Expectation values are obtained in CUDA-Q with the `observe` command. First, you must specify a spin operator as the target observable.  See the section on spin operators for more information (link). Observe follows the same syntax as `sample` except that the observable needs to be specified followed by any additional kernel arguments. Note, do not specify a measure command when computing expectation values, otherwise the result will only correspond to one measurement result and not an average.

.. code-block:: python

   observable  = spin.x(1)
   N=2

   @cudaq.kernel
   def kernel(qubits: int):
       reg  = cudaq.qvector(qubits)
       h(reg[0])
       x.ctrl(reg[0], reg[1])

   observe_result   = cudaq.observe(kernel, observable, N)
   print(observe_result.expectation())

The  `expectation` command then returns the desired expectation value.  By default, the result corresponds to the exact expectation value. The `shots_count` parameter can be specified if a finite number of shots is needed.


Variational Quantum Eigensolver (VQE) Wrapper
+++++++++++++++++++++++++++++++++++++++++

A common application that requires expectation values is the variational quantum eigensolver. CUDA-Q has a wrapper function that allows easy execution of VQE experiments. To use, specify a parameterized kernel (link), a spin operator (link), an optimizer (link), and the number of parameters as an inputs to the `vqe` function. Calling the function below will return the optimized expectation value and the associated variational parameters.

.. code-block:: python

   hamiltonian = spin.z(0)
   optimizer = cudaq.optimizers.COBYLA()


   @cudaq.kernel
   def vqe_kernel(thetas: list[float]):
       qubits = cudaq.qvector(2)
       rx(thetas[0], qubits[0])
       ry(thetas[1], qubits[1])


   exp_value, parameters = cudaq.vqe(kernel=vqe_kernel,
                                  spin_operator=hamiltonian,
                                  optimizer=optimizer,
                                  parameter_count=2)
   
   print(f"Expectation value: {exp_value}")
   print(f"Optimal parameters: {parameters}")

   #-0.9999999999999981
   #[3.141592653589793, 0.0]

CUDA-Q can also build standard ansatze like the UCCSD ansatz for chemistry. See the VQE tutorial found here (link) to learn how to build a UCCSD ansatz kernel from a specified molecule.




Obtaining the State Vector
+++++++++++++++++++++++++++++++++++++++++

If the desired output is not a sample or expectation value, the get state method provides a convenient way to produce the state vector of the kernel. The command `get_state` is provided with the kernel and produces a state vector object that can be easily transformed into a numpy array.

.. code-block:: python

   import numpy as np

   print(np.array(cudaq.get_state(bell_state_kernel, 2)))

   #[0.70710677+0.j 0.        +0.j 0.        +0.j 0.70710677+0.j]

Pauli Words and Exponentiating Pauli Words
+++++++++++++++++++++++++++++++++++++++++
Pauli Words and Exponentiating Pauli Words
+++++++++++++++++++++++++++++++++++++++++
