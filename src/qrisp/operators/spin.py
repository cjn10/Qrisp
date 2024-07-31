"""
\********************************************************************************
* Copyright (c) 2024 the Qrisp authors
*
* This program and the accompanying materials are made available under the
* terms of the Eclipse Public License 2.0 which is available at
* http://www.eclipse.org/legal/epl-2.0.
*
* This Source Code may also be made available under the following Secondary
* Licenses when the conditions for such availability set forth in the Eclipse
* Public License, v. 2.0 are satisfied: GNU General Public License, version 2
* with the GNU Classpath Exception which is
* available at https://www.gnu.org/software/classpath/license.html.
*
* SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
********************************************************************************/
"""

import sympy as sp
from sympy import Symbol, I, Quaternion
import numpy as np

#
# Helper functions
#

def delta(i, j):
    if i==j:
        return 1
    else:
        return 0
    
def epsilon(i, j, k):
    if (i, j, k) in (("X", "Y", "Z"), ("Y", "Z", "X"), ("Z", "X", "Y")):
        return 1
    if (i, j, k) in (("Z", "Y", "X"), ("Y", "X", "Z"), ("X", "Z", "Y")):
        return -1
    return 0

def mul_helper(P1,P2):
    pauli_table = {("X","X"):("I",1),("X","Y"):("Z",1j),("X","Z"):("Y",-1j),
            ("Y","X"):("Z",-1j),("Y","Y"):("I",1),("Y","Z"):("X",1j),
            ("Z","X"):("Y",1j),("Z","Y"):("X",-1j),("Z","Z"):("I",1)}
    
    if P1=="I":
        return (P2,1)
    if P2=="I":
        return (P1,1)
    return pauli_table[(P1,P2)]
#
# Pauli symbols (only used for visualization, i.e., LateX printing with SymPy)
#  

class X_(Symbol):

    __slots__ = ("axis","index")

    def __new__(cls, index):
        obj = Symbol.__new__(cls, "%s%d" %("X",index), commutative=False, hermitian=True)
        obj.index = index
        obj.axis = "X"
        return obj

    def get_quaternion(self):
        return Quaternion(0,I,0,0)
    
    def get_matrix(self):
        return np.array([[0,1],[1,0]])
    
    def get_axis(self):
        return "X" 
    
    def _eval_power(b, e):
        if e.is_Integer and e.is_positive:
            return super().__pow__(int(e) % 2)
        
    def __mul__(self, other):
        if isinstance(other, (X_,Y_,Z_)):
            if self.index == other.index:
                i = self.axis
                j = other.axis
                return delta(i, j) \
                    + I*epsilon(i, j, "X")*X_(self.index) \
                    + I*epsilon(i, j, "Y")*Y_(self.index) \
                    + I*epsilon(i, j, "Z")*Z_(self.index)
        return super().__mul__(other)
    
    __rmul__ = __mul__

class Y_(Symbol):

    __slots__ = ("axis","index")

    def __new__(cls, index):
        obj = Symbol.__new__(cls, "%s%d" %("Y",index), commutative=False, hermitian=True)
        obj.index = index
        obj.axis = "Y"
        return obj

    def get_quaternion(self):
        return Quaternion(0,0,I,0)
    
    def get_matrix(self):
        return np.array([[0,-1j],[1j,0]])
    
    def get_axis(self):
        return "Y"
    
    def _eval_power(b, e):
        if e.is_Integer and e.is_positive:
            return super().__pow__(int(e) % 2)

    def __mul__(self, other):
        if isinstance(other, (X_,Y_,Z_)):
            if self.index == other.index:
                i = self.axis
                j = other.axis
                return delta(i, j) \
                    + I*epsilon(i, j, "X")*X_(self.index) \
                    + I*epsilon(i, j, "Y")*Y_(self.index) \
                    + I*epsilon(i, j, "Z")*Z_(self.index)
        return super().__mul__(other)     
      
    __rmul__ = __mul__
       
class Z_(Symbol):

    __slots__ = ("axis","index")

    def __new__(cls, index):
        obj = Symbol.__new__(cls, "%s%d" %("Z",index), commutative=False, hermitian=True)
        obj.index = index
        obj.axis = "Z"
        return obj

    def get_quaternion(self):
        return Quaternion(0,0,0,I)
    
    def get_matrix(self):
        return np.array([[1,0],[0,-1]])
    
    def get_axis(self):
        return "Z"
    
    def _eval_power(b, e):
        if e.is_Integer and e.is_positive:
            return super().__pow__(int(e) % 2)
        
    def __mul__(self, other):
        if isinstance(other, (X_,Y_,Z_)):
            if self.index == other.index:
                i = self.axis
                j = other.axis
                return delta(i, j) \
                    + I*epsilon(i, j, "X")*X_(self.index) \
                    + I*epsilon(i, j, "Y")*Y_(self.index) \
                    + I*epsilon(i, j, "Z")*Z_(self.index)
        return super().__mul__(other)
    
    __rmul__ = __mul__


def to_pauli_dict(expr):

    pauli_dict = {}

    for monomial in expr.expand().as_ordered_terms():
        factors = monomial.as_ordered_factors()

        p_dict = {} # dictionary encoding a Pauli product
        coeff = 1

        for arg in factors:
            if isinstance(arg, (X_,Y_,Z_)):
                pauli, coeff_ = mul_helper(p_dict.get(arg.index,"I"),arg.get_axis())
                if pauli!="I":
                    p_dict[arg.index] = pauli
                else:
                    del p_dict[arg.index]
                coeff *= coeff_
            else:
                coeff *= arg

        sorted_pauli = tuple(sorted(p_dict.items()))
        pauli_dict[sorted_pauli] = pauli_dict.get(sorted_pauli,0)+complex(coeff)

    return pauli_dict 






