Simple Streamlit app with different tasks to help study German.

der/die/das uses gambolputty's german-nouns library to help the user practice recognizing word genders. It uses the Deepl Python library to translate the word; this does not always work, and in that case the translation is skipped. It also hyperlinks to the word's Wiktionary page, from where the list was sourced.

Text correction uses the Deepl Python library to take a German text written by a user, translate it back into the user's native language, and then translate it again into German. The idea behind it is that the user's grammatical mistakes are caused by imposing their original language's grammar on the foreign language, so translating it into the user's language recovers the meaning, while translating it back into German leaves a gramatically correct result. This sometimes causes loss of gender in pronouns: ihn/sie and ihm/ihr may be replaced with es/ihm.