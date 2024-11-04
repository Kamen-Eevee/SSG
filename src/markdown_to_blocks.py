def markdown_to_blocks(markdown):
    block_list = []
    blocks = []
    blocks= markdown.split("\n\n")
    for i in range(0,len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] != "":
            block_list.append(blocks[i])
    return block_list
    
def block_to_block_type(block):
    first_char = block[0]
    match first_char:
        case "#":
            i = 0
            while i <= 6:
                if block[i] == "#":
                    i += 1
                else:
                    if block[i] == " ":
                        return "heading"
                    else:
                        return "paragraph"
            return "paragraph"
        case "`":
            if block.startswith("```") and block.endswith("```"):
                return "code"
            else:
                return "paragraph"
        case ">":
            quote = True
            lines = block.split("\n")
            for i in range(0, len(lines)):
                if not lines[i].startswith(">"):
                    quote = False
            if quote == True:
                return "quote"
            else:
                return "paragraph"

        case "*":
            unordered = True
            lines = block.split("\n")
            for i in range(0, len(lines)):
                if not (lines[i].startswith("* ") or lines[i].startswith("- ")): 
                    unordered = False
            if unordered == True:
                return "unordered list"
            else:
                return "paragraph"
        case "-":
            unordered = True
            lines = block.split("\n")
            for i in range(0, len(lines)):
                if not (lines[i].startswith("* ") or lines[i].startswith("- ")):
                    unordered = False
            if unordered == True:
                return "unordered list"
            else:
                return "paragraph"
        case "1":
            ordered_list = True
            lines = block.split("\n")
            for i in range(0, len(lines)):
                line_number = str(i + 1)
                if not lines[i].startswith(line_number + ". "):
                    ordered_list = False
            if ordered_list == True:
                return "ordered list"
            else:
                return "paragraph"
        case _:
            return "paragraph"