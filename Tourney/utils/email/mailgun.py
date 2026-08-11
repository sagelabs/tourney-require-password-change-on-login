from Tourney.utils.email.providers.mailgun import MailgunEmailProvider


def sendmail(addr, text, subject):
    print(
        "Tourney.utils.email.mailgun.sendmail will raise an exception in a future minor release of Tourney and then be removed in Tourney v4.0"
    )
    return MailgunEmailProvider.sendmail(addr, text, subject)
