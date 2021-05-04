#!/usr/bin/env python3
import os
import shutil


from wreckhelpers import url_to_screenshot_name


def generate_head(title):
    return '''
<head>
    <title>%s</title>
    <link rel="stylesheet" href="./res/style.css">
</head>''' % (title,)


def generate_page_report(url):
    return '''
<hr/>
<h3><a href="%s">%s</a></h3>
<img src="../screenshots/%s"/>
''' % (url, url, url_to_screenshot_name(url))


def generate_body(title, urls):
    return '''
<body>
    <h1>%s</h1>
    <h2>Targets:</h2>
    <ul>''' % (title,) +\
        '\n'.join(['<li><a href="%s">%s</a></li>' % (i, i,) for i in urls]) +\
        '''
    </ul>''' +\
        '\n'.join([generate_page_report(url) for url in urls]) +\
'''
</body>'''


def generate_html_report(title, output_dir, urls):
    os.mkdir(output_dir)
    
    html_report = '<html>' +\
        generate_head(title) +\
        generate_body(title, urls) +\
        '</html>'

    index_filename = os.path.join(output_dir, 'index.html')
    with open(index_filename, 'w+') as index:
        index.write(html_report)

    resources_dir = os.path.join(output_dir, 'res')

    os.mkdir(resources_dir)
    shutil.copyfile('./res/style.css', os.path.join(resources_dir, 'style.css'))
