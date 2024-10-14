"""
Practice Test
Written by Jesse Fry
This program allows the user to enter, take, and delete practice tests. It is intended to be a study tool for students like myself.
The interface is optimized for simplicity and ease of use over customization.
All questions are stored in a .txt file.

Main Window:
newTestButton is the new test button that opens the new test dialog.
self.testIsOpen is a boolean that is true if a test is open.

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

paper.gif acquired via Pixabay https://pixabay.com/vectors/paper-sheets-multiple-ruled-page-23700/
attention.gif acquired via Pixabay https://pixabay.com/vectors/attention-warning-exclamation-mark-98529/

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
        self.testIsOpen = False
        EasyFrame.__init__(self, title = "Practice Test", resizable = False)
        self.setResizable(False)
        self.newTestBtn = self.addButton(text = "New Test", row = 0, column = 0, command = self.newTest)
        self.takeTestBtn = self.addButton(text = "Take Test", row = 0, column = 1, command = self.takeTest)
        self.deleteTestBtn = self.addButton(text = "Delete Test", row = 0, column = 2, command = self.deleteTest)
        self.addButton(text = "Help", row = 0, column = 3, command = self.help) # TODO


    def help(self):
        """Opens a new dialog for viewing the help file."""
        self.messageBox(title = "Help", message = """
        Welcome to Practice Test! This is an application I developed to help with studying. The main window lists four different tasks that you can do in this simple application.

        New Test opens up a window that allows you to submit a new practice test. As of today, the application accepts two types of question formats: Multiple Choice and True/False. Before you can begin adding questions to the practice test, you must enter the title of the new test. Once you have done that, the fun begins!

        You can toggle back and forth between Multiple Choice and True/False format questions by using the radio buttons directly underneath the title of your test.

        For multiple choice questions, enter the question in the text box directly under the text that says "Question:" Then, add the possible answers into the text boxes labeled A through E. You must include at least an A and B answer, but the rest are optional.

        Below the Answers area you will find a set of radio buttons labeled "Correct Answer:" which you will use to pick the correct answer. Click the Submit Question button to save the question and answers you have entered, and click the Submit Test button when you are done creating the test.

        For True/False questions, you only need to enter the question (or statement) into the Question field, mark the correct True or False radio button, and click the Submit Question button.

        The Back button will bring you back to the main window at any time, but if you have started a test and not submitted it that test data will be lost.

        Take Test opens up a window that allows you to take any of the practice tests that you have saved. A list of your saved tests will populate. Click the corresponding radio button of the test you would like to take, then click the Start Test button.

        For each question, choose the answer you think is correct and click the Submit Question button when you are ready. If you get the answer correct, the next question will populate. If your answer was incorrect, a message box will appear to let you know what the correct answer was before the next question populates. When you reach the final question on the practice test, the Submit Question button will become a Submit Test button. After you submit the test, another message box will appear displaying your test score. You will then be brought back to the Take Test selection window.

        The Back button will bring you back to the main window at any time.

        Delete Test opens a window that allows you to delete any of the tests you have created and saved. Be careful, because this is permanent! PLEASE DO NOT DELETE ANYTHING FROM THE TEST FOLDER BY ANY METHOD OTHER THAN THIS WINDOW.

        Select the saved test you wish to delete from the menu, then click the Delete button. A message box will pop up to inform you the test was deleted, and you will be brought back to the main window.

        The Back button will bring you back to the main window at any time.

        Help opens up this help file.

        If you have any questions or feedback, you can email me at jfry59@ivytech.edu
        """, width = 50, height = 50)
        

    def reset(self):
        """Resets state of the main menu."""
        self.newTestBtn.configure(state = "normal")
        self.takeTestBtn.configure(state = "normal")
        self.deleteTestBtn.configure(state = "normal")

    def newTest(self):
        """
        Opens a new dialog for creating a new practice test.
        """
        self.newTestBtn.configure(state = "disabled")
        self.takeTestBtn.configure(state = "disabled")
        self.deleteTestBtn.configure(state = "disabled")
        
        class NewTest(EasyFrame):
            """This is the test creation part of the program."""
            def __init__(self, practice_test):
                EasyFrame.__init__(self, title = "New Test", resizable = False)
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
                self.multipleChoice.configure(state = "disabled")
                self.trueFalse = self.questionFormat.addRadiobutton(text = "True/False", command = self.setTrueFalse)
                self.trueFalse.configure(state = "disabled")
                self.questionFormat.setSelectedButton(self.multipleChoice)
                self.addButton(text = "Back" , row = 1, column = 2, command = self.newTestBack)

                # Add panels for true/false
                self.trueFalseFrame = self.addPanel(row = 2, column = 0, columnspan = 3)
                self.trueFalseFrame.addLabel(text = "Question:", row = 0, column = 0)
                self.trueFalseQuestion = self.trueFalseFrame.addTextArea(text = "", row = 1, column = 0, width = 30, height = 5, columnspan = 4, wrap = "word")
                self.trueFalseFrame.addLabel(text = "Answer:", row = 2, column = 0)
                self.trueFalseAnswer = self.trueFalseFrame.addRadiobuttonGroup(row = 3, column = 0, columnspan=3, orient = "horizontal")
                self.trueFalseAnswerVar = StringVar()
                self.trueFalseAnswerVar.set("True")
                self.true = self.trueFalseAnswer.addRadiobutton(text = "True", command = lambda: self.trueFalseAnswerVar.set("True"))
                self.false = self.trueFalseAnswer.addRadiobutton(text = "False", command = lambda: self.trueFalseAnswerVar.set("False"))
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
                self.answerC.configure(state = "disabled")
                self.multipleChoiceFrame.addLabel(text = "D. ", row = 6, column = 0, sticky="NSEW")
                self.answerD = self.multipleChoiceFrame.addTextArea(text = "", row = 6, column = 1, height=2, width=20, columnspan=2, wrap="word")
                self.answerD.configure(state = "disabled")
                self.multipleChoiceFrame.addLabel(text = "E. ", row = 7, column = 0, sticky="NSEW")
                self.answerE = self.multipleChoiceFrame.addTextArea(text = "", row = 7, column = 1, height=2, width=20, columnspan=2, wrap="word")
                self.answerE.configure(state = "disabled")
                self.multipleChoiceFrame.addLabel(text = "Correct Answer:", row = 8, column = 0)
                self.multipleChoiceAnswer = self.multipleChoiceFrame.addRadiobuttonGroup(row = 8, column = 1, orient = "horizontal")
                self.multipleChoiceAnswerVar = StringVar()
                self.multipleChoiceAnswerVar.set("A")
                self.A = self.multipleChoiceAnswer.addRadiobutton(text = "A", command = lambda: self.multipleChoiceAnswerVar.set("A"))
                self.B = self.multipleChoiceAnswer.addRadiobutton(text = "B", command = lambda: self.multipleChoiceAnswerVar.set("B"))
                self.C = self.multipleChoiceAnswer.addRadiobutton(text = "C", command = lambda: self.multipleChoiceAnswerVar.set("C"))
                self.C.configure(state="disabled")
                self.D = self.multipleChoiceAnswer.addRadiobutton(text = "D", command = lambda: self.multipleChoiceAnswerVar.set("D"))
                self.D.configure(state="disabled")
                self.E = self.multipleChoiceAnswer.addRadiobutton(text = "E", command = lambda: self.multipleChoiceAnswerVar.set("E"))
                self.E.configure(state="disabled")
                self.multipleChoiceAnswer.setSelectedButton(self.A)
                self.submitMcBtn = self.multipleChoiceFrame.addButton(text = "Submit Question", row = 10, column = 0, command = self.submitMc)
                self.submitTestBtn = self.multipleChoiceFrame.addButton(text="Submit Test", row=10, column=1, command = self.submitTest)

                # Bind keys to answer text areas so not selectable if blank
                self.answerA.bind("<KeyRelease>", self.updateAnswerAB)
                self.answerB.bind("<KeyRelease>", self.updateAnswerAB)
                self.answerC.bind("<KeyRelease>", self.updateAnswerC)
                self.answerD.bind("<KeyRelease>", self.updateAnswerD)
                self.answerE.bind("<KeyRelease>", self.updateAnswerE)


                # Default panel when adding a new test. This panel hides the true/false and multiple choice panels until test is named.
                self.nullFrame = self.addPanel(row = 2, column = 0, columnspan = 3)
                self.image = PhotoImage(file = "images/paper.gif")
                self.image = self.image.subsample(2, 2)
                self.imageLabel = self.nullFrame.addLabel(text = "", row = 2, column = 0, sticky = "NSEW", rowspan = 3)
                self.imageLabel.configure(image = self.image)
                self.nullFrame.lift()


            def updateAnswerAB(self, event):
                """Updates state of option A and B based on answerA and answerB fields"""
                self.answerC.configure(state="normal" if self.answerA.get("1.0", "end").strip() and self.answerB.get("1.0", "end").strip() else "disabled")

            def updateAnswerC(self, event):
                """Updates state of option C based on answerC field"""
                self.C.configure(state="normal" if self.answerC.get("1.0", "end").strip() else "disabled")
                self.answerD.configure(state="normal" if self.answerC.get("1.0", "end").strip() else "disabled")

            def updateAnswerD(self, event):
                """Updates state of option D based on answerD field"""
                self.D.configure(state="normal" if self.answerD.get("1.0", "end").strip() else "disabled")
                self.answerE.configure(state="normal" if self.answerD.get("1.0", "end").strip() else "disabled")

            def updateAnswerE(self, event):
                """Updates state of option E based on answerE field"""
                self.E.configure(state="normal" if self.answerE.get("1.0", "end").strip() else "disabled")

            def enterTitle(self):
                """
                Called when the user presses the "Enter" button. Opens a
                .txt file with the name of the test, and disables the button
                and the text field. Also selects the "Multiple Choice" radio
                button.
                """
                if self.newTitle.getText() == "":
                    self.messageBox(title = "Error", message = "Please enter a title.")
                else:
                    with open("tests/TestDir.txt", "r") as dir:
                        for line in dir:
                            test = line.strip()
                            if test == self.newTitle.getText():
                                self.messageBox(title = "Error", message = "Test already exists.")
                                break
                        else:
                            self.practice_test.testIsOpen = True
                            self.new_test = open("tests/" + self.newTitle.getText() + ".txt", "wb")
                            self.enterBtn.configure(state = "disabled")
                            self.newTitle.configure(state = "readonly")
                            self.multipleChoice.configure(state = "normal")
                            self.trueFalse.configure(state = "normal")
                            self.nullFrame.destroy()

            def setTrueFalse(self):
                """
                Called when the user selects the "True/False" radio button. Lifts
                the panel for entering true/false questions, and lowers the panel
                for entering multiple choice questions.
                """
                self.trueFalseFrame.lift()
                self.multipleChoiceFrame.lower()

            def newTestBack(self):
                """Returns the user to the main menu. Closes and deletes the test if it is open."""
                if self.practice_test.testIsOpen:
                    if os.path.exists("tests/" + self.newTitle.getText() + ".txt"):
                        os.remove("tests/" + self.newTitle.getText() + ".txt")
                    self.practice_test.testIsOpen = False
                self.practice_test.reset()
                self.destroy()

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
                    self.trueFalseAnswerVar.set("True")
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
                # Much Input Validation
                if self.multipleChoiceQuestion.get("1.0", "end").strip() == "":
                    self.messageBox(title = "Error", message = "Please enter a question")
                elif self.answerA.get("1.0", "end").strip() == "" or self.answerB.get("1.0", "end").strip() == "":
                    self.messageBox(title = "Error", message = "Please enter an answer for A and B at least.")
                elif self.answerE.get("1.0", "end").strip() != "":
                    if self.answerC.get("1.0", "end").strip() == "" or self.answerD.get("1.0", "end").strip() == "":
                        self.messageBox(title = "Error", message = "You can't have an answer for E without an answer for C and D.")
                elif self.answerE.get("1.0", "end").strip() == "" and self.multipleChoiceAnswerVar.get() == "E":
                    self.messageBox(title = "Error", message = "The answer E cannot be selected if the answer is empty.")
                elif self.answerD.get("1.0", "end").strip() != "":
                    if self.answerC.get("1.0", "end").strip() == "":
                        self.messageBox(title = "Error", message = "You can't have an answer for D without an answer for C.")
                elif self.answerC.get("1.0", "end").strip() == "" and self.multipleChoiceAnswerVar.get() == "C":
                    self.messageBox(title = "Error", message = "The answer C cannot be selected if the answer is empty.")
                elif self.answerD.get("1.0", "end").strip() == "" and self.multipleChoiceAnswerVar.get() == "D":
                    self.messageBox(title = "Error", message = "The answer D cannot be selected if the answer is empty.")
                
                else:
                    self.test.append(McQuestion(self.number, self.multipleChoiceQuestion.get("1.0", "end"), self.multipleChoiceAnswerVar.get(), self.answerA.get("1.0", "end"), self.answerB.get("1.0", "end"), self.answerC.get("1.0", "end"), self.answerD.get("1.0", "end"), self.answerE.get("1.0", "end")))
                    self.number += 1
                    self.questionNumber = self.addLabel(text = f"Question number {self.number}", row = 1, column = 0)
                    self.multipleChoiceQuestion.delete("1.0", "end")
                    self.multipleChoiceAnswer.setSelectedButton(self.A)
                    self.multipleChoiceAnswerVar.set("A")
                    self.answerA.delete("1.0", "end")
                    self.answerB.delete("1.0", "end")
                    self.answerC.delete("1.0", "end")
                    self.answerD.delete("1.0", "end")
                    self.answerE.delete("1.0", "end")
                    self.C.configure(state = "disabled")
                    self.D.configure(state = "disabled")
                    self.E.configure(state = "disabled")
                    # print(self.test) # TESTING PURPOSES
                    # print(McQuestion) # TESTING PURPOSES

            def submitTest(self):
                """Submits the test to the .txt file."""
                if self.number == 1:
                    self.messageBox(title = "Error", message = "Please add at least one question")
                else:
                    with self.new_test:
                        pickle.dump(self.test, self.new_test)
                    with open("tests/TestDir.txt", "a") as file:
                        file.write(self.newTitle.getText() + "\n")
                    self.messageBox(title = "Success", message = f"{self.newTitle.getText()} successfully created")
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
        self.deleteTestBtn.configure(state = "disabled")

        class PracticeTest(EasyFrame):
            """Practice Test Selection Window"""
            def __init__(self, practice_test):
                EasyFrame.__init__(self, title="Practice Test", resizable = False)
                self.practice_test = practice_test
                self.addLabel(text = "Select Test you wish to take:", row = 0, column = 0)
                self.startTestBtn = self.addButton(text="Start Test", row = 0, column = 1, command = self.startTest)
                self.directory = self.addRadiobuttonGroup(row = 1, column = 0, orient = "vertical")
                self.test_name = StringVar()
                # Open test directory and add radiobuttons from it.
                with open("tests/TestDir.txt", "r") as dir:
                    for line in dir:
                        test = line.strip()
                        self.directory.addRadiobutton(test, command=lambda test=test: self.selectTest(test))
                self.addButton(text="Back", row = 1, column = 1, command = self.takeTestBack)

            def selectTest(self, test):
                """Called when a test is selected."""
                self.test_name.set(test)


            def startTest(self):
                """Initializes and loads the practice test"""
                if self.test_name.get() == "":
                    self.messageBox(title = "Error", message = "Please select a test")
                else:
                    testAnswers = []
                    self.correctAnswer = 0
                    with open("tests/" + self.test_name.get() + ".txt", "rb") as test:
                        self.test_data = pickle.load(test)
                    self.startTestBtn.configure(state = "disabled")
                    
                    # Interface changes depending on question type
                    if len(self.test_data) > 0 and isinstance(self.test_data[0], McQuestion):
                        length = len(self.test_data)
                        MCPopup(length, self.test_data[0].number, self.test_data[0].question, self.test_data[0].a, self.test_data[0].b, self.test_data[0].c, self.test_data[0].d, self.test_data[0].e, self.test_data, testAnswers, startTestBtn = self.startTestBtn).mainloop()
                    elif len(self.test_data) > 0 and isinstance(self.test_data[0], TfQuestion):
                        length = len(self.test_data)
                        TFPopup(length, self.test_data[0].number, self.test_data[0].question, self.test_data[0].correct, self.test_data, testAnswers, startTestBtn = self.startTestBtn).mainloop()
                    # print(testAnswers) # TESTING PURPOSES
                    # Testing Purposes
                    # for question in test:
                    #     if type(question) == McQuestion:
                    #         print("Multiple Choice")
                    #     elif type(question) == TfQuestion:
                    #         print("True/False")
                    # print(test)

            def takeTestBack(self):
                """Closes the practice test and re-enables New Test and Take Test buttons."""
                self.practice_test.reset()
                if hasattr(MCPopup, 'current_popup') and MCPopup.current_popup is not None:
                    MCPopup.current_popup.destroy()
                if hasattr(TFPopup, 'current_popup') and TFPopup.current_popup is not None:
                    TFPopup.current_popup.destroy()
                self.destroy()
                
        takeTest = PracticeTest(self)
        takeTest.mainloop()

    def deleteTest(self):
        """Opens a dialog for selecting a practice test to delete."""
        self.newTestBtn.configure(state = "disabled")
        self.takeTestBtn.configure(state = "disabled")
        self.deleteTestBtn.configure(state = "disabled")

        class DeleteTest(EasyFrame):
            def __init__(self, practice_test):
                EasyFrame.__init__(self, title="Delete Test")
                self.practice_test = practice_test
                self.image = PhotoImage(file = "images/attention.gif")
                self.image = self.image.subsample(10, 10)
                self.imageLabel = self.addLabel(text = "", row = 2, column = 0, sticky = "NSEW", rowspan = 1)
                self.imageLabel.configure(image = self.image)
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
                self.addButton(text="Back", row = 1, column = 1, command = self.deleteTestBack)



            def selectTest(self, test):
                """Called when a test is selected."""
                self.test_name.set(test)


            def delete(self):
                """Deletes the selected test unless it is the one for Understanding This Program."""
                if not self.test_name.get():
                    self.messageBox(title = "Error", message = "No test selected.")
                    return
                if self.test_name.get() == "Understanding This Program":
                    self.messageBox(title = "Error", message = "You cannot delete this test.")
                    return
                test_file = "tests/" + self.test_name.get() + ".txt"
                if os.path.exists(test_file):
                    os.remove(test_file)
                with open("tests/TestDir.txt", "r") as dir:
                    lines = dir.readlines()
                with open("tests/TestDir.txt", "w") as dir:
                    for line in lines:
                        if line.strip() != self.test_name.get():
                            dir.write(line)
                self.messageBox(title = "Test Deleted", message = f"{self.test_name.get()} has been deleted.")
                self.practice_test.reset()
                self.destroy()

            def deleteTestBack(self):
                """Closes Delete Test and resets main menu."""
                self.practice_test.reset()
                self.destroy()

        DeleteTest(self).mainloop()

class MCPopup(EasyFrame):
    """Popup for multiple choice questions."""
    def __init__(self, length, number, question, a, b, c=None, d=None, e=None, question_list = None, answers = None, startTestBtn = None):
        EasyFrame.__init__(self, title = "Multiple Choice", resizable = False)
        self.question_list = question_list if question_list is not None else []
        self.answers = answers if answers is not None else []
        self.current_index = (number - 1)
        self.startTestBtn = startTestBtn

        MCPopup.current_popup = self

        if self.current_index == len(self.question_list) - 1:
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
        """Called when the user submits an answer."""
        self.answers.append(self.takeTestQuestVar.get())
        if self.takeTestQuestVar.get() != self.question_list[self.current_index].correct:
            self.messageBox(title = "Incorrect", message = "Incorrect. The correct answer was " + self.question_list[self.current_index].correct)

        self.current_index += 1
        if self.current_index < len(self.question_list):
            next_question = self.question_list[self.current_index]
            self.destroy()
            if isinstance(next_question, McQuestion):
                MCPopup(len(self.question_list), next_question.number, next_question.question, next_question.a, next_question.b, next_question.c, next_question.d, next_question.e, self.question_list, self.answers, startTestBtn = self.startTestBtn).mainloop()
            elif isinstance(next_question, TfQuestion):
                TFPopup(len(self.question_list), next_question.number, next_question.question, next_question.correct, self.question_list, self.answers, startTestBtn = self.startTestBtn).mainloop()            
        else:
            self.messageBox(title = "Test Completed", message = "Test Completed")
                # Calculate the score
            correct_answers = sum(1 for answer, question in zip(self.answers, self.question_list) if answer == question.correct)
            score = correct_answers / len(self.question_list) * 100

            # Display the score
            self.messageBox(title = "Test Completed", message = f"Your score is: {score:.2f}%")
            self.startTestBtn.configure(state = "normal")
            self.destroy()
            
class TFPopup(EasyFrame):
    """Popup for true/false questions."""
    def __init__(self, length, number, question, correct, question_list = None, answers = None, startTestBtn = None):
        EasyFrame.__init__(self, title = "True/False", resizable = False)
        self.correct = correct
        self.question_list = question_list if question_list is not None else []
        self.answers = answers if answers is not None else []
        self.current_index = (number - 1)
        self.startTestBtn = startTestBtn

        TFPopup.current_popup = self

        if self.current_index == len(self.question_list) - 1:
            testBtn = "Submit Test"
        else:
            testBtn = "Submit Question"
        self.addLabel(text = f"{number}. {question}", row = 0, column = 0)
        self.takeTestQuest = self.addRadiobuttonGroup(row = 1, column = 0, orient = "vertical")
        self.takeTestQuestVar = StringVar()
        self.takeTestQuestVar.set("True")
        self.takeTestTrueBtn = self.takeTestQuest.addRadiobutton(text = "True", command = lambda: self.takeTestQuestVar.set("True"))
        self.takeTestFalseBtn = self.takeTestQuest.addRadiobutton(text = "False", command = lambda: self.takeTestQuestVar.set("False"))
        self.takeTestQuest.setSelectedButton(self.takeTestTrueBtn)
        self.addButton(text = testBtn, row = 2, column = 0, command = self.takeTestSubmit)

    def takeTestSubmit(self):
        """Called when the user submits an answer."""
        self.answers.append(self.takeTestQuestVar.get())
        if self.takeTestQuestVar.get() != self.question_list[self.current_index].correct:
            self.messageBox(title = "Incorrect", message = "Incorrect. The correct answer was " + self.question_list[self.current_index].correct)

        self.current_index += 1
        if self.current_index < len(self.question_list):
            next_question = self.question_list[self.current_index]
            self.destroy()
            if isinstance(next_question, McQuestion):
                MCPopup(len(self.question_list), next_question.number, next_question.question, next_question.a, next_question.b, next_question.c, next_question.d, next_question.e, self.question_list, self.answers, startTestBtn = self.startTestBtn).mainloop()
            elif isinstance(next_question, TfQuestion):
                TFPopup(len(self.question_list), next_question.number, next_question.question, next_question.correct, self.question_list, self.answers, startTestBtn = self.startTestBtn).mainloop()
        else:
            # Calculate the score
            correct_answers = sum(1 for answer, question in zip(self.answers, self.question_list) if answer == question.correct)
            score = correct_answers / len(self.question_list) * 100

            # Display the score
            self.messageBox(title = "Test Completed", message = f"Your score is: {score:.2f}%")
            self.startTestBtn.configure(state = "normal")
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

# 10/12/2024
# During take test, Submit Question button now displays as Submit Test if there are no more questions.
# All main GUI buttons except Help disabled when on different screen.
# Back button now works during New Test.
# Back button now works during Take Test.
# Back button now works during Delete Test.
# Delete Test now works. A popup should be opened to confirm deletion.
# New Test popup now works. A popup should be opened to confirm test creation.
# Fixed the TFPopup error. Had to fix capitalization issues and for some reason I had the defaul answer set to 
# correct instead of "True".

# 10/13/2024
# 2am and I finally got basic functionality on everything. New Test, Take Test, and Delete Test. Also created a help popup.
# 3:30am. There is more stuff I'd like to do, but I am running out of time. I would like to figure out how to get the
# delete test radio button to set to default value. I also need to rework the Understanding This Program test.
# The test had a couple incorrect answers when I tried taking it, an I'm not sure if it is a bug or if I'm just too 
# tired to enter a test right now.
# Question 5 and 8 and 10 are incorrect.
# I think I should set a fixed size for the test taking window as well. Simply setting the window size and ability to
# resize the window does not work.

# 10/13/2024
# Last minute fix. I figured out why the test answers were off! When running tf and mc submit question, the answers were not being reset.
# So if a question was entered that was not A or True, the next time I entered a question that was A or True the radio button would be set but the 
# answer itself would still be the previous one. For example if question 1 was A, that's fine. Question 2 is C, that is also fine. Question 3 is A
# then the radio button is on a, but the variable is saved as C. I fixed it.
# Added and tested Understanding This Program test. It works flawllessly!

# 10/14/2024
# Input validation for the multiple choice test creation implemented. Text boxes and radio buttons are are disabled if unusable, and if radio buttons 
# are selected that shouldn't be or text is entered in a box it shouldn't be an error message pops up.

# Added some more notes. I think I have a few unused variables to remove from this program. length?