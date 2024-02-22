CUDA Quantum Basics
*******************

.. _cudaq-basics-landing-page:

What is a CUDA Quantum kernel?
-------------------------------

Quantum kernels are defined as functions that are executed on a quantum processing unit (QPU) or
a simulator. They generalize quantum circuits and provide a new abstraction for quantum programming.
Quantum kernels can be combined with classical functions to create quantum-classical applications
that can be executed on a heterogeneous system of QPUs, GPUs, and CPUs to solve real-world problems.

**What’s the difference between a quantum kernel and a quantum circuit?**

Every quantum circuit is a kernel, but not every quantum kernel is a circuit. For instance, a quantum
kernel can be built up from other kernels, allowing us to interpret a large quantum program as a sequence
of subroutines or subcircuits.  

Moreover, since quantum kernels are functions, there is more expressibility available compared to a
standard quantum circuit. We can not only parameterize the kernel, but can also apply classical controls
(`if`, `for`, `while`, etc.). As functions, quantum kernels can return void, Boolean values, integers,
floating point numbers, and vectors of Boolean values. Conditional statements on quantum memory and qubit
measurements can be included in quantum kernels to enable dynamic circuits and fast feedback, particularly
useful for quantum error correction. 

**How do I build and run a quantum kernel?**

Once a quantum kernel has been defined in a program, it can be executed using the `sample` or the `observe` primitives.
Let’s take a closer look at how to build and execute a quantum kernel with CUDA Quantum.


Building your first CUDA Quantum Program
-----------------------------------------

.. tab:: Python

  We can define our quantum kernel as we do any other function in Python, through the use of the
  `@cudaq.kernel` decorator. Let's begin with a simple GHZ-state example, producing a state of
  maximal entanglement amongst an allocated set of qubits. 
  
  .. literalinclude:: ../snippets/python/using/first_kernel.py
      :language: python
      :start-after: [Begin Documentation]
      :end-before: [End Documentation]

  This kernel function can accept any number of arguments, allowing for flexibility in the construction
  of the quantum program. In this case, the `qubit_count` argument allows us to dynamically control the
  number of qubits allocated to the kernel. As we will see in further :ref:`examples <python-examples-landing-page>`,
  we could also use these arguments to control various parameters of the gates themselves, such as rotation
  angles.


.. tab:: C++

  We can define our quantum kernel as we do any other typed callable in C++, through the use of the
  `__qpu__` annotation. For the following example, we will define a kernel for a simple GHZ-state as
  a standard free function.

  .. literalinclude:: ../snippets/cpp/using/first_kernel.cpp
      :language: cpp
      :start-after: [Begin Documentation]
      :end-before: [End Documentation]

  This kernel function can accept any number of arguments, allowing for flexibility in the construction
  of the quantum program. In this case, the `qubit_count` argument allows us to dynamically control the
  number of qubits allocated to the kernel. As we will see in further :ref:`examples <cpp-examples-landing-page>`,
  we could also use these arguments to control various parameters of the gates themselves, such as rotation
  angles.



Running your first CUDA Quantum Program
----------------------------------------



After building a quantum kernel, you can execute it using either the sample or observe method to obtain results.

3.1 Sample:

The `sample` method takes a quantum state (a kernel) and any kernel arguments as inputs and returns a `SampleResult` object containing the counts from repeated measurement of the prepared quantum state. Measurement occurs in the Z basis by default. The `dump` method prints a dictionary containing the measurements and their respective counts. The following example builds a 2 qubit GHZ state and returns the sample results.


.. literalinclude:: ../snippets/python/using/sample.py
      :language: python
      :start-after: [Begin Sample1]
      :end-before: [End Sample1]

By default, `sample` produces an ensemble of 1000 shots. This can be changed by specifying an integer argument for `shots_count`.

.. literalinclude:: ../snippets/python/using/sample.py
      :language: python
      :start-after: [Begin Sample2]
      :end-before: [End Sample2]

A variety of methods can be used to extract useful information from a sample result such as the most probable measurement and its respective count. See the API specifications for more options.

.. literalinclude:: ../snippets/python/using/sample.py
      :language: python
      :start-after: [Begin Sample3]
      :end-before: [End Sample3]

3.2 Observe:

`Observe` is used to produce expectation values provided a quantum state and a spin operator. 

First, an operator (i.e. a linear combination of Pauli strings) must be specified. To do so, import `spin` from cudaq. Any linear combination of the I, X, Y, and Z spin operators can be constructed with using spin.i(q), spin.x(q), spin.y(q), and spin.z(q), respectively, where q is the index of the target qubit. 

Below is an example of a spin operator object consisting of a Z(0) operator, followed by construction of a kernel with a single qubit in an equal superposition. The Hamiltonian is printed to confirm it has been constructed properly.

.. literalinclude:: ../snippets/python/using/observe.py
      :language: python
      :start-after: [Begin Observe1]
      :end-before: [End Observe1]

`Observe` takes a kernel, kernel arguments (if any),  and a spin operator as inputs and produces an `ObserveResult` object. The expectation value can be printed using the `expectation` method. It is important to exclude a measurement in the kernel, otherwise the expectation value will be determined from a collapsed classical state. For this example, the expected result of 0.0 is produced.

.. literalinclude:: ../snippets/python/using/observe.py
      :language: python
      :start-after: [Begin Observe2]
      :end-before: [End Observe2]

Unlike `sample`, the default `shots_count` for `observe` is 1. This result is deterministic and equivalent to the expectation value in the limit of infinite shots.  To produce an approximate expectation value from sampling, `shots_count` can be specified to any integer.

.. literalinclude:: ../snippets/python/using/observe.py
      :language: python
      :start-after: [Begin Observe3]
      :end-before: [End Observe3]

3.3. Running on a GPU

Using `cudaq.set_target`, different targets can be specified for kernel execution. By default, the NVIDIA target will use a single GPU if it is available or fall back to the CPU otherwise.  To demonstrate the benefits of using a GPU. Below is an example of a 25 qubit GHZ state sampled 1 million times.  Using a GPU accelerates this task by more than 35x. To learn about all of the available targets and ways to accelerate kernel execution, visiting the —  page.

.. literalinclude:: ../snippets/python/using/time.py
      :language: python
      :start-after: [Begin Time]
      :end-before: [End Time]





Language Fundamentals
----------------------

CUDA Quantum kernels support a subset of native Python syntax. We will now outline the supported syntax
and highlight important features of the CUDA Quantum kernel API.
.. FIXME ... better copy here

Quantum Memory
++++++++++++++++++++++++++++++++++

Todo



Troubleshooting
-----------------


Debugging and Verbose Simulation Output
+++++++++++++++++++++++++++++++++++++++++

One helpful mechanism of debugging CUDA Quantum simulation execution is
the :code:`CUDAQ_LOG_LEVEL` environment variable. For any CUDA Quantum
executable, just prepend this and turn it on:

.. tab:: Python

  .. code-block:: bash

      CUDAQ_LOG_LEVEL=info python3 file.py

.. tab:: C++

    .. code-block:: bash

      CUDAQ_LOG_LEVEL=info ./a.out

Similarly, one may write the IR to their console or to a file before remote
submission. This may be done through the :code:`CUDAQ_DUMP_JIT_IR` environment
variable. For any CUDA Quantum executable, just prepend as follows:

.. tab:: Python

  .. code-block:: bash

      CUDAQ_DUMP_JIT_IR=1 python3 file.py
      # or
      CUDAQ_DUMP_JIT_IR=<output_filename> python3 file.py

.. tab:: C++

  .. code-block:: bash

      CUDAQ_DUMP_JIT_IR=1 ./a.out
      # or
      CUDAQ_DUMP_JIT_IR=<output_filename> ./a.out
