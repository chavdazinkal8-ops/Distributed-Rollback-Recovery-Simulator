
import tkinter as tk
from tkinter import ttk

from process import Process
from recovery import RecoveryManager


class RollbackSimulator:
    """Tkinter GUI for the distributed rollback recovery simulator."""

    def __init__(self, root):
        self.root = root
        self.root.title("Distributed Rollback Recovery Simulator")
        self.root.geometry("900x800")
        self.root.minsize(720, 650)

        # Create the simulated processes.
        self.processes = [
            Process("P1"),
            Process("P2"),
            Process("P3")
        ]

        self.manager = RecoveryManager(self.processes)
        self.process_labels = {}

        self.create_widgets()

        # Create the initial checkpoint.
        _, message = self.manager.create_checkpoint()
        self.add_log(message)

        self.set_status(
            "Normal",
            "All processes are running normally."
        )

        self.refresh_processes()

    def create_widgets(self):
        """Build the application interface."""

        # Header
        title = tk.Label(
            self.root,
            text="DISTRIBUTED ROLLBACK RECOVERY SIMULATOR",
            font=("Arial", 16, "bold"),
            bg="#183b64",
            fg="white",
            pady=18
        )
        title.pack(fill="x")

        # Recovery status
        self.status_label = tk.Label(
            self.root,
            text="Status: Normal",
            font=("Arial", 12, "bold"),
            fg="#167044"
        )
        self.status_label.pack(pady=(10, 3))

        self.explanation_label = tk.Label(
            self.root,
            text="All processes are running normally.",
            wraplength=820
        )
        self.explanation_label.pack(pady=(0, 8))

        # Process cards
        process_frame = ttk.LabelFrame(
            self.root,
            text="Distributed Processes",
            padding=10
        )
        process_frame.pack(fill="x", padx=15, pady=6)

        for process in self.processes:
            card = ttk.Frame(
                process_frame,
                padding=8,
                relief="ridge"
            )
            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=5
            )

            ttk.Label(
                card,
                text=process.process_id,
                font=("Arial", 15, "bold")
            ).pack(pady=3)

            status_label = tk.Label(
                card,
                text="RUNNING",
                fg="#167044",
                font=("Arial", 10, "bold")
            )
            status_label.pack(pady=3)

            state_label = ttk.Label(
                card,
                text="State: 0"
            )
            state_label.pack(pady=3)

            # NEW: Messages sent counter
            sent_label = ttk.Label(
                card,
                text="Messages sent: 0",
                wraplength=230
            )
            sent_label.pack(pady=3)

            # Messages received counter
            inbox_label = ttk.Label(
                card,
                text="Messages received: 0",
                wraplength=230
            )
            inbox_label.pack(pady=3)

            self.process_labels[process.process_id] = {
                "status": status_label,
                "state": state_label,
                "sent": sent_label,
                "inbox": inbox_label
            }

        # Message passing controls
        message_frame = ttk.LabelFrame(
            self.root,
            text="Message Passing",
            padding=10
        )
        message_frame.pack(fill="x", padx=15, pady=6)

        selection_frame = ttk.Frame(message_frame)
        selection_frame.pack(fill="x", pady=4)

        ttk.Label(
            selection_frame,
            text="Sender:"
        ).pack(side="left")

        self.sender_var = tk.StringVar(value="P1")

        self.sender_box = ttk.Combobox(
            selection_frame,
            textvariable=self.sender_var,
            values=["P1", "P2", "P3"],
            state="readonly",
            width=6
        )
        self.sender_box.pack(side="left", padx=6)

        ttk.Label(
            selection_frame,
            text="Receiver:"
        ).pack(side="left", padx=(12, 0))

        self.receiver_var = tk.StringVar(value="P2")

        self.receiver_box = ttk.Combobox(
            selection_frame,
            textvariable=self.receiver_var,
            values=["P1", "P2", "P3"],
            state="readonly",
            width=6
        )
        self.receiver_box.pack(side="left", padx=6)

        # Message input
        input_frame = ttk.Frame(message_frame)
        input_frame.pack(fill="x", pady=5)

        ttk.Label(
            input_frame,
            text="Message:"
        ).pack(side="left")

        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        ttk.Button(
            input_frame,
            text="Send Message",
            command=self.send_message
        ).pack(side="left")

        # Simulation controls
        controls = ttk.LabelFrame(
            self.root,
            text="Simulation Controls",
            padding=10
        )
        controls.pack(fill="x", padx=15, pady=6)

        buttons = [
            ("Create Checkpoint", self.create_checkpoint),
            ("Fail P1", lambda: self.fail_process("P1")),
            ("Fail P2", lambda: self.fail_process("P2")),
            ("Fail P3", lambda: self.fail_process("P3")),
            ("Rollback Recovery", self.rollback),
            ("Reset", self.reset)
        ]

        for index, (text, command) in enumerate(buttons):
            ttk.Button(
                controls,
                text=text,
                command=command
            ).grid(
                row=index // 3,
                column=index % 3,
                padx=6,
                pady=6,
                sticky="ew"
            )

        for column in range(3):
            controls.columnconfigure(column, weight=1)

        # Latest checkpoint
        self.checkpoint_label = ttk.Label(
            self.root,
            text="Latest checkpoint: C0",
            font=("Arial", 10, "bold")
        )
        self.checkpoint_label.pack(pady=4)

        # Event log
        log_frame = ttk.LabelFrame(
            self.root,
            text="Event Log",
            padding=8
        )
        log_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(6, 12)
        )

        self.log_box = tk.Text(
            log_frame,
            height=9,
            wrap="word",
            state="disabled",
            font=("Consolas", 9)
        )
        self.log_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            log_frame,
            orient="vertical",
            command=self.log_box.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.log_box.configure(
            yscrollcommand=scrollbar.set
        )

    def add_log(self, message):
        """Display an event in the log."""

        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def set_status(self, status, explanation):
        """Update the system status."""

        colors = {
            "Normal": "#167044",
            "Failure Detected": "#bd3542",
            "Rolling Back": "#875600",
            "Recovery Completed": "#174d91"
        }

        self.status_label.configure(
            text="Status: " + status,
            fg=colors.get(status, "#202b3c")
        )

        self.explanation_label.configure(
            text=explanation
        )

    def refresh_processes(self):
        """Refresh states, sent counts, received counts and status."""

        for process in self.processes:
            labels = self.process_labels[process.process_id]

            labels["state"].configure(
                text=f"State: {process.state}"
            )

            labels["sent"].configure(
                text=f"Messages sent: {process.messages_sent}"
            )

            labels["inbox"].configure(
                text=f"Messages received: {len(process.inbox)}"
            )

            if process.status == "FAILED":
                labels["status"].configure(
                    text="FAILED",
                    fg="#bd3542"
                )
            else:
                labels["status"].configure(
                    text="RUNNING",
                    fg="#167044"
                )

        checkpoint_id = self.manager.checkpoint_id or "None"

        self.checkpoint_label.configure(
            text=f"Latest checkpoint: {checkpoint_id}"
        )

    def send_message(self):
        """Send a message and refresh the counters."""

        sender = self.sender_var.get()
        receiver = self.receiver_var.get()
        message = self.message_entry.get().strip()

        success, result = self.manager.send_message(
            sender,
            receiver,
            message
        )

        self.add_log(result)

        if success:
            self.set_status(
                "Normal",
                f"Message delivered from {sender} to {receiver}."
            )

            self.message_entry.delete(0, "end")

        self.refresh_processes()

    def create_checkpoint(self):
        """Create a global checkpoint."""

        success, message = self.manager.create_checkpoint()
        self.add_log(message)

        if success:
            self.set_status(
                "Normal",
                f"Checkpoint {self.manager.checkpoint_id} saved."
            )

        self.refresh_processes()

    def fail_process(self, process_id):
        """Simulate a process failure."""

        success, message = self.manager.fail_process(process_id)
        self.add_log(message)

        if success:
            self.set_status(
                "Failure Detected",
                f"{process_id} has failed. Rollback is available."
            )

        self.refresh_processes()

    def rollback(self):
        """Restore the latest checkpoint."""

        if not any(
            process.status == "FAILED"
            for process in self.processes
        ):
            success, message = self.manager.rollback()
            self.add_log(message)
            self.set_status("Normal", message)
            return

        self.set_status(
            "Rolling Back",
            "Restoring all processes to the saved checkpoint."
        )
        self.add_log("Rollback started.")

        success, message = self.manager.rollback()
        self.add_log(message)

        if success:
            self.set_status(
                "Recovery Completed",
                "Recovery Successful — System restored to checkpoint."
            )
            self.add_log("All processes restored and running.")
        else:
            self.set_status(
                "Failure Detected",
                message
            )

        # Refresh sent and received counts after recovery.
        self.refresh_processes()

    def reset(self):
        """Reset the simulator and create checkpoint C0."""

        self.manager.reset()

        # Reset the sent counters too.
        for process in self.processes:
            process.messages_sent = 0

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        self.add_log("Simulation reset.")
        self.add_log("Initial checkpoint C0 created.")

        self.set_status(
            "Normal",
            "All processes are running normally."
        )

        self.refresh_processes()


if __name__ == "__main__":
    root = tk.Tk()
    app = RollbackSimulator(root)
    root.mainloop()
