import argparse
from os.path import expanduser
home = expanduser("~")

def start_corpus_db_browser():
    """
    start sqlite browser with the ConferenceCorpus database
    """

    db_file = home+"/.conferencecorpus/EventCorpus.db"
    parser = argparse.ArgumentParser(
            prog='ConferenceCorpusDbWebBrowser',
            description='Web interface for the database of the ConferenceCorpus',
            add_help=True
    )
    parser.add_argument("-p", dest="port", help="Port the web server should use")
    args = parser.parse_args()
    commands = ["sqlite_web"]
    if args.port:
        commands.extend(["-p", args.port])
    import subprocess
    subprocess.run([*commands, db_file])


start_corpus_db_browser()
