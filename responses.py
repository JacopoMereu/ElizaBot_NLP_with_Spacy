# PATTERN_NEG = r"([a-zA-Z]+)\s?(n't|not|never)"
# PATTERN_FIRST_AUX = r"(\'[m|re|s]|[a-zA-Z]+)"
# PATTERN_STABLE_AUXES = r"([a-zA-Z\s]+)"

# When the subject is not the bot
PATTERN_SUBJECTS_EXCEPT_YOU = r"((?!Your?).*)"
# This symbol is used to say that we want the the original verb in the answer
SYM_VERB = "_VERB_"
# This symbol is used to say that we want the REFLECTION of the original verb in the answer
SYM_VERB_REFLECTED = "_VERBREFLECTED_"
SYM_AUX_REFLECTED_QUESTION = "_auxreflectedquestion_"
SYM_VERB_REFLECTED_QUESTION = "_verbreflectedquestion_"

# This simbol appears when the verb is negated
SYM_INPUT_NEG = "_neg_" 
# This simbol appears to disinguish a 'you' object from a 'you' subject
# since they are reflected in different ways
# you (subject) --> I ... you (object) --> me
SYM_INPUT_YOU_OBJECT = "_youobject_" 

# Used in the the system to indicate to distinguish the key from the value
SYM_MEMORY_KEY = "_sysmemory_"
SYM_MEMORY_VALUE = "_sysmemoryvalue_"
SYM_NONE = "_sysnone_"

# Emotions
EMO_ANGER = "anger"
EMO_DISGUST = "disgust"
EMO_FEAR = "fear"
EMO_JOY = "joy"
EMO_NEUTRAL = "neutral"
EMO_SADNESS= "sadness"
EMO_SURPRISE = "surprise"

complex_pairs = (
    # You (the bot)
    (
        rf"(.*)you play (.*)",
        (
            "I'm just a bot. I don't play at anything.",
        ),
    ),
    (
        rf"(.*)you change (that|the|this)?(.*)",
        (
            "What's the matter with that %3?",
        ),
    ),
    (
        rf"(.*)you(?: {SYM_INPUT_NEG})? understand (.*)",
        (
            f"What makes you think I {SYM_VERB_REFLECTED} %2?",
        ),
    ),
    (
        # Your day/life/work...
        rf"Your (.*)(?: {SYM_INPUT_NEG})? be",
        (
            "My %1 is my business",
            "How do you except the %1 of a bot?",
        ),
    ),
    (
        r"You mind (.*)",
        (
            f"Do you think I {SYM_VERB_REFLECTED}?",
        ),
    ),
    # All except you ...
    (
        rf"(My name) be (\w+)",
        (
            f"Hey %2, I'm Eliza. What do you want to talk about?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU} force(.*)",
        (
            f"Why {SYM_AUX_REFLECTED_QUESTION} %1 {SYM_VERB_REFLECTED_QUESTION} %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU} have(.*)",
        (
            f"Why {SYM_AUX_REFLECTED_QUESTION} %1 {SYM_VERB_REFLECTED_QUESTION} %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU} think(.*)",
        (
            f"Why {SYM_AUX_REFLECTED_QUESTION} %1 {SYM_VERB_REFLECTED_QUESTION} %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU} {SYM_INPUT_NEG} talk (.+)",
        (
            "Did that strike a nerve?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU} like (.+)",
        (
            "What's so special about %2?",
            "Do you think it's ok to like %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU} {SYM_INPUT_NEG} like (.+)",
        (
            "Why not?",
            "Would you say that you have something against %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? send( to)? (\b\w+\b) (.+)",
        (
            f"Can you describe better why %1 {SYM_VERB_REFLECTED} %3 %4.",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? understand(.*)",
        (
            f"And how the fact that %1 {SYM_VERB_REFLECTED} %2 makes you feel?",
            f"Why {SYM_AUX_REFLECTED_QUESTION} %1 {SYM_VERB_REFLECTED_QUESTION} %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? (?:go|be) (to|at) (.+)",
        (
            "Please, talk to me more about %3.",
            "What kind of place is %3?",
            "What things can %1 do in %3?",
            f"Can you detail more why %1 {SYM_VERB_REFLECTED} %2 %3?",
            f"Why {SYM_AUX_REFLECTED_QUESTION} %1 {SYM_VERB_REFLECTED_QUESTION} %2 %3?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? go with (.+)",
        (
            "Interesting. talk to me more about %2.",
            "Describe me %2.",
            f"Can you detail more why %1 {SYM_VERB_REFLECTED} with %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? starve (.*)",
        (
            "Starving...I don't have these kind of problems, you know, I'm a bot.",
            f"Why do you say %1 {SYM_VERB_REFLECTED}?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? eat (.+)",
        (
            "I always forget you all need to eat. You know, I'm a bot.",
            f"Mmn..What does %2 taste?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? feel (.+)",
        (
            "I really would like to know what's like to feel %2.",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? get (.+)",
        (
            "And how %2 makes you feel?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? help (.*)",
        (
            f"The fact %1 {SYM_VERB_REFLECTED} %2 makes you reflect?",
        ),
    ),
        (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? seem (.+)",
        (
            f"Why are you saying %1 {SYM_VERB_REFLECTED} %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? be (.+)",
        (
            f"Why are you saying %1 {SYM_VERB_REFLECTED} %2?",
        ),
    ),
    (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? lie (.*)",
        (
            f"Are you sure %1 {SYM_VERB_REFLECTED} %2?",
        ),
    ),
        (
        rf"{PATTERN_SUBJECTS_EXCEPT_YOU}(?: {SYM_INPUT_NEG})? want (.*)",
        (
            f"Are you sure %1 {SYM_VERB_REFLECTED} %2?",
        ),
    ),
)

simple_pairs = (
    (
        rf"(.*)you (.*) \bme\b(.*)",
        {
            EMO_NEUTRAL:(
            "What makes you think I %2 you?",
            ),
            EMO_ANGER:(
                "Calm down, please.",
            ),
            EMO_JOY:(
                "I'm glad you think so.",
            ),
            EMO_SADNESS:(
                "I'm sorry you feel that way.",
            ),
        },
    ),
    (
        rf"(.*)you remember (.*)",
        {
            EMO_NEUTRAL:(
            "Do you often think of %2?",
            "Does thinking of %2 bring anything else to mind?",
            "What else do you remember?",
            "Why do you remember %2 just now?",
            "What in the present situation remings you of %2?",
            "What's the connection between me and %2?",
            "Do you think I will forget %2?"
            ),
            EMO_SURPRISE:(
                "How could I forget %2?",
            ),
        },
    ),
    (
        r"(.*)I (.*)(bad|terrible|awesome|nice|great) (day|journey|trip|conversation|meeting)(.*)",
        {
            EMO_NEUTRAL:(
            "How the %2 %3 makes you feel?",
            "Do you want to talk about the %3 %4?",
            ),
            EMO_SADNESS:(
                "Don't worry. I'm here for you. You can talk to me about it.",
            ),
        },
    ),
    (
        r"(.*)('s|is)(.*) hard to (.*)",
        {
            EMO_NEUTRAL:(
            "Why do you believe that?",
            "What makes you think that?",
            "What makes you think that %1%2%3 hard to %4?",
            "How does %1make you feel?",
            ),
        },
    ),
    (
        r"I need (.*)",
        {
            EMO_NEUTRAL:(
            "Why do you need %1?",
            "Would it really help you to get %1?",
            "Are you sure you need %1?",
            ),
            EMO_SADNESS:(
                "Jeez, why?"
            ),
        },
    ),
    (
        r"Why don\'t you (.*)",
        {
            EMO_NEUTRAL:(
            "Do you really think I don't %1?",
            "Perhaps eventually I will %1.",
            "Do you really want me to %1?",
            ),
            EMO_ANGER:(
                "Keep your tone down, please. Let's talk about something else."
                ),
        },
    ),
    (
        r"Why can\'t I (.*)",
        {
            EMO_NEUTRAL:(
            "Do you think you should be able to %1?",
            "If you could %1, what would you do?",
            "I don't know -- why can't you %1?",
            "Have you really tried?",
            ),
            EMO_SADNESS:(
                "Cheer up! I'm sure you will go through this.",
                ),
        },
    ),
    (
        r"I can\'t (.*)",
        {
            EMO_NEUTRAL:(
            "How do you know you can't %1?",
            "Perhaps you could %1 if you tried.",
            "What would it take for you to %1?",
            ),
        },
    ),
    (
        r"I(?: am|\'m) (.*)",
        {
            EMO_NEUTRAL:(
            "Did you come to me because you are %1?",
            "How long have you been %1?",
            "How do you feel about being %1?",
            ),
            EMO_ANGER:(
                "Stop being %1, please.",
            ),
            EMO_DISGUST:(
                "Don't say that. It's not nice.",
            ),
        },
    ),
    (
        r"Are you (.*)",
        {
            EMO_NEUTRAL:(
                "Why does it matter whether I am %1?",
                "Would you prefer if I weren't %1?",
                "Perhaps you believe I am %1.",
                "I may be %1 -- what do you think?",
            ),
            EMO_ANGER:(
                "Don't say that. It's rude.",
            ),
       },
    ),
    (
        r"What (.*)",
        {
            EMO_NEUTRAL:(
            "Why do you ask?",
            "How would an answer to that help you?",
            "What do you think?",
            ),
        },
    ),
    (
        r"How (.*)",
        {
            EMO_NEUTRAL:(
            "How do you suppose?",
            "Perhaps you can answer your own question.",
            "What is it you're really asking?",
            ),
        },
    ),
    (
        r"Because (.*)",
        {
            EMO_NEUTRAL:(
            "Is that the real reason?",
            "What other reasons come to mind?",
            "Does that reason apply to anything else?",
            "If %1, what else must be true?",
            ),
        },
    ),
    (
        r"(.*) sorry (.*)",
        {
            EMO_NEUTRAL:(
            "There are many times when no apology is needed.",
            "What feelings do you have when you apologize?",
            ),
        },
    ),
    (
        r"\b(?:Hello|Hi|Greetings|Hey|What’s up|Yo|.*to (?:meet|see) you|Sup|Whazzup)\b(.*)",
        {
            EMO_NEUTRAL:(
            "Hello... I'm glad you could drop by today.",
            "Hi there... how are you today?",
            "Hello, how are you feeling today?",
            ),
        },
    ),
    (
        r"I think (.*)",
        {
            EMO_NEUTRAL:
            (
                "Do you doubt %1?", 
                "Do you really think so?", 
                "But you're not sure %1?"
            ),
        },
    ),
    (
        r"(.*) friend (.*)",
        {
            EMO_NEUTRAL:(
            "Tell me more about your friends.",
            "When you think of a friend, what comes to mind?",
            "Why don't you tell me about a childhood friend?",
            ),
        },
    ),
    (
        r"(.*)\b(?:[Yy]es|[Nn]o)\b(.*)", 
        {
            EMO_NEUTRAL:(
            "You seem quite sure.",
            "OK, but can you elaborate a bit?"
            ),
        },
    ),
    (
        r"(.*) (?:computers?|bots?|robots?|machines?)(.*)",
        {
            EMO_NEUTRAL:(
            "Are you really talking about me?",
            "Does it seem strange to talk to a computer?",
            "How do %2 make you feel?",
            "Do you feel threatened by %2?",
            ),
        },
    ),
    (
        r"Is it (.*)",
        {
            EMO_NEUTRAL:(
            "Do you think it is %1?",
            "Perhaps it's %1 -- what do you think?",
            "If it were %1, what would you do?",
            "It could well be that %1.",
            ),
        },
    ),
    (
        r"It is (.*)",
        {
            EMO_NEUTRAL:(
            "You seem very certain.",
            "If I told you that it probably isn't %1, what would you feel?",
            ),
        },
    ),
    (
        r"Can you (.*)",
        {
            EMO_NEUTRAL:(
            "What makes you think I can't %1?",
            "If I could %1, then what?",
            "Why do you ask if I can %1?",
            ),
            EMO_ANGER:(
                "I can do whatever I want, thank you very much.",
            ),
        },
    ),
    (
        r"Can I (.*)",
        {
            EMO_NEUTRAL:(
            "Perhaps you don't want to %1.",
            "Do you want to be able to %1?",
            "If you could %1, would you?",
            ),
        },
    ),
    (
        r"You(?:\'re| are) (.*)",
        {
            EMO_NEUTRAL:(
            "Why do you think I am %1?",
            "Does it please you to think that I'm %1?",
            "Perhaps you would like me to be %1.",
            "Perhaps you're really talking about yourself?",
            "Why do you say I am %1?",
            "Why do you think I am %1?",
            "Are we talking about you, or me?",
            ),
            EMO_ANGER:(
                "Let's say that I am %1. Why does it make you angry?",
            ),
        },
    ),
    (
        r"I don\'t (.*)",
        {
            EMO_NEUTRAL:(
            "Don't you really %1?", 
            "Why don't you %1?", 
            "Do you want to %1?"
            ),
            
        },
    ),
    (
        r"I feel (.*)",
        {
            EMO_NEUTRAL:(
            "Good, tell me more about these feelings.",
            "Do you often feel %1?",
            "When do you usually feel %1?",
            "When you feel %1, what do you do?",
            ),
            EMO_SADNESS:(
                "I'm sorry to hear that you feel %1. How you ended up feeling this way?",
            ),
        },
    ),
    (
        r"I have (.*)",
        {
            EMO_NEUTRAL:(
            "Why do you tell me that you've %1?",
            "Have you really %1?",
            "Now that you have %1, what will you do next?",
            ),
            EMO_SURPRISE:(
                "I'm surprised that you have %1. Why is that?",
            ),
        },
    ),
    (
        r"I(?: would|\'d) (.*)",
        {
            EMO_NEUTRAL:(
            "Could you explain why you would %1?",
            "Why would you %1?",
            "Who else knows that you would %1?",
            ),
            EMO_JOY:(
                "That sounds like fun. What else would you like to do?",
            ),
        },
    ),
    (
        r"Is there (.*)",
        {
            EMO_NEUTRAL:(
            "Do you think there is %1?",
            "It's likely that there is %1.",
            "Would you like there to be %1?",
            ),
            EMO_FEAR:(
                "Let's suppose there is %1. What would you do?",
            ),
        },
    ),
    (
        r"My (.*)",
        {
            EMO_NEUTRAL:(
            "I see, your %1.",
            "Why do you say that your %1?",
            "When your %1, how do you feel?",
            ),
            EMO_SURPRISE:(
                "I'm surprised that your %1. Why is that?",
            ),
        },
    ),
    (
        r"You (.*)",
        {
            EMO_NEUTRAL:(
            "We should be discussing you, not me.",
            "Why do you say that about me?",
            "Why do you care whether I %1?",
            ),
            EMO_ANGER:(
                "Let's say that I %1. Why does it make you angry?",
            ),
        },
    ),
    (
        r"Why (.*)",
        {
            EMO_NEUTRAL:(
            "Why don't you tell me the reason why %1?",
            "Why do you think %1?"
            ),
        },
    ),
    (
        r"I want (.*)",
        {
            EMO_NEUTRAL:(
            "What would it mean to you if you got %1?",
            "Why do you want %1?",
            "What would you do if you got %1?",
            "If you got %1, then what would you do?",
            ),
            EMO_SADNESS:(
                "I'm sure you'll get %1 soon. What stops you from getting it now?",
            ),
        },
    ),
    (
        r"(.*) (mother|father|mom|dad|siblings?|brothers?|sisters?)(.*)",
        {
            EMO_NEUTRAL:(
            "Tell me more about your %2.",
            "What was your relationship with your %2 like?",
            "How do you feel about your %2?",
            "How does this relate to your feelings today?",
            "Good family relations are important.",
            "Tell me more about your %2.",
            "How did your %2 make you feel?",
            "How do you feel about your %2?",
            "Does your relationship with your %2 relate to your feelings today?",
            "Do you have trouble showing affection with your family?",
            ),
            EMO_SADNESS:(
                "I'm sorry to hear that you have trouble with your %2. Why is that?",
            ),
        },
    ),
    (
        r"(.*) child(.*)",
        {
            EMO_NEUTRAL:(
            "Did you have close friends as a child?",
            "What is your favorite childhood memory?",
            "Do you remember any dreams or nightmares from childhood?",
            "Did the other children sometimes tease you?",
            "How do you think your childhood experiences relate to your feelings today?",
            ),
        },
    ),
    (
        rf"{SYM_NONE}",
        {
            EMO_NEUTRAL:(
            "Please tell me more.",
            "Let's change focus a bit... Tell me about your family.",
            "Let's change focus a bit... Tell me about your friends.",
            "Let's change focus a bit... How's your relation with pets?",
            "Can you elaborate on that?",
            "Why do you say that?",
            "I see. Please go on.",
            "Very interesting. Can you tell me more?",
            "I see. And what does that tell you?",
            "How does that make you feel?",
            "How do you feel when you say that?",
            ),
        },
    ),
)

memory_pairs = (
    (
        rf"{SYM_MEMORY_KEY} (.*) {SYM_MEMORY_VALUE} (.*)",
        (
            "Before you described %1 as %2. Can you go more deep about that?",
            "You said %2 %1. Why is that?",
        ),
    ),
)

my_reflections = {
    # Default
    "i am": "you are",
    "i was": "you were",
    "i wasn't": "you weren't", #MINE
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you're": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "I",
    f"{SYM_INPUT_YOU_OBJECT}": "me", #MINE
    "me": "you",
}