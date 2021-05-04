def url_to_screenshot_name(s):
    return ''.join([i if i.isalpha() else '_' for i in s]) + '.png'
