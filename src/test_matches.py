from chatbot import handle_input

# Regenerate schedule first
result0 = handle_input('прегенерирай програма "Primeira Liga" "2025/2026"')
print("Regenerate schedule result:", result0)

# Test selecting league
result1 = handle_input('избери лига "Primeira Liga" "2025/2026"')
print("Select league result:", result1)

# Test showing round
result2 = handle_input('покажи кръг 1')
print("Show round result:", result2)

# Test selecting a match (use ID 31 from the output)
result3 = handle_input('избери мач 31')
print("Select match result:", result3)

# Test recording result (no quotes for clubs in this command)
result4 = handle_input('резултат Botev Plovdiv-Ludogorets 2:1 запиши')
print("Record result:", result4)

# Test adding goal
result5 = handle_input('гол "Ivan Petrov" "Botev Plovdiv" 23 минута')
print("Add goal:", result5)

# Test adding card
result6 = handle_input('картон "Ivan Petrov" "Botev Plovdiv" Y 45')
print("Add card:", result6)

# Test showing events
result7 = handle_input('покажи събития')
print("Show events:", result7)
