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

complex_pairs = (
    # You (the bot)
    (
        rf"(.*)you {SYM_INPUT_NEG}? understand (.*)",
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
        )
    ),
    # All except you ...
    (
        rf"(My name) be (\w+)",
        (
            f"Hey %2, I'm Eliza. What do you want to talk about?",
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
            "Would you say that you have something agains %2?",
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
            # "Please, talk to me more about %3.",
            # "What kind of place is %3?",
            # "What things can %1 find in %3?",
            # f"Can you detail more why %1 {SYM_VERB_REFLECTED} %2 %3?",
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
        r"(.*)('s|is)(.*) hard to (.*)",
        (
            "Why do you believe that?",
            "What makes you think that?",
            "What makes you think that %1%2%3 hard to %4?",
            "How does %1make you feel?",
        ),
    ),
    (
        r"I need (.*)",
        (
            "Why do you need %1?",
            "Would it really help you to get %1?",
            "Are you sure you need %1?",
        ),
    ),
    (
        r"Why don\'t you (.*)",
        (
            "Do you really think I don't %1?",
            "Perhaps eventually I will %1.",
            "Do you really want me to %1?",
        ),
    ),
    (
        r"Why can\'t I (.*)",
        (
            "Do you think you should be able to %1?",
            "If you could %1, what would you do?",
            "I don't know -- why can't you %1?",
            "Have you really tried?",
        ),
    ),
    (
        r"I can\'t (.*)",
        (
            "How do you know you can't %1?",
            "Perhaps you could %1 if you tried.",
            "What would it take for you to %1?",
        ),
    ),
    (
        r"I am (.*)",
        (
            "Did you come to me because you are %1?",
            "How long have you been %1?",
            "How do you feel about being %1?",
        ),
    ),
    (
        r"I\'m (.*)",
        (
            "How does being %1 make you feel?",
            "Do you enjoy being %1?",
            "Why do you tell me you're %1?",
            "Why do you think you're %1?",
        ),
    ),
    (
        r"Are you (.*)",
        (
            "Why does it matter whether I am %1?",
            "Would you prefer if I weren't %1?",
            "Perhaps you believe I am %1.",
            "I may be %1 -- what do you think?",
        ),
    ),
    (
        r"What (.*)",
        (
            "Why do you ask?",
            "How would an answer to that help you?",
            "What do you think?",
        ),
    ),
    (
        r"How (.*)",
        (
            "How do you suppose?",
            "Perhaps you can answer your own question.",
            "What is it you're really asking?",
        ),
    ),
    (
        r"Because (.*)",
        (
            "Is that the real reason?",
            "What other reasons come to mind?",
            "Does that reason apply to anything else?",
            "If %1, what else must be true?",
        ),
    ),
    (
        r"(.*) sorry (.*)",
        (
            "There are many times when no apology is needed.",
            "What feelings do you have when you apologize?",
        ),
    ),
    (
        r"\b(?:Hello|Hi|Greetings|Hey|What’s up|Yo|.*to (?:meet|see) you|Sup|Whazzup)\b(.*)",
        (
            "Hello... I'm glad you could drop by today.",
            "Hi there... how are you today?",
            "Hello, how are you feeling today?",
        ),
    ),
    (
        r"I think (.*)",
        ("Do you doubt %1?", "Do you really think so?", "But you're not sure %1?"),
    ),
    (
        r"(.*) friend (.*)",
        (
            "Tell me more about your friends.",
            "When you think of a friend, what comes to mind?",
            "Why don't you tell me about a childhood friend?",
        ),
    ),
    (
        r"(.*)\b[Yy]es\b(.*)", 
        (
            "You seem quite sure.", "OK, but can you elaborate a bit?"
        ),
    ),
    (
        r"(.*) (?:computer|bot|robot)(.*)",
        (
            "Are you really talking about me?",
            "Does it seem strange to talk to a computer?",
            "How do computers make you feel?",
            "Do you feel threatened by computers?",
        ),
    ),
    (
        r"Is it (.*)",
        (
            "Do you think it is %1?",
            "Perhaps it's %1 -- what do you think?",
            "If it were %1, what would you do?",
            "It could well be that %1.",
        ),
    ),
    (
        r"It is (.*)",
        (
            "You seem very certain.",
            "If I told you that it probably isn't %1, what would you feel?",
        ),
    ),
    (
        r"Can you (.*)",
        (
            "What makes you think I can't %1?",
            "If I could %1, then what?",
            "Why do you ask if I can %1?",
        ),
    ),
    (
        r"Can I (.*)",
        (
            "Perhaps you don't want to %1.",
            "Do you want to be able to %1?",
            "If you could %1, would you?",
        ),
    ),
    (
        r"You(?:\'re|\sare) (.*)",
        (
            "Why do you think I am %1?",
            "Does it please you to think that I'm %1?",
            "Perhaps you would like me to be %1.",
            "Perhaps you're really talking about yourself?",
            "Why do you say I am %1?",
            "Why do you think I am %1?",
            "Are we talking about you, or me?",
        ),
    ),
    (
        r"I don\'t (.*)",
        (
            "Don't you really %1?", 
            "Why don't you %1?", 
            "Do you want to %1?"
        ),
    ),
    (
        r"I feel (.*)",
        (
            "Good, tell me more about these feelings.",
            "Do you often feel %1?",
            "When do you usually feel %1?",
            "When you feel %1, what do you do?",
        ),
    ),
    (
        r"I have (.*)",
        (
            "Why do you tell me that you've %1?",
            "Have you really %1?",
            "Now that you have %1, what will you do next?",
        ),
    ),
    (
        r"I would (.*)",
        (
            "Could you explain why you would %1?",
            "Why would you %1?",
            "Who else knows that you would %1?",
        ),
    ),
    (
        r"Is there (.*)",
        (
            "Do you think there is %1?",
            "It's likely that there is %1.",
            "Would you like there to be %1?",
        ),
    ),
    (
        r"My (.*)",
        (
            "I see, your %1.",
            "Why do you say that your %1?",
            "When your %1, how do you feel?",
        ),
    ),
    (
        r"You (.*)",
        (
            "We should be discussing you, not me.",
            "Why do you say that about me?",
            "Why do you care whether I %1?",
        ),
    ),
    (
        r"Why (.*)",
        (
            "Why don't you tell me the reason why %1?",
            "Why do you think %1?"
        )
    ),
    (
        r"I want (.*)",
        (
            "What would it mean to you if you got %1?",
            "Why do you want %1?",
            "What would you do if you got %1?",
            "If you got %1, then what would you do?",
        ),
    ),
    (
        r"(.*) (mother|father|mom|dad|siblings?|brothers?|sisters?)(.*)",
        (
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
    ),
    (
        r"(.*) child(.*)",
        (
            "Did you have close friends as a child?",
            "What is your favorite childhood memory?",
            "Do you remember any dreams or nightmares from childhood?",
            "Did the other children sometimes tease you?",
            "How do you think your childhood experiences relate to your feelings today?",
        ),
    ),
    (
        r"(.*)\?",
        (
            "Why do you ask that?",
            "Please consider whether you can answer your own question.",
            "Perhaps the answer lies within yourself?",
            "Why don't you tell me?",
        ),
    ),
    (
        rf"{SYM_NONE}",
        (
            "Please tell me more.",
            "Let's change focus a bit... Tell me about your family.",
            "Let's change focus a bit... Tell me about your friends.",
            "Let's change focus a bit... How's your relation with pets?",
            "Can you elaborate on that?",
            "Why do you say that?",
            "I see. Please go on.",
            "Very interesting. Can you tell me more?",
            "I see.  And what does that tell you?",
            "How does that make you feel?",
            "How do you feel when you say that?",
        ),
    ),
)

memory_pairs = (
    (
        rf"{SYM_MEMORY_KEY} (.*) {SYM_MEMORY_VALUE} (.*)",
        (
            "Before you described %1 as %2. Can you go more deep about that?",
            "Earlier you used words like %2 to describe %1. Why is that?",
        ),
    ),
)

string_moods = ['sad', 'happy', 'angry', 'tired']

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
    "you're": "I'm",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "I",
    f"{SYM_INPUT_YOU_OBJECT}": "me", #MINE
    "me": "you",
}