from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import pyarabic.araby as araby
from tashaphyne.stemming import ArabicLightStemmer
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db       

app = FastAPI(
    title="Juzur API",
    description="""
    ## Welcome to the Juzur API!
    This API's goal is to help you making linguistic analysis of arabic texts.
    For now, the expected features are:
       -Tokenization ( dividing a text into words)
       -Normalization ( clearing the vocalisation :'tashkeel' : removing diacritics, punctuation, etc.)
       -Stemming ( reducing words to their root form)
    i might add more features in the future, i am open to any suggestions or contributions.
    Hope this API will be useful for you!
    

    ## Bienvenue sur l'API Juzur!
    Le but de cette API est de vous aider à faire l'analyse linguistique des textes arabes.
    Pour l'instant, les fonctionnalités attendues sont:
         -Tokenisation (découper un texte en mots individuels)
         -Nettoyage (suppression de la vocalisation : 'tashkeel' : suppression des diacritiques, de la ponctuation, etc.)
         -analyse morphologique (Extraction de la racine trilittère)
    je pourrai ajouter d'autres features à l'avenir, je suis ouvert à toutes suggestions ou contributions.
    En espérant que cette API vous sera utile!
    """,

    version="1.0.0",)

stemmer = ArabicLightStemmer()

class TextRequest(BaseModel):
    text: str   

@app.get("/")
def read_root():
    return {"status": "l'API est en ligne", "message": "l'API est fonctionnelle"}

@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connectée à PostgreSQL"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur BDD: {str(e)}")


@app.post("/analyze")
def analyze_text(payload: TextRequest):
    raw_text = payload.text                             # 1) Extraction : Texte brut du JSON
    clean_text = araby.strip_tashkeel(raw_text)         # 2) Nettoyage : Suppression des voyelles (Tashkeel)
    words = araby.tokenize(clean_text)                  # 3) Tokenisation : Découpage mot par mot en liste
    
    # 4) Analyse morphologique avec Tashaphyne
    analysis_results = []                               # Liste vide qui va stocker l'analyse de chaque mot
    
    for word in words:
        stemmer.light_stem(word)                        # Lance l'algorithme de découpage sur le mot courant
        
        analysis_results.append({
            "word": word,                               # Mot d'origine (nettoyé)
            "prefix": stemmer.get_prefix(),             # Préfixe détecté (ex: و, يت, ال)
            "stem": stemmer.get_stem(),                 # Radical / Cœur du mot
            "suffix": stemmer.get_suffix(),             # Suffixe détecté (ex: ون, ات, ها)
            "root": stemmer.get_root()                  # Racine supposée (ex: خرج)
        })
    
    # 5) Réponse JSON complète renvoyée au client
    return {
        "original_text": raw_text,       # Texte de départ intact
        "clean_text": clean_text,        # Texte sans voyelles
        "word_count": len(words),        # Nombre de mots
        "analysis": analysis_results     
    }
