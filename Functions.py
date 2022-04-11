#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import Classes as Cls
import random as rd
import numpy as np
import copy
import tkinter as tk


def component_generator(num_of_components, containers_capacities, min_cost, max_cost):
    list_of_components = []
    list_container_type = list(containers_capacities.keys())
    list_container_capacities = list(containers_capacities.values())
    # Create the required number of components
    for next_component in range(num_of_components):
        # Select data for a component
        container_type = rd.choice(list_container_type)
        container_capacity = containers_capacities[container_type]
        cost = round(rd.uniform(min_cost, max_cost), 1)
        # Create and add a new component to the list
        new_component = Cls.Component(next_component + 1, container_type, container_capacity, cost)
        list_of_components.append(new_component)
    return list_of_components


def products_generator(num_of_components, num_of_products, min_profit, max_profit, min_req_components,
                       max_req_components, min_prod_per_min, max_prod_per_min, min_req_num, max_req_num):
    list_of_products = []
    # Create the required number of products
    for next_product in range(num_of_products):
        # Select data about components for a product
        profit = round(rd.uniform(min_profit, max_profit), 1)
        prod_per_min = round(rd.uniform(min_prod_per_min, max_prod_per_min), 1)
        # prod_per_min = rd.randint(min_prod_per_min, max_prod_per_min)
        req_num_components = rd.randint(min_req_components, max_req_components)
        # Select first component requirements data
        req_num = rd.randint(min_req_num, max_req_num)
        idx = rd.randint(1, num_of_components)
        req_components = {idx: req_num}
        # Select next component data (if needed)
        if req_num_components > 1:
            for elem in range(req_num_components - 1):
                # Select next component data
                idx = rd.randint(1, num_of_components)
                while idx in req_components.keys():
                    # Select an unused component
                    idx = rd.randint(1, num_of_components)
                req_num = rd.randint(min_req_num, max_req_num)
                req_components[idx] = req_num
        # Create and add a new product to the list
        new_product = Cls.Product(next_product + 1, req_components, prod_per_min, profit)
        list_of_products.append(new_product)
    return list_of_products


def man_cells_generator(plant, max_containers_num):
    # Separation of machines into production cells
    list_of_machines = list(range(1, plant.num_of_machines + 1))
    temp = np.array_split(list_of_machines, plant.num_prod_cells)
    list_distributed_machines = []
    for elem in temp:
        list_distributed_machines.append(list(elem))
    # Creation production cells/stores
    list_prod_cells = []
    reserved = []
    for idx in range(1, plant.num_prod_cells + 1):
        section = rd.randint(1, plant.num_of_section)
        position = rd.randint(1, plant.section_length)
        # Providing a unique position
        while [section, position] in reserved:
            position = rd.randint(1, plant.section_length)
        reserved.append([section, position])
        list_prod_cells.append(
            Cls.Store(section, idx, position, max_containers_num, list_distributed_machines[idx - 1]))
    return list_prod_cells


def select_production(list_prod_cells, list_of_product):
    # Randomize the order of assigning products to machines
    copy_prod_list = copy.deepcopy(list_of_product)
    rd.shuffle(copy_prod_list)
    # Assign products from list to production cells
    for cell in list_prod_cells:
        quantity = len(cell.supplied_machines)
        cell.manufactured_products = copy_prod_list[:quantity]
        copy_prod_list = copy_prod_list[quantity:]


def identify_needed_components(list_prod_cells):  # probably unused
    # Select a cell
    for cell in list_prod_cells:
        necessary_components = {}
        # Check the manufactured products
        for product in cell.manufactured_products:
            # Add needed components to the main requirement for a given cell
            for key, value in product.component_consumption.items():
                if key in necessary_components:
                    necessary_components[key] += value * product.prod_per_min
                else:
                    necessary_components[key] = value * product.prod_per_min
        cell.necessary_components = necessary_components


def schedule_details_generator(list_prod_cells, list_of_components):
    schedule_details = []
    # Select a cell
    for cell in list_prod_cells:
        # Check the manufactured products
        mach_idx = 0
        for product in cell.manufactured_products:
            # Check components and consumption used to manufactured products
            for component_idx, consumption in product.component_consumption.items():
                component = list_of_components[component_idx - 1]
                consumption_per_min = consumption * product.prod_per_min
                # Percentage consumption by capacity
                consumption_per_min = round(
                    100 * consumption_per_min / (cell.max_containers_num * component.container_capacity), 2)
                cost_per_min = round(component.cost * product.prod_per_min, 2)
                # Add component to list
                schedule_details.append(Cls.ProductionPlan(component_idx, consumption_per_min, product.index,
                                                           int(cell.supplied_machines[mach_idx]), cell.index,
                                                           cost_per_min, component.container_type,
                                                           cell.max_containers_num))
            mach_idx += 1
    return schedule_details


def update_schedule_generator(schedule_details, initial_quantity, work_time):
    update_schedule = np.zeros((len(schedule_details), int(work_time * 60)))
    update_schedule[:, 0] = initial_quantity
    return update_schedule


def update_update_schedule(update_schedule, update_data):
    update_idx = update_data[0]
    update_time = update_data[1]
    update_value = round(update_data[2], 2)
    update_schedule[update_idx, update_time] += update_value
    return update_schedule


def schedule_generator(update_schedule, schedule_details):
    # Generate schedule
    work_time = len(update_schedule[0])
    schedule = np.zeros((len(schedule_details), int(work_time)))
    schedule[:, 0] = update_schedule[:, 0]
    production_data = iter(range(len(schedule_details)))
    # Component selection
    for idx in production_data:
        next_elem = schedule_details[idx]
        # Check which product it is and all its components
        all_components = [i for i, x in enumerate(schedule_details) if x.product_idx == next_elem.product_idx
                          and x.store_idx == next_elem.store_idx and x.machine_idx == next_elem.machine_idx]
        # Loop through next columns of schedule
        time_idx = 1
        while time_idx < work_time:  # and stop_flag == 0:
            # Check if there are enough components for production
            flag = 1
            for elem_idx in all_components:
                if schedule[elem_idx, time_idx - 1] < schedule_details[elem_idx].consumption_per_min:
                    flag = 0
            # Calculate next value for all components of product if production is ON
            if flag == 1:
                for elem_idx in all_components:
                    schedule[elem_idx, time_idx] = schedule[elem_idx, time_idx - 1] - \
                                                   schedule_details[elem_idx].consumption_per_min + \
                                                   update_schedule[elem_idx, time_idx]
            # Calculate next value for all components of product if production is OFF
            else:
                for elem_idx in all_components:
                    schedule[elem_idx, time_idx] = schedule[elem_idx, time_idx - 1] + \
                                                   update_schedule[elem_idx, time_idx]
            time_idx += 1

        # list_all_components.append(all_components)  # only for debug
        # Skip the completed components
        if len(all_components) > 1:
            for temp_idx in range(0, len(all_components) - 1):
                next(production_data)
    return schedule


def calculate_distance(plant, list_prod_cells, list_of_stops):  # Calculate distance between cells idx or warehouse (0)
    distance = 0
    # Calculate the total distance to the warehouse
    for stop in list_of_stops:
        if stop == 0:
            distance += plant.warehouse_distance
    # Calculate the distance between consecutive stops
    for stop_idx in range(1, len(list_of_stops)):
        # Clear values
        start_section, stop_section, start_position, stop_position, position, section = 6 * [0]
        # Check if the stop is not a warehouse
        if list_of_stops[stop_idx - 1] != 0 and list_of_stops[stop_idx] != 0:
            # Find sections and positions for stops
            for cell in list_prod_cells:
                if cell.index == list_of_stops[stop_idx - 1]:
                    start_section = cell.section
                    start_position = cell.position
                if cell.index == list_of_stops[stop_idx]:
                    stop_section = cell.section
                    stop_position = cell.position
            # Calculate distance between sections
            section_distance = abs(stop_section - start_section) * plant.sections_distance
            # Calculate position distance between stops
            if start_section != stop_section:
                position_distance = start_position + stop_position
            else:
                position_distance = abs(start_position - stop_position)
            distance += (section_distance + position_distance)
        # If the stop is a warehouse
        else:
            # Check which stop is the warehouse
            if list_of_stops[stop_idx - 1] != 0:
                stop = list_of_stops[stop_idx - 1]
            else:
                stop = list_of_stops[stop_idx]
            # Find section and position for this stop
            for cell in list_prod_cells:
                if cell.index == stop:
                    section = cell.section
                    position = cell.position
                    break
            # Add to total distance
            section_distance = section * plant.sections_distance
            distance += (section_distance + position)
    return distance


def randomize_supply_idx(plant, schedule_details, list_prod_cells, worker, attempts):
    while 1:
        supply_idx = rd.randint(0, len(schedule_details) - 1)
        # Create a list of stops and calculate components delivery time
        stop_list = []
        if len(worker.supplied_idx) >= 1:
            stop_list.append(schedule_details[worker.supplied_idx[-1]].store_idx)
        else:
            stop_list.append(0)
        stop_list.append(schedule_details[supply_idx].store_idx)
        stop_list.append(0)
        distance = calculate_distance(plant, list_prod_cells, stop_list)
        needed_time = distance // worker.vehicle.speed
        # Preventing infinite loops
        if (supply_idx in worker.supplied_idx) or (needed_time > (worker.work_time - worker.current_time)):
            attempts -= 1
            if attempts == 0:
                return None
            else:
                continue
        else:
            break
    return supply_idx


def create_single_delivery(update_schedule, schedule_details, list_prod_cells, worker, plant, attempts):
    # The loop planning the delivered components in one delivery
    worker.supplied_idx = []
    worker.current_capacity = worker.vehicle.capacity
    while worker.current_capacity > 0:
        check = worker.current_capacity
        # Randomize supply index
        supply_idx = randomize_supply_idx(plant, schedule_details, list_prod_cells, worker, attempts)
        if supply_idx is None:
            break
        # Check the store level on delivery
        schedule = schedule_generator(update_schedule, schedule_details)
        idx_level = schedule[supply_idx, worker.current_time]
        max_supply = 100 - idx_level
        # Check that the delivery of the maximum quantity will not exceed the maximum stock level
        update_schedule_elem = np.array([update_schedule[supply_idx]])
        details_elem = [schedule_details[supply_idx]]
        # Calculate needed time
        if len(worker.supplied_idx) >= 1:
            last_idx = schedule_details[worker.supplied_idx[-1]].store_idx
        else:
            last_idx = 0
        stop_list = [last_idx, details_elem[0].store_idx]
        distance = calculate_distance(plant, list_prod_cells, stop_list)
        needed_time = int(distance // worker.vehicle.speed)
        # Create a clipping
        data = [0, worker.current_time + needed_time, max_supply]
        update_schedule_elem = update_update_schedule(update_schedule_elem, data)
        schedule_elem = schedule_generator(update_schedule_elem, details_elem)
        max_level_idx = np.where(schedule_elem[0] == np.amax(schedule_elem[0]))
        max_level_idx = (list(zip(max_level_idx[0])))[0][0]
        max_value = schedule_elem[0, max_level_idx]
        # Set the allowed maximum
        if max_value > 100:
            supply_value = round(max_supply - (max_value - 100), 2)
        else:
            supply_value = round(max_supply, 2)
        # Determine the maximum number of containers delivered
        container_capacity = plant.containers_capacities[details_elem[0].container_type]
        max_components = int(supply_value * details_elem[0].max_containers_num * container_capacity / 100)
        max_containers = max_components // container_capacity
        # Check how much space is left and draw the provided value
        container_size = plant.containers_size[details_elem[0].container_type]
        if max_containers >= 1 and container_size <= worker.current_capacity:
            # Check how much space is left
            current_capacity = worker.current_capacity
            max_capacity = 0
            while current_capacity >= container_size:
                max_capacity += 1
                current_capacity -= container_size
            max_containers = min(max_capacity, max_containers)
            # Draw the provided value
            supply_containers = rd.randint(1, max_containers)
            supply_value = round(100 * supply_containers / details_elem[0].max_containers_num, 2)
            # Update the data
            worker.current_capacity -= (supply_containers * plant.containers_size[details_elem[0].container_type])
            worker.supplied_idx.append(supply_idx)
            worker.current_time += needed_time
            # Update update_schedule
            update_data = [supply_idx, worker.current_time, supply_value]
            update_schedule = update_update_schedule(update_schedule, update_data)
        # Preventing infinite loops
        if check == worker.current_capacity:
            attempts -= 1
            if attempts == 0:
                break
            else:
                continue
    return update_schedule


def find_solution(update_schedule, schedule_details, list_prod_cells, worker, plant, attempts):
    # The main loop planning the employee's work during the shift
    main_loop_attempts = attempts
    worker.current_time = 1
    worker.distance = 0
    worker.supply_schedule = []
    worker.store_schedule = []
    update_schedule_copy = copy.deepcopy(update_schedule)
    new_update_schedule = np.zeros_like(update_schedule)
    while worker.current_time < worker.work_time:
        check = worker.current_time
        new_update_schedule = create_single_delivery(update_schedule_copy, schedule_details, list_prod_cells,
                                                     worker, plant, attempts)
        # Check if something has been delivered
        if len(worker.supplied_idx) > 0:
            worker.supply_schedule.append(worker.supplied_idx)
            # Go back to the warehouse
            last_idx = schedule_details[worker.supplied_idx[-1]].store_idx
            stop_list = [last_idx, 0]
            distance = calculate_distance(plant, list_prod_cells, stop_list)
            needed_time = int(distance // worker.vehicle.speed)
            worker.current_time += needed_time
        # Preventing infinite loops
        if check == worker.current_time:
            main_loop_attempts -= 1
            if main_loop_attempts == 0:
                break
            else:
                continue
    # Calculate distance
    worker.distance = worker.vehicle.speed * worker.current_time
    # Make a list of visited stores
    for delivery in worker.supply_schedule:
        worker.store_schedule.append(0)
        for component in delivery:
            worker.store_schedule.append(schedule_details[component].store_idx)
    worker.store_schedule.append(0)
    return new_update_schedule


def production_evaluation(update_schedule, schedule_details, list_of_product, multipliers):
    profit_multiplier = multipliers[0]
    costs_multiplier = multipliers[1]
    # Determine the schedule
    schedule = schedule_generator(update_schedule, schedule_details)
    work_time = len(schedule[0])
    # Separation of components into products
    production_data = iter(range(len(schedule_details)))
    production_rate = 0
    production_details = {}
    for idx in production_data:
        production_time = 0
        next_elem = schedule_details[idx]
        # Check which product it is and all its components
        all_components = [i for i, x in enumerate(schedule_details) if x.product_idx == next_elem.product_idx
                          and x.store_idx == next_elem.store_idx and x.machine_idx == next_elem.machine_idx]
        # Check if all components are available for production
        time_idx = 0
        while time_idx < work_time:
            # Check if there are enough components for production
            flag = 1
            for elem_idx in all_components:
                if schedule[elem_idx, time_idx] < schedule_details[elem_idx].consumption_per_min:
                    flag = 0
            # Increase production time if production is ON
            if flag == 1:
                production_time += 1
            time_idx += 1
        # Count production costs
        production_costs = 0
        for elem_idx in all_components:
            production_costs += costs_multiplier * schedule_details[elem_idx].cost_per_min
        # Count the profit on production
        elem_idx = all_components[0]
        product_idx = schedule_details[elem_idx].product_idx
        production_profit = profit_multiplier * list_of_product[product_idx-1].prod_per_min * list_of_product[
            product_idx-1].profit
        # Sum profit and costs
        production_rate += round((production_profit - production_costs) * production_time, 2)
        production_details[product_idx] = production_time
        # Skip the completed components
        if len(all_components) > 1:
            for temp_idx in range(0, len(all_components) - 1):
                next(production_data)
    return production_rate, production_details


def workers_evaluation(list_of_workers, multipliers):
    fuel_multiplier = multipliers[2]
    salary_multiplier = multipliers[3]
    workers_costs = 0
    vehicles_costs = 0
    workers_details = {}
    # Calculate for all workers:
    for idx in range(len(list_of_workers)):
        worker = list_of_workers[idx]
        workers_costs += salary_multiplier * worker.driver_cost * worker.work_time
        vehicles_costs += fuel_multiplier * worker.distance * worker.vehicle.fuel_cost
        workers_details[idx+1] = worker.distance
    return workers_costs + vehicles_costs, workers_details


def objective_function(update_schedule, schedule_details, list_of_product, list_of_workers, multipliers):
    production_rate, production_details = production_evaluation(update_schedule, schedule_details, list_of_product, multipliers)
    workers_costs, workers_details = workers_evaluation(list_of_workers, multipliers)
    return production_rate - workers_costs, [production_details, workers_details]


def tabu_search(update_schedule, schedule_details, list_of_product, list_of_workers, list_prod_cells, plant,
                attempts, number_of_iterations, reset_time, multipliers, self=None):

    # Define variables
    time_start = time.time()
    iteration = 1
    tabu_list = []
    first_update_schedule = copy.deepcopy(update_schedule)
    new_update_schedule = np.zeros_like(update_schedule)
    schedule = np.zeros_like(update_schedule)
    num_of_worker = len(list_of_workers)

    # Create taboo list
    for i in range(0, reset_time):
        tabu_list.append([])

    # Find first solution and save schedule of every worker
    for worker in list_of_workers:
        last_update_schedule = copy.deepcopy(first_update_schedule)
        first_update_schedule = find_solution(first_update_schedule, schedule_details, list_prod_cells, worker, plant, attempts)
        worker.update_schedule = np.subtract(first_update_schedule, last_update_schedule)

    best_update_schedule = copy.deepcopy(first_update_schedule)
    best_schedule = schedule_generator(best_update_schedule, schedule_details)
    best_rate, best_evaluation_details = objective_function(first_update_schedule, schedule_details, list_of_product, list_of_workers, multipliers)
    best_iteration = 0

    # tabu_list[0] = best_update_schedule

    # Solution search loop with the taboo algorithm
    while iteration <= number_of_iterations:

        # Randomly select an employee to change the delivered components
        idx = rd.randint(0, num_of_worker - 1)
        worker = list_of_workers[idx]

        # Looking for a new solution that is not on the taboo list
        flag = True
        while flag:
            flag = False

            last_update_schedule = copy.deepcopy(update_schedule)
            for elem in range(num_of_worker):
                if elem != idx:
                    last_update_schedule = np.add(last_update_schedule, list_of_workers[elem].update_schedule)
            new_update_schedule = find_solution(last_update_schedule, schedule_details, list_prod_cells, worker, plant, attempts)
            schedule = schedule_generator(new_update_schedule, schedule_details)

            # Move the selected employee to the end of the list and save new update schedule
            if idx < num_of_worker-1:
                list_of_workers.append(list_of_workers.pop(idx))

            list_of_workers[-1].update_schedule = np.subtract(new_update_schedule, last_update_schedule)

            for elem in tabu_list:
                is_in_tabu = np.array_equal(new_update_schedule, elem)
                if is_in_tabu:
                    flag = True

            rate, evaluation_details = objective_function(new_update_schedule, schedule_details, list_of_product, list_of_workers, multipliers)
            if rate > best_rate:
                flag = False

        # rate, evaluation_details = objective_function(new_update_schedule, schedule_details, list_of_product, list_of_workers, multipliers)

        # Check if the new solution is better
        if rate > best_rate:
            best_update_schedule = copy.deepcopy(new_update_schedule)
            best_schedule = copy.deepcopy(schedule)
            best_rate = round(rate, 2)
            best_evaluation_details = evaluation_details
            best_iteration = iteration

        # Progress bar
        progress_value = 100 * iteration // number_of_iterations
        if self is not None:
            progress_string = 'Progress: {0}%'.format(progress_value)
            progress_label = tk.Label(self.frame2, text=progress_string, font='arial 10')
            progress_label.grid(row=1, column=0, pady=[0, 20], padx=10)
            self.update_idletasks()
        else:
            print('Progress: {0}%'.format(progress_value))

        # Prepare for next iteration
        idx = iteration % reset_time
        tabu_list[idx] = copy.deepcopy(new_update_schedule)
        iteration += 1

    best_schedule = schedule_generator(best_update_schedule, schedule_details)
    time_end = time.time() - time_start

    return best_schedule, best_rate, best_evaluation_details, best_iteration, time_end
