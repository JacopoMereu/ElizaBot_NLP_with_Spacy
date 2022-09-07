import spacy
from spacy.matcher import Matcher
import re



# SUBJECTS_DEP_ = ["nsubj", 'conj', "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
# SUBJECTS_POS_STOP_AFTER = ["PRON"]

# VERBS_DEP_ = ["dobj", "aux", "ROOT", "conj"]
# VERBS_POS_ = ["VERB", "AUX"]
# OBJECTS = ["dobj", "dative", "attr", "oprd"]

def preprocessing(nlp, input):
    """ Preprocessing necessary before to transform the input text into a spacy doc.
    Args:
        nlp (the Spacy model): the Spacy model to use.
        input (string): the input text to preprocess.

    Returns:
        string: the preprocessed input text.
    """
    # dashes are dangerous, it's better to replace them with spaces
    input = re.sub(r'-', ' ', input)
    # "you all" and variations can break the patterns, so we replace it with you
    input = re.sub(r'(y\'all|you-all|you all|you guys)', 'you', input)
    # remove extra spaces
    input = re.sub(r'\s+', ' ', input)
    # ; and ! are converted into .
    input = re.sub(r'[;!]', '.', input)

    # Change ", subject verb" to ". subject verb"
    comma_between_clauses_patterns = [
        # , I aux/verb =>  . I aux/verb
        [
            {"TAG": ","},
            {"POS":"PRON", "DEP":{"IN":["conj","nsubj", "nsubjpass"]}},
            {"POS":{"IN":["AUX","PART","VERB", "ADP", "ADV"]},"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "RB", "MD", "TO"]}, "OP":"+"}
        ],
    ]

    tmp_doc = nlp(input)
    matcher = Matcher(nlp.vocab)
    matcher.add("comma_to_change_in_fullstop", comma_between_clauses_patterns, greedy="FIRST")
    matches = matcher(tmp_doc)
    # For each match
    for match in matches:
        # Get the text of the match excluding the comma
        match_string = tmp_doc[match[1]+1:match[2]]
        # Replace the comma with a fullstop followed by a space
        input = re.sub(rf',\s*(?={match_string})', '. ', input)

    # Remove the remaining , => it might bring to a wrong sents creation
    # input = re.sub(r',', '', input)

    return input

def get_full_subject(nlp, doc, clause, isQuestion):
    """Get the first subject within a clause, adjectives included.

    Args:       
        nlp (Spacy model): The Spacy model loaded.
        doc (Spacy document): The Spacy document to be analyzed
        clause (Spacy Span): The clause from which to extract the subject.
        isQuestion (bool): flag to indicate if the clause is a question.

    Returns:
        Spacy span: the sequence of token representing the subject.
    """    
    subject_patterns = [
        # My/The (incredible, smart and brilliant) children and I
        [{"POS": {"IN": ["PRON", "DET"]}, "DEP":{"IN":["poss", "det"]}}, {"POS": {"IN": ["ADJ", "PUNCT", "CCONJ"]}, "OP": "*"}, {"POS":"NOUN"}, {"POS": "CCONJ", "DEP": "cc"}, {"POS":"PRON", "DEP":{"IN":["conj","nsubj"]}}],
        # My/The (incredible, smart and brilliant) children (and Mr. Rob)
        [{"POS": {"IN": ["PRON", "DET"]}, "DEP":{"IN":["poss", "det"]}}, {"POS": {"IN": ["ADJ", "PUNCT", "CCONJ"]}, "OP": "*"}, {"POS":"NOUN"}, {"POS": "CCONJ", "DEP": "cc"}, {"POS":"PROPN", "DEP":"compound","OP":"?"}, {"POS":"PROPN", "DEP":"nsubj"}],
        # My/The (incredible, smart and brilliant) children
        [{"POS": {"IN": ["PRON", "DET"]}, "DEP":{"IN":["poss", "det"]}}, {"POS": {"IN": ["ADJ", "PUNCT", "CCONJ"]}, "OP": "*"}, {"POS":"NOUN"}], 
        # Children
        [{"POS":"NOUN", "DEP":{"IN":["conj","nsubj", "nsubjpass"]}}],
        # # Bob, Paul and I 
        [{"POS": {"IN": ["PROPN", "PUNCT"]}, "OP": "+"},  {"POS": "CCONJ", "DEP": "cc"}, {"POS":"PRON", "DEP":{"IN":["conj","nsubj"]}}],
        # Bob, Paul and (Mr) Robinson
        [{"POS": {"IN": ["PROPN", "PUNCT"]}, "OP": "+"},  {"POS": "CCONJ", "DEP": "cc"}, {"POS":"PROPN", "DEP":"compound","OP":"?"}, {"POS":"PROPN"}],
        # (Mr.) Bob
        [{"POS":"PROPN", "DEP":"compound","OP":"?"}, {"POS":"PROPN"}],
        # I
        [{"POS":"PRON", "DEP":{"IN":["conj","nsubj", "nsubjpass"]}}],
        # You all / You guys No more necessary
        # [{"POS":"PRON", "DEP":{"IN":["conj","nsubj", "nsubjpass","nmod"]}, "LOWER": {"REGEX":"(you|y')"}}, {"LOWER":{"REGEX":"guys|all"}}],
    ]

    # Duplicate the patterns, one for the question and one for the non-question.
    # The question pattern have an auxiliar at the beginning, while the non-question pattern have an auxiliar/verb at the end.
    affermativeList = []
    interrogativeList = []
    non_question_verbs_pattern = {"POS": {"IN": ["AUX", "VERB"]}}
    question_verbs_pattern = {"POS": {"IN": ["AUX", "VERB", "PART"]}}

    for i in subject_patterns:
        affermative = i.copy()
        interrogative = i.copy()
        
        affermative.append(non_question_verbs_pattern)
        interrogative.insert(0, question_verbs_pattern)

        
        affermativeList.append(affermative)
        interrogativeList.append(interrogative)

    # If it's a question, use the question patterns, otherwise use the non-question patterns.
    subject_patterns = interrogativeList if isQuestion else affermativeList

    # Get the matches
    matcher = Matcher(nlp.vocab)
    matcher.add("PROPN_MATCH", subject_patterns, greedy="FIRST")
    matches = matcher(clause)

    # If there is no match = no subject found => return None
    if len(matches) == 0:
        return None 

    # Sort the matches by their index position
    matches.sort(key=lambda x: x[1])

    # Get the first match
    output =  matches[0]

    if isQuestion:
        # Remove auxiliar before subject
        output = clause[output[1]+1:output[2]]
    else:
        # remove verb/aux after subject
        output = clause[output[1]:output[2]-1]
        
    return output

"""
# def split_nouns_and_adjectives(doc, sentence):
#     if sentence is None:
#         return {}

#     noun_adj_pairs = {}
#     for chunk in sentence.noun_chunks:
#         adj = []
#         noun = ""
#         for tok in chunk:
#             if tok.dep_ in SUBJECTS_DEP_ :
#                 noun = tok.text
#             if tok.pos_ == "ADJ" or tok.pos_ == "CCONJ":
#                 adj.append(tok.text)
#         if noun:
#             noun_adj_pairs.update({noun:" ".join(adj)})
#     return noun_adj_pairs
"""

"""
# def get_subject_phrase(doc, sentence):
#     output = list()
#     for token in sentence:
#         if (token.dep_ in SUBJECTS_DEP_):
#             isPersonalPron = token.pos == "PRON" and token.dep == "nsubj"
#             isPossesivePron = token.pos == "PRON" and token.dep == "poss"
#             isDet = token.pos == "DET" and token.dep == "det"
#             if (isPersonalPron):
#                 output.append(token)
#                 break
#             subtree = list(token.subtree)
            
#             subtree = [i for i in subtree if i.dep_ in SUBJECTS_DEP_ or i.orth_ == "and" or isPersonalPron or isPossesivePron or isDet]
            
#             start = subtree[0].i
#             end = subtree[-1].i + 1
#             output.extend(doc[start:end])
#             if(len(subtree)==1):
#                 break
#     return output
"""

def get_verb_phrase(nlp, doc, clause):
    """Get the verb list of the clause, where for verb I mean a consecutive sequence of auxliar, modals, negation, verbs, interrogative words (what/why), to preposition of infinite verb.

    Args:
        nlp (Spacy model): The Spacy model loaded.
        doc (Spacy document): The Spacy document to be analyzed
        clause (Spacy Span): The clause from which to extract the verb.

    Returns:
        List of Spacy span: The list containing the verbs. The eventually auxiliar verbs is at the beginning.
    """    
    generic_verb_min_one = {"POS":{"IN":["AUX","PART","VERB", "ADP", "ADV"]},"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "RB", "MD", "TO"]}, "OP":"+"}
    generic_verb_optional = {"POS":{"IN":["AUX","PART","VERB", "ADP", "ADV"]},"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "RB", "MD", "TO"]}, "OP":"*"}
    verb_patterns = [
        [generic_verb_min_one],
        #######
        [generic_verb_min_one,
        {"POS":"ADP","DEP":"prep"}, # singular preposition
        generic_verb_min_one],
        # ... verb1 what/how to verb2 ...
        [generic_verb_min_one, 
        {"LOWER": {"REGEX":"(what|how)"}},
        generic_verb_min_one],
        # ... VERB(non-aux) (what/how)? you aux/verb...
        [generic_verb_optional,
        {"POS":{"IN":["VERB", "ADP"]},"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "RB", "MD", "TO"]}, "OP":"+"}, # end with a main verb before the what/how
        {"LOWER": {"REGEX":"(what|how)"}, "OP":"?"},
        {"POS":{"IN":["PRON", "PROPN"]}},
        generic_verb_min_one],
    ]
    # Get the matches
    matcher = Matcher(nlp.vocab)
    matcher.add("VERB_MATCH", verb_patterns, greedy="LONGEST")
    matches = matcher(clause)
    # If there is no match = no verb found => return None
    if len(matches) == 0:
        return []

    # Sort the matches by their index position
    matches.sort(key=lambda x: x[1])
    
    # Append the span into the output list
    output=list()
    for match in matches:
        output.append(clause[match[1]:match[2]])
    return output

def get_adjectives(doc, clause):
    output = {}
    # For each token in the clause
    for token in clause:
        # We care only about adjectives linked to something which is not theirselves (it might happen with non grammatically correct sentences and this will bring to a loop)
       if (token.pos_ == "ADJ" and token != token.head):
            tmp = token
            # The head of the adjective is the noun or the verb, but if we have multiple adjectives linked to the same noun or verb,
            # e.g. I'm happy and excited --> the 2nd adjective will be the head of the 1st and the head of the 1st will be 'm,
            # so we want to iterate until we reach a noun or a verb
            while(tmp.head.pos_ == "ADJ"):
                print(token, "ADJ", tmp,"HEAD", tmp.head)
                tmp = tmp.head

            # If the key is not present, add an empty list as value and store the token inside it.
            # Othwerwise, append the token to the list associated to the key.
            output.setdefault(tmp.head,[]).append(token)
    return output


def get_object_phrase(doc, clause):
    """Get the list of object spans of the clause, where for object I mean a preposition linked to a verb or the object of a verb.

    Args:
        doc (Spacy document): The Spacy document to be analyzed
        clause (Spacy Span): The clause from which to extract the verb.

    Returns:
        list of span: a list containing the object spans.
    """
    verb_found = False
    output = list()
    token_already_inserted = list()

    # For each token in the clause
    for token in clause:
        # We want firstly to find the verb (because the object is always after the verb)
        if (token.pos_ in ["AUX", "VERB"]):
            verb_found = True
            continue

        if verb_found and token.dep_ in ["prep","dobj", "pobj", "attr", "dative"]:

            subtree = list(token.subtree)
            # print("TOKEN", token, "SUBTREE OBJ TOKEN" , subtree)

            # Get the span of the subtree
            start = subtree[0].i
            end = subtree[-1].i + 1
            # For each token in this span
            for tok in doc[start:end]:
                # If we found a verb, we want to stop the search and change the end index to the index of the verb token so that we can get its previous
                # This is useful for things like the preposition "about VERB PREP NOUN" --> We want to obtain about now and "prep noun" in the future
                if tok.pos_ in ["AUX", "VERB"]:
                    end = tok.i
                    break
            # Create the new span
            new_item = doc[start:end]

            # We don't want to add token that are already in the output list, things that happens with the attribute subtree
            foundAlreadyInsertedToken = False
            for token in new_item:                
                if token in token_already_inserted:
                    foundAlreadyInsertedToken=True
                    break

            if foundAlreadyInsertedToken:
                continue

            # Add the new span to the output list and update the token_already_inserted list
            token_already_inserted.extend(new_item)
            output.append(new_item)

    return output

def print_all(doc):
    """Print info about the tokens of a document

    Args:
        doc (Spacy document): the Spacy document whose information are printed
    """
    for token in doc:
        # if token.pos_ in ["VERB", "AUX","PART"]:
        print('Tok : ' , token, '| Dep_ : ', token.dep_, '| Pos_ : ', token.pos_, '| morph : ', token.morph, ' | morph_number ', token.morph.get('Number'), ' | tag_ : ', token.tag_, '| lemma: ', token.lemma_)


def get_clauses(nlp, doc, sentence):
    """Get a list of clauses from a sentence splitting it in two parts when we find a special splitting token

    Args:
        nlp (_type_): the Spacy model to use for the matcher
        doc (Spacy document): The Spacy document to be analyzed
        sentence (Spacy Span): The sentence from which we want to seek the clauses.

    Returns:
        _type_: _description_
    """
    splitting_adverb_patterns = [
        # Since/Because/...
        # Tok :  because | Dep_ :  mark | Pos_ :  SCONJ | morph :   | tag_ :  IN
        [{"POS":"SCONJ", "TAG":"IN"}],
        # Then/After/... 
        # Tok :  then | Dep_ :  advmod | Pos_ :  ADV | morph :  PronType=Dem | tag_ :  RB
        # Tok :  so | Dep_ :  advmod | Pos_ :  ADV | morph :   | tag_ :  RB
        # Tok :  away | Dep_ :  advmod | Pos_ :  ADV | morph :   | tag_ :  RB
        [{"POS":"ADV", "DEP":"advmod", "lower":{"IN":["then","after"]}}],
        ##
    ]

    conj_patterns = [
        [{"POS":{"IN":["PRON", "PROPN"]}}, #first subject
        {"POS":{"IN":["AUX","VERB"]}}, #first verb
        {"OP":"*"}, # anything
        {"TAG":"CC"}, # conjunction
        {"POS":"ADV", "DEP":"advmod", "OP":"?"}, #optional adv
        {"POS":"PRON"},  #pronoun
        {"POS":{"IN":["AUX","VERB"]}}], # verb
        ## 
    ]

    # Add the first pattern and get the matches
    matcher = Matcher(nlp.vocab)
    matcher.add("CLAUSES_MATCH", splitting_adverb_patterns, greedy="FIRST")
    matches = matcher(sentence)

    # Remove the first pattern, add the second and get the new matches.
    matcher.remove("CLAUSES_MATCH")
    matcher.add("CONJ_MATCH", conj_patterns, greedy="FIRST")
    conjunction_matches = matcher(sentence)

    # From the new matches, get only the conjunctions
    # For each match in the conjunction matches
    for idx, start, end in conjunction_matches:
        # For each token on the span of the match
        for idx_s, token in enumerate(sentence[start:end]):
            # After we find the conjunction
            if token.tag_ == "CC":
                start2 = idx_s+start
                end2 = start2 + 1
                # e.g. and then
                if doc[token.i+1].dep_ == "advmod":
                    end2 += 1
                    matches = [(idx, start, end) for (idx, start, end) in matches if start != token.i+1]
                break
        # Creates the span for the conjunction
        new_span = (idx, start2, end2)
        # Append the new span to the first group of matches
        matches.append(new_span)

    # If no matches found, return a vector containing the original sentence
    if len(matches) == 0:
        return [sentence] 

    # Sort the matches by start index
    matches.sort(key=lambda x: x[1])
    
    output_clauses = list()
    last_end2 = -1
    # Split the sentence in chunks for each match,
    # and return the list of sentence chunks
    for j, (match_id, start, end) in enumerate(matches):
        start2 = start + sentence[0].i
        end2 = end + sentence[0].i

        # If it's the first match
        if j==0:

            # If the match is at the beginning of the sentence, skip
            if sentence[0].i==start2:
                continue
            # Chunk = the sentence from the beginning of the sentence to the token before the first match
            output_clauses.append(doc[sentence[0].i : start2 ])
        else:
            # Chunk = token after the last match to the token before the current match
            output_clauses.append(doc[last_end2:start2])
        last_end2=end2
    
    # Chunk = the token after the last match to the end of the sentence
    last_match = matches[-1]
    start, end = last_match[1], last_match[2]
    start2 = start + sentence[0].i
    end2 = end + sentence[0].i
    output_clauses.append(doc[ start2+1 : sentence[-1].i+1])

    # Return the chunks
    return output_clauses

#############################

def get_analyzed_clause(nlp, doc, clause, isQuestion):
    """Analyze a clause and return a tuple containing subject,verbs,adjectives,objects and (again) the flag if it's a question.

    Args:
        nlp (Spacy model): the spacy model used to create the document
        doc (Spacy document): The Spacy document from which we extracted the clause
        clause (Spacy Span): The clause to analyze.
        isQuestion (bool): the flag if the clause is a question.

    Returns:
        tuple(list of tokens, list of span, dictionary{token:span}, boolean): return the subject, verbs, adjectives, objects and the input flag isQuestion.
    """    
    subj = get_full_subject(nlp, doc, clause, isQuestion)
    verb = get_verb_phrase(nlp, doc, clause)
    adjs = get_adjectives(doc, clause)
    obj = get_object_phrase(doc, clause)
    print((subj, verb, adjs, obj, isQuestion))

    ### REMOVE ADJECTIVES from SUBJECT AND TRANSFORM THE SPAN INTO A LIST OF TOKENS
    if subj is not None:
        list_new_subj = []
        subject_text_without_adjectives = [key for key in adjs if key in subj]
        for key in subject_text_without_adjectives:
            key = subject_text_without_adjectives[0]
            value = adjs[key]
            first = value[0].i
            last = value[-1].i
            r = range(first,last+1)
            list_new_subj.extend(r)
        subj = [token for token in subj if token.i not in list_new_subj]
    ###

    ### REMOVE PREPOSITIONS FOUND IN THE VERBS FROM THE OBJECTS
    for obj_item in obj:
        if len(obj_item)==1:
            for verb_item in verb:
                for token in verb_item:
                    if token.dep_ == "prep":
                        obj.remove(obj_item)
    ###
    return (subj, verb, adjs, obj, isQuestion)


def get_interrogative_auxiliar_from_verb(isThirdPerson, verb):
    """Generate the interrogative auxiliar adapted to the given verb 

    Args:
        isThirdPerson (bool): If the subject is third person or not
        verb (Spacy token): The token verb to analyze 

    Returns:
        string: the auxiliar verb to use in the interrogative sentence
    """
    # non-3rd person singular present verb
    if verb.tag_ == "VBP":
        return "do"
    # 3rd person singular present verb
    elif verb.tag_ == "VBZ":
        return "does"
    # past tense verb
    elif verb.tag_ == "VBD":
        return "did"
    # past participle verb
    elif verb.tag_ == "VBN":
        if isThirdPerson:
            return "has"
        else:
            return "have"

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_lg")
    txt = ("My smart, incredible and brilliant friends and she went to the mall, then we went to the magnificent grocery store."
            + " Bob, Mario and Jessie went to the U.S.A. I couldn't believe it"
            +" I'm startving!"
            +" Would I eat a bear?"
            +" Mr. Robinson went to the store yesterday."
            +" How's your day?"
            +" I was thinking about going to the mall with my friends."
            +" Mr. Robinson sent me at home yesterday."
            +" Do you mind?"
            +" I was thinking about going to the mall with my friends, but suddenly I changed my mind."
            +" Bob and I are so mad!"
            +" I'm crashing... I feel so tired."
            +" The pink, beautiful, and small flowers are blown away."
            +" I got a red candy and an interesting book."
            +" This will be interesting."
            +" I'm mad, thirsty and tired."
            + " Yestarday, during the day, I went to the mall with my friends."
            + " Bob visited me and I helped him."
            + " Why weren't you at my house yesterday?"
            + " I'm not lying."
            + " I would never do that!"
            + " The ladies were happy."
            + " The ladies were happy because they reached the wonderful mall."
            + " Yesterday I helped a nice and charismatic old woman."
            + " At the beginning I was sad, then I was happy."
            + " Carla drove to my office and collected my keys."
            + " She's so clever."
            + " She's got a new car."
            + " Were you listening to me or you were doing nothing?"
            + " Can't you swim?"
            + " I don't understand how to sleep in that position like you do."
            + " I don't think you can act like that."
            # + " Are you guys going to go to the pool tomorrow?"
            # + " Bob's so clever."
            # + " Bob's starving."
            # + " I don't think I can do that."
            + "I went at home yesteday."
            + " I'm Jacob."
            + " My name is Bob."
            + " I think you are fooling me."
            + " Did you know a cat cannot climb a tree?"
            + " It's nice to meet you. I wanted to ask you something."
            + " my family is ok, i'm lucky."
            + " I'm sad. My friends ate my last sandwich."
            + " Because this feeling makes me feel better than other kind of feelings."
            + " I know. He knows. I knew. I have known. She has known."
            + "Bob visited me and we chatted about my problems."
            + " fine thanks, and you?"
            + " I've already told you that."
            + " Let's talk about music."
            + " Do you know what malloreddus means?"
            + " Today is a cloudy day."
            + " I don't understand how Bob could say something that cruel about me."
    )
    txt = preprocessing(nlp, txt)
    doc = nlp(txt)
    
    for sentence in doc.sents:
            print("******************************")
            isQuestion = sentence[-1].orth_ == "?"

            sentence_clauses = get_clauses(nlp, doc, sentence)
            # print(sentence_clauses)
            print(sentence)
            print_all(sentence)
            for i, clause in enumerate(sentence_clauses):
                print(f"Clause #{i}: " , clause)

                analysis = get_analyzed_clause(nlp, doc, clause, isQuestion and i == 0)
                print(analysis)


