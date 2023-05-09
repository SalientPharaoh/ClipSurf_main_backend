def recognize(prompt):
    import spacy

    # Load a pre-trained model
    nlp = spacy.load('en_core_web_sm')

    # Define the text to analyze
    text = prompt

    # Process the text
    doc = nlp(text)

    # Extract the named entities
    entities = [entity.text for entity in doc.ents]

    return entities