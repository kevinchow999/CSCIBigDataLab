def string_compression(input):
    output = ""
    count = 1  # Initialize count for the first character

    # Iterate through the characters in the input string
    for i in range(1, len(input)):
        if input[i] == input[i - 1]: # Counts the number of repetitions that occurs
            count += 1
        else: # A new char that is not the same as the previous appears
            if count > 1:
                # The next line is where the String compression occurs
                output += input[i - 1] + str(count) 
            else:
                output += input[i - 1]
            count = 1  # Reset count for the new char

    output += input[-1] + (str(count) if count > 1 else "")

    return output

# Prompts the user for a string
input_str = input("Enter a string: ").strip()

# Call the functiion and displays the output
output = string_compression(input_str)
print("Compressed message:", output)
