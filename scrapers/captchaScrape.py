from seleniumbase import SB

def getHTMLCaptcha(url: str) -> str:
    """
    Returns the page source (HTML) for soup to eat
    
    :return string: HTML behind the captcha
    """
    # use SB webdriver instance
    with SB(uc=True, test=True, locale="en") as sb:

        sb.activate_cdp_mode(url)       # in Chrome Devtools Protocol Mode
        sb.uc_gui_click_captcha()       # click captcha just in case
        sb.sleep(2)    
        html = sb.get_page_source()     # assign value

    return html
