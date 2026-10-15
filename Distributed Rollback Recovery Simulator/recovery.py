
from copy import deepcopy


class RecoveryManager:
    """Manages messages, checkpoints, failures and recovery."""

    def __init__(self, processes):
        self.processes = {
            process.process_id: process
            for process in processes
        }

        self.checkpoint = None
        self.checkpoint_id = None
        self.next_checkpoint_number = 0

    def send_message(self, sender_id, receiver_id, message):
        """Send any user-entered text between two processes."""

        if sender_id not in self.processes:
            return False, "Invalid sender."

        if receiver_id not in self.processes:
            return False, "Invalid receiver."

        if sender_id == receiver_id:
            return False, "Sender and receiver must be different."

        if not message.strip():
            return False, "Please enter a message."

        sender = self.processes[sender_id]
        receiver = self.processes[receiver_id]

        if sender.status == "FAILED" or receiver.status == "FAILED":
            return False, "Both processes must be running."

        sender.send_message(receiver, message)

        return True, f'{sender_id} sent "{message}" to {receiver_id}.'

    def create_checkpoint(self):
        """Save a global snapshot of all process states and inboxes."""

        if any(
            process.status == "FAILED"
            for process in self.processes.values()
        ):
            return False, "Cannot create checkpoint while a process has failed."

        # Save independent copies of the complete process state.
        snapshot = {}

        for process_id, process in self.processes.items():
            snapshot[process_id] = {
                "state": process.state,
                "status": process.status,
                "inbox": deepcopy(process.inbox)
            }

        self.checkpoint = snapshot
        self.checkpoint_id = f"C{self.next_checkpoint_number}"
        self.next_checkpoint_number += 1

        return True, f"Checkpoint {self.checkpoint_id} created."

    def fail_process(self, process_id):
        """Simulate failure of one process."""

        if process_id not in self.processes:
            return False, "Invalid process."

        process = self.processes[process_id]

        if process.status == "FAILED":
            return False, f"{process_id} has already failed."

        process.fail()

        return True, f"{process_id} failed."

    def rollback(self):
        """Restore all processes to the latest global checkpoint."""

        if self.checkpoint is None:
            return False, "Rollback unavailable: no checkpoint exists."

        if not any(
            process.status == "FAILED"
            for process in self.processes.values()
        ):
            return False, "Simulate a failure before rollback."

        saved_checkpoint_id = self.checkpoint_id

        # Restore every process from the same saved snapshot.
        for process_id, saved in self.checkpoint.items():
            process = self.processes[process_id]

            process.state = saved["state"]
            process.status = saved["status"]
            process.inbox = deepcopy(saved["inbox"])

        return True, (
            f"Recovery successful. Restored to {saved_checkpoint_id}."
        )

    def reset(self):
        """Reset all processes and create the initial checkpoint C0."""

        for process in self.processes.values():
            process.state = 0
            process.status = "RUNNING"
            process.inbox = []
            process.checkpoint_state = None

        self.checkpoint = None
        self.checkpoint_id = None
        self.next_checkpoint_number = 0

        return self.create_checkpoint()
