#!/usr/bin/python
# -*- coding: utf-8 -*-

class Vehicle:
    def __init__(self, speed, capacity, fuel_consumption):
        self.speed = speed
        self.capacity = capacity
        self.fuel_cost = fuel_consumption


class Worker:
    def __init__(self, vehicle, driver_cost, work_time):
        self.vehicle = vehicle
        self.driver_cost = driver_cost
        self.work_time = int(work_time*60)-1
        self.current_time = 1
        self.current_capacity = vehicle.capacity
        self.distance = 0
        self.supplied_idx = []
        self.supply_schedule = []
        self.store_schedule = []
        self.update_schedule = None


class Store:
    def __init__(self, section, index, position, max_containers_num, supplied_machines):
        self.section = section
        self.index = index
        self.position = position
        self.max_containers_num = max_containers_num
        self.supplied_machines = supplied_machines
        self.manufactured_products = []
        self.necessary_components = {}  # probably unused


class Factory:
    def __init__(self, num_of_section, section_length, sections_distance, warehouse_distance,
                 num_of_machines, num_prod_cells, containers_size, containers_capacities):
        self.num_of_section = num_of_section
        self.section_length = section_length
        self.sections_distance = sections_distance
        self.warehouse_distance = warehouse_distance
        self.num_of_machines = num_of_machines
        self.num_prod_cells = num_prod_cells
        self.containers_size = containers_size
        self.containers_capacities = containers_capacities


class Product:
    def __init__(self, index, component_consumption, prod_per_min, profit):
        self.index = index
        self.component_consumption = component_consumption
        self.prod_per_min = prod_per_min
        self.profit = profit


class Component:
    def __init__(self, index, container_type, container_capacity, cost):
        self.index = index
        self.container_type = container_type
        self.container_capacity = container_capacity
        self.cost = cost


class ProductionPlan:
    def __init__(self, component_idx, consumption_per_min, product_idx, machine_idx, store_idx, cost_per_min,
                 container_type, max_containers_num):
        self.component_idx = component_idx
        self.consumption_per_min = consumption_per_min  # [in %]
        self.product_idx = product_idx
        self.machine_idx = machine_idx
        self.store_idx = store_idx
        self.cost_per_min = cost_per_min
        self.container_type = container_type
        self.max_containers_num = max_containers_num
