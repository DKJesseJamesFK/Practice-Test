"""
Main Window:
newTestButton is the new test button that opens the new test dialog.

New Test Window:
newTitle is the Title text box. Enter test name here to create a new test.
enterBtn is the Enter button that submits the test name.
questionFormat is the radio button group for multiple choice and true/false questions.
multipleChoice is the radio button for multiple choice questions.
trueFalse is the radio button for true/false questions.
test is a list to hold question objects.
number is the current question number.

trueFalseFrame is the frame for the true/false questions:
trueFalseQuestion is the question text box.
trueFalseAnswer is the true/false answer radio button group.
true is the true answer radio button.
false is the false answer radio button.
submitTfBtn is the submit question button.

multipleChoiceFrame is the frame for the multiple choice questions:
multipleChoiceQuestion is the question text box.
answerA is the first answer text box.
answerB is the second answer text box.
answerC is the third answer text box.
answerD is the fourth answer text box.
answerE is the fifth answer text box.
multipleChoiceAnswer is the multiple choice answer radio button group.

new_test is the .txt file that will hold the questions.
submitTestBtn is the submit test button and will pickle new test.

nullFrame should be a frame that hides the trueFalseFrame and multipleChoiceFrame.

takeTest window will display the tests saved to TestDir.txt as radio buttons, and lets you choose a test to take.
"""

from breezypythongui import EasyFrame
from tkinter import StringVar
from questions import TestQuestion, TfQuestion, McQuestion
from tkinter import PhotoImage
import pickle
import os

class PracticeTest(EasyFrame):
    def __init__(self):
        # create the frame and widgets
        EasyFrame.__init__(self, title = "Practice Test")
        self.newTestBtn = self.addButton(text = "New Test", row = 0, column = 0, command = self.newTest)
        self.takeTestBtn = self.addButton(text = "Take Test", row = 0, column = 1, command = self.takeTest) # TODO
        self.addButton(text = "Help", row = 0, column = 2) # TODO
        self.addButton(text = "Delete Test", row = 0, column = 3, command = self.deleteTest) # TODO

    def reset(self):
        self.newTestBtn.configure(state = "normal")
        self.takeTestBtn.configure(state = "normal")

    def newTest(self):
        """
        Opens a new dialog for creating a new practice test.
        """
        self.newTestBtn.configure(state = "disabled")
        self.takeTestBtn.configure(state = "disabled")
        class NewTest(EasyFrame):
            def __init__(self, practice_test):
                EasyFrame.__init__(self, title = "New Test")
                self.practice_test = practice_test
                # Sets up empty list for questions
                self.test = []
                # Set starting question number
                self.number = 1
                # Create widgets
                self.addLabel(text = "Enter Title of Test", row = 0, column = 0)
                self.newTitle = self.addTextField(text = "", row = 0, column = 1)
                self.enterBtn = self.addButton(text = "Enter", row = 0, column = 2, command = self.enterTitle)
                self.questionNumber = self.addLabel(text = f"Question number {self.number}", row = 1, column = 0)
                self.questionFormat = self.addRadiobuttonGroup(row = 1, column = 1, orient = "horizontal")
                self.multipleChoice = self.questionFormat.addRadiobutton(text = "Multiple Choice", command = self.setMultipleChoice)
                self.trueFalse = self.questionFormat.addRadiobutton(text = "True/False", command = self.setTrueFalse)
                self.questionFormat.setSelectedButton(self.multipleChoice)

                # Add panels for true/false
                self.trueFalseFrame = self.addPanel(row = 2, column = 0, columnspan = 3)
                self.trueFalseFrame.addLabel(text = "Question:", row = 0, column = 0)
                self.trueFalseQuestion = self.trueFalseFrame.addTextArea(text = "", row = 1, column = 0, width = 30, height = 5, columnspan = 4)
                self.trueFalseFrame.addLabel(text = "Answer:", row = 2, column = 0)
                self.trueFalseAnswer = self.trueFalseFrame.addRadiobuttonGroup(row = 3, column = 0, columnspan=3, orient = "horizontal")
                self.trueFalseAnswerVar = StringVar()
                self.trueFalseAnswerVar.set("True")
                self.true = self.trueFalseAnswer.addRadiobutton(text = "True", command = lambda: self.trueFalseAnswerVar.set("true"))
                self.false = self.trueFalseAnswer.addRadiobutton(text = "False", command = lambda: self.trueFalseAnswerVar.set("false"))
                self.trueFalseAnswer.setSelectedButton(self.true)
                self.submitTfBtn = self.trueFalseFrame.addButton(text = "Submit Question", row = 4, column = 0, command = self.submitTf)
                self.submitTestBtn = self.trueFalseFrame.addButton(text="Submit Test", row=4, column=1, command=self.submitTest)

                # Add panels for multiple choice
                self.multipleChoiceFrame = self.addPanel(row = 2, column = 0, columnspan = 3)
                self.multipleChoiceFrame.addLabel(text = "Question:", row = 0, column = 0)
                self.multipleChoiceQuestion = self.multipleChoiceFrame.addTextArea(text = "", row = 1, column = 0, width = 30, height = 5, columnspan = 3, wrap = "word")
                self.multipleChoiceFrame.addLabel(text = "Answers:", row = 2, column = 0)
                self.multipleChoiceFrame.addLabel(text = "A. ", row = 3, column = 0, sticky="NSEW")
                self.answerA = self.multipleChoiceFrame.addTextArea(text = "", row = 3, column = 1, height=2, width=20, columnspan=2, wrap="word")
                self.multipleChoiceFrame.addLabel(text = "B. ", row = 4, column = 0, sticky="NSEW")
                self.answerB = self.multipleChoiceFrame.addTextArea(text = "", row = 4, column = 1, height=2, width=20, columnspan=2, wrap="word")
                self.multipleChoiceFrame.addLabel(text = "C. ", row = 5, column = 0, sticky="NSEW")
                self.answerC = self.multipleChoiceFrame.addTextArea(text = "", row = 5, column = 1, height=2, width=20, columnspan=2, wrap="word")
                self.multipleChoiceFrame.addLabel(text = "D. ", row = 6, column = 0, sticky="NSEW")
                self.answerD = self.multipleChoiceFrame.addTextArea(text = "", row = 6, column = 1, height=2, width=20, columnspan=2, wrap="word")
                self.multipleChoiceFrame.addLabel(text = "E. ", row = 7, column = 0, sticky="NSEW")
                self.answerE = self.multipleChoiceFrame.addTextArea(text = "", row = 7, column = 1, height=2, width=20, columnspan=2, wrap="word")
                self.multipleChoiceFrame.addLabel(text = "Correct Answer:", row = 8, column = 0)
                self.multipleChoiceAnswer = self.multipleChoiceFrame.addRadiobuttonGroup(row = 8, column = 1, orient = "horizontal")
                self.multipleChoiceAnswerVar = StringVar()
                self.multipleChoiceAnswerVar.set("A")
                self.A = self.multipleChoiceAnswer.addRadiobutton(text = "A", command = lambda: self.multipleChoiceAnswerVar.set("A"))
                self.B = self.multipleChoiceAnswer.addRadiobutton(text = "B", command = lambda: self.multipleChoiceAnswerVar.set("B"))
                self.C = self.multipleChoiceAnswer.addRadiobutton(text = "C", command = lambda: self.multipleChoiceAnswerVar.set("C"))
                self.D = self.multipleChoiceAnswer.addRadiobutton(text = "D", command = lambda: self.multipleChoiceAnswerVar.set("D"))
                self.E = self.multipleChoiceAnswer.addRadiobutton(text = "E", command = lambda: self.multipleChoiceAnswerVar.set("E"))
                self.multipleChoiceAnswer.setSelectedButton(self.A)
                self.submitMcBtn = self.multipleChoiceFrame.addButton(text = "Submit Question", row = 10, column = 0, command = self.submitMc)
                self.submitTestBtn = self.multipleChoiceFrame.addButton(text="Submit Test", row=10, column=1, command = self.submitTest)

                self.nullFrame = self.addPanel(row = 3, column = 0, columnspan = 3)
                self.nullFrame.lift()
                
            def enterTitle(self):
                """
                Called when the user presses the "Enter" button. Opens a
                .txt file with the name of the test, and disables the button
                and the text field. Also selects the "Multiple Choice" radio
                button.
                """
                self.new_test = open("tests/" + self.newTitle.getText() + ".txt", "wb")
                self.enterBtn.configure(state = "disabled")
                self.newTitle.configure(state = "readonly")

            def setTrueFalse(self):
                """
                Called when the user selects the "True/False" radio button. Lifts
                the panel for entering true/false questions, and lowers the panel
                for entering multiple choice questions.
                """
                self.trueFalseFrame.lift()
                self.multipleChoiceFrame.lower()

            def submitTf(self):
                """Submits a true/false question to the test."""
                if self.trueFalseQuestion.get("1.0", "end").strip() == "":
                    self.messageBox(title = "Error", message = "Please enter a question")
                else:
                    self.test.append(TfQuestion(self.number, self.trueFalseQuestion.get("1.0", "end"), self.trueFalseAnswerVar.get()))
                    self.number += 1
                    self.questionNumber = self.addLabel(text = f"Question number {self.number}", row = 1, column = 0)
                    self.trueFalseQuestion.delete("1.0", "end")
                    self.trueFalseAnswer.setSelectedButton(self.true)
                    # print(self.test) # TESTING PURPOSES

            def setMultipleChoice(self):
                """
                Called when the user selects the "Multiple Choice" radio button. Lifts
                the panel for entering multiple choice questions, and lowers the panel
                for entering true/false questions.
                """
                self.multipleChoiceFrame.lift()
                self.trueFalseFrame.lower()

            def submitMc(self):
                """Submits a multiple choice question to the test."""
                if self.multipleChoiceQuestion.get("1.0", "end").strip() == "":
                    self.messageBox(title = "Error", message = "Please enter a question")
                else:
                    self.test.append(McQuestion(self.number, self.multipleChoiceQuestion.get("1.0", "end"), self.multipleChoiceAnswerVar.get(), self.answerA.get("1.0", "end"), self.answerB.get("1.0", "end"), self.answerC.get("1.0", "end"), self.answerD.get("1.0", "end"), self.answerE.get("1.0", "end")))
                    self.number += 1
                    self.questionNumber = self.addLabel(text = f"Question number {self.number}", row = 1, column = 0)
                    self.multipleChoiceQuestion.delete("1.0", "end")
                    self.multipleChoiceAnswer.setSelectedButton(self.A)
                    self.answerA.delete("1.0", "end")
                    self.answerB.delete("1.0", "end")
                    self.answerC.delete("1.0", "end")
                    self.answerD.delete("1.0", "end")
                    self.answerE.delete("1.0", "end")
                    # print(self.test) # TESTING PURPOSES
                    # print(McQuestion) # TESTING PURPOSES

            def submitTest(self):
                """Submits the test to the .txt file."""
                with self.new_test:
                    pickle.dump(self.test, self.new_test)
                with open("tests/TestDir.txt", "a") as file:
                    file.write(self.newTitle.getText() + "\n")
                self.practice_test.reset()
                self.destroy()
                # Testing Purposes
                # for question in self.test:
                #     if type(question) == McQuestion:
                #         print("Multiple Choice")
                #     elif type(question) == TfQuestion:
                #         print("True/False")
                
        NewTest(self).mainloop()

    def takeTest(self):
        """Opens a new dialog for selecting a practice test to run."""
        # Disable New Test Button and Take Test Button.
        self.newTestBtn.configure(state = "disabled")
        self.takeTestBtn.configure(state = "disabled")

        class PracticeTest(EasyFrame):
            """Practice Test Selection Window"""
            def __init__(self):
                EasyFrame.__init__(self, title="Practice Test")
                self.addLabel(text = "Select Test you wish to take:", row = 0, column = 0)
                self.addButton(text="Start Test", row = 0, column = 1, command = self.startTest)
                self.directory = self.addRadiobuttonGroup(row = 1, column = 0, orient = "vertical")
                self.test_name = StringVar()
                # Open test directory and add radiobuttons from it.
                with open("tests/TestDir.txt", "r") as dir:
                    for line in dir:
                        test = line.strip()
                        self.directory.addRadiobutton(test, command=lambda test=test: self.selectTest(test))

            def selectTest(self, test):
                """Called when a test is selected."""
                self.test_name.set(test)


            def startTest(self):
                """Initializes and loads the practice test"""
                testAnswers = []
                with open("tests/" + self.test_name.get() + ".txt", "rb") as test:
                    self.test_data = pickle.load(test)
                
                # Interface changes depending on question type
                if len(self.test_data) > 0 and isinstance(self.test_data[0], McQuestion):
                    length = len(self.test_data)
                    MCPopup(length, self.test_data[0].number, self.test_data[0].question, self.test_data[0].a, self.test_data[0].b, self.test_data[0].c, self.test_data[0].d, self.test_data[0].e, self.test_data, testAnswers).mainloop()
                elif len(self.test_data) > 0 and isinstance(self.test_data[0], TfQuestion):
                    length = len(self.test_data)
                    TFPopup(length, self.test_data[0].number, self.test_data[0].question, self.test_data[0].correct, self.test_data, testAnswers).mainloop()
                print(testAnswers) # TESTING PURPOSES
                # Testing Purposes
                # for question in test:
                #     if type(question) == McQuestion:
                #         print("Multiple Choice")
                #     elif type(question) == TfQuestion:
                #         print("True/False")
                # print(test)
                

        takeTest = PracticeTest()
        takeTest.mainloop()

    def deleteTest(self):
        self.newTestBtn.configure(state = "disabled")
        self.takeTestBtn.configure(state = "disabled")


        class DeleteTest(EasyFrame):
            def __init__(self, practice_test):
                EasyFrame.__init__(self, title="Delete Test")
                self.practice_test = practice_test
                self.addLabel(text = "Select Test you wish to delete:", row = 0, column = 0)
                self.directory = self.addRadiobuttonGroup(row = 1, column = 0, orient = "vertical")
                self.test_name = StringVar()
                # Open test directory and add radiobuttons from it.
                added_labels = set()
                with open("tests/TestDir.txt", "r") as dir:
                    for line in dir:
                        test = line.strip()
                        if test not in added_labels:
                            self.directory.addRadiobutton(test, command=lambda test=test: self.selectTest(test))
                            added_labels.add(test)

                self.addButton(text="Delete", row = 0, column = 1, command = self.delete)


            def selectTest(self, test):
                """Called when a test is selected."""
                self.test_name.set(test)


            def delete(self):
                """Deletes the selected test."""
                test_file = "tests/" + self.test_name.get() + ".txt"
                if os.path.exists(test_file):
                    os.remove(test_file)
                with open("tests/TestDir.txt", "r") as dir:
                    lines = dir.readlines()
                with open("tests/TestDir.txt", "w") as dir:
                    for line in lines:
                        if line.strip() != self.test_name.get():
                            dir.write(line)

                self.practice_test.reset()
                self.destroy()

        DeleteTest(self).mainloop()

class MCPopup(EasyFrame):
    def __init__(self, length, number, question, a, b, c=None, d=None, e=None, question_list = None, answers = None):
        EasyFrame.__init__(self, title = "Multiple Choice")
        self.question_list = question_list if question_list is not None else []
        self.answers = answers if answers is not None else []
        self.current_index = (number - 1)

        MCPopup.current_popup = self

        if length == 1:
            testBtn = "Submit Test"
        else:
            testBtn = "Submit Question"
        self.addLabel(text = f"{number}. {question}", row = 0, column = 0)
        self.takeTestQuest = self.addRadiobuttonGroup(row = 1, column = 0, orient = "vertical")
        self.takeTestQuestVar = StringVar()
        self.takeTestQuestVar.set("A")
        AnsA = self.takeTestQuest.addRadiobutton(text = f"A. {a}", command = lambda: self.takeTestQuestVar.set("A"))
        self.takeTestQuest.addRadiobutton(text = f"B. {b}", command = lambda: self.takeTestQuestVar.set("B"))
        if c.strip() != "":
            self.takeTestQuest.addRadiobutton(text = f"C. {c}", command = lambda: self.takeTestQuestVar.set("C"))
        if d.strip() != "":
            self.takeTestQuest.addRadiobutton(text = f"D. {d}", command = lambda: self.takeTestQuestVar.set("D"))
        if e.strip() != "":
            self.takeTestQuest.addRadiobutton(text = f"E. {e}", command = lambda: self.takeTestQuestVar.set("E"))
        self.takeTestQuest.setSelectedButton(AnsA)
        self.addButton(text = testBtn, row = 2, column = 0, command = self.takeTestSubmit)

    def takeTestSubmit(self):
        self.answers.append(self.takeTestQuestVar.get())

        self.current_index += 1
        if self.current_index < len(self.question_list):
            next_question = self.question_list[self.current_index]
            self.destroy()
            if isinstance(next_question, McQuestion):
                MCPopup(len(self.question_list), next_question.number, next_question.question, next_question.a, next_question.b, next_question.c, next_question.d, next_question.e, self.question_list, self.answers).mainloop()
            elif isinstance(next_question, TfQuestion):
                TFPopup(len(self.question_list), next_question.number, next_question.question, next_question.correct, self.question_list, self.answers).mainloop()            
        else:
            self.messageBox(title = "Test Completed", message = "Test Completed")
            self.destroy()
            
class TFPopup(EasyFrame):
    def __init__(self, length, number, question, correct, question_list = None, answers = None):
        EasyFrame.__init__(self, title = "True/False")
        self.question_list = question_list if question_list is not None else []
        self.answers = answers if answers is not None else []
        self.current_index = (number - 1)

        TFPopup.current_popup = self

        if length == 1:
            testBtn = "Submit Test"
        else:
            testBtn = "Submit Question"
        self.addLabel(text = f"{number}. {question}", row = 0, column = 0)
        self.takeTestQuest = self.addRadiobuttonGroup(row = 1, column = 0, orient = "vertical")
        self.takeTestQuestVar = StringVar()
        self.takeTestQuestVar.set(correct)
        self.takeTestTrueBtn = self.takeTestQuest.addRadiobutton(text = "True", command = lambda: self.takeTestQuestVar.set("True"))
        self.takeTestFalseBtn = self.takeTestQuest.addRadiobutton(text = "False", command = lambda: self.takeTestQuestVar.set("False"))
        self.takeTestQuest.setSelectedButton(self.takeTestTrueBtn)
        self.addButton(text = testBtn, row = 2, column = 0, command = self.takeTestSubmit)

    def takeTestSubmit(self):
        self.answers.append(self.takeTestQuestVar.get())

        self.current_index += 1
        if self.current_index < len(self.question_list):
            next_question = self.question_list[self.current_index]
            self.destroy()
            if isinstance(next_question, McQuestion):
                MCPopup(len(self.question_list), next_question.number, next_question.question, next_question.a, next_question.b, next_question.c, next_question.d, next_question.e, self.question_list, self.answers).mainloop()
            elif isinstance(next_question, TfQuestion):
                TFPopup(len(self.question_list), next_question.number, next_question.question, next_question.correct, self.question_list, self.answers).mainloop()
        else:
            self.messageBox(title = "Test Completed", message = "Test Completed")
            self.destroy()
        

def main():
    PracticeTest().mainloop()

if __name__ == "__main__":
    main()



# 10/4/2024
# Added functionality to tf questions. Now creates object for question and adds to list.
# Defined __str__ and __repr__ for question.
# Fixed tf radio button bug.
# new test button disabled when new test is open.
# take test button disabled when new test is open.

# 10/7/2024
# Added question and answer text areas to multiple choice questions, and a radio button
# group for the correct answer.
# Added submit button to multiple choice questions.
# Added submit button to new test.
# Added notes to keep track of assigned variables.
# Added another frame to hopefully hide the interactive frames before they are in use.

# 10/10/2024
# Question Number now updates in the New Test / TF Frame
# I got MC questions to work. Finally.
# Submit Test should pickle the test object list. It also should write the test name to a TestDir.txt file. These will be in the "tests" folder.
# Added functionality to Take Test. It should open a new window for selecting a test to take. It should also have a button to start the test.
# Added MCPopup class. It should open a new window for multiple choice questions. It should also have a button to submit the question.
# Added TFPopup class. It should open a new window for true/false questions. It should also have a button to submit the question.
# Got basic functionality working on the Take Test for both MC and TF. 
# Added and implemented a Delete Test function.