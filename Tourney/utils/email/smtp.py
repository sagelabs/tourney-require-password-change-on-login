from Tourney.utils.email.providers.smtp import SMTPEmailProvider


def sendmail(addr, text, subject):
    print(
        "Tourney.utils.email.smtp.sendmail will raise an exception in a future minor release of Tourney and then be removed in Tourney v4.0"
    )
    return SMTPEmailProvider.sendmail(addr, text, subject)
