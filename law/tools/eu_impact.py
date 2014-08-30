if __name__ == "__main__":
    ## setup the Django with public settings for using the database
    from main.tools import set_up
    set_up.set_up_django_environment('main.tools.settings_for_script')

    from law.models import Document
    # prints the relative number of laws that have no text
    import datetime
    date = datetime.date(1986, 1, 1)

    # 95, 97, 145, 150 are types that are not laws:
    # are summaries and technical sheets of the diary
    documents = Document.laws.filter(date__gt=date)

    total = documents.count()
    actual = documents.filter(text=None).count()

    print(actual*1./total*100)
