import sys
import random
import numpy as np
from sklearn.neural_network import MLPRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load student data from CSV file
def read_student_data(filename):
    student_data = pd.read_csv(filename)
    return student_data

# Split student data into features and target
def get_student_scores(student_data):
    X = student_data[['algebra_score', 'geometry_score', 'pre_calculus_score']].values
    y = student_data[['final_score']].values.ravel()
    return X, y

# Load and preprocess student data
filename = 'student_data.csv'
student_data = read_student_data(filename)
X, y = get_student_scores(student_data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a neural network regressor with 2 hidden layers
regressor = MLPRegressor(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)

# Train the neural network on the training data
regressor.fit(X_train, y_train)

# Make predictions on the test set
y_pred = regressor.predict(X_test)

# Calculate mean squared error and R^2 score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print results
print("Mean Squared Error:", mse)
print("R^2 Score:", r2)

difficulty_levels = [{'category': 'Algebra', 'difficulty': 'Very Easy', 'ability_level': 'Low'},
                     {'category': 'Algebra', 'difficulty': 'Easy', 'ability_level': 'Low'},
                     {'category': 'Algebra', 'difficulty': 'Medium', 'ability_level': 'Low'},
                     {'category': 'Algebra', 'difficulty': 'Hard', 'ability_level': 'Low'},
                     {'category': 'Algebra', 'difficulty': 'Very Easy', 'ability_level': 'High'},
                     {'category': 'Algebra', 'difficulty': 'Easy', 'ability_level': 'High'},
                     {'category': 'Algebra', 'difficulty': 'Medium', 'ability_level': 'High'},
                     {'category': 'Algebra', 'difficulty': 'Hard', 'ability_level': 'High'},
                     {'category': 'Geometry', 'difficulty': 'Very Easy', 'ability_level': 'Low'},
                     {'category': 'Geometry', 'difficulty': 'Easy', 'ability_level': 'Low'},
                     {'category': 'Geometry', 'difficulty': 'Medium', 'ability_level': 'Low'},
                     {'category': 'Geometry', 'difficulty': 'Hard', 'ability_level': 'Low'},
                     {'category': 'Geometry', 'difficulty': 'Very Easy', 'ability_level': 'High'},
                     {'category': 'Geometry', 'difficulty': 'Easy', 'ability_level': 'High'},
                     {'category': 'Geometry', 'difficulty': 'Medium', 'ability_level': 'High'},
                     {'category': 'Geometry', 'difficulty': 'Hard', 'ability_level': 'High'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Very Easy', 'ability_level': 'Low'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Easy', 'ability_level': 'Low'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Medium', 'ability_level': 'Low'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Hard', 'ability_levellevel': 'Low'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Very Easy', 'ability_level': 'High'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Easy', 'ability_level': 'High'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Medium', 'ability_level': 'High'},
                     {'category': 'Pre-Calculus', 'difficulty': 'Hard', 'ability_level': 'High'}]

difficulty_transition = {
    (0, 0): 0,
    (0, 1): 1,
    (0, 2): 1,
    (0, 3): 2,
    (1, 0): 0,
    (1, 1): 1,
    (1, 2): 2,
    (1, 3): 2,
    (2, 0): 1,
    (2, 1): 1,
    (2, 2): 2,
    (2, 3): 3,
    (3, 0): 2,
    (3, 1): 2,
    (3, 2): 3,
    (3, 3): 3,
}

# Define difficulty transition matrix for each category and ability level
difficulty_transition_matrix_dict = {}
for category in ['Algebra', 'Geometry', 'Pre-Calculus']:
    for difficulty in ['Very Easy', 'Easy', 'Medium', 'Hard']:
        for ability_level in ['Low', 'High']:
            key = (category, difficulty, ability_level)
            if difficulty == 'Very Easy':
                if ability_level == 'Low':
                    difficulty_transition_matrix_dict[key] = [0.5, 0.5, 0, 0]
                else:
                    difficulty_transition_matrix_dict[key] = [0.7, 0.3, 0, 0]
            elif difficulty == 'Easy':
                if ability_level == 'Low':
                    difficulty_transition_matrix_dict[key] = [0.2, 0.6, 0.2, 0]
                else:
                    difficulty_transition_matrix_dict[key] = [0.4, 0.4, 0.2, 0]
            elif difficulty == 'Medium':
                if ability_level == 'Low':
                    difficulty_transition_matrix_dict[key] = [0, 0.5, 0.5, 0]
                else:
                    difficulty_transition_matrix_dict[key] = [0, 0.3, 0.7, 0]
            else:
                if ability_level == 'Low':
                    difficulty_transition_matrix_dict[key] = [0, 0, 0.6, 0.4]
                else:
                    difficulty_transition_matrix_dict[key] = [0, 0, 0.3, 0.7]

def next_question(difficulty_levels, current_category, current_difficulty, current_ability_level):
    # Get the index of the current category, difficulty level, and ability level
    current_category_idx = [i for i, d in enumerate(difficulty_levels) if d['category'] == current_category][0]
    current_difficulty_idx = [i for i, d in enumerate(difficulty_levels) if d['difficulty'] == current_difficulty][0]
    current_ability_level_idx = [i for i, d in enumerate(difficulty_levels) if d['ability_level'] == current_ability_level][0]

    # Compute the probability distribution for the next difficulty level
    difficulty_probs = difficulty_transition_matrix_dict[(current_category, current_difficulty, current_ability_level)]
    # Sample the next difficulty level from the probability distribution
    next_difficulty_idx = random.choices(range(len(difficulty_levels)), weights=difficulty_probs)[0]
    next_difficulty = difficulty_levels[next_difficulty_idx]['difficulty']

    return next_difficulty

question_bank = [{'question_id': 1, 'category': 'Algebra', 'difficulty': 'Very Easy'},
                 {'question_id': 2, 'category': 'Algebra', 'difficulty': 'Easy'},
                 {'question_id': 3, 'category': 'Algebra', 'difficulty': 'Medium'},
                 {'question_id': 4, 'category': 'Algebra', 'difficulty': 'Hard'},
                 {'question_id': 5, 'category': 'Geometry', 'difficulty': 'Very Easy'},
                 {'question_id': 6, 'category': 'Geometry', 'difficulty': 'Easy'},
                 {'question_id': 7, 'category': 'Geometry', 'difficulty': 'Medium'},
                 {'question_id': 8, 'category': 'Geometry', 'difficulty': 'Hard'},
                 {'question_id': 9, 'category': 'Pre-Calculus', 'difficulty': 'Very Easy'},
                 {'question_id': 10, 'category': 'Pre-Calculus', 'difficulty': 'Easy'},
                 {'question_id': 11, 'category': 'Pre-Calculus', 'difficulty': 'Medium'},
                 {'question_id': 12, 'category': 'Pre-Calculus', 'difficulty': 'Hard'}]

def predict_question(model, question_category, current_difficulty, difficulty_transition_matrix_dict, difficulty_transition_index, correct_answer, current_difficulty_index):
    # Get current difficulty level and ability level
    current_difficulty_level = current_difficulty['difficulty']
    current_ability_level = current_difficulty['ability_level']

    # Get current difficulty transition matrix
    difficulty_transition_matrix = difficulty_transition_matrix_dict[(question_category, current_difficulty_level, current_ability_level)]

    # Use model to predict student's answer
    predicted_answer = model.predict([[question_category, current_difficulty_level, current_ability_level, correct_answer, difficulty_transition_index]])[0]

    # Get predicted difficulty level and ability level
    predicted_difficulty_index = np.argmax(predicted_answer[:len(difficulty_levels)])
    predicted_difficulty_level = difficulty_levels[predicted_difficulty_index]['difficulty']
    predicted_ability_level = predicted_answer[-1]

    # Get difficulty transition index
    for key, value in difficulty_transition_index.items():
        if value == (current_difficulty_index, predicted_difficulty_index):
            difficulty_transition_index = key[0]
            break

    return predicted_ability_level, predicted_difficulty_index, difficulty_transition_index

class Question:
    def __init__(self, question_id, question_category, correct_answer, current_difficulty):
        self.question_id = question_id
        self.question_category = question_category
        self.correct_answer = correct_answer
        self.current_difficulty = current_difficulty
        self.predicted_answer = None
        self.predicted_difficulty = None

    def predict(self, difficulty_transition_matrix):
        # Calculate predicted answer and difficulty level based on current difficulty level and transition matrix
        # Set predicted_answer and predicted_difficulty attributes on question object
        pass

# Define function to make predictions on test set and evaluate model using mean squared error and R-squared
def evaluate_model(model, X_test, difficulty_levels, difficulty_transition, difficulty_transition_matrix_dict):
    # Define dictionary to store predictions for each student
    predictions = {}

 # Loop through each student in test set and make predictions
    for student_id in X_test['student_id'].unique():
        # Get student's data from test set
        student_data = X_test.loc[X_test['student_id'] == student_id, :]

        # Initialize variables for first question
        current_difficulty_index = 0
        current_difficulty = difficulty_levels[current_difficulty_index]
        predicted_difficulty_index = 0

        # Define dictionary to store data for each question
        question_data = {}

        # Loop through each question and make predictions
        for i, row in student_data.iterrows():
            # Get question data
            question_id = row['question_id']
            question_category = row['category']
            correct_answer = row['correct_answer']

            # Get current difficulty transition matrix
            difficulty_transition_index = difficulty_transition[(current_difficulty_index, predicted_difficulty_index)]
            difficulty_transition_matrix = difficulty_transition_matrix_dict[(question_category, current_difficulty['difficulty'], current_difficulty['ability_level'])]

            # Make prediction for current question
            predicted_answer, predicted_difficulty_index = predict_question(model, row['category'], current_difficulty, difficulty_transition_matrix, difficulty_transition_index, correct_answer)

            # Store question data in dictionary
            question_data[question_id] = {'question_category': question_category, 
                                          'current_difficulty': current_difficulty,
                                          'predicted_difficulty_index': predicted_difficulty_index,
                                          'correct_answer': correct_answer,
                                          'predicted_answer': predicted_answer}

            # Update current difficulty for next question
            current_difficulty_index = predicted_difficulty_index
            current_difficulty = difficulty_levels[current_difficulty_index]

        # Store predictions for current student
        predictions[student_id] = question_data

    # Calculate mean squared error and R-squared
    mse = 0
    ss_res = 0
    ss_tot = 0
    n = 0

    for student_id, student_data in predictions.items():
        for question_id, question_data in student_data.items():
            # Get actual and predicted scores
            actual_score = question_data['correct_answer']
            predicted_score = question_data['predicted_answer']

            # Update mean squared error and R-squared
            mse += (predicted_score - actual_score) ** 2
            ss_res += (predicted_score - actual_score) ** 2
            ss_tot += (actual_score - np.mean(y)) ** 2
            n += 1

    # Calculate mean squared error and R-squared
    mse /= n
    r2 = 1 - (ss_res / ss_tot)

# Define function to predict difficulty level based on student's ability level
def predict_difficulty(algebra, geometry, pre_calculus):
    x = np.array([[algebra, geometry, pre_calculus]])
    y_pred = regressor.predict(x)[0]
    if y_pred == 0:
        return 'Very Easy'
    elif y_pred == 1:
        return 'Easy'
    elif y_pred == 2:
        return 'Medium'
    else:
        return 'Hard'

# Define function to generate assessment based on difficulty level
def generate_assessment(difficulty, num_questions, questions):
    category_questions = [q for q in questions if q['category'] == difficulty['category']]
    np.random.shuffle(category_questions)
    assessment = category_questions[:num_questions]
    return assessment

def adjust_difficulty_level(predicted_difficulty, current_difficulty):
    difficulty_levels = ['Very Easy', 'Easy', 'Medium', 'Hard']
    current_difficulty_index = difficulty_levels.index(current_difficulty['difficulty'])
    predicted_difficulty_index = difficulty_levels.index(predicted_difficulty)
    difficulty_transition = {
        (0, 0): 0,
        (0, 1): 1,
        (0, 2): 1,
        (0, 3): 2,
        (1, 0): 0,
        (1, 1): 1,
        (1, 2): 2,
        (1, 3): 2,
        (2, 0): 1,
        (2, 1): 1,
        (2, 2): 2,
        (2, 3): 3,
        (3, 0): 2,
        (3, 1): 2,
        (3, 2): 3,
        (3, 3): 3,
    }
    difficulty_transition_index = difficulty_transition[(current_difficulty_index, predicted_difficulty_index)]
    new_difficulty = {'category': current_difficulty['category'], 'difficulty': difficulty_levels[difficulty_transition_index]}
    return new_difficulty

# Load assessment questions from CSV file
assessment_questions = pd.read_csv('assessment_questions.csv')

# Load student data from CSV file
student_data = pd.read_csv('student_data.csv', dtype={'student_id': str})

# Define function to generate assessment questions based on student ability level
def generate_questions(student_id):
    # Get student's ability level from student data
    student_ability_level = student_data.loc[student_data['student_id'] == student_id, 'ability_level'].values[0]

    # Get list of categories and difficulty levels
    categories = list(set(assessment_questions['category']))
    difficulty_levels = list(set(assessment_questions['difficulty']))

    # Define dictionary to store questions for each category and difficulty level
    questions = {}

    # Generate questions for each category and difficulty level
    for category in categories:
        category_questions = {}
        for difficulty in difficulty_levels:
            # Get questions for current category and difficulty level
            current_questions = assessment_questions.loc[(assessment_questions['category'] == category) & 
                                                     (assessment_questions['difficulty'] == difficulty)]
            # Shuffle questions
            current_questions = current_questions.sample(frac=1).reset_index(drop=True)

            # Determine number of questions to select
            if student_ability_level >= 4:
                num_questions = 2
            elif student_ability_level >= 2:
                num_questions = 1
            else:
                num_questions = 1  # Set a minimum of 1 question for each category and difficulty level

            # Select questions for current category and difficulty level
            if len(current_questions) < num_questions:
                selected_questions = current_questions  # Select all available questions
            else:
                selected_questions = current_questions.sample(n=num_questions)

            # Add selected questions to dictionary
            category_questions[difficulty] = selected_questions

        # Add category questions to main dictionary
        questions[category] = category_questions

    return questions

def score_assessment(student_id):
    # Generate assessment questions
    questions = generate_questions(student_id)

    # Define variables to store score and total number of questions
    total_score = 0
    total_questions = 0

    # Define list to store questions and answers
    question_list = []

    # Define a variable to keep track of the question number
    question_number = 1

    # Loop through categories and difficulty levels to present questions to student
    for category, difficulty_levels in questions.items():
        print(f'Category: {category}\n')
        for difficulty, question_data in difficulty_levels.items():
            print(f'Difficulty level: {difficulty}\n')

            # Add this loop to present the questions
            for i, question in enumerate(question_data.iterrows(), start=1):
                # Get question and answer
                question_text = question[1]['question']
                answer = question[1]['answer']

                # Ask question and get student's answer
                student_answer = input(f'{question_text}\nAnswer: ')

                # Check if student's answer is correct
                if student_answer == str(answer):
                    print('Correct!\n')
                    total_score += 1
                    is_correct = True
                else:
                    print(f'Incorrect. The correct answer is {answer}.\n')
                    is_correct = False

                # Increment total number of questions
                total_questions += 1

                # Add question and answer to list
                question_list.append({
                    'question_number': question_number,
                    'category': category,
                    'difficulty': difficulty,
                    'question': question_text,
                    'answer': answer,
                    'student_answer': student_answer,
                    'is_correct': is_correct
                })

                # Increment question number
                question_number += 1
                
    # Calculate score percentage only if there are questions
    if total_questions > 0:
        score_percentage = (total_score / total_questions) * 100
    else:
        score_percentage = 0
    
    # Give feedback to student based on score
    feedback = ''
    if score_percentage >= 80:
        feedback = 'Congratulations! You did an excellent job on the assessment.'
    elif score_percentage >= 60:
        feedback = 'Good job, but there is room for improvement. Consider studying more and taking the assessment again.'
    else:
        feedback = 'It seems like you may need additional practice before taking the assessment again.'
    
    return (score_percentage, feedback, question_list)

print("\n")
print("Welcome to the High School Math Assessment Program.")
print("This program will be asking you ten questions.")
print("Please separate terms and arithmetic symbols with a space.")
print("Leave answers in terms of pi when needed.")
print("\n")
# Prompt the user to enter a student ID
student_id = input("Enter the student ID: ")

# Check if entered student ID is valid
if student_id not in student_data['student_id'].values.tolist():
    print("Invalid student ID.")
    sys.exit(0)

# Score the assessment for the student5
score_percentage, feedback, question_list = score_assessment(student_id)

# Print the score and feedback
print("Assessment Score: {:.2f}%".format(score_percentage))
print("Feedback: {}".format(feedback))

# Print the student's answers and correctness for each question
print("\nQuestion-wise Results:")
for question in question_list:
    question_number = question['question_number']
    question_text = question['question']
    student_answer = question['student_answer']
    correct_answer = question['correct_answer']
    is_correct = question['is_correct']
    correctness = "Correct" if is_correct else "Incorrect"
    print("Question {}: {}".format(question_number, question_text))
    print("Your Answer: {}".format(student_answer))
    print("Correct Answer: {}".format(correct_answer))
    print("Result: {}\n".format(correctness))