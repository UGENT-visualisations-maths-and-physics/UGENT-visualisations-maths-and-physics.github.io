#%% Combine all the Tikz files into one tex file and compile
from visualisations.z_python_scripts.TexCompiler import tex_compiler

# actually call the class now
Analyse_compiler = tex_compiler(folder="Calculus_III")
Analyse_compiler.create_summary_file(title="Calculus_III", authors="Felix Claeys, Brecht Verbeken, Simon Verbruggen", reset=False)
#%%
#Analyse_compiler.export_for_syllabus()      # export standalone files for syllabus integration
#%%
"Ensure all changes are committed!"
Analyse_compiler.push_content_to_gh_pages()

# %%
