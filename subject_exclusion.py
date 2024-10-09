def read_excluded_subjects(filename='excluded_subjects.txt'):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def write_excluded_subjects(subjects, filename='excluded_subjects.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for subject in subjects:
            file.write(f"{subject}\n")