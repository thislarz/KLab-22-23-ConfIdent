"""
Script to ensure the ConferenceCorpus database exits at the default location otherwise it is downloaded
"""
import corpus.eventcorpus
from datetime import datetime


def download_conferencecorpus():
    """
    Download the ConferenceCorpus database to the default location $HOME/.conferencecorpus/EventCorpus.db
    """
    print("Start downloading ConferenceCorpus database")
    start = datetime.now()
    corpus.eventcorpus.EventCorpus.download()
    end = datetime.now()
    print(f"Download took {end-start}")


if __name__ == '__main__':
    download_conferencecorpus()