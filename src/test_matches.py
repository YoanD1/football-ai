from chatbot import handle_input

# Generate schedule first
result0 = handle_input('генерирай програма "Primeira Liga" "2025/2026"')
print("Generate schedule result:", result0)

# Test selecting league
result1 = handle_input('избери лига "Primeira Liga" "2025/2026"')
print("Select league result:", result1)

# Test showing round
result2 = handle_input('покажи кръг 1')
print("Show round result:", result2)
