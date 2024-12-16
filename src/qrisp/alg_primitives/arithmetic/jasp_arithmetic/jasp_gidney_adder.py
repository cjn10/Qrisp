"""
\********************************************************************************
* Copyright (c) 2023 the Qrisp authors
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

from qrisp.jasp import qache, jrange, AbstractQubit, make_jaspr, Jaspr
from qrisp.core import h, cx, t, t_dg, s, measure, cz, QuantumVariable
from qrisp.qtypes import QuantumBool
from qrisp.environments import control, custom_control


def gidney_mcx_impl(a, b, c):
    
    h(c)
    t(c)
    
    cx(a, c)
    cx(b, c)
    cx(c, a)
    cx(c, b)
    
    t_dg(a)
    t_dg(b)
    t(c)
    
    cx(c,a)
    cx(c,b)
    
    h(c)
    s(c)

def gidney_mcx_inv_impl(a, b, c):
    h(c)
    bl = measure(c)
    
    with control(bl):
        cz(a,b)

gidney_mcx_jaspr = make_jaspr(gidney_mcx_impl)(AbstractQubit(), AbstractQubit(), AbstractQubit()).flatten_environments()
gidney_mcx_inv_jaspr = make_jaspr(gidney_mcx_inv_impl)(AbstractQubit(), AbstractQubit(), AbstractQubit()).flatten_environments()

class GidneyMCXJaspr(Jaspr):
    
    slots = ["inv"]
    def __init__(self, inv):
        self.inv = inv
        if self.inv:
            Jaspr.__init__(self, gidney_mcx_inv_jaspr)
        else:
            Jaspr.__init__(self, gidney_mcx_jaspr)
        self.envs_flattened = True
            
    def inverse(self):
        return GidneyMCXJaspr(not self.inv)

def gidney_mcx(a, b, c):
    GidneyMCXJaspr(False).embedd(a, b, c, name = "gidney_mcx")

def gidney_mcx_inv(a, b, c):
    GidneyMCXJaspr(True).embedd(a, b, c, name = "gidney_mcx_inv")

@custom_control
def jasp_gidney_adder(a, b, ctrl = None):
    
    gidney_anc = QuantumVariable(a.size-1, name = "gidney_anc*")
    
    if ctrl is not None:
        ctrl_anc = QuantumBool(name = "gidney_anc_2*")
    
    i = 0
    gidney_mcx(a[i], b[i], gidney_anc[i])
    
    for j in jrange(a.size-2):
        i = j+1
    
        cx(gidney_anc[i-1], a[i])
        cx(gidney_anc[i-1], b[i])
        gidney_mcx(a[i], b[i], gidney_anc[i])
        cx(gidney_anc[i-1], gidney_anc[i])
        
    cx(gidney_anc[a.size-2], b[b.size-1])
    
    for j in jrange(a.size-2):
        i = a.size-j-2
        
        cx(gidney_anc[i-1], gidney_anc[i])
        gidney_mcx_inv(a[i], b[i], gidney_anc[i])
        
        if ctrl is not None:
            
            gidney_mcx(ctrl, a[i], ctrl_anc[0])
            cx(ctrl_anc[0], b[i])
            gidney_mcx(ctrl, a[i], ctrl_anc[0])
            
            cx(gidney_anc[i-1], a[i])
            cx(gidney_anc[i-1], b[i])
        else:
            cx(gidney_anc[i-1], a[i])
            cx(a[i], b[i])
    
    gidney_mcx_inv(a[0], b[0], gidney_anc[0])
    cx(a[0], b[0])
    
    gidney_anc.delete()
    
    if ctrl is not None:
        ctrl_anc.delete()        
