<p align="center" width="100%"><img src="logo/qrisp_logo.png" width=30% height=30%></p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/qrisp.svg)](https://badge.fury.io/py/qrisp)
[![Build Status](https://github.com/eclipse-qrisp/Qrisp/workflows/CI/badge.svg)](https://github.com/eclipse-qrisp/Qrisp/actions)
[![Downloads](https://img.shields.io/pypi/dm/qrisp.svg)](https://pypi.org/project/qrisp/)
[![Contributors](https://img.shields.io/github/contributors/eclipse-qrisp/Qrisp.svg)](https://github.com/eclipse-qrisp/Qrisp/graphs/contributors)
[![Open Issues](https://img.shields.io/github/issues/eclipse-qrisp/Qrisp.svg)](https://github.com/eclipse-qrisp/Qrisp/issues)
[![Forks](https://img.shields.io/github/forks/eclipse-qrisp/Qrisp.svg)](https://github.com/eclipse-qrisp/Qrisp/network/members)
[![Stars](https://img.shields.io/github/stars/eclipse-qrisp/Qrisp.svg)](https://github.com/eclipse-qrisp/Qrisp/stargazers)

Qrisp is the next generation of quantum algorithm development.

## About

Qrisp is a high-level quantum programming framework that allows for intuitive development of quantum algorithms. It provides a rich set of tools and abstractions to make quantum computing more accessible to developers and researchers.

## Features

- Intuitive quantum circuit design
- High-level quantum operations
- Efficient quantum algorithm implementation
- Extensive documentation and examples

## Installation

You can install Qrisp using pip:




Qrisp is an open-source python framework for high-level programming of Quantum computers.
By automating many steps one usually encounters when progrmaming a quantum computer, introducing quantum types, and many more features Qrisp makes quantum programming more user-friendly yet stays performant when it comes to compiling programs to the circuit level.

## Documentation
The full documentation, alongside with many tutorials and examples, is available under [Qrisp Documentation](https://www.qrisp.eu/).

## Installing
The easiest way to install Qrisp is via ``pip``
```bash
pip install qrisp
```
Qrisp has been confirmed to work with Python version 3.8, 3.9 & 3.10.

If you want to work with IQM quantum computers as a backend, you need to install additional dependencies using
```bash
pip install qrisp[iqm]
```

## Shor's Algorithm with Qrisp

Shor's algorithm is among the most famous quantum algorithm since it provides a provably exponential speed-up for a practically relevant problem: Facotrizing integers. This is an important application because much of modern cryptography is based on RSA, which heavily relies on integer factorization being insurmountable.

Despite this importance, the amount of software that is actually able to compile the algorithm to the circuit level is extremely limited. This is because a key operation within the algorithm (modular in-place multiplication) is difficult to implement and has strong requirements for the underlying compiler. These problems highlight how the Qrisp programming-model delivers significant advantages to quantum programmers because the quantum part of the algorithm can be expressend within a few lines of code:

```python

from qrisp import QuantumFloat, QuantumModulus, h, QFT

def find_order(a, N):
    qg = QuantumModulus(N)
    qg[:] = 1
    qpe_res = QuantumFloat(2*qg.size + 1, exponent = -(2*qg.size + 1))
    h(qpe_res)
    for i in range(len(qpe_res)):
        with control(qpe_res[i]):
            qg *= a
            a = (a*a)%N
    QFT(qpe_res, inv = True)
    return qpe_res.get_measurement()
```

To find out how this can be used to break encryption be sure to check the [tutorial](https://www.qrisp.eu/general/tutorial.html).

Qrisp offers much more than just factoring! More examples, like simulating molecules at the quantum level or how to solve the Travelling Salesman Problem, can be found [here](https://www.qrisp.eu/general/tutorial.html).

## Authors and Citation
Qrisp was mainly devised and implemented by Raphael Seidel, supported by Sebastian Bock, Nikolay Tcholtchev, René Zander, Niklas Steinmann and Matic Petric.

If you have comments, questions or love letters, feel free to reach out to us:

raphael.seidel@fokus.fraunhofer.de

sebastian.bock@fokus.fraunhofer.de

nikolay.tcholtchev@fokus.fraunhofer.de

If you want to cite Qrisp in your work, please use:

```
@misc{seidel2024qrisp,
      title={Qrisp: A Framework for Compilable High-Level Programming of Gate-Based Quantum Computers}, 
      author={Raphael Seidel and Sebastian Bock and René Zander and Matic Petrič and Niklas Steinmann and Nikolay Tcholtchev and Manfred Hauswirth},
      year={2024},
      eprint={2406.14792},
      archivePrefix={arXiv},
      primaryClass={quant-ph},
      url={https://arxiv.org/abs/2406.14792}, 
}
```


## License
[Eclipse Public License 2.0](https://github.com/fraunhoferfokus/Qrisp/blob/main/LICENSE)

