# from email.policy import default # No idea what this is.
import spacy
import random
from nltk.chat.util import Chat
from NLTK_Chat_modified import Chat_with_emotion_rules
from responses import *
from sentence_analysis import get_analyzed_clause, get_clauses, preprocessing, get_interrogative_auxiliar_from_verb
from emotion_analyzer_classifier import MyEmotionAnalyzer
import re
import json
import time

NOT_MANANGEABLE_TEXT_LIST = ["Let's"]

class MyBot(Chat):
    def __init__(self):
        # The current object is for the advanced patterns
        super().__init__(complex_pairs, my_reflections)

        # Create a bot for generic patterns
        self._GENERIC_patterns_extractor = Chat_with_emotion_rules(simple_pairs, my_reflections)

        # Memory = (string: key, string: information, boolean: is_used)
        self._MEMORY = list()
        # The memory patterns are specified in anoter bot
        self._MEMORY_EXTRACTOR = Chat(memory_pairs, my_reflections)

        # Load the largest and accurate Spacy English model
        self._Spacy_model = spacy.load("en_core_web_lg")
        # # Add pipe and patterns for semi-modals not found by spacy model
        # ruler = self._Spacy_model.add_pipe("entity_ruler")
        # patterns = [
        #         {"id": "special_modal", "label":"be-going-to-verb", "pattern":[ {"LEMMA": "be"}, {"LOWER": "going"}, {"LOWER": "to", "TAG":"TO"}, {"POS":"VERB"}]},
        #         {"id": "special_modal", "label":"have-to-verb", "pattern":[ {"DEP": "ROOT", "POS": "VERB", "LEMMA": "have"}, {"LOWER": "to", "TAG":"TO"}, {"POS":"VERB"}]},
        #         ]
        # ruler.add_patterns(patterns)

        # Load the emotion analyzer
        self._emotion_analyzer = MyEmotionAnalyzer()

        # Load the list of moods
        """ EDIT: It's no longer used: check below for details
        self._MOODS = [self._Spacy_model(m) for m in string_moods]
        """

    """ EDIT: Not used
    def get_moods(self, SVA):
        moods_found = list()
        adjectives_dict = SVA[2]
        list_verbs = SVA[1]
        threshold = 0.53

        # TEST
        # a,b = self._NLP("cat"), self._NLP("dog")
        # print("SIMILARITY: ", a, "VS", b, ":  ", a.similarity(b))
        # a,b = self._NLP("mad"), self._NLP("tired")
        # print("SIMILARITY: ", a, "VS", b, ":  ", a.similarity(b))
        # a,b = self._NLP("happy"), self._NLP("tired")
        # print("SIMILARITY: ", a, "VS", b, ":  ", a.similarity(b))
        # a,b = self._NLP("sad"), self._NLP("tired")
        # print("SIMILARITY: ", a, "VS", b, ":  ", a.similarity(b))

        for mood in self._MOODS:
            for key, list_adjs_value in adjectives_dict.items():
                for adj in list_adjs_value:
                    print("SIMILARITY: ", "MOOD", mood, "ADJ ", adj, mood.similarity(adj))
                    if mood.similarity(adj) > threshold:
                        moods_found.append({key, mood})
                        break
            print(f"MOODS FOUND AFTER ADJECTIVE {mood}: ", moods_found)

            for verb in list_verbs:
                if mood.similarity(verb) > threshold:
                    moods_found.append({verb, mood})
                    break
            print(f"MOODS FOUND AFTER verbs {mood}: ", moods_found)
            print()

        return moods_found
    """

    def get_index_most_weighted(self, sentences):
        """ Returns the index of the sentence/clause with the highest weight

        Args:
            sentences (list of list of tokens | list of spans | iterator of spans): The list of sentences/clauses to be analyzed

        Returns:
            int : the highest weighted sentence/clause index
        """
        sentences_list = list(sentences)
        weights = list()
        for idx, sent in enumerate(sentences_list):
            # Check if the sentence ends with a punctuation mark
            isQuestion = sent[-1].lower == "?"
            isLargeEnough = len(sent) > 3

            # The weight of n-th sentence > the weight of the n-1th sentence > ... > the weight of the 1st sentence
            weight = 2*(idx+10)
            #  A question sentence is more important than a non-question sentence
            weight += 100 if isQuestion else 0
            #  A sentence with more than 3 words is far more important than a sentence with less than 3 words
            weight += 50 if isLargeEnough else 0
            weights.append((idx, weight))

        return max(weights, key=lambda x: x[1])[0]


    def find_info_to_save(self, doc, SVA):
        """ Finds the information to save in the memory (and stores them)

        Args:
            doc (Spacy document): The Spacy document to be analyzed
            SVA (tuple(Subject, Verb list, Adjective dictionary, Object list, boolean isQuestion), dict(Spacy token key, string value)): The analysis of the sentence/clause
        """
        # Save adjectives into memory
        adjectives_dict = SVA[2]
        subject = SVA[0]

        # If there is no subject, exit
        if subject is None:
            return


        for key, list_adjs_value in adjectives_dict.items():
            # We want only the adjectives linked to a noun
            isValidElement = key.pos_ not in ["VERB", "AUX"]
            if not isValidElement:
                continue

            # Check if an information about this nous is already in the memory,
            # if not, save it
            already_exists = key.lower_ in [item[0] for item in self._MEMORY]
            if already_exists:
                continue

            # Extract the information to save as string
            first = list_adjs_value[0].i
            last = list_adjs_value[-1].i
            adjectives_string = doc[first:last+1].text.lower()

            # Check for possesive pronouns or the article "the" to add in the string
            key_str = key.text.lower()
            for j, tok in enumerate(subject):
                if tok == key:
                    if subject[j-1].tag_ in ['DT','PRP$']:
                        key_str = subject[j-1].text.lower() + " " + key_str

            # Save the information in the memory
            self._MEMORY.append((key_str, adjectives_string, False))
            print("Added fragment " ,  (key_str, adjectives_string, False))

    def use_memory_frag(self):
        """Creates an answer to the user using a memory fragment if at least one is available.

        Args:
            doc (Spacy document): The Spacy document to be analyzed
            SVA (tuple(Subject, Verb list, Adjective dictionary, Object list, boolean isQuestion), dict(Spacy token key, string value)): The analysis of the sentence/clause

        Returns:
            string : the answer to the user if a memory fragment is available, otherwise an empty string
        """
        print("Trying to use a MEMORY Fragment")
        print("Current memory status", self._MEMORY)

        # Check if there is at least one memory fragment available
        idx , item = next(((i,v) for i,v in enumerate([item for item in self._MEMORY]) if v[2] == False), (-1, None))
        if idx == -1:
            return ""

        # Set the frag as used
        print("I'M USING ", item)
        self._MEMORY[idx]= (item[0], item[1], True)
        print("New memory status", self._MEMORY)

        # Create the pattern information as:
        # {SYS_MEMORY_KEY} (.*) {SYS_MEMORY_VALUE} (.*)
        pattern = f"{SYM_MEMORY_KEY} {item[0]} {SYM_MEMORY_VALUE} {item[1]}"
        print("pattern for the memory extractor: ", pattern)
        memory_frag_extracted = self._MEMORY_EXTRACTOR.respond(pattern)
        print("ANSWER OF THE MEMORY EXTRACTOR, ", memory_frag_extracted)

        return memory_frag_extracted

    def create_input_advanced_chatbot(self, doc, SVA):
        """ Create the input for the specific patterns from the SVA analysis of the clause

        Args:
            doc (Spacy document): The Spacy document to be analyzed
            SVA (tuple(Subject, Verb list, Adjective dictionary, Object list, boolean isQuestion), dict(Spacy token key, string value)): The analysis of the sentence/clause

        Returns:
            string: the input for the specific patterns from the SVA analysis of the clause
                if there are at least one adjective (linked to the verb) or one object.
                Otherwise, it returns an empty string.
        """
        print("SVA analysis of the clase: ", SVA)

        # Check if there is at least one verb.
        verb_list = SVA[1]
        if len(verb_list) == 0:
            return ""

        subject = SVA[0]
        verb = verb_list[-1] # pick last span verb in list
        adjs = SVA[2]
        obj = SVA[3]
        isQuestion = SVA[4]
        
        # The subject is necessary for the pattern
        if subject is None:
            return ""

        # If no object or adjectives associated to a verb are found,
        # return an empty string
        if obj == [] \
        and (adjs == {} or len([k for k in adjs if k in verb])==0):
            return ""

        ### SUBJECT SECTION ###
        # Convert the subject into a pronoun string if it's possible
        nouns = [tok for tok in subject if tok.pos_ == "NOUN"]
        prons = [tok for tok in subject if tok.pos_ == "PRON" and tok.tag_ in ["NN","NNS", "PRP", "DT"]]
        propns = [tok for tok in subject if tok.pos_ == "PROPN" and tok.dep_ == "nsubj"]

        pron_dict = {'i':False, 'you':False, 'he':False, 'she':False, 'it':False, 'we':False, 'they':False,
                    'this':False, 'that':False, 'these':False, 'those':False}
        # If there is a pronoun, set it's presence in the dictionary to True
        if len(prons) > 0:
            for pron in prons:
                if pron.lower_ in pron_dict:
                    pron_dict[pron.lower_] = True
        # A noun can be singular or plural: Book = singular, Books = plural
        # A pronoun can be singular or plural: I... = singular, we... = plural
        atLeastOnePlural = any(["Plur" in noun.morph.get('Number') for noun in nouns]) or any(["Plur" in pron.morph.get('Number') for pron in prons])

        # If the subject is plural
        isThirdPerson = False
        if (len(nouns) + len(prons) + len(propns)) >= 2 or atLeastOnePlural:
            # We/My friend and I/Bob, you and I --> we
            if pron_dict['we'] or pron_dict['i']:
                subject = "we"
            # You/My friends and you/she and you --> you
            elif pron_dict['you']:
                subject = "you"
            # He/My friend and he/Bob and He --> he
            else:
                subject = "they"
                # if len(prons) > 0:
                #     subject = [key for key, value in pron_dict.items() if value == True][0]
                # else:
                #     subject = "they"
        # else, the subject is singular (1 noun or 1 pronoun or 1 proper noun)
        else:
            isThirdPerson = True
            # I/you/she/he/it
            if len(prons) > 0:
                subject_pronouns_used = [key for key, value in pron_dict.items() if value == True]
                subject = prons[0].lower_ if subject_pronouns_used == [] else subject_pronouns_used[0]
                subject = 'I' if subject == 'i' else subject
            else:
                # NOUNS: Children, Book, Cat, ...
                if len(nouns) > 0:
                    # There's only one noun, so it's the first
                    idx = subject.index(nouns[0])
                    # If there is The or My/.../Your/.../His/.../Her/.../Their/...
                    # add it.
                    if idx>0 and subject[idx-1].tag_ in ['DT','PRP$']:
                        subject = subject[idx-1].text + " " + nouns[0].text
                    # otherwise it's only the nouns
                    else:
                        subject = nouns[0].text
                # PROPNS: Mr. Robinson
                else:
                    # If it's neither a pronouns nor a noun, it's a proper noun
                    subject = propns[0].text
                    idx = propns[0].i
                    # If there is Mr. or Mrs....
                    if idx-1>0 and doc[idx-1].dep in ['compound']:
                        subject = doc[idx-1].text + " " + subject
        # print("SUBJECT: ", subject)

        ### VERB SECTION ###
        auxes, originalConjugatedVerb, reflectedOriginalVerb, verbToSearch = None, None, None, ""
        reflectedAuxiliarQuestion, reflectedVerbQuestion = None, None
        # Search how many verbs are in the sentence: don't know how to make --> [know, make] 
        mainVerbsList = [(tok, i) for i, tok in enumerate(verb) if tok.pos_ in ["VERB"]]
        ######################
        # If there are no main verbs, 'be' was used as main verb (Where were you? | I'm happy)
        onlyAuxiliar = len(mainVerbsList) == 0
        if onlyAuxiliar:
            # List of tuple (verb, index). Actually it's a list of tuples with only one element
            mainVerbsList = [(tok, i) for i, tok in enumerate(verb) if tok.dep_ in ["ROOT"]]
            if len(mainVerbsList) == 0: # Cannot be empty
                return ""
            firstMainVerb = mainVerbsList[0][0] # Take the verb of the first tuple
            verbToSearch = firstMainVerb.lemma_ # We want to search the lemma of the verb

            if isQuestion:
                interrogative_auxiliar = (SVA[1])[0]
                # In a question the negative part is in the auxiliar before the subject
                hasNegation = len(interrogative_auxiliar)>1 and (interrogative_auxiliar[1].dep_ == "neg")
            else:
                # In a non-question the negative part is in the auxiliar after the subject
                hasNegation = len(verb)>1 and verb[1].dep_ == "neg"

            if hasNegation:
                verbToSearch = SYM_INPUT_NEG + ' ' + verbToSearch
            originalConjugatedVerb = [verb]
            originalConjugatedVerb = ' '.join([tok.text for tok in originalConjugatedVerb])           
            
        # Otherwise, there is at least one main (not be/have) verb
        else:
            # If it's a question, the negative part is in the auxiliar before the subject
            if isQuestion:
                interrogative_auxiliar = (SVA[1])[0]
                print("interrogative_auxiliar: ", interrogative_auxiliar)
                hasNegation = len(interrogative_auxiliar)>1 and interrogative_auxiliar[1].dep_ == "neg"
            # If it's not a question, the negative part is in the auxiliar after the subject
            else:
                hasNegation = len(verb)>1 and verb[1].dep_ == "neg"

            firstMainTuple = mainVerbsList[0] # (UNDERSTAND, IDX)
            ##### CASE COMPLEX VERB: I don't know how you can do that --> main verbs = [know, do]
            if len(mainVerbsList) >= 1: # |[UNDERSTAND, DO]| = 2 > 1
                firstMainVerb = firstMainTuple[0] # UNDERSTAND
                originalConjugatedVerb = verb[firstMainTuple[1]:] # VERB[IDX:]
                auxes = verb[:firstMainTuple[1]] # VERB[:IDX]
                post_verb_str = str(originalConjugatedVerb[1:])
                verbToSearch = firstMainVerb.lemma_ + ' ' + post_verb_str if post_verb_str != '' else firstMainVerb.lemma_
            ##### CASE SIMPLE VERB I don't know that
            else:
                firstMainVerb = verb[-1] # know
                auxes = verb[:-1] # don't
                verbToSearch = firstMainVerb.lemma_
            
            #### Add negation placeholder to the verb to search ###
            if hasNegation:
                verbToSearch = SYM_INPUT_NEG + ' ' + verbToSearch

            originalConjugatedVerb = [auxes] + [firstMainVerb]
            originalConjugatedVerb = ' '.join([tok.text for tok in originalConjugatedVerb])
            if isQuestion:
                originalConjugatedVerb = interrogative_auxiliar.text.lower() + originalConjugatedVerb

        print("ORIGINAL VERB:"+ originalConjugatedVerb)

        # Reflect the original verb: aren't --> am not
        if subject.lower() in ["i","you"]:
            if originalConjugatedVerb.lower().startswith("'"):
                reflectedOriginalVerb = self._substitute(subject.lower() + originalConjugatedVerb)
            else:
                reflectedOriginalVerb = self._substitute(subject.lower() + ' ' + originalConjugatedVerb)

            reflectedOriginalVerb = reflectedOriginalVerb.split(' ', 1)[1]
        else:
            reflectedOriginalVerb = self._substitute(originalConjugatedVerb)

        # Question reflection
        if onlyAuxiliar:
            ### Set the interrogative reflection ###
            reflectedAuxiliarQuestion = reflectedOriginalVerb 
            reflectedVerbQuestion = "" 
        else:
            ### Set the interrogative reflection ###
            if isQuestion:
                reflectedAuxiliarQuestion = interrogative_auxiliar.text.lower() 
                reflectedVerbQuestion = firstMainVerb.lemma_ 
            else:
                if hasNegation:
                    reflectedAuxiliarQuestion = reflectedOriginalVerb.split(' ', 1)[0]
                    reflectedVerbQuestion = firstMainVerb.text.lower() 
                elif len(auxes) == 0:
                    reflectedAuxiliarQuestion = get_interrogative_auxiliar_from_verb(isThirdPerson, firstMainVerb) 
                    reflectedVerbQuestion = firstMainVerb.lemma_ 
                # I was thinking --> You were thinking
                else:
                    reflectedAuxiliarQuestion = reflectedOriginalVerb.split(' ', 1)[0]
                    reflectedVerbQuestion = firstMainVerb.text.lower() 

        ### ADJECTIVES (RELATED TO THE VERB) ###
        adjectives_string = ""
        for key, value in adjs.items():
            if key in verb:
                first = value[0].i
                last = value[-1].i
                adjectives_string = " " + doc[first:last+1].text
                break

        ### OBJECT ###
        # If I have at least one object
        if len(obj)>0:
            # Heuristic: the i-th verb is associated to the i-th object
            obj = obj[min(len(SVA[1]) ,len(obj))-1:]
            obj_text = []
            for span in obj:
                for tok in span:
                    # If token is already in verb span, don't add it
                    if tok in verb:
                        continue
                    # Convert the object list to a string changing the 'you' used as object with a custom string
                    # since it can cause confusion with the 'you' used as subject
                    if tok.pos_ == "PRON" and tok.text == "you":
                        obj_text.append(SYM_INPUT_YOU_OBJECT)
                    else:
                        obj_text.append(tok.text)
            obj = ' '.join(obj_text)

            # # Remove the adjectives related to the object
            # for key, value in adjs.items():
            #     first = value[0].i
            #     last = value[-1].i
            #     string_to_remove = doc[first:last+1].text
            #     obj = re.sub(rf"{string_to_remove}", '', obj)
            #     obj = re.sub(r'\s+', ' ', obj)

            obj = " " + obj

        # If there is no object, obj is an empty string
        else:
            obj = ""

        ## OUTPUT
        output = subject + ' ' + verbToSearch + adjectives_string + obj
        output = re.sub(r'\s+', ' ', output)

        # print("BOT INPUT ELABORDATED:" , output)
        return (output, {SYM_VERB: originalConjugatedVerb, SYM_VERB_REFLECTED: reflectedOriginalVerb, 
                         SYM_AUX_REFLECTED_QUESTION: reflectedAuxiliarQuestion, SYM_VERB_REFLECTED_QUESTION: reflectedVerbQuestion})

    def elaborate_response_advanced_bot(self, SVA, input_chatbot, output_chatbot):
        """Post-processing of the advanced bot response.

        Args:
            SVA (tuple(Subject, Verb list, Adjective dictionary, Object list, boolean isQuestion), dict(Spacy token key, string value)): The analysis of the sentence/clause
            input_chatbot (string): the input sent to the bot
            output_chatbot (string): the output produced by the bot

        Returns:
            string: the output without placeholders
        """
        if output_chatbot == "" or output_chatbot is None:
            return ""

        # VERB
        bot_output_modified = str(output_chatbot)
        for key, value in input_chatbot[1].items():
            string_to_remove = key
            string_to_restore = value
            bot_output_modified = re.sub(rf"{string_to_remove}", f'{string_to_restore}', bot_output_modified)

        # REMOVE SYS_INPUT_NEG
        bot_output_modified = re.sub(rf"{SYM_INPUT_NEG}", '', bot_output_modified)
        bot_output_modified = re.sub(r'\s+', ' ', bot_output_modified)
        bot_output_modified = re.sub(r'\s(\'(?:s|m|re|ve))', r'\1', bot_output_modified)

        return bot_output_modified

    def respond_with_simple_bot(self, input_chatbot):
        """Respond with the simple bot, that is the one which uses generic regex patterns.

        Args:
            input_chatbot (string): the input sent to the bot

        Returns:
            string: the output produced by the simple bot, None if nothing was matches
        """
        # Remove punctuation except ' (we want to preserve 'm/'d/...)
        input_chatbot_modified = re.sub(r"[^\w\s\d']",'',input_chatbot)
        print("BOT INPUT MODIFIED:" , input_chatbot_modified)
        
        # Get the emotion
        emotion = self._emotion_analyzer.get_emotion(input_chatbot_modified)
        print("I found the emotion: ["+ emotion+']')

        # Get the response
        output_chatbot = self._GENERIC_patterns_extractor.respond(input_chatbot_modified, emotion=emotion)
        
        # If the bot doesn't understand the input and the input was a question, return a random default answer
        if output_chatbot is None and input_chatbot[-1] == "?":
            default_answers = [
            "Why do you ask that?",
            "Please consider whether you can answer your own question.",
            "Perhaps the answer lies within yourself?",
            "Why don't you tell me?"]
            output_chatbot = random.choice(default_answers)
    
        return output_chatbot

    def respond(self, str_input):
        """ Creates a response for the user input.

        Args:
            str_input (string): the input from the user

        Returns:
            string: a non-empty response for the input
        """
        output_chatbot = ""
        str_input = preprocessing(self._Spacy_model, str_input) # Pre-processing
        doc = self._Spacy_model(str_input)  # Create the doc object
        sentences = list(doc.sents) # doc.sents is an iterable, so I need to convert it into a list

        # Get the index of the most important sentence
        idx_chosen_sentence = self.get_index_most_weighted(sentences)
        
        # If the sentence chosen is too short, use the simple bot with classic regex
        if len(sentences[idx_chosen_sentence]) <= 3 \
            or any(x.lower() in sentences[idx_chosen_sentence].text.lower() for x in NOT_MANANGEABLE_TEXT_LIST):

            print("(< 4w or not allowed) SIMPLE BOT INPUT: ", sentences[idx_chosen_sentence])
            # output_chatbot = self._GENERIC_patterns_extractor.respond(sentences[idx_chosen_sentence].text)
            output_chatbot = self.respond_with_simple_bot(sentences[idx_chosen_sentence].text)

        # Otherwise, try to use the advanced bot
        else:
            # For each sentence
            for idx_sent, sent in enumerate(sentences):
                # Split it into clauses
                clauses = get_clauses(self._Spacy_model, doc, sent)
                isQuestion = sent[-1].orth_ == "?"
                # Get the index of the most important clause if it's the most important sentence, -1 otherwise
                idx_chosen_clause = self.get_index_most_weighted(clauses) if (idx_sent == idx_chosen_sentence) else -1

                # For each clause
                for idx_clause, clause in enumerate(clauses):
                    print(f"SENTENCE #{idx_sent} - CLAUSE #{idx_clause}: ", clause)

                    # Get the analysis of the clause
                    SVA = get_analyzed_clause(self._Spacy_model, doc, clause, isQuestion and idx_clause == 0 )

                    # moods = self.get_moods(SVA) # Moods not able to be implemented

                    # Check if there are info to save, if yes store them into the memory
                    self.find_info_to_save(doc, SVA) # memory = [tuple(key, info, already_used?)]
                    
                    # If it's the most important clause, elaborate the input for the advanced bot
                    if idx_chosen_clause == idx_clause:
                        input_chatbot = self.create_input_advanced_chatbot(doc, SVA)


            print("INPUT CHATBOT: ", input_chatbot)
            # Choose the final input for the bot
            """ EDIT: TRYING TO GET MOOD INFORMATION IS EITHER COMPLICATED OR SLOW
            mood_response = ""
            if len(moods) > 0:
                # Choose if to REPLACE the final answer using a mood status or to simply ADD information
                mood_mode = random.choice(["_REP", "_ADD"])
                chosen_mood = random.choice(moods)
                mood_response = super().respond(chosen_mood + mood_mode)
                if mood_mode == "_REP":
                    return mood_response
            """
            # If the input is not empty, use the advanced bot, otherwise use the simple bot
            if input_chatbot != "":
                print("COMPLEX BOT INPUT: ", input_chatbot[0])
                # Try to get a response from the advanced bot and remove the placeholders
                output_chatbot = super().respond(input_chatbot[0])
                output_chatbot = self.elaborate_response_advanced_bot(SVA, input_chatbot, output_chatbot)

            # If the advanced bot did not return anything, use the simple bot
            if output_chatbot == "" or output_chatbot is None:
                print("SIMPLE BOT INPUT: ", sentences[idx_chosen_sentence].text)
                # output_chatbot = self._GENERIC_patterns_extractor.respond(sentences[idx_chosen_sentence].text)
                output_chatbot = self.respond_with_simple_bot(sentences[idx_chosen_sentence].text)

        ##
        # If the advanced or simple bot did not return anything, use the simple bot
        if output_chatbot is None or output_chatbot == "":
            print("TRYING TO USE A FRAG")
            output_chatbot = self.use_memory_frag()
            if output_chatbot == "":
                print("USING FRAG FAILED, DEFAULT ANSWER INSTEAD")
                # output_chatbot = self._GENERIC_patterns_extractor.respond(SYM_NONE)
                output_chatbot = self.respond_with_simple_bot(SYM_NONE)

        return output_chatbot

if __name__ == "__main__":
    _EXTERNAL_CHATBOT = MyBot()
    text = (""
        # "My smart, incredible and brilliant friends and she went to the mall, then we went to the magnificent grocery store."
            # +  " Bob, Mario and Jessie are going to the USA."
            # +" Bob is starving!"
            # +" Would you eat a bear?"
            # +" Mr. Robinson didn't go to the store yesterday."
            # +" How's your day?"
            # +" I was thinking about going to the mall with my friends."
            # +" Mr. Robinson sent me at home yesterday."
            # +" Do you mind?"
            # +" I was thinking about going to the mall with my friends, but suddenly I changed my mind."
            # +" Bob and I are so mad! I would crash that asshole!"
            # +" I'm crashing... I feel so tired."
            # +" The pink, beautiful, and small flowers and I are blown away."
            # +" I got a red candy and a lovely book."
            # +" This will be interesting."
            # + " I don't understand how you should love that place."
            # +" I'm mad, thirsty and tired."
            # + " Yestarday, during the day, I went to the mall with my friends."
            # + " Bob visited me and I didn't help him."
            # + " I was at your house yesterday"
            # + " I went at home yesterday."
            # + " Are you happy?"
        #     + " I'm not lying to you."
            # + " I would never do that!"
            # + " The ladies were happy."
            # + " The ladies were happy because they reached the wonderful mall."
            # + " Yesterday I helped a nice and charismatic old woman."
            # + " At the beginning I was sad, then I was happy."
            # + " Carla drove to the vet's office and retrieved her cat."
            # + " Are you clever?"
            # + " She's got a new car."
            # + " Were you listening to me?"
            # + " Can't you swim?"
            # + " I understand how you can sleep in that position."
            # + " Won't Bob go to the pool tomorrow?"
            # + " Doesn't Bob go to the pool tomorrow?"
            # + "Nodoby can understand me."
            # + "you hate me."
            # + "Do you remember the old John?"
            # + "Does she think about you?"
            # + "Bob visited me and we chatted about my nightmare."
            # + " Hello, I'm a human. Fine thanks, and you?"
            # + " Well, I had a bad day."
            # + " Did you have a bad day? I'm sorry to hear that."
            # + " It depends. You?"
            # + " I've already told you that."
            # + " This is not your business."
            # + " You are asking too personal questions."
            # + " We are not friends."
            # + " Because we aren't."
            # + " Today is a cloudy day."
            # + " It might rain soon."
            # + " Because I'm wrong."
            # + " I don't talk about that."
            # + " Can you change the question please?"
            # + " Let's talk about music."
            # + " I'm feeling good."
            # " I don't want to talk about that. Sorry."
            # + " Do you play chess?"
            # " No, I don't think so."
            # " I was thinking about going to the gym."
            # + " I couldn't understand how you can sleep in that position."
            # + " Yesteday I felt so happy after I picked up my new car, but then I felt so sad because I was forced to leave it at home."
            # + "You surprise me."
            + " You're wonderful."

    )
    hard_coded_case = False
    if hard_coded_case:
        response = _EXTERNAL_CHATBOT.respond(text.strip())
        print("bot:", response)
        exit()
    else:
        print("Hi I'm Eliza. What's up?")
        JSON = {"conversation": []}
        while True:
            try:
                user_input = input(">")
                response = _EXTERNAL_CHATBOT.respond(user_input.strip())
                print("bot:", response)
                print("")
                JSON["conversation"].append({"user": user_input, "bot": response})
            except(KeyboardInterrupt, SystemExit):
                print("goodbye!")
                break

        JSON["N_rounds"]=-1
        output_conversation_folder = "saved_conversations"
        with open(f'{output_conversation_folder}/MyBot_conversation{time.strftime("%Y%m%d-%H%M%S")}.json', 'w') as fp:
            json.dump(JSON, fp)