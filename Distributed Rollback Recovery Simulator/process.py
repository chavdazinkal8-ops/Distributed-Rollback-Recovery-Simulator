
class Process:
    """Represents one simulated process in the distributed system."""

    def __init__(self, process_id):
        self.process_id = process_id
        self.state = 0
        self.status = "RUNNING"

        # Messages received by this process.
        self.inbox = []

        # Total messages sent by this process.
        self.messages_sent = 0

        # Saved state for individual checkpoint demonstrations.
        self.checkpoint_state = None

    def send_message(self, receiver, message):
        """Send a text message to another process."""

        if self.status == "FAILED" or receiver.status == "FAILED":
            return False

        # Update the process states.
        self.state += 1
        receiver.state += 1

        # Store the message in the receiver's inbox.
        receiver.inbox.append({
            "sender": self.process_id,
            "message": message
        })

        # Increment the sender's message counter.
        self.messages_sent += 1

        return True

    def create_checkpoint(self):
        """Save this process's state."""
        self.checkpoint_state = self.state

    def fail(self):
        """Mark this process as failed."""
        self.status = "FAILED"

    def restore(self):
        """Restore this process to its saved state."""
        if self.checkpoint_state is not None:
            self.state = self.checkpoint_state

        self.status = "RUNNING"
