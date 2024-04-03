import sys
from essay_grader import EssayGrader  # Assume you have a module `essay_grader` that contains your grading logic

def main(essay_file_path):
    """
    Main function to grade an essay based on various criteria.

    :param essay_file_path: Path to the file containing the essay to grade.
    """
    try:
        with open(essay_file_path, 'r', encoding='utf-8') as file:
            essay_text = file.read()

        grader = EssayGrader()
        score_report = grader.grade_essay(essay_text)

        print("Essay Score Report:")
        print("===================")
        for criterion, score in score_report.items():
            print(f"{criterion}: {score}")

        final_score = grader.calculate_final_score(score_report)
        print("\nFinal Score:", final_score)
        print("Final Judgment:", "High" if final_score > grader.threshold else "Low")

    except FileNotFoundError:
        print(f"Error: The file {essay_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_essay_file>")
    else:
        essay_file_path = sys.argv[1]
        main(essay_file_path)