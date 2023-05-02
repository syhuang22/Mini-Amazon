# Mini-Amazon Project

This project is a simulation of a mini-Amazon system, which includes an online store and its interactions with the mini-UPS shipping system. The goal is to develop a system that works seamlessly with the UPS systems.

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [World Simulation](#world-simulation)
4. [Amazon and UPS Commands](#amazon-and-ups-commands)
5. [Protocol Specification](#protocol-specification)

## Overview

The project consists of the following components:

- **Amazon**: An online store where users can place orders.
- **UPS**: A shipping system responsible for picking up packages from warehouses and delivering them to customers.
- **World**: A simulated environment that includes warehouses, trucks, and a coordinate grid to represent addresses.

## Getting Started

To set up the project, follow these steps:

1. Clone the repository.
2. Set up the required dependencies.
3. Run the Amazon and UPS services.
4. Connect to the World simulation server.

## World Simulation

The World simulation server provides a virtual environment for warehouses and trucks. Amazon and UPS systems can connect to the server and send commands to control their respective components. The server supports different worlds, each identified by a 64-bit number.

The world consists of a Cartesian coordinate grid, where addresses are represented as integer coordinates (e.g., (2, 4)). The grid includes trucks (controlled by UPS) and warehouses (controlled by Amazon) that need to work together to deliver packages.

## Amazon and UPS Commands

Amazon and UPS systems can send and receive messages to and from the World simulation server to control their components. The supported commands and responses can be found in the provided `.proto` files (amazon.proto and ups.proto).

For more details on the available Amazon and UPS commands, refer to the [project description](https://github.com/syhuang22/Mini-Amazon/blob/main/amazon_services/proto_files/Mini-Amazon%20Spec.pdf).
