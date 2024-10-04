from breezypythongui import EasyFrame
from questions import TestQuestion, TfQuestion, McQuestion
from tkinter import PhotoImage

class PracticeTest(EasyFrame):
    def __init__(self):
        # create the frame and widgets
        EasyFrame.__init__(self, title = "Practice Test")
        self.addButton(text = "New Test", row = 0, column = 0, command = self.newTest)
        self.addButton(text = "Take Test", row = 0, column = 1) # TODO
        self.addButton(text = "Help", row = 0, column = 2) # TODO
        self.addButton(text = "Exit", row = 0, column = 3) # TODO

    def newTest(self):
        """
        Opens a new dialog for creating a new practice test.
        """
        class NewTest(EasyFrame):
            def __init__(self):
                EasyFrame.__init__(self, title = "New Test")
                # Set starting question number
                number = 1
                # Create widgets
                self.addLabel(text = "Enter Title of Test", row = 0, column = 0)
                self.newTitle = self.addTextField(text = "", row = 0, column = 1)
                self.enterBtn = self.addButton(text = "Enter", row = 0, column = 2, command = self.enterTitle)
                self.addLabel(text = f"Question number {number}", row = 1, column = 0)
                self.questionFormat = self.addRadiobuttonGroup(row = 1, column = 1, orient = "horizontal")
                self.multipleChoice = self.questionFormat.addRadiobutton(text = "Multiple Choice", command = self.setMultipleChoice)
                self.trueFalse = self.questionFormat.addRadiobutton(text = "True/False", command = self.setTrueFalse)

                # Add panels for true/false
                self.trueFalseFrame = self.addPanel(row = 2, column = 0, columnspan = 3)
                self.trueFalseFrame.addLabel(text = "Question:", row = 0, column = 0)
                self.trueFalseFrame.addTextArea(text = "", row = 1, column = 0, width = 30, height = 5, columnspan = 4)
                self.trueFalseFrame.addLabel(text = "Answer:", row = 2, column = 0)
                self.trueFalseAnswer = self.trueFalseFrame.addRadiobuttonGroup(row = 3, column = 0, orient = "horizontal")
                self.true = self.trueFalseAnswer.addRadiobutton(text = "True")
                self.false = self.trueFalseAnswer.addRadiobutton(text = "False")
                self.submitTfBtn = self.trueFalseFrame.addButton(text = "Submit Question", row = 3, column = 3)

                # Add panels for multiple choice
                self.multipleChoiceFrame = self.addPanel(row = 2, column = 0, columnspan = 3)
                self.multipleChoiceFrame.addLabel(text = "Question:", row = 0, column = 0)
                self.multipleChoiceFrame.addTextArea(text = "", row = 1, column = 0, width = 30, height = 5, columnspan = 3)
                self.multipleChoiceFrame.addLabel(text = "Answer:", row = 2, column = 0)
                
                
            def enterTitle(self):
                """
                Called when the user presses the "Enter" button. Opens a
                .txt file with the name of the test, and disables the button
                and the text field. Also selects the "Multiple Choice" radio
                button.
                """
                open(self.newTitle.getText() + ".txt", "w")
                self.enterBtn.configure(state = "disabled")
                self.newTitle.configure(state = "readonly")
                self.questionFormat.setSelectedButton(self.multipleChoice)

            def setTrueFalse(self):
                """
                Called when the user selects the "True/False" radio button. Lifts
                the panel for entering true/false questions, and lowers the panel
                for entering multiple choice questions.
                """
                self.trueFalseFrame.lift()
                self.multipleChoiceFrame.lower()

            def setMultipleChoice(self):
                """
                Called when the user selects the "Multiple Choice" radio button. Lifts
                the panel for entering multiple choice questions, and lowers the panel
                for entering true/false questions.
                """
                self.multipleChoiceFrame.lift()
                self.trueFalseFrame.lower()
                
        NewTest().mainloop()

def main():
    PracticeTest().mainloop()

if __name__ == "__main__":
    main()