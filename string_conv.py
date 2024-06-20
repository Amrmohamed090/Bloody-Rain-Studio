# Open a file named 'example.txt' in the current directory for reading ('r' mode)
with open('example.txt', 'r') as file:
    # Read the entire content of the file into a variable (assuming it's text)
    old_string = file.read()
    
    # Print the content of the file
    
old_string = [char for char in old_string]

current_number = ""
index = 0
for i , char in enumerate(old_string):
    try:
        print(int(char))
        if current_number == "":
            index = i
            print(index)
        current_number += str(int(char))

    except:
        if current_number and old_string[i] == 'p' and old_string[i+1] == 'x' :

            new_number = str(round((int(current_number)*100)/1440,3)) + "vw"
            count = 0
            for j in range(index,index + len(current_number)+2):
                old_string[j] = ""
            old_string[index] = new_number
        current_number = ""


new_s = ""

for c in old_string:
    new_s +=c

print(new_s)
            