
# Distributed Rollback Recovery Simulator

## 1. Abstract

The Distributed Rollback Recovery Simulator is a small educational
project developed using Python and Tkinter. It demonstrates how
a distributed system can restore its process states after a failure.

The simulator contains three processes: P1, P2 and P3. Users can
send text messages, create checkpoints, simulate process failures,
and perform rollback recovery.

## 2. Problem Statement

When a process fails, its current state may be lost. Rollback
recovery helps restore the system to a previously saved state.
This project demonstrates that concept using a simple GUI.

## 3. Objectives

- Represent three simulated processes.
- Demonstrate message passing.
- Allow users to enter any text message.
- Create global checkpoints.
- Simulate process failure.
- Restore saved states using rollback recovery.
- Display events in a log.

## 4. Technologies Used

- Python 3
- Tkinter
- Python standard library

## 5. How the Simulator Works

1. The application initializes P1, P2 and P3 at state 0.
2. It creates an initial global checkpoint C0.
3. The user selects a sender and receiver and enters a message.
4. The sender and receiver states are updated.
5. The user creates a checkpoint to save all process states.
6. The user simulates a process failure.
7. Rollback restores all processes to the latest checkpoint.
8. The GUI displays the restored states and recovery status.

All communication is simulated within the application.
No real network communication is performed.

## 6. Project Structure

distributed_rollback_simulator/
    main.py
    process.py
    recovery.py
    README.md

## 7. How to Run

1. Install Python 3.
2. Ensure Tkinter is available.
3. Open a terminal in the project folder.
4. Run:

       python main.py

On some systems, use:

       python3 main.py

## 8. Example Execution

Initial states:
P1 = 0, P2 = 0, P3 = 0

Send "Hello" from P1 to P2:
P1 = 1, P2 = 1, P3 = 0

Create a checkpoint.

Send "How are you?" from P2 to P3:
P1 = 1, P2 = 2, P3 = 1

Fail P2 and perform rollback.

Restored states:
P1 = 1, P2 = 1, P3 = 0

Recovery Successful — System restored to checkpoint.

## 9. Conclusion

The project demonstrates checkpoint creation, message passing,
failure simulation and rollback recovery through a simple GUI.
It helps students understand the basic concepts of fault
tolerance and recovery in distributed computing.

## 10. Future Scope

Future improvements could include a visual message timeline,
multiple checkpoint selection, and a comparison of recovery
strategies.
