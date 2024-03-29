import numpy as np
import copy
from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox import set_qubit_state
from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.classical_communication.message import StructuredMessage

def main(app_config=None, phi=0., theta=0.):
    log_config = app_config.log_config
    app_logger = get_new_app_logger(app_name="sender", log_config=log_config)

    # Create a socket to send classical information
    socket = Socket("sender", "receiver", log_config=log_config)

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("receiver")

    print("Starting DEJMPS protocol")

    # Initialize the connection to the backend
    sender = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=log_config,
        epr_sockets=[epr_socket]
    )
    N = 1
    socket.send_structured(StructuredMessage("Number of iterations", N))
    # epr_list = epr_socket.create(number=N+1)
    success = False
    with sender, open("outcomes.txt", 'a') as file:
        for i in range(N):
            # sender.flush()
            # print(f"iteration {i+1}")
            # Create EPR pairs
            # print(f"Alice: success={success}")
            if not success:
                epr1 = epr_socket.create()[0]  # note: in the paper, Eve makes the pairs
            # print("Alice sent first pair")
            sender.flush()
            original_dm = get_qubit_state(epr1, reduced_dm=False)
            # print(original_dm, type(original_dm))
            original_dm = copy.copy(original_dm)
            sender.flush()
            epr2 = epr_socket.create()[0]

            # epr1 = epr_list[0]
            # original_dm = get_qubit_state(epr1, reduced_dm=False)
            # epr2 = epr_list[i+1]
            # print("After receive")
            sender.flush()
            # print("Alice has created the EPR pairs")
            epr1.rot_X(1, 1)  # X-rotation of pi/2
            epr2.rot_X(1, 1)
            # epr2.H()
            # epr2.rot_Y(angle=0.234245)
            epr1.cnot(epr2)
            # print("Alice applied her gates")
            sender.flush()
            print("before meas:\n", np.round(get_qubit_state(epr1, reduced_dm=False)))
            sender_outcome = epr2.measure()
            sender.flush()  # flush only for print
            # print(np.round(get_qubit_state(epr1, reduced_dm=False),2))

            # print(f"Alice measured {sender_outcome}")


            # Send the correction information

            socket.send_structured(StructuredMessage("Alice\'s outcome", sender_outcome))
            # print(f"Alice sent her outcome {sender_outcome} to Bob")
            sender.flush()

            success = socket.recv_structured().payload
            sender.flush()

            dm = get_qubit_state(epr1, reduced_dm=False)

            socket.send_structured(StructuredMessage("Acknowledged", '0'))  # this is just to make sure that Alice
            #                                                                 gets the epr1 state before Bob measures it

            phi00 = np.array([1, 0, 0, 1]) / np.sqrt(2)
            # print(original_dm.shape)
            # print(dm.shape)
            # print(np.round(original_dm,2))
            print(np.round(dm,2))
            F_in = phi00.T @ original_dm @ phi00
            F_out = phi00.T @ dm @ phi00
            # print(np.round(dm, 2))
            # print(f"F_in: {np.round(np.real(F_in), 3)}, F_out: {np.round(np.real(F_out), 3)}")
            # if success:
            #     file.write(f"{np.real(F_in)} {np.real(F_out)}\n")
            file.write(f"{int(success)} {int(F_out > F_in)}\n")
            # if not success:
            #     return
            # print("Alice tries to free")
            sender.flush()
            if not success:
                # print("Not free")
                epr1.measure()
                # print("Free")
            # print("flush?")
            sender.flush()
            # print("flush!")
            print(int(success), np.real(F_in), np.real(F_out))


if __name__ == "__main__":
    main()
