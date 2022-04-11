#!/usr/bin/python
# -*- coding: utf-8 -*-

import Classes as Cls
import Functions as Fun
import random as rd
import numpy as np

# Containers
containers_size = {1: 1, 2: 2, 3: 4}
containers_capacities = {1: 40, 2: 80, 3: 160}
max_containers_num = 3
initial_quantity = 20  # [in %]


# Products and components
num_of_components = 30
min_cost = 0.2
max_cost = 0.5
list_of_components = Fun.component_generator(num_of_components, containers_capacities, min_cost, max_cost)

num_of_products = 10
min_profit = 5
max_profit = 10
min_req_components = 1
max_req_components = 3
min_prod_per_min = 1
max_prod_per_min = 2
min_req_num = 1
max_req_num = 3

list_of_product = Fun.products_generator(num_of_components, num_of_products, min_profit, max_profit, min_req_components,
                                         max_req_components, min_prod_per_min, max_prod_per_min, min_req_num,
                                         max_req_num)


# Factory
num_of_section = 3
section_length = 50
sections_distance = 10
warehouse_distance = 10
num_of_machines = num_of_products  # num_of_machines <= num_of_products
num_prod_cells = rd.randint(int(0.5 * num_of_machines), int(0.75 * num_of_machines))

plant = Cls.Factory(num_of_section, section_length, sections_distance, warehouse_distance, num_of_machines,
                    num_prod_cells, containers_size, containers_capacities)
list_prod_cells = Fun.man_cells_generator(plant, max_containers_num)
Fun.select_production(list_prod_cells, list_of_product)
Fun.identify_needed_components(list_prod_cells)
schedule_details = Fun.schedule_details_generator(list_prod_cells, list_of_components)


# Workers
delivery_cart = Cls.Vehicle(speed=20, capacity=14, fuel_consumption=0.5)
number_of_carts = 3
driver_cost = 0.5
work_time = 0.5  # [in hours]

list_of_workers = []
for num in range(0, number_of_carts):
    list_of_workers.append(Cls.Worker(delivery_cart, driver_cost, work_time))


# Schedule
list_2 = []
for i in range(len(schedule_details)):
    list_2.append(schedule_details[i].consumption_per_min)
arr_2 = np.array(list_2)

update_schedule = Fun.update_schedule_generator(schedule_details, initial_quantity, work_time)


# Find solution
profit_multiplier = 1
costs_multiplier = 1
fuel_multiplier = 1
salary_multiplier = 1
multipliers = [profit_multiplier, costs_multiplier, fuel_multiplier, salary_multiplier]

attempts = 20
number_of_iterations = 10
reset_time = int(0.2 * number_of_iterations)

schedule, rate, evaluation_details, iteration, time = Fun.tabu_search(update_schedule, schedule_details, list_of_product,
                                                                      list_of_workers, list_prod_cells, plant, attempts,
                                                                      number_of_iterations, reset_time, multipliers)

print('\nBest schedule:\n{0}'.format(schedule))
print('\nProduction details:')
for key, value in evaluation_details[0].items():
    print('Product index: {0} -> production {1}/{2} minutes'.format(key, value, int(60*work_time)))
print('\nWorkers details:')
for key, value in evaluation_details[1].items():
    print('Worker: {0} -> distance: {1}'.format(key, value))
print('\nBest rate:\n{0}'.format(rate))
print('Best iteration:\n{0}'.format(iteration))


pass
