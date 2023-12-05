import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap

visual = "528143709634712"
auditory = "963805217468325"


def get_length(inp, test):
    length = 0
    counter = -1
    for i in range(len(inp) - 1):
        subseq = inp[i:i+2]
        position = test.find(subseq)
        if position > -1:
            length += 2
            if counter == i:
                length -= 1
            counter = i + 1

    return length


def plot(results):
    visual_count = sum(results[0][i] > results[1][i]
                       for i in range(len(results[0])))
    auditory_count = sum(results[0][i] < results[1][i]
                         for i in range(len(results[0])))

    plt.figure(figsize=(12, 5))

    # Plot 1: Visual vs Auditory
    plt.subplot(1, 2, 1)
    plt.bar(['Visual', 'Auditory'], [visual_count,
            auditory_count], color=['blue', 'orange'])
    plt.title('Visual vs Auditory')
    plt.ylabel('Count')
    plt.xlabel('Category')
    plt.legend(['Visual', 'Auditory'])

    # Plot 2: Values for each participant
    plt.subplot(1, 2, 2)
    bar_width = 0.35
    index = range(len(results[0]))

    plt.bar(index, results[0], bar_width, color='blue', label='Visual')
    plt.bar([i + bar_width for i in index], results[1],
            bar_width, color='orange', label='Auditory')

    plt.xlabel('Participant')
    plt.ylabel('Value')
    plt.title('Values for Each Participant')
    plt.xticks([i + bar_width / 2 for i in index],
               [f'Participant {i+1}' for i in index])
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()


class PDFDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.pdfList = []

        self.layout = QVBoxLayout()

        # Logo
        self.logo = QLabel(self)
        pixmap = QPixmap('rug.png')
        scaled_pixmap = pixmap.scaled(600, 900, Qt.KeepAspectRatio)
        self.logo.setPixmap(scaled_pixmap)
        self.layout.addWidget(self.logo)

        # Title
        self.title = QLabel("Basic Scientific Skills", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-weight: bold; font-size: 25px;")
        self.layout.addWidget(self.title)

        # Description
        self.description = QLabel("Team Who?", self)
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.description)

        # Dropdown
        self.participantSelect = QComboBox(self)
        self.participantSelect.addItems([str(i) for i in range(1, 17)])
        self.participantSelect.currentIndexChanged.connect(
            self.onParticipantSelect)
        self.layout.addWidget(self.participantSelect)

        # Container for participant inputs
        self.participantInputs = QVBoxLayout()
        self.layout.addLayout(self.participantInputs)

        # Submit Button
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.clicked.connect(self.onSubmit)
        self.layout.addWidget(self.submitButton)

        self.setLayout(self.layout)

    @pyqtSlot()
    def onParticipantSelect(self):
        # Clear existing inputs
        for i in reversed(range(self.participantInputs.count())):
            widgetToRemove = self.participantInputs.itemAt(i).widget()
            self.participantInputs.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        # Add new inputs
        participants = int(self.participantSelect.currentText())
        for i in range(1, participants + 1):
            hLayout = QHBoxLayout()

            visualInput = QLineEdit(self)
            visualInput.setPlaceholderText(f'Participant {i} Visual')

            auditoryInput = QLineEdit(self)
            auditoryInput.setPlaceholderText(f'Participant {i} Auditory')

            hLayout.addWidget(visualInput)
            hLayout.addWidget(auditoryInput)

            self.participantInputs.addLayout(hLayout)

    @pyqtSlot()
    def onSubmit(self):
        results = [[], []]
        print("Submitted Data: ")
        for i in range(self.participantInputs.count()):
            hLayout = self.participantInputs.itemAt(i)
            visualInput = hLayout.itemAt(0).widget()
            auditoryInput = hLayout.itemAt(1).widget()
            results[0].append(get_length(visualInput.text(), visual))
            results[1].append(get_length(auditoryInput.text(), auditory))
            print(
                f'Participant {i+1}: Visual - {results[0][i]}, Auditory - {results[1][i]}')

        plot(results)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFDropWidget()
    ex.show()
    sys.exit(app.exec_())
