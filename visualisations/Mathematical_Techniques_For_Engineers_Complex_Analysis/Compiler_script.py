#%% Combine all the Tikz files into one tex file and compile
from visualisations.z_python_scripts.TexCompiler import tex_compiler

# actually call the class now
Analyse_compiler = tex_compiler(folder="Mathematical_Techniques_For_Engineers_Complex_Analysis")
Analyse_compiler.create_summary_file(title="Mathematical_Techniques_For_Engineers_Complex_Analysis", authors="Felix Claeys, Brecht Verbeken, Simon Verbruggen", reset=True)
#%%
Analyse_compiler.export_for_syllabus()      # export standalone files for syllabus integration
#%%
"Ensure all changes are committed!"
Analyse_compiler.push_content_to_gh_pages()
# %%