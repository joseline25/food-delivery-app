def calculate_overall_progress(weights, progress, x):
    total_weighted_progress = 0
    for i in range(len(weights)):
        if i <= x:
            total_weighted_progress += progress[i] * weights[i]
    return total_weighted_progress


weights = [0.2, 0.5, 0.3]
progress = [1.5, 0.4, 0.3]
x = 1  # Calculate progress at day 3
overall_progress = calculate_overall_progress(weights, progress, x)
print(f"Overall progress at day {x}: {overall_progress * 100}%")