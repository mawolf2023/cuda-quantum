Operators
-------------------

Operators are important constructs for a variety of applications.  This section covers how to define and use spin operators as well as additional tools for defining more sophisticated operators. 


Constructing Spin Operators
+++++++++++++++++++++++++++++++++++++++++
The `spin_op`  type provides an abstraction for a general tensor product of Pauli spin operators, and their sums. 

Spin operators are constructed using the `spin.z()`, `spin.y()`, `spin.x()`, and `spin.i()` functions, corresponding to the Z, Y, X, and I Pauli operators. For example,  `spin.z(0)` corresponds to a Pauli Z operation acting on qubit 0.  The example below demonstrates how to construct the following operator 2XYX - 3ZZY. 


.. code-block:: python

     from cudaq import spin

     operator = 2 * spin.x(0) * spin.y(1) * spin.x(2) - 3 * spin.z(0) * spin.z( 1) * spin.y(2)    


This section (link) details how to comoute expectation values, a common applications of spin operators for variational algorithms..

The API (link)  provides a number of convenient methods for combining, comparing, iterating through, and extracting information from spin operators and can be referenced here.

Pauli Words and Exponentiating Pauli Words
+++++++++++++++++++++++++++++++++++++++++

The `pauli_word` type specifies a string of Pauli operations (e.g. ‘XYXZ’) and is convenient for applying operations based on exponentiated Pauli words.  The code below demonstrates how a list of Pauli words, along with their coefficients, are provided as kernel inputs and converted into operators by the `exp_pauli` function.


.. code-block:: python
     
      words = ['XYZ', 'IXX']
      coefficients = [0.432, 0.324]


      @cudaq.kernel
      def kernel(coefficients: list[float], words: list[cudaq.pauli_word]):
      q = cudaq.qvector(3)

      for i in range(len(coefficients)):
          exp_pauli(coefficients[i], q, words[i])
