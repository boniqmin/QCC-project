import os
import numpy as np
import matplotlib.pyplot as plt

# The number with which the fidelity is increased in network.yaml
delta_fidelity = 0.02

# An empty array to store the output values in
measurements = []

# The starting fidelity for the network.yaml file
fidelity = 0.0

# Loop over the fidelity
while fidelity <=1:
    # Load the networl.yaml and the template file
    fin = open("network_template.yaml", "rt")
    fout = open("network.yaml", "wt")

    # Update the fidelity in network.yaml
    for line in fin:
        # read replace the string and write to output file
        fout.write(line.replace('    fidelity: 1.0', '    fidelity: '+str(fidelity)))
    fin.close()
    fout.close()

    # Run netqasm simulation and store the result as an array
    d = os.popen('netqasm simulate --formalism dm').read().split("\n")

    # Upon success, store the measurement and increase the fidelity parameter
    if d[0]=="True":
        measurements.append([float(d[1]),float(d[2])])
        fidelity += delta_fidelity
    print(d)

# Convert the measurements to an array
measurements = np.array(measurements)
x= np.arange(0.25,1,0.001)
analytical_fraction = lambda x: (x**2+1/9*(1-x)**2)/(x**2+2/3*x*(1-x)+5/9*(1-x)**2)/x
# Plot the results
plt.plot(measurements[:,0],measurements[:,1]/measurements[:,0],label="Measured values")

# Plot the analytical solution
plt.plot(x,analytical_fraction(x),":",label="Analytical solution")

plt.title("The fraction $F_{out}/F_{in}$ upon success as function of $F_{in}$")
plt.xlabel("$F_{in}$")
plt.ylabel("$F_{out}/F_{in}$")
plt.grid()
plt.show()


