from __future__ import unicode_literals, print_function

import plac
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

# new entity label
LABEL = "ANIMAL"

# training data
TRAIN_DATA = [
    ("Hvordan du bedst passer på hesten i varmen", {"entities": [(27, 33, LABEL)]},),
    ("Bider de?", {"entities": []}),
    ("Jeg købte en fisk nede ved havnen", {"entities":[(13, 17, LABEL)]}),
    ("Må man ikke bruge træknet når man fanger fisk?", {"entities":[(41, 45, LABEL)]}),
    ("Niels fik en giraf i fødselsdagsgave", {"entities":[(13, 18, LABEL)]}),
    ("Fugle har det ikke godt af altid at være i bur", {"entities":[(0, 5, LABEL)]}),
    ("Børge havde en guldfisk i sit akvarie, men den døde", {"entities":[(15, 23, LABEL)]}),
#    ("Jeg købte en fisk nede ved havnen", {"entities":[(13, 17, LABEL)]}),
#    ("Jeg købte en fisk nede ved havnen", {"entities":[(13, 17, LABEL)]}),
#    ("Jeg købte en fisk nede ved havnen", {"entities":[(13, 17, LABEL)]}),
    ("Der findes lige over 1000 køer af racen Jysk Kvæg i Danmark", {"entities": [(40, 59, LABEL)]}),
    ("Heste er for høje og de er ligeglade med dine følelser", {"entities": [(0, 5, LABEL)]},),
    ("Heste lader som om de går op i dine følelser", {"entities": [(0, 5, LABEL)]}),
    ("De lader som om de går op i dine følelser, de heste",{"entities": [(46, 51, LABEL)]},),
    ("Skygge er også meget essentielt til heste på græs", {"entities": [(36, 41, LABEL)]}),
    ("Din hest har svedt rigtig meget", {"entities": [(4, 8, LABEL)]}),    
    ("heste?", {"entities": [(0, 5, LABEL)]}),
    ("Til gengæld har Frankrig meget god og dyrkbar jord", {"entities": [(16, 24, "LOC")]}),
    ("Herhjemme vil der fra åbningen komme fokus på A.P. Møller-Mærsk", {"entities": [(46,63, "ORG")]}),
    ("Opfølgeren til succesen Det gyldne bur, den mest læste bog i Sverige 2019" , {"entities": [(24,38, "MISC")]}),
    ("Ud over Djævelens lærling har Kenneth Bøgh Andersen også skrevet 5 andre bøger i samme serie" , {"entities": [(30,51, "PER")]}),
    ("Frank Jensen er Københavns overborgmester" , {"entities": [(0,12, "PER")]}),
    ("Den største nationalpark i Danmark, hedder Nationalpark Vadehavet" , {"entities": [(43,65, "LOC")]}), #område
    ("Aarhus er den største by i Region Midtjylland " , {"entities": [(0,6, "LOC")]}), #by
    ("Inden i Den Sorte Diamant kan man finde Det Kongelige Bibliotek" , {"entities": [(8,25, "LOC")]}), #bygning
    ("Som respons til Covid-19 har Aalborg Universitet set det nødvendigt at afholde hybridforelæsninger" , {"entities": [(29,48, "ORG")]}),
    ("Statens Serum Institut står for størstedelen af de danske coronastatistikker" , {"entities": [(0, 22, "ORG")]}),
    ("Guitaren er en meget populært instrument" , {"entities": [(0,8, "MISC")]}),
    ("Spejderhytten ligger på Fredrik Bajers Vej 7G", {"entities": [(24, 45, "LOC")]})
]



@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model="da_core_news_lg", new_model_name="da_core_news_and_animals", output_dir="C:/Users/skyri/Desktop/Software/Models", n_iter=30):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    random.seed(0)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    ner.add_label(LABEL)  # add new entity label to entity recognizer
    # Adding extraneous labels shouldn't mess anything up
    if model is None:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.resume_training()
    move_names = list(ner.move_names)
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    # only train NER
    with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
        # show warnings for misaligned entity spans once
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        sizes = compounding(1.0, 4.0, 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("Losses", losses)

    # test the trained model
    test_text = "Kan du lide heste?"
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta["name"] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        # Check the classes have loaded back consistently
        assert nlp2.get_pipe("ner").move_names == move_names
        doc2 = nlp2(test_text)
        for ent in doc2.ents:
            print(ent.label_, ent.text)


if __name__ == "__main__":
    plac.call(main)