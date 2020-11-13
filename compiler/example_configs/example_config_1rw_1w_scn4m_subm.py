word_size = 4
num_words = 16
write_size = 2

num_rw_ports = 1
num_r_ports = 0
num_w_ports = 1

tech_name = "scn4m_subm"
nominal_corner_only = False
process_corners = ["TT"]
supply_voltages = [5.0]
temperatures = [25]

route_supplies = False
check_lvsdrc = True

output_path = "temp"
output_name = "sram_1rw_1r_{0}_{1}_{2}".format(word_size,
                                               num_words,
                                               tech_name)