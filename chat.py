import openai
import os
import json
import re

# set your OpenAI API key
openai.api_key = "sk-"
def chat(req, username):
    # define the prompt for the text generation
    s2 = " Answer should be as a valid json object with this structure: 1) 'title' field representing title of ppt 2) 'slides' field representing array of slides 3) Each 'slide' having: 'title', 'content' fields. Also, 'content' is a list of strings representing points each not having more than 20 words. Double Check that output is a valid json and that the number of slides is correct."
    # req = "Make a powerpoint presentation with five slides for a programmer audience on technical and ethical advantages of linux vs windows with each slide having around 200 words. It should be technical and complex."
    prompt = req + s2


    # define the model and parameters
    model_engine = "text-davinci-002"
    parameters = {
        "temperature": 0.5,
        "max_tokens": 3000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    # generate text using the model and prompt
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=parameters["max_tokens"],
        temperature=parameters["temperature"],
        top_p=parameters["top_p"],
        frequency_penalty=parameters["frequency_penalty"],
        presence_penalty=parameters["presence_penalty"]
    )

    result = response["choices"][0]["text"]

    output = re.sub(r'^.*?{', '{', result)

    # Save the JSON data string to a file
    with open(username+"ppt.json", "w") as json_file:
        json_file.write(output)


    with open(username+"ppt.json", "r") as f:
        # Read the lines of the file into a list
        lines = f.readlines()

    delimiter = "{"
    for i in range(len(lines)):
        # Find the index of the delimiter in the current line
        index = lines[i].find(delimiter)
        # If found....
        if index != -1:
            # Remove characters before the delimiter and update the line
            lines[i] = lines[i][index:]
            break
        else:
            lines[i]=""

    # Write the updated lines to a new file
    with open(username+"ppt1.json", "w") as f:
        f.writelines(lines)

    return output