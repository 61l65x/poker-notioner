import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QMessageBox, QSlider, QComboBox
from PyQt5.QtCore import Qt

def calculate_pot_odds(pot_size, call_amount):
    # Pot odds calculation
    total_pot = pot_size + call_amount
    pot_odds = call_amount / total_pot
    return pot_odds * 100  # Convert to percentage

def estimate_equity(outs, street='flop'):
    # Quick equity estimation using the Rule of 2 and 4
    if street == 'flop':  # Flop: 2 cards to come (turn + river)
        return outs * 4
    elif street == 'turn':  # Turn: 1 card to come (river only)
        return outs * 2
    else:
        return 0  # Invalid street

class PokerCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize default street value as 'flop'
        self.selected_street = 'flop'

        # Setup the layout
        self.init_ui()

    def init_ui(self):
        # Create grid layout
        layout = QGridLayout()

        # Create widgets
        self.pot_label = QLabel('Pot Size (chips):')
        self.pot_entry = QLineEdit()
        self.pot_slider = QSlider(Qt.Horizontal)
        self.pot_slider.setSingleStep(1)  # Set step size to 1
        self.pot_slider.valueChanged.connect(self.update_pot_entry)

        self.call_label = QLabel('Call Amount (chips):')
        self.call_entry = QLineEdit()
        self.call_slider = QSlider(Qt.Horizontal)
        self.call_slider.setSingleStep(1)  # Set step size to 1
        self.call_slider.valueChanged.connect(self.update_call_entry)

        self.outs_label = QLabel('Outs:')
        self.outs_entry = QLineEdit()
        self.outs_slider = QSlider(Qt.Horizontal)
        self.outs_slider.setRange(0, 20)  # Outs are usually between 0 and 20
        self.outs_slider.setSingleStep(1)  # Set step size to 1
        self.outs_slider.valueChanged.connect(self.update_outs_entry)

        # Dropdown for selecting chip stage
        self.stage_dropdown = QComboBox()
        self.stage_dropdown.addItems(["100k", "1 Million", "100 Million"])
        self.stage_dropdown.currentIndexChanged.connect(self.change_stage)

        # Button for toggling between Flop and River
        self.street_button = QPushButton('Flop')
        self.street_button.clicked.connect(self.toggle_street)

        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignCenter)

        self.calculate_button = QPushButton('Calculate')
        self.calculate_button.clicked.connect(self.calculate)

        # Add widgets to the layout
        layout.addWidget(self.stage_dropdown, 0, 2)  # Dropdown to select the chip stage
        layout.addWidget(self.pot_label, 1, 0)
        layout.addWidget(self.pot_entry, 1, 1)
        layout.addWidget(self.pot_slider, 1, 2)

        layout.addWidget(self.call_label, 2, 0)
        layout.addWidget(self.call_entry, 2, 1)
        layout.addWidget(self.call_slider, 2, 2)

        layout.addWidget(self.outs_label, 3, 0)
        layout.addWidget(self.outs_entry, 3, 1)
        layout.addWidget(self.outs_slider, 3, 2)

        # Add the toggle button for Flop/River selection
        layout.addWidget(self.street_button, 4, 1, 1, 1)

        layout.addWidget(self.calculate_button, 5, 1)
        layout.addWidget(self.result_label, 6, 0, 1, 3)

        self.setLayout(layout)

        self.setWindowTitle('Poker Calculator')

        # Set default stage
        self.change_stage(0)
        self.setGeometry(100, 100, 800, 550)

    def toggle_street(self):
        # Toggle between Flop and River
        if self.selected_street == 'flop':
            self.selected_street = 'river'
            self.street_button.setText('River')
        else:
            self.selected_street = 'flop'
            self.street_button.setText('Flop')

    def update_pot_entry(self, value):
        self.pot_entry.setText(str(value))

    def update_call_entry(self, value):
        self.call_entry.setText(str(value))

    def update_outs_entry(self, value):
        self.outs_entry.setText(str(value))

    def change_stage(self, index):
        # Change the slider range based on the selected stage
        if index == 0:  # 100k stage
            self.pot_slider.setRange(0, 100000)
            self.call_slider.setRange(0, 50000)
        elif index == 1:  # 1 Million stage
            self.pot_slider.setRange(0, 1000000)
            self.call_slider.setRange(0, 500000)
        elif index == 2:  # 100 Million stage
            self.pot_slider.setRange(0, 100000000)
            self.call_slider.setRange(0, 50000000)

        # Reset the slider and input fields when the stage is changed
        self.pot_slider.setValue(0)
        self.call_slider.setValue(0)
        self.pot_entry.setText("0")
        self.call_entry.setText("0")
        self.result_label.setText(f"Stage changed to {self.stage_dropdown.currentText()}")

    def calculate(self):
        try:
            # Get input values
            pot_size = float(self.pot_entry.text())
            call_amount = float(self.call_entry.text())
            outs = int(self.outs_entry.text())

            # Perform calculations using the selected street (flop or river)
            pot_odds = calculate_pot_odds(pot_size, call_amount)
            equity = estimate_equity(outs, self.selected_street)

            # Display results
            result = f"Pot Odds: {pot_odds:.2f}%\nEstimated Equity: {equity:.2f}%"
            if equity > pot_odds:
                result += "\nIt's profitable to call!"
            else:
                result += "\nYou should fold."
            self.result_label.setText(result)

        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid numbers.')

# Main application
app = QApplication(sys.argv)
window = PokerCalculator()
window.show()
sys.exit(app.exec_())
