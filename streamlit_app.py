import streamlit as st
import random
from german_nouns.lookup import Nouns
import deepl

translator = deepl.Translator(st.secrets["apikey"])

st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

game = st.sidebar.radio("",["nothing","der, die, das?","text correction"],index=0)

if game == "nothing":
    st.markdown("Welcome! Please choose your activity in the sidebar.")

if game == "der, die, das?":
    #initial definitions
    nouns = Nouns()
    translateGender = {'m':'der','f':'die','n':'das'}
    known_endings = ["ei","anz","enz","heit","keit","ie","ik","ion","ität","schaft","ung","ur","in","ant","ent","ich","ling","ismus","ist","or","chen","lein","ment","um","ma"]
    
    #sidebar creation
    st.sidebar.markdown("Include words with regular endings?")
    mode = st.sidebar.selectbox('i.e. -ung, -keit, -chen, etc...',['No','Yes'])
    st.sidebar.markdown('Full list: '+', '.join(known_endings))

    #function that filters words with gender determined by ending
    def known_rule(nominativ):
        #known_endings = ["ei","anz","enz","heit","keit","ie","ik","ion","ität","schaft","ung","ur","in","ant","ent","ich","ling","er","ismus","ist","or","chen","lein","ment","um","ma"]
        endings = [nominativ[-2:],nominativ[-3:],nominativ[-4:]]
        rule_match = nominativ[-2:] in known_endings or nominativ[-3:] in known_endings or nominativ[-4:] in known_endings
        if rule_match or nominativ[-6:]=="schaft" or nominativ[0:2]=="ge":
            return True
        return False

    #play counter to reinitialize gender selectbox
    if 'plays' not in st.session_state:
        st.session_state.plays = 0
    
    #session state to persist randomly selected word until manually cleared
    if 'nounInt' not in st.session_state:
        st.session_state.nounInt = random.randint(1,len(nouns))
    nounEntries = nouns[st.session_state.nounInt-1]
    
    #tries variable counts how many times the for loop met a word that is not useful for the game
    tries = 0
    
    #a word may have more than one entry, so we loop over them
    for entry in nounEntries:
        nominativ = entry['lemma']
        #logs to console for debugging
        print(nominativ)
        print(st.session_state.nounInt)
        if known_rule(nominativ) and mode == 'No':
            print('known rule')
            tries += 1
            continue
        try:
            gender = entry['genus']
        except KeyError:
            print('no gender')
            tries += 1
            continue
        
        #translate word and generates correct link string to Wiktionary
        if 'translation' not in st.session_state:
            st.session_state.translation = translator.translate_text(nominativ, target_lang="EN-US").text
        link = "https://de.wiktionary.org/wiki/{}".format(nominativ.replace(' ','_'))
        
        #show word prompt
        if nominativ != st.session_state.translation:
            st.info('Your noun is [{0}]({1}), meaning \"{2}\"...'.format(nominativ,link,st.session_state.translation))
        else:
            st.info('Your noun is [{0}](https://de.wiktionary.org/wiki/{1})...'.format(nominativ,link))
        
        #show gender options and check if selected is correct
        option = st.radio('Select a gender',['Choose your answer','der','die','das'],key=st.session_state.plays)
        if translateGender[gender]==option:
            st.markdown('Correct! 🎉')
        elif option == 'Choose your answer':
            pass
        else:
            st.markdown('Sorry, the correct answer was {}.'.format(translateGender[gender]))
            
        #show a (centered) refresh button that reruns to choose a new random int
        col1, col2, col3= st.columns(3)
        with col1:
            pass
        with col3:
            pass
        with col2 :
            refresh = st.button('Give me a new word!')
        if refresh == len(nounEntries):
            del st.session_state["nounInt"]
            try:
                del st.session_state["translation"]
            except KeyError:
                pass
            st.session_state.plays += 1
            st.experimental_rerun()
    
    #if word is not useful, reruns to choose a new random int
    if tries >= len(nounEntries):
        del st.session_state["nounInt"]
        try:
            del st.session_state["translation"]
        except KeyError:
            pass
        st.experimental_rerun()
        
if game == "text correction":
    #st.title("Automatic text correction")
    languages = {'English (US)':'EN-US', 'Spanish':'ES', "Portuguese (Portugal)":'PT-PT'}
    selectedLang = st.selectbox('Select your native language',languages)
    langCode = languages[selectedLang]
    
    text = st.text_area("Enter your German text to be corrected", height=200)
    submit = st.button("Submit")
    
    if submit and text != "":
        st.info("Note: these corrections may mix articles (i.e. replace ihn/sie with es).")
        for sentence in text.split(". "):
            
            #recover original meaning intended by user (hopefully)
            to_src = translator.translate_text(sentence, target_lang=langCode).text
            
            #translate to gramatically correct German
            to_german = translator.translate_text(to_src, target_lang="DE").text
            
            st.markdown(f'>>{sentence}\n')
            if to_german == to_src:
                st.markdown('This means: ')
                st.markdown(f'>>{to_src}\n')
                st.markdown("This sentence could not be corrected.")
                st.markdown('---')
            if to_german != sentence and to_german != to_src:
                st.markdown('This should (probably) be: ')
                st.markdown(f'>>{to_german}\n')
                st.markdown('Which means: ')
                st.markdown(f'>>{to_src}\n')
                st.markdown('---')
            if to_german == sentence:
                st.markdown('This sentence was perfect!\n')
                st.markdown('---')