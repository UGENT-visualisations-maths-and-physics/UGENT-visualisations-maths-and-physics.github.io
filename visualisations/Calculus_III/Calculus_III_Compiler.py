#%% Combine all the Tikz files of "Calculus_III" into one tex file and compile
import os
from visualisations.python_scripts.TexCompiler import tex_compiler

# actually call the class now
Analyse_compiler = tex_compiler(folder="Calculus_III")
Analyse_compiler.create_standalone_tex_files(reset=False)
Analyse_compiler.create_summary_file(title="Calculus_III", authors="Felix Claeys, Brecht Verbeken, Simon Verbruggen")
#%%
Analyse_compiler.push_content_to_gh_pages()
# %%
