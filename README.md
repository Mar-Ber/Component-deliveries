## Planning component deliveries in a production plant

#### The project is part of the thesis

The aim of the project is to implement an algorithm that approximates the supply problem components in the factory. The resulting application enables simulation of the problem for the created factory model and finding a solution for it.

### Description of the problem
The problem under consideration is the supply of components needed for on-site production factories. It consists of the main warehouse, production cells, local warehouses, machines and transport paths. Internal logistics is based on Lean Manufacturing rules.

The factory is divided into sections. They are marked by paths along the length factories with production cells. All sections are connected by road main, the beginning of which is in the main warehouse. It is assumed that the main warehouse continuously has the number of components needed to download. The task of the employees there is a cyclical delivery of parts from the main warehouse to local warehouses in one shift. Each employed person is associated with the costs of their work. Employees are equipped with vehicles characterized by certain average speeds movement, maximum number of containers transported at one time, and costs using. Transports should ensure such levels of components in warehouses local so that the machines in the production cells can run without interruption. The delivered components are transported in containers. The parts differ from each other dimensions, therefore it is necessary to apply several standards containers. They differ in size and capacity. Each of the vehicles simultaneously can transport containers of various standards. Their total size can not, however exceed the maximum load of the truck. Moreover, each machine is undergoing a shift produces one type of product (assuming that each product can only be assigned to one machine). There are several components that may be required to create a product in different amounts. One type of part may be required for several types of production machines. 

Local warehouses have some initial level of components. The frequency of replenishment of production parts depends on the processing time of a given product. Each of the warehouses contains a sufficient number of racks for the room components needed for production in a given production cell. It is defined maximum number of containers with a given component in the local warehouse. 

The solution to the problem is to plan routes for employees during their work, with the aim of maximizing profits. They have the option of supplying individual ones machines with a large number of components or a large number of machines with a small number of components, depending on which strategy will bring more profit. The goal is uninterrupted production of products with a specific number of employees.

### Implementation
All the components, such as workers, machines, transport routes, products, etc., have been organized into classes, listed in the UML diagram below. External functions are responsible for operating on objects of these classes.

![uml](https://github.com/Mar-Ber/Component-deliveries/blob/main/UML.png)

