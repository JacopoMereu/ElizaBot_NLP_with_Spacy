# ElizaBot_NLP_with_Spacy
 The project for the NLP course: an Eliza-like chatbot created combining classic generic regex matching and specific spacy matching.

<br>
 <h2>Library dependencies</h2>
    <ul>
    <li>pip install python-telegram-bot</li>
    <li>pip install clean-text</li>
    <li>pip install setuptools wheel</li>
    <li>pip install spacy</li>
    <li>python -m spacy download en_core_web_lg</li>
    <li>pip install numpy</li>
    <li>pip install nltk</li>
    </ul>

<br>
<h2>Files</h2>
    <ul>
    <li><b><i>main.py</i></b> contains the connection to the telegram API.
                            <br>&emsp;Runs this file to start up the telegram bot.</li>
    <br>
    <li><b><i>logic.py</i></b> contains the main logic of the chatbot.
                            <br>&emsp;Runs this file to use the terminal version of the chatbot.
                            <br>&emsp;&emsp;The <i>hard_coded_case</i> flag let the bot respond to an hard-coded input. Disable it if you want to chat with the bot via terminal.</li>
    <br>
    <li><b><i>sentence_analysis.py</i></b> contains all the functions used to analyze the user input text with Spacy.</li>
    <li><b><i>responses.py</i></b> contains the patterns/responses rules and the bot reflections.</li>
    <li><b><i>my_secrets.py</i></b> should contain the bot's token given by the @BotFather.</li>
    </ul>
