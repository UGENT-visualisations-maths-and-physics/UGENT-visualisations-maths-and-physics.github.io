#%% Combine all the Tikz files into one tex file and compile
# add script to path
import os, sys
python_scripts_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "z_python_scripts")
sys.path.append(python_scripts_path)
from TexCompiler import tex_compiler

# call the class now
Analyse_compiler = tex_compiler(folder="Calculus_III")
Analyse_compiler.create_summary_file(title="Calculus_III", authors="Felix Claeys, Brecht Verbeken, Simon Verbruggen", reset=False)
#%%
Analyse_compiler.export_for_syllabus()      # export standalone files for syllabus integration
#%%
"Ensure all changes are committed!"
# pushing to the website, only available for people with access to push to the website branch (gh-pages)
Analyse_compiler.push_content_to_gh_pages()

