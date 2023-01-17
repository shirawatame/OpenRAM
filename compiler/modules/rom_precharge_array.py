# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from math import ceil
from openram.base import geometry
from openram.base import design
from openram.sram_factory import factory
from openram.base import vector
from openram.tech import layer, drc



class rom_precharge_array(design):
    """
    An array of inverters to create the inverted address lines for the rom decoder
    """
    def __init__(self, cols, pmos_size=None, name="", route_layer="li", strap_spacing=None):
        self.cols = cols
        self.route_layer = route_layer
        if name=="":
            name = "rom_inv_array_{0}".format(cols)
        # if pmos_size == None:
        #     self.pmos_size = dff.height * 0.5
        # else: 
        #     self.pmos_size = inv_size
        if strap_spacing != None:
            self.strap_spacing = strap_spacing 
        else:
            self.strap_spacing = 0

        if "li" in layer:
            self.inv_layer = "li"
        else:
            self.inv_layer = "m1"

        
        if strap_spacing != 0:
            self.num_straps = ceil(self.cols / self.strap_spacing)
            self.array_col_size = self.cols + self.num_straps  
        else:
            self.num_straps = 0
            self.array_col_size = self.cols

        super().__init__(name)
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        self.create_modules()
        self.add_pins()
        self.create_instances()
        


    def create_layout(self):
        self.width = self.cols * self.pmos.width 
        self.height = self.pmos.width
        self.place_instances()
        self.create_layout_pins()
        self.add_well_tap()
        self.route_supply()
        
        self.add_boundary()
        


    def add_boundary(self):
        # self.translate_all(self.well_ll)
        ur = self.find_highest_coords()
        # ur = vector(ur.x, ur.y - self.well_ll.y)
        super().add_boundary(vector(0, 0), ur)
        self.width = self.cols * self.pmos.width 
        self.height = ur.y 

    def create_modules(self):

        self.pmos = factory.create(module_type="rom_precharge_cell", module_name="precharge_cell", route_layer=self.route_layer)

        # For layout constants
        self.dummy = factory.create(module_type="rom_base_cell")
        self.poly_tap = factory.create(module_type="rom_poly_tap", strap_length=self.strap_spacing)

    def add_pins(self):
        for col in range(self.cols):
            self.add_pin("pre_bl{0}_out".format(col), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gate", "INPUT")

    def create_instances(self):
        self.array_insts = []
        self.pmos_insts = []
        self.tap_insts = []

        self.tap_insts.append(self.add_inst(name="tap_0", mod=self.poly_tap))
        self.connect_inst([])
        for col in range(self.cols):
            

            # if col % self.strap_spacing  == 0:
            #         name = "tap_c{}".format(col)
            #         tap = self.add_inst(name=name, mod=self.poly_tap)
            #         self.array_insts.append(tap)
            #         self.tap_insts.append(tap)
            #         self.connect_inst([])
            name = "Xpmos_c{0}".format(col)
            pmos = self.add_inst(name=name, mod=self.pmos)
            self.array_insts.append(pmos)
            self.pmos_insts.append(pmos)
            bl = "pre_bl{0}_out".format(col)
            self.connect_inst(["vdd", "gate", bl, "vdd"])
            
        print(self.array_insts)



    def place_instances(self):
        self.add_label("ZERO", self.route_layer)

        self.array_pos = []
        strap_num = 0      
        cell_y = 0  
        # columns are bit lines4
        cell_x = 0

        self.tap_insts[0].place(vector(cell_x, cell_y))

        for col in range(self.cols):

            # if col % self.strap_spacing == 0 :
            #     self.tap_insts[strap_num].place(vector(cell_x, cell_y))
            #     self.add_label("debug", "li", vector(cell_x, cell_y))
            #     cell_x += self.poly_tap.width
            #     strap_num += 1
                
            self.pmos_insts[col].place(vector(cell_x, cell_y))
            self.add_label("debug", "li", vector(cell_x, cell_y))
            cell_x += self.pmos.width
            

    def create_layout_pins(self):
        self.copy_layout_pin(self.tap_insts[0], "via", "gate")
        for col in range(self.cols):
            source_pin = self.pmos_insts[col].get_pin("D")
            bl = "pre_bl{0}_out".format(col)
            self.add_layout_pin_rect_center(bl, self.route_layer, source_pin.center())
        

    def add_well_tap(self):

        layer_stack = self.active_stack
        contact_x = self.pmos_insts[self.cols - 1].rx() + self.active_space
        contact_offset = vector(contact_x, self.pmos.height * 0.5)

        self.nwell_contact = self.add_via_center(layers=layer_stack,
                                                 offset=contact_offset,
                                                 implant_type="n",
                                                 well_type="n",
                                                 directions=("V", "V"))

    def route_supply(self):

        
        start_pin = self.pmos_insts[0].get_pin("S").lx()
        end_pin = self.pmos_insts[-1].get_pin("S").rx()
        spacing = drc["{0}_to_{0}".format(self.route_layer)]
        start = vector(start_pin, -2*spacing)
        end = vector(end_pin, -2*spacing)

        self.vdd = self.add_layout_pin_segment_center("vdd", "m1", start, end)

        for i in range(self.cols):
            start = self.pmos_insts[i].get_pin("S").center()
            end = vector(start.x, self.vdd.cy())

            self.add_segment_center(self.route_layer, start, end)
            self.add_via_stack_center(end, self.route_layer, "m1")


        # connect nwell tap to vdd

        start = end
        end = vector(self.nwell_contact.cx(), start.y)
        self.add_segment_center(self.route_layer, start, end)

        start = end - vector(0, 0.5 * self.mcon_width)
        end = self.nwell_contact.center()
        self.add_segment_center(self.route_layer, start, end)

