from chatbot import handle_input

# Test showing standings for a league with no matches
result1 = handle_input('покажи класиране "Primeira Liga" "2025/2026"')
print("Show standings (no matches):", result1[:200] + "...")

# Test with non-existent league
result2 = handle_input('покажи класиране "NonExistent League" "2025/2026"')
print("Show standings (non-existent league):", result2)

# Test with wrong format
result3 = handle_input('покажи класиране wrong format')
print("Show standings (wrong format):", result3)
