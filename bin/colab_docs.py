
# colab_docs.py - save new copies of docs notebooks with updated links to work with google colab (new notebooks saved in docs/colab directory)

usage = '  usage: python colab_docs.py'  # executed from the bin folder of repo

notebook_names = ["contents.ipynb",
                  "fast_demo.ipynb",
                  "overview.ipynb",
                  "state_objects.ipynb",
                  "gcode_controls.ipynb",
                  "plot_controls.ipynb",
                  "geometry_functions.ipynb",
                  "other_functions.ipynb",
                  "design_tips.ipynb",
                  "lab_geometry.ipynb",
                  "lab_five_axis_demo.ipynb"]

notebook_addresses = ["../docs/" + notebook_name for notebook_name in notebook_names]
notebook_colab_urls = [
    f'https://githubtocolab.com/FullControlXYZ/fullcontrol/blob/master/docs/colab/{notebook_name[0:-6]}_colab.ipynb' for notebook_name in notebook_names]

old_import = "import fullcontrol as fc"
new_import = "if 'google.colab' in str(get_ipython()):\\n  !pip install git+https://github.com/FullControlXYZ/fullcontrol\\n" + old_import

string_to_delete = 'links will work in vscode, jupyter lab, etc. - the notebooks can also be access [online](https://github.com/FullControlXYZ/fullcontrol/tree/master/docs) and run in google colab'

model_notebook_names = ["nonplanar_spacer.ipynb",
                        "nuts_and_bolts.ipynb"]
model_notebook_colab_urls = [
    f'https://githubtocolab.com/FullControlXYZ/fullcontrol/blob/master/models/colab/{model_notebook_name[0:-6]}_colab.ipynb' for model_notebook_name in model_notebook_names]


for notebook_address in notebook_addresses:
    content_string = open(notebook_address).read()
    # replace import statement with install+import statements:
    content_string = content_string.replace(old_import, new_import)
    # delete this line in contents.ipynb:
    content_string = content_string.replace(string_to_delete, '')
    # replace links to models in contents.ipynb:
    for i in range(len(model_notebook_names)):
        content_string = content_string.replace(f'({"../models/" + model_notebook_names[i]})', f'({model_notebook_colab_urls[i]})')
    # replace links to notebooks with colab notebook links:
    for i in range(len(notebook_names)):
        content_string = content_string.replace(f'({notebook_names[i]})', f'({notebook_colab_urls[i]})')
    open(f'{notebook_address[:-6].replace("docs","docs/colab")}_colab.ipynb', 'w').write(content_string)
