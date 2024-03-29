import os
import csv
# import matplotlib.pyplot as plt
import numpy as np
import yamltools

# yamltools.change_link_fidelity(0.7)
# yamltools.change_gate_fidelity(1)
# quit()
def get_output_fidelity():
    # if os.name == 'nt':
    #     print("yeah")
    #     # command = "wsl cd /mnt/c/users/benja/Programming/PycharmProjects/QCC-project/DEJMPS & wsl netqasm simulate --formalism dm"
    #     os.system("wsl")
    #     print('1')
    #     os.system("cd /mnt/c/users/benja/Programming/PycharmProjects/QCC-project/DEJMPS")
    #     print('?')
    d = os.popen("netqasm simulate --formalism dm").read().split("\n")
    # print(d)
    x = float(d[-2])
    # if x <= 0.25:   # TODO: fix DEJMPS such that this doesn't happen anymore
    #     return get_output_fidelity()
    print(x)
    return x


def get_fidelity_ratio(gate_fidelity, link_fidelity):
    yamltools.change_gate_fidelity(gate_fidelity)
    yamltools.change_link_fidelity(link_fidelity)
    while True:
        cmd_out = os.popen("netqasm simulate --formalism dm").read()
        d = cmd_out.split("\n")
        last_line_split = d[-2].split()
        print(last_line_split)
        success = int(last_line_split[0])
        F_in = float(last_line_split[1])
        F_out = float(last_line_split[2])
        if success:
            break

    # if x <= 0.25:   # TODO: fix DEJMPS such that this doesn't happen anymore
    #     return get_output_fidelity()
    return F_out/F_in

# def find_min_fidelity(gate_fidelity, n_iter=6, file=None):
#     # find minimum link fidelity such that fidelity improves under DEJMPS given gate fidelity
#     # make sure N=1 in app_sender!
#     yamltools.change_gate_fidelity(gate_fidelity)
#     min_input_fidelity = 0
#     max_input_fidelity = 1
#     for i in range(n_iter):
#         current_input_fidelity = (min_input_fidelity + max_input_fidelity)/2
#         yamltools.change_link_fidelity(current_input_fidelity)
#         output_fidelity = get_output_fidelity()
#         if output_fidelity > current_input_fidelity:
#             max_input_fidelity = current_input_fidelity
#         else:
#             min_input_fidelity = current_input_fidelity
#
#     return (min_input_fidelity + max_input_fidelity)/2



gate_fidelities = np.arange(0.9, 1.00001, 0.001)
link_fidelities = np.arange(0, 1.00001, 0.01)
with open("gate_fidelity_axes.csv", 'a') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(gate_fidelities)
    writer.writerow(link_fidelities)
    print("written")
# grid = np.meshgrid(gate_fidelities, link_fidelities)


for f_gate in gate_fidelities:
    print(f"f_gate: {f_gate}")
    f_ratios = [get_fidelity_ratio(f_gate, f_link) for f_link in link_fidelities]
    with open("gate_fidelity_data.csv", 'a') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(f_ratios)
        print("written")

# x_axis = np.linspace(0,1, 3)
# y = [find_min_fidelity(float(x), n_iter=2) for x in x_axis]
# print(y)
# plt.plot(x_axis, y)


