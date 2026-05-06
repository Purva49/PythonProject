def calculate_grade(marks):
    if marks >= 90:
        return "A", "Excellent work! Keep shining! 🌟"
    elif marks >= 80:
        return "B", "Very Good! Keep it up! 👍"
    elif marks >= 70:
        return "C", "Good job! You can do even better! 😊"
    elif marks >= 60:
        return "D", "Nice try! Keep practicing! 💪"
    else:
        return "F", "Don't give up! Work hard and try again! 📚"


student_name = input("Enter student name: ")

while True:
    try:
        marks = float(input("Enter marks (0-100): "))

        if marks < 0 or marks > 100:
            print("Invalid marks! Please enter marks between 0 and 100.")
        else:
            break

    except ValueError:
        print("Invalid input! Please enter numbers only.")


grade, message = calculate_grade(marks)

print("\n📊 RESULT FOR", student_name.upper())
print(f"Marks: {marks}/100")
print(f"Grade: {grade}")
print(f"Message: {message}")