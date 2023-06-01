# | tag: hide
import json
import subprocess
import os

def fast_html(ipynb_file, html_file):
    #make your ipynb file into html
    #if cell starts with '#| hide', hide its script content
    os.chdir("..")
    with open(ipynb_file, 'r') as f:
        r = json.load(f)
        for i in range(len(r['cells'])):
            if r['cells'][i]['cell_type'] == 'code':
                if len(r['cells'][i]['source']) and r['cells'][i]['source'][0].startswith('#| hide'):
                    r['cells'][i]['metadata'] = {'tags': ['hide']}
                else:
                    r['cells'][i]['metadata'] = {'tags': ['normal']}
        r['metadata']['celltoolbar'] = 'Tags'

    temp_ipynb = f'_temp_{ipynb_file}'
    temp_html = temp_ipynb.replace('.ipynb', '.html')
    with open(temp_ipynb, 'w') as f:
        f.write(json.dumps(r))

    subprocess.run(f'jupyter nbconvert --to html --no-input '
                   f'--TagRemovePreprocessor.remove_cell_tags="hidec" {temp_ipynb}',
        shell=True)

    os.rename(temp_html, html_file)

fast_html('research.ipynb', 'research_case.html')