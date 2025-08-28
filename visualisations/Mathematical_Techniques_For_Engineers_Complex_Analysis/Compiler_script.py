#%% Combine all the Tikz files into one tex file and compile
from visualisations.python_scripts.TexCompiler import tex_compiler

# actually call the class now
Complex_Analysis_compiler = tex_compiler(folder="Mathematical_Techniques_For_Engineers_Complex_Analysis")
Complex_Analysis_compiler.create_standalone_tex_files(reset=False)
Complex_Analysis_compiler.create_summary_file(title="Mathematical_Techniques_For_Engineers_Complex_Analysis", authors="Felix Claeys, Brecht Verbeken, Simon Verbruggen")
Complex_Analysis_compiler.export_for_syllabus()      # export standalone files for syllabus integration
#%%
"Ensure all changes are committed!"
Complex_Analysis_compiler.push_content_to_gh_pages()
# %%