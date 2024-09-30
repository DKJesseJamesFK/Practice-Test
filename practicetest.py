from breezypythongui import EasyFrame
from tkinter import PhotoImage

class PracticeTest(EasyFrame):
    def __init__(self):
        # create the frame and widgets
        EasyFrame.__init__(self, title = "Practice Test")
        self.addButton(text = "New Test", row = 0, column = 0, command = self.newTest)
        self.addButton(text = "Take Test", row = 0, column = 1)

    def newTest(self):
        class NewTest(EasyFrame):
            def __init__(self):
                EasyFrame.__init__(self, title = "New Test")
                number = 1
                self.addLabel(text = "Enter Title of Test", row = 0, column = 0)
                self.newTitle = self.addTextField(text = "", row = 0, column = 1)
                self.enterBtn = self.addButton(text = "Enter", row = 0, column = 2, command = self.enterTitle)
                self.addLabel(text = f"Question number {number}", row = 1, column = 0)
                self.questionFormat = self.addRadiobuttonGroup(row = 1, column = 1, orient = "horizontal")
                self.multipleChoice = self.questionFormat.addRadiobutton(text = "Multiple Choice")
                self.trueFalse = self.questionFormat.addRadiobutton(text = "True/False")
                self.questionFormat.setSelectedButton(self.multipleChoice)
                
            
            def enterTitle(self):
                open(self.newTitle.getText() + ".txt", "w")
                self.enterBtn.configure(state = "disabled")
                self.newTitle.configure(state = "readonly")
                
                
        NewTest().mainloop()

def main():
    PracticeTest().mainloop()

if __name__ == "__main__":
    main()