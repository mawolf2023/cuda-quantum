Building Quantum Kernels and Applying Gates
-------------------

Welcome to the CUDA-Q documentation. This guide will help you understand how to use CUDA-Q for building and applying quantum kernels.

Defining Kernels
+++++++++++++++++++++++++++++++++++++++++

Kernels are the building blocks of quantum algorithms in CUDA-Q. A kernel is specified by using the following syntax:

.. code-block:: python

    @cudaq.kernel
    def kernel():
        A = cudaq.qubit()
        B = cudaq.qvector(3)
        C = cudaq.qvector(5)

Kernels can also take a variety of objects as inputs. This is accomplished by specifying a parameter in the kernel definition along with the appropriate type. The kernel below takes an integer to define a register of N qubits.

.. code-block:: python

    @cudaq.kernel
    def kernel(N: int):
        register = cudaq.qvector(N)

Initializing States
+++++++++++++++++++++++++++++++++++++++++

It is often helpful to define an initial state for a kernel. There are a few ways to do this in CUDA-Q. Note 5 is particularly useful for cases where the state of one kernel is passed into a second kernel to prepare its initial state.

1) Passing Complex Vectors as Parameters

.. code-block:: python

   c = [0.70710678 + 0j, 0., 0., 0.70710678]

   @cudaq.kernel
   def kernel(vec: list[complex]):
       q = cudaq.qvector(vec)

2) Capturing Complex Vectors

.. code-block:: python

   c = [0.70710678 + 0j, 0., 0., 0.70710678]

   @cudaq.kernel
   def kernel():
       q = cudaq.qvector(c)

3) Precision-Agnostic API

.. code-block:: python

   import numpy as np

   c = np.array([0.70710678 + 0j, 0., 0., 0.70710678], dtype=cudaq.complex())

   @cudaq.kernel
   def kernel():
       q = cudaq.qvector(c)

4) Define as CUDA-Q amplitudes

.. code-block:: python

   c = cudaq.amplitudes([0.70710678 + 0j, 0., 0., 0.70710678], dtype=cudaq.complex())

   @cudaq.kernel
   def kernel():
       q = cudaq.qvector(c)

5) Pass in a state from another kernel

.. code-block:: python

   c = [0.70710678 + 0j, 0., 0., 0.70710678]

   @cudaq.kernel
   def kernel_initial():
       q = cudaq.qvector(c)

   state_to_pass = cudaq.get_state(kernel_initial)

   @cudaq.kernel
   def kernel(state: cudaq.State):
       q = cudaq.qvector(state)

   kernel(state_to_pass)

Applying Gates
+++++++++++++++++++++++++++++++++++++++++

After a kernel is constructed, gates can be applied to start building out a quantum circuit.

Gates can be applied to all qubits in a register:

.. code-block:: python

    @cudaq.kernel
    def kernel():
        register = cudaq.qvector(10)
        h(register)

A single qubit in a register:

.. code-block:: python

    @cudaq.kernel
    def kernel():
        register = cudaq.qvector(10)
        h(register[0])  # first qubit
        h(register[-1])  # last qubit

or some subset of a register.

.. code-block:: python

    @cudaq.kernel
    def kernel():
        register = cudaq.qvector(10)
        swap(register[0], register[1])  # swap qubit 0 and 1
        h(register[0:5])  # h applied to first 5 qubits

Controlled Operations
+++++++++++++++++++++++++++++++++++++++++

Controlled operations are available for any gate and can be used by adding `.ctrl` to the end of any gate, followed by specification of the control qubit and the target qubit.

.. code-block:: python

    @cudaq.kernel
    def kernel():
        register = cudaq.qvector(10)
        x.ctrl(register[0], register[1])  # CNOT gate applied with qubit 0 as control

Multi-Controlled Operations
+++++++++++++++++++++++++++++++++++++++++

It is valid for more than one qubit to be used for multi-controlled gates. The control qubits are specified as a list.

.. code-block:: python

    @cudaq.kernel
    def kernel():
        register = cudaq.qvector(10)
        x.ctrl([register[0], register[1]], register[2])  # X applied to qubit two controlled by qubit 0 and 1

Adjoint Operations
+++++++++++++++++++++++++++++++++++++++++

The adjoint of any gate can be applied by appending the gate with the `adj` designation.

.. code-block:: python

    @cudaq.kernel
    def kernel():
        register = cudaq.qvector(10)
        t.adj(register[0])

Custom Operations
+++++++++++++++++++++++++++++++++++++++++

Custom gate operations can be specified using `cudaq.register_operation`. A one-dimensional Numpy array specifies the unitary matrix to be applied.

.. code-block:: python

    import numpy as np

    cudaq.register_operation("custom_x", np.array([0, 1, 1, 0]))

    @cudaq.kernel
    def kernel():
        qubits = cudaq.qvector(2)
        h(qubits[0])
        custom_x(qubits[0])
        custom_x.ctrl(qubits[0], qubits[1])

Measurement
+++++++++++++++++++++++++++++++++++++++++

Kernel measurement can be specified in the Z, X, or Y basis using `mz`, `mx`, and `my`. If a measurement is specified with no argument, the entire kernel is measured in that basis.

.. code-block:: python

    @cudaq.kernel
    def kernel():
        qubits = cudaq.qvector(2)
        mz()

Specific qubits or registers can be measured rather than the entire kernel.

.. code-block:: python

    @cudaq.kernel
    def kernel():
        qubits_a = cudaq.qvector(2)
        qubit_b = cudaq.qubit()
        mz(qubits_a)
        mx(qubit_b)

Using Kernels Inside Other Kernels
+++++++++++++++++++++++++++++++++++++++++

For many complex applications, it is helpful to use a kernel inside of another kernel.

.. code-block:: python

    @cudaq.kernel
    def kernel_A(qubit_0: cudaq.qubit, qubit_1: cudaq.qubit):
        x.ctrl(qubit_0, qubit_1)

    @cudaq.kernel
    def kernel_B():
        reg = cudaq.qvector(10)
        for i in range(5):
            kernel_A(reg[i], reg[i + 1])

Parameterized Kernels
+++++++++++++++++++++++++++++++++++++++++

It is often useful to define parameterized circuit kernels which can be used for applications like VQE.

.. code-block:: python

    @cudaq.kernel
    def kernel(thetas: list[float]):
        qubits = cudaq.qvector(2)
        rx(thetas[0], qubits[0])
        ry(thetas[1], qubits[1])

    thetas = [.024, .543]
