#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import tkinter as tk
import Classes as Cls
import Functions as Fun
import Errors as Err
import random as rd
import numpy as np

containers_size_ = {1: 1, 2: 2, 3: 4}
containers_capacities_ = {1: 40, 2: 80, 3: 160}
max_containers_num_ = 3
initial_quantity_ = 20  # [in %]

num_of_components_ = 30
min_cost_ = 0.2
max_cost_ = 0.5

num_of_products_ = 10
min_profit_ = 10.0
max_profit_ = 12.0
min_req_components_ = 1
max_req_components_ = 3
min_prod_per_min_ = 1.0
max_prod_per_min_ = 2.0
min_req_num_ = 1
max_req_num_ = 3

speed_ = 1.0
capacity_ = 16
fuel_consumption_ = 0.01
number_of_carts_ = 3
driver_cost_ = 20.0
work_time_ = 0.5  # [in hours]

num_of_section_ = 3
section_length_ = 100
sections_distance_ = 50
warehouse_distance_ = 100
num_of_machines_ = num_of_products_  # num_of_machines <= num_of_products
num_prod_cells_ = rd.randint(int(0.5 * num_of_machines_), int(0.75 * num_of_machines_))

profit_multiplier_ = 1.0
costs_multiplier_ = 1.0
fuel_multiplier_ = 1.0
salary_multiplier_ = 1.0
attempts_ = 20
number_of_iterations_ = 10
reset_time_ = int(0.2 * number_of_iterations_)

schedule_ = None
schedule_details_ = None
update_schedule_ = None
list_of_products_ = []
list_of_components_ = []
list_prod_cells_ = []
rate_ = 0
time_ = 0
evaluation_details_ = []
iteration_ = 0
check = 0


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(MainMenu)
        self.title('Application')

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()


class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        title = tk.Label(self, text="Planning the delivery of components\nin the production plant", font='arial 14 bold')
        title.grid(row=0, column=0, pady=50, padx=50)

        instruction_button = tk.Button(self, text="Instruction", font='arial 12', command=lambda: master.switch_frame(Instruction))
        instruction_button.grid(row=1, column=0, pady=10, padx=10)
        production_button = tk.Button(self, text="Production", font='arial 12', command=lambda: master.switch_frame(Production))
        production_button.grid(row=2, column=0, pady=10, padx=10)
        plant_button = tk.Button(self, text="Plant", font='arial 12', command=lambda: master.switch_frame(Plant))
        plant_button.grid(row=3, column=0, pady=10, padx=10)
        solution_button = tk.Button(self, text="Solution", font='arial 12', command=lambda: master.switch_frame(Solution))
        solution_button.grid(row=4, column=0, pady=[10, 50], padx=10)


class Instruction(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.frame0 = tk.Frame(self)
        self.frame0.grid(row=0, column=0)
        self.frame1 = tk.Frame(self.frame0)
        self.frame1.grid(row=1, column=0, padx=20)

        title = tk.Label(self.frame0, text="Instruction", font='arial 12 bold')
        title.grid(row=0, column=0, pady=30, padx=30)

        scroll = tk.Scrollbar(self.frame1)
        textarea = tk.Text(self.frame1, font='arial 11', wrap=tk.WORD)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        textarea.pack(side=tk.LEFT, fill=tk.Y)
        scroll.config(command=textarea.yview)
        textarea.config(yscrollcommand=scroll.set)

        with open("instruction.txt", "r") as instr:
            data = instr.read()
        textarea.insert(tk.END, data)

        textarea.tag_configure("center", justify='center')
        textarea.tag_add("center", 1.0, "end")

        return_button = tk.Button(self.frame0, text="Return", font='arial 12', command=lambda: master.switch_frame(MainMenu))
        return_button.grid(row=2, column=0, pady=20, padx=10)


class Production(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # CONTAINERS
        title = tk.Label(self, text="Containers", font='arial 12 bold')
        title.grid(row=0, column=0, pady=10, padx=10)

        tk.Label(self, text="Containers size: ", font='arial 11').grid(row=1, column=0, padx=10)
        tk.Label(self, text="Container 1: ").grid(row=1, column=1, padx=10)
        tk.Label(self, text="Container 2: ").grid(row=1, column=3, padx=10)
        tk.Label(self, text="Container 3: ").grid(row=1, column=5, padx=10)
        self.con_1_size = tk.IntVar()
        self.con_2_size = tk.IntVar()
        self.con_3_size = tk.IntVar()
        tk.Entry(self, textvariable=self.con_1_size).grid(row=1, column=2, padx=10)
        tk.Entry(self, textvariable=self.con_2_size).grid(row=1, column=4, padx=10)
        tk.Entry(self, textvariable=self.con_3_size).grid(row=1, column=6, padx=10)
        self.con_1_size.set(containers_size_[1])
        self.con_2_size.set(containers_size_[2])
        self.con_3_size.set(containers_size_[3])

        tk.Label(self, text="Containers capacities: ", font='arial 11').grid(row=2, column=0, padx=10)
        tk.Label(self, text="Container 1: ").grid(row=2, column=1, padx=10)
        tk.Label(self, text="Container 2: ").grid(row=2, column=3, padx=10)
        tk.Label(self, text="Container 3: ").grid(row=2, column=5, padx=10)
        self.con_1_cap = tk.IntVar()
        self.con_2_cap = tk.IntVar()
        self.con_3_cap = tk.IntVar()
        tk.Entry(self, textvariable=self.con_1_cap).grid(row=2, column=2, padx=10)
        tk.Entry(self, textvariable=self.con_2_cap).grid(row=2, column=4, padx=10)
        tk.Entry(self, textvariable=self.con_3_cap).grid(row=2, column=6, padx=10)
        self.con_1_cap.set(containers_capacities_[1])
        self.con_2_cap.set(containers_capacities_[2])
        self.con_3_cap.set(containers_capacities_[3])

        tk.Label(self, text="Number of containers in the store:", font='arial 11').grid(row=3, column=0, padx=10)
        tk.Label(self, text="Maximum: ").grid(row=3, column=1, padx=10)
        self.con_num = tk.IntVar()
        tk.Entry(self, textvariable=self.con_num).grid(row=3, column=2, padx=10)
        self.con_num.set(max_containers_num_)
        tk.Label(self, text="Initial quantity of components in the store:", font='arial 11').grid(row=4, column=0, padx=10)
        tk.Label(self, text="Value [%]: ").grid(row=4, column=1, padx=10)
        self.init_quantity = tk.IntVar()
        tk.Entry(self, textvariable=self.init_quantity).grid(row=4, column=2, padx=10)
        self.init_quantity.set(initial_quantity_)

        # COMPONENTS
        title = tk.Label(self, text="Components", font='arial 12 bold')
        title.grid(row=6, column=0, pady=10, padx=10)

        tk.Label(self, text="Number of components:", font='arial 11').grid(row=7, column=0, padx=10)
        tk.Label(self, text="Value: ").grid(row=7, column=1, padx=10)
        self.comp_num = tk.IntVar()
        tk.Entry(self, textvariable=self.comp_num).grid(row=7, column=2, padx=10)
        self.comp_num.set(num_of_components_)

        tk.Label(self, text="Component cost per item:", font='arial 11').grid(row=8, column=0, padx=10)
        tk.Label(self, text="Minimum: ").grid(row=8, column=1, padx=10)
        tk.Label(self, text="Maximum: ").grid(row=8, column=3, padx=10)
        self.min_cost = tk.DoubleVar()
        self.max_cost = tk.DoubleVar()
        tk.Entry(self, textvariable=self.min_cost).grid(row=8, column=2, padx=10)
        tk.Entry(self, textvariable=self.max_cost).grid(row=8, column=4, padx=10)
        self.min_cost.set(min_cost_)
        self.max_cost.set(max_cost_)

        # PRODUCTS
        title = tk.Label(self, text="Products", font='arial 12 bold')
        title.grid(row=10, column=0, pady=10, padx=10)

        tk.Label(self, text="Number of products:", font='arial 11').grid(row=11, column=0, padx=10)
        tk.Label(self, text="Value: ").grid(row=11, column=1, padx=10)
        self.prod_num = tk.IntVar()
        tk.Entry(self, textvariable=self.prod_num).grid(row=11, column=2, padx=10)
        self.prod_num.set(num_of_products_)

        tk.Label(self, text="Profit for one item produced:", font='arial 11').grid(row=12, column=0, padx=10)
        tk.Label(self, text="Minimum: ").grid(row=12, column=1, padx=10)
        tk.Label(self, text="Maximum: ").grid(row=12, column=3, padx=10)
        self.min_profit = tk.DoubleVar()
        self.max_profit = tk.DoubleVar()
        tk.Entry(self, textvariable=self.min_profit).grid(row=12, column=2, padx=10)
        tk.Entry(self, textvariable=self.max_profit).grid(row=12, column=4, padx=10)
        self.min_profit.set(min_profit_)
        self.max_profit.set(max_profit_)

        tk.Label(self, text="Required number of components for production:", font='arial 11').grid(row=13, column=0, padx=10)
        tk.Label(self, text="Minimum: ").grid(row=13, column=1, padx=10)
        tk.Label(self, text="Maximum: ").grid(row=13, column=3, padx=10)
        self.min_req = tk.IntVar()
        self.max_req = tk.IntVar()
        tk.Entry(self, textvariable=self.min_req).grid(row=13, column=2, padx=10)
        tk.Entry(self, textvariable=self.max_req).grid(row=13, column=4, padx=10)
        self.min_req.set(min_req_components_)
        self.max_req.set(max_req_components_)

        tk.Label(self, text="Produced quantity per minute:", font='arial 11').grid(row=14, column=0, padx=10)
        tk.Label(self, text="Minimum: ").grid(row=14, column=1, padx=10)
        tk.Label(self, text="Maximum: ").grid(row=14, column=3, padx=10)
        self.min_prod = tk.DoubleVar()
        self.max_prod = tk.DoubleVar()
        tk.Entry(self, textvariable=self.min_prod).grid(row=14, column=2, padx=10)
        tk.Entry(self, textvariable=self.max_prod).grid(row=14, column=4, padx=10)
        self.min_prod.set(min_prod_per_min_)
        self.max_prod.set(max_prod_per_min_)

        tk.Label(self, text="Required amount of a given component for production:", font='arial 11').grid(row=15, column=0, padx=10)
        tk.Label(self, text="Minimum: ").grid(row=15, column=1, padx=10)
        tk.Label(self, text="Maximum: ").grid(row=15, column=3, padx=10)
        self.min_req_num = tk.IntVar()
        self.max_req_num = tk.IntVar()
        tk.Entry(self, textvariable=self.min_req_num).grid(row=15, column=2, padx=10)
        tk.Entry(self, textvariable=self.max_req_num).grid(row=15, column=4, padx=10)
        self.min_req_num.set(min_req_num_)
        self.max_req_num.set(max_req_num_)

        generate_button = tk.Button(self, text="Save", font='arial 12', command=self.generate_data)
        generate_button.grid(row=16, column=0, pady=[20, 0], padx=10)

        return_button = tk.Button(self, text="Return", font='arial 12', command=lambda: master.switch_frame(MainMenu))
        return_button.grid(row=18, column=0, pady=20, padx=10)

    def generate_data(self):
        global containers_size_, containers_capacities_, max_containers_num_, initial_quantity_
        containers_size_ = {1: self.con_1_size.get(), 2: self.con_2_size.get(), 3: self.con_3_size.get()}
        containers_capacities_ = {1: self.con_1_cap.get(), 2: self.con_2_cap.get(), 3: self.con_3_cap.get()}
        max_containers_num_ = self.con_num.get()
        initial_quantity_ = self.init_quantity.get()

        global num_of_components_, min_cost_, max_cost_, list_of_components_
        num_of_components_ = self.comp_num.get()
        min_cost_ = self.min_cost.get()
        max_cost_ = self.max_cost.get()
        list_of_components_ = Fun.component_generator(num_of_components_, containers_capacities_, min_cost_, max_cost_)

        global num_of_products_, min_profit_, max_profit_, min_req_components_, max_req_components_, min_prod_per_min_, \
            max_prod_per_min_, min_req_num_, max_req_num_, list_of_products_
        num_of_products_ = self.prod_num.get()
        min_profit_ = self.min_profit.get()
        max_profit_ = self.max_profit.get()
        min_req_components_ = self.min_req.get()
        max_req_components_ = self.max_req.get()
        min_prod_per_min_ = self.min_prod.get()
        max_prod_per_min_ = self.max_prod.get()
        min_req_num_ = self.min_req_num.get()
        max_req_num_ = self.max_req_num.get()
        list_of_products_ = Fun.products_generator(num_of_components_, num_of_products_, min_profit_, max_profit_,
                                                   min_req_components_, max_req_components_, min_prod_per_min_,
                                                   max_prod_per_min_, min_req_num_, max_req_num_)
        if list_of_products_:
            global check
            check = 1
            save_label = tk.Label(self, text="Saved!", font='arial 11')
            save_label.grid(row=17, column=0, padx=10)


class Plant(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # WORKERS
        title = tk.Label(self, text="Workers", font='arial 12 bold')
        title.grid(row=0, column=0, pady=10, padx=10)

        tk.Label(self, text="Vehicle: ", font='arial 11').grid(row=1, column=0, padx=10)
        tk.Label(self, text="Speed [m/s]: ").grid(row=1, column=1, padx=10)
        tk.Label(self, text="Capacity: ").grid(row=1, column=3, padx=10)
        tk.Label(self, text="Fuel consumption [/m]: ").grid(row=1, column=5, padx=10)
        self.speed = tk.DoubleVar()
        self.capacity = tk.IntVar()
        self.fuel_cons = tk.DoubleVar()
        tk.Entry(self, textvariable=self.speed).grid(row=1, column=2, padx=10)
        tk.Entry(self, textvariable=self.capacity).grid(row=1, column=4, padx=10)
        tk.Entry(self, textvariable=self.fuel_cons).grid(row=1, column=6, padx=10)
        self.speed.set(speed_)
        self.capacity.set(capacity_)
        self.fuel_cons.set(fuel_consumption_)

        tk.Label(self, text="Number of workers:", font='arial 11').grid(row=2, column=0, padx=10)
        tk.Label(self, text="Value: ").grid(row=2, column=1, padx=10)
        self.num_carts = tk.IntVar()
        tk.Entry(self, textvariable=self.num_carts).grid(row=2, column=2, padx=10)
        self.num_carts.set(number_of_carts_)

        tk.Label(self, text="Employee salary:", font='arial 11').grid(row=3, column=0, padx=10)
        tk.Label(self, text="Value: [/hour]").grid(row=3, column=1, padx=10)
        self.driver_cost = tk.DoubleVar()
        tk.Entry(self, textvariable=self.driver_cost).grid(row=3, column=2, padx=10)
        self.driver_cost.set(driver_cost_)

        tk.Label(self, text="Work time:", font='arial 11').grid(row=4, column=0, padx=10)
        tk.Label(self, text="Value [hours]: ").grid(row=4, column=1, padx=10)
        self.work_time = tk.DoubleVar()
        tk.Entry(self, textvariable=self.work_time).grid(row=4, column=2, padx=10)
        self.work_time.set(work_time_)

        # PLANT

        title = tk.Label(self, text="Plant", font='arial 12 bold')
        title.grid(row=8, column=0, pady=10, padx=10)

        tk.Label(self, text="Number of sections:", font='arial 11').grid(row=9, column=0, padx=10)
        tk.Label(self, text="Value: ").grid(row=9, column=1, padx=10)
        self.num_sec = tk.IntVar()
        tk.Entry(self, textvariable=self.num_sec).grid(row=9, column=2, padx=10)
        self.num_sec.set(num_of_section_)

        tk.Label(self, text="Sections length:", font='arial 11').grid(row=10, column=0, padx=10)
        tk.Label(self, text="Value [m]: ").grid(row=10, column=1, padx=10)
        self.sec_length = tk.IntVar()
        tk.Entry(self, textvariable=self.sec_length).grid(row=10, column=2, padx=10)
        self.sec_length.set(section_length_)

        tk.Label(self, text="Distance between sections:", font='arial 11').grid(row=11, column=0, padx=10)
        tk.Label(self, text="Value [m]: ").grid(row=11, column=1, padx=10)
        self.sec_dist = tk.IntVar()
        tk.Entry(self, textvariable=self.sec_dist).grid(row=11, column=2, padx=10)
        self.sec_dist.set(sections_distance_)

        tk.Label(self, text="Distance to warehouse:", font='arial 11').grid(row=12, column=0, padx=10)
        tk.Label(self, text="Value [m]: ").grid(row=12, column=1, padx=10)
        self.war_dist = tk.IntVar()
        tk.Entry(self, textvariable=self.war_dist).grid(row=12, column=2, padx=10)
        self.war_dist.set(warehouse_distance_)

        tk.Label(self, text="Number of machines:", font='arial 11').grid(row=13, column=0, padx=10)
        tk.Label(self, text="Value: ").grid(row=13, column=1, padx=10)
        self.num_mach = tk.IntVar()
        tk.Entry(self, textvariable=self.num_mach).grid(row=13, column=2, padx=10)
        self.num_mach.set(num_of_machines_)

        tk.Label(self, text="Number of production cells:", font='arial 11').grid(row=14, column=0, padx=10)
        tk.Label(self, text="Value: ").grid(row=14, column=1, padx=10)
        self.num_cells = tk.IntVar()
        tk.Entry(self, textvariable=self.num_cells).grid(row=14, column=2, padx=10)
        self.num_cells.set(num_prod_cells_)

        generate_plant_button = tk.Button(self, text="Save", font='arial 12', command=self.generate_plant_data)
        generate_plant_button.grid(row=15, column=0, pady=[20, 10], padx=10)

        return_button = tk.Button(self, text="Return", font='arial 12', command=lambda: master.switch_frame(MainMenu))
        return_button.grid(row=17, column=0, pady=20, padx=10)

    def generate_plant_data(self):
        global check
        if check > 0:
            global delivery_cart_, list_of_workers_, speed_, capacity_, fuel_consumption_, number_of_carts_, \
                update_schedule_, driver_cost_, work_time_
            speed_ = self.speed.get()
            capacity_ = self.capacity.get()
            fuel_consumption_ = self.fuel_cons.get()
            number_of_carts_ = self.num_carts.get()
            driver_cost_ = self.driver_cost.get()
            work_time_ = self.work_time.get()  # [in hours]

            delivery_cart_ = Cls.Vehicle(60*speed_, capacity_, fuel_consumption_)  # calculate speed from m/s to m/min
            list_of_workers_ = []
            for num in range(0, number_of_carts_):
                list_of_workers_.append(Cls.Worker(delivery_cart_, (driver_cost_/60), work_time_))

            global num_of_section_, section_length_, sections_distance_, warehouse_distance_, num_of_machines_, \
                num_prod_cells_, plant_, list_prod_cells_, schedule_details_, update_schedule_, list_of_products_
            num_of_section_ = self.num_sec.get()
            section_length_ = self.sec_length.get()
            sections_distance_ = self.sec_dist.get()
            warehouse_distance_ = self.war_dist.get()
            num_of_machines_ = self.num_mach.get()  # num_of_machines <= num_of_products
            if num_of_machines_ > num_of_products_:
                error_ = tk.Toplevel(self)
                Err.NumberOfMachines(error_)
                num_of_machines_ = num_of_products_
            num_prod_cells_ = self.num_cells.get()

            plant_ = Cls.Factory(num_of_section_, section_length_, sections_distance_, warehouse_distance_, num_of_machines_,
                                 num_prod_cells_, containers_size_, containers_capacities_)
            list_prod_cells_ = Fun.man_cells_generator(plant_, max_containers_num_)
            Fun.select_production(list_prod_cells_, list_of_products_)
            Fun.identify_needed_components(list_prod_cells_)
            schedule_details_ = Fun.schedule_details_generator(list_prod_cells_, list_of_components_)
            update_schedule_ = Fun.update_schedule_generator(schedule_details_, initial_quantity_, work_time_)

            if update_schedule_ is not None:
                check = 2
                save_label = tk.Label(self, text="Saved!", font='arial 11')
                save_label.grid(row=16, column=0, padx=10)
        else:
            info_label = tk.Label(self, text="Generate products first!", font='arial 11')
            info_label.grid(row=16, column=0, padx=10)


class Solution(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.frame0 = tk.Frame(self)
        self.frame0.grid(row=0, column=0)
        self.frame1 = tk.Frame(self)
        self.frame1.grid(row=1, column=0)
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=2, column=0)
        self.frame3 = tk.Frame(self)
        self.frame3.grid(row=3, column=0)

        title = tk.Label(self.frame0, text="Solution", font='arial 14 bold')
        title.grid(row=0, column=0, pady=10, padx=50)

        tk.Label(self.frame1, text="Multipliers: ", font='arial 11').grid(row=2, column=0, padx=10)
        tk.Label(self.frame1, text="Profit: ").grid(row=2, column=1, padx=10)
        tk.Label(self.frame1, text="Costs: ").grid(row=2, column=3, padx=10)
        tk.Label(self.frame1, text="Fuel: ").grid(row=2, column=5, padx=10)
        tk.Label(self.frame1, text="Salary: ").grid(row=2, column=7, padx=10)
        self.profit_m = tk.DoubleVar()
        self.costs_m = tk.DoubleVar()
        self.fuel_m = tk.DoubleVar()
        self.salary_m = tk.DoubleVar()
        tk.Entry(self.frame1, textvariable=self.profit_m).grid(row=2, column=2, padx=10)
        tk.Entry(self.frame1, textvariable=self.costs_m).grid(row=2, column=4, padx=10)
        tk.Entry(self.frame1, textvariable=self.fuel_m).grid(row=2, column=6, padx=10)
        tk.Entry(self.frame1, textvariable=self.salary_m).grid(row=2, column=8, padx=10)
        self.profit_m.set(profit_multiplier_)
        self.costs_m.set(costs_multiplier_)
        self.fuel_m.set(fuel_multiplier_)
        self.salary_m.set(salary_multiplier_)

        tk.Label(self.frame1, text="Algorithm: ", font='arial 11').grid(row=3, column=0, padx=10)
        tk.Label(self.frame1, text="Iteration: ").grid(row=3, column=1, padx=10)
        tk.Label(self.frame1, text="Reset: ").grid(row=3, column=3, padx=10)
        self.num_iter = tk.IntVar()
        self.reset_t = tk.IntVar()
        tk.Entry(self.frame1, textvariable=self.num_iter).grid(row=3, column=2, padx=10)
        tk.Entry(self.frame1, textvariable=self.reset_t).grid(row=3, column=4, padx=10)
        self.num_iter.set(number_of_iterations_)
        self.reset_t.set(reset_time_)

        generate_button = tk.Button(self.frame2, text="Find solution", font='arial 12', command=self.generate_data)
        generate_button.grid(row=0, column=0, pady=[20, 20], padx=10)

        self.text_field = tk.Text(self.frame2, width=60)
        self.text_field.grid(row=2, column=0, sticky="nsew")
        scroll_y = tk.Scrollbar(self.frame2, command=self.text_field.yview)
        scroll_y.grid(row=2, column=1, sticky='nsew')
        self.text_field['yscrollcommand'] = scroll_y.set
        self.text_field.config(borderwidth=3)
        self.text_field.insert(tk.END, "Run the algorithm to see the result.\n")

        show_button = tk.Button(self.frame3, text="Show solution", font='arial 12', command=self.show_solution)
        show_button.grid(row=0, column=0, pady=20, padx=20)

        details_button = tk.Button(self.frame3, text="Solution details", font='arial 12', command=lambda: master.switch_frame(Details))
        details_button.grid(row=0, column=1, pady=20, padx=20)

        return_button = tk.Button(self.frame3, text="Return", font='arial 12', command=lambda: master.switch_frame(MainMenu))
        return_button.grid(row=0, column=2, pady=20, padx=20)

    def generate_data(self):
        global check
        if check == 2:
            global profit_multiplier_, costs_multiplier_, fuel_multiplier_, salary_multiplier_, multipliers_, attempts_, \
                number_of_iterations_, reset_time_, schedule_, rate_, evaluation_details_, iteration_, time_
            profit_multiplier_ = self.profit_m.get()
            costs_multiplier_ = self.costs_m.get()
            fuel_multiplier_ = self.fuel_m.get()
            salary_multiplier_ = self.salary_m.get()
            number_of_iterations_ = self.num_iter.get()
            reset_time_ = self.reset_t.get()

            multipliers_ = [profit_multiplier_, costs_multiplier_, fuel_multiplier_, salary_multiplier_]
            update_schedule = copy.copy(update_schedule_)
            schedule_details = copy.copy(schedule_details_)
            list_of_products = copy.copy(list_of_products_)
            list_of_workers = copy.copy(list_of_workers_)
            list_prod_cells = copy.copy(list_prod_cells_)
            plant = copy.copy(plant_)
            attempts = copy.copy(attempts_)
            number_of_iterations = copy.copy(number_of_iterations_)
            reset_time = copy.copy(reset_time_)
            multipliers = copy.copy(multipliers_)

            self.text_field.delete('1.0', tk.END)
            self.text_field.insert(tk.END, "Wait for the result.\n")
            schedule_, rate_, evaluation_details_, iteration_, time_ = Fun.tabu_search(update_schedule, schedule_details, list_of_products, list_of_workers, list_prod_cells,
                                                                                       plant, attempts, number_of_iterations, reset_time, multipliers, self)
            self.show_solution()
        else:
            info_label = tk.Label(self.frame2, text="Generate plant first!", font='arial 11')
            info_label.grid(row=1, column=0, pady=[0, 20], padx=10)

    def show_solution(self):
        global rate_, evaluation_details_, iteration_
        if rate_ == 0:
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert(tk.END, 'Run the algorithm first')
        else:
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert(tk.END, 'Best rate:          {0}\n'.format(round(rate_, 2)))
            self.text_field.insert(tk.END, 'Best iteration:     {0}\n'.format(iteration_))
            self.text_field.insert(tk.END, '\nProduction details:\n')
            for key, value in evaluation_details_[0].items():
                self.text_field.insert(tk.END, 'Product index: {0} -> production {1}/{2} minutes\n'.format(key, value, int(60 * work_time_)))
            self.text_field.insert(tk.END, '\nWorkers details:')
            for key, value in evaluation_details_[1].items():
                self.text_field.insert(tk.END, '\nWorker: {0} -> distance: {1} m'.format(key, value))
            self.text_field.insert(tk.END, '\n\nExecution time:     {0}\n'.format(round(time_, 2)))


class Details(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.frame0 = tk.Frame(self)
        self.frame0.grid(row=0, column=0)
        self.frame1 = tk.Frame(self)
        self.frame1.grid(row=1, column=0)
        self.frame2 = tk.Frame(self.frame1)
        self.frame2.grid(row=0, column=2)

        title = tk.Label(self.frame0, text="Solution details", font='arial 14 bold')
        title.grid(row=0, column=0, pady=20, padx=50)

        self.text_field = tk.Text(self.frame1)
        self.text_field.grid(row=0, column=0, pady=[0, 20], padx=[20, 0], sticky="nsew")
        scroll_y = tk.Scrollbar(self.frame1, command=self.text_field.yview)
        scroll_y.grid(row=0, column=1, sticky='nsew')
        self.text_field['yscrollcommand'] = scroll_y.set
        self.text_field.config(borderwidth=3)
        self.text_field.insert(tk.END, "Choose what you want to see.\n")

        details_button = tk.Button(self.frame2, text="Plant", font='arial 12', command=self.print_plant)
        details_button.grid(row=0, column=0, pady=10, padx=10)

        details_button = tk.Button(self.frame2, text="Products details", font='arial 12', command=self.print_details)
        details_button.grid(row=1, column=0, pady=10, padx=10)

        schedule_button = tk.Button(self.frame2, text="Schedule", font='arial 12', command=self.print_schedule)
        schedule_button.grid(row=2, column=0, pady=10, padx=10)

        return_button = tk.Button(self.frame2, text="Return", font='arial 12', command=lambda: master.switch_frame(Solution))
        return_button.grid(row=3, column=0, pady=20, padx=10)

    def print_schedule(self):
        global schedule_
        if schedule_ is not None:
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert(tk.END, 'Best schedule:\n')
            schedule_ = np.around(schedule_, decimals=2)
            self.text_field.insert(tk.END, '{0}'.format(schedule_))
        else:
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert(tk.END, 'Run the algorithm first')

    def print_plant(self):
        global list_prod_cells_
        self.text_field.delete('1.0', tk.END)
        if list_prod_cells_:
            self.text_field.insert(tk.END, 'Plant details:\n')
            for cell in list_prod_cells_:
                self.text_field.insert(tk.END, '\nCell index: {0}\n'.format(cell.index))
                self.text_field.insert(tk.END, 'Section: {0}\n'.format(cell.section))
                self.text_field.insert(tk.END, 'Position: {0}\n'.format(cell.position))
                self.text_field.insert(tk.END, 'Manufactured products:\n')
                for elem in cell.manufactured_products:
                    self.text_field.insert(tk.END, '    Product index: {0}\n'.format(elem.index))
        else:
            self.text_field.insert(tk.END, 'Run the algorithm first')

    def print_details(self):
        global schedule_details_, list_of_products_
        self.text_field.delete('1.0', tk.END)
        if schedule_details_ is not None:
            self.text_field.insert(tk.END, 'Production details:\n')
            production_data = iter(range(len(schedule_details_)))
            for idx in production_data:
                next_elem = schedule_details_[idx]
                all_components = [i for i, x in enumerate(schedule_details_) if x.product_idx == next_elem.product_idx
                                  and x.store_idx == next_elem.store_idx and x.machine_idx == next_elem.machine_idx]

                product_idx = schedule_details_[all_components[0]].product_idx
                self.text_field.insert(tk.END, '\nProduct index: {0}\n'.format(product_idx))
                self.text_field.insert(tk.END, 'Production per minute: {0}\n'.format(list_of_products_[product_idx-1].prod_per_min))
                self.text_field.insert(tk.END, 'Profit per item: {0}\n'.format(list_of_products_[product_idx-1].profit))
                self.text_field.insert(tk.END, 'Needed components per item:\n')
                for component_idx, need_value in list_of_products_[product_idx-1].component_consumption.items():
                    self.text_field.insert(tk.END, '    Component index: {0}, Needed: {1}, Cost: {2}\n'
                                           .format(component_idx, need_value, list_of_components_[component_idx-1].cost))

                if len(all_components) > 1:
                    for temp_idx in range(0, len(all_components) - 1):
                        next(production_data)
        else:
            self.text_field.insert(tk.END, 'Run the algorithm first')


app = Application()
app.mainloop()
