"""
********************************************************************************
* Copyright (c) 2025 the Qrisp authors
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
********************************************************************************
"""

from qrisp import QuantumChar, QuantumString

q_str = QuantumString()
q_str_2 = QuantumString()
q_ch = QuantumChar()

q_str[:] = "hello"
q_ch[:] = " "
q_str_2[:] = "world"
q_str += q_ch
q_str += q_str_2
q_str += "! "
q_str_3 = q_str.duplicate(init=True)

print(q_str + q_str_3)
