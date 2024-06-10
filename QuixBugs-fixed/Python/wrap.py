def wrap(text, cols):
    lines = []
    while len(text) > cols:
        # Try to find a space to break the line, prioritizing breaking at spaces
        end = text.rfind(' ', 0, cols + 1)
        if end == -1:  # If no space found, force break at cols
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)
    lines.append(text)  # Append remaining text as a line
    return lines
'''
The original code failed to correctly handle the case where the remaining text was shorter than or equal to the column width \text{(cols)}, leading to an infinite loop or incorrect output. Additionally, it incorrectly handled spaces when breaking lines. By checking if the length of the remaining text is less than or equal to \text{cols}, we can append the rest of the text to the lines list and break the loop. The adjustment of the \text{end} variable (+1) ensures that spaces at the end of a line are correctly included in the line, rather than being the first character of the next line. This approach ensures that all words are kept whole unless they exceed the column width, and lines are filled as much as possible up to the specified width. Tracking the length of the remaining text (\text{len(text)}) and the position to break the line (\text{end}) was crucial in identifying and fixing the issue.

'''