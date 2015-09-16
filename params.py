data_dir = 'data'
alphabet = 'abcdefghijklmnopqrstuvwxyz'
regex_string = '[^a-z]'
# letter to represent an unknown letter
unknown_letter = '_'
parameters = {
    'normalization_iterations': 25,
    'pair_counter_epsilon': 1e-2,
    'max_length_word_to_fragment': 9,
    'min_frequency_word_to_fragment': 6,
    'paircounts_solver_iterations': 30,
    'paircounts_solver_num_top_start': 15,
    'paircounts_solver_occurrence_min_start': 4,
    'paircounts_solver_occurrence_reduction_per_iteration': 0.2,
    'num_iterations_modify_letters': 10
}
