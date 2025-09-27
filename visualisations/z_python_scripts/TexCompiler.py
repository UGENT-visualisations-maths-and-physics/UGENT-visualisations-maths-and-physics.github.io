"Functions for extracting Tikz code from a directory of Tex files and writing to summary Tex files"

# Make sure to install "poppler" for export to website.

import os, re, subprocess, glob
import shutil
import pdf2image
import yaml

def find_files(root_directory, filename):
    """find all the files with a certain name in a root directory"""
    files_abs, files_rel = [], []   # lists of all absolute and relative paths of the files
    # walk through all subdirectories and files
    for root, directory, files in os.walk(root_directory):
        for file in files:
            if file == filename:
                # create absolute path
                full_abs_path = os.path.join(root, file)    

                # create relative path (relative to the starting directory)
                directory_rel = os.path.relpath(root, root_directory)
                full_rel_path = os.path.join(directory_rel, file)

                files_rel.append(full_rel_path), files_abs.append(full_abs_path)
    return files_abs, files_rel

def chapter_and_number(path):
    """extract the chapter and the chapter number from path of main.tex file"""
    assert isinstance(path, str)
    chapter = path.split('/')[-2]                       # extract the name of parent directory(=chapter)
    chapter_proper_name = chapter.replace('_', ' ')     # replace underscores by " " (for actual chapter name)

    # extract the digits:chapter number, section number, subsection number...
    parts = chapter.split(".")      
    chapter_digits = []
    for part in parts[:-1]:                     # first parts: all digits
        chapter_digits.append(int(part))
    last_digit = int(parts[-1].split("_")[0])   # extract the last digit (before the chapter name)
    chapter_digits.append(int(last_digit))

    return chapter_digits, chapter_proper_name

def sorting_key(path):
    """creates a key that allows sorting per ascending chapter digits"""
    chapter_digits, chapter = chapter_and_number(path)
    return tuple(chapter_digits)

def get_section(chapter_digits, chapter_parts):
    """Defines tex command for creating a relevant chapter/section/subsection in latex

    Args:
        chapter (str): chapter of the section: e.g. "3.4.5"
        chapter_parts (list): contains the parts of a chapter e.g 3.4.5 -> [3, 4, 5]

    Returns:
        str: section in tex code
    """
    if len(chapter_parts)==1:
        section = "\\chapter*"
    elif len(chapter_parts)==2:
        section = "\\section*"
    elif len(chapter_parts)==3:
        section = "\\subsection*"
    return section + "{" + chapter_digits + "}\n"

def find_pattern(pattern, string_unseparated, without_begin_and_end=1):
    """Find text between a pattern (begin and end statement) in a string
    Args:
        pattern (str): Substring which we are looking for in unseparated string.
        string_unseparated (str): The input string where we will look for the pattern.
        without_begin_and_end (binary, optional): Specifies if we exclude the begin and end (pattern) of the separated string. Defaults to 1 (exclude).
    
    Returns:
        str: string between pattern
    """
    string_pattern = re.search(pattern, string_unseparated, re.DOTALL)  # search for the pattern using "re"
    if string_pattern:
        string_pattern = string_pattern.group(without_begin_and_end)    # exclude or include the pattern from the result (depending on "without_begin_and_end")
    else:
        print("Error section %s not found." % (pattern))
    return string_pattern

# relevant patterns (for re.search)
package_pattern = r"{(.*?)}"                        # for finding used packages
documentclass_pattern = r"\\documentclass{(.*?)}"   # for finding the used documentclass


#%% Compiler class

class figure:
    def __init__(self, parent_directory_path, standalone_pdf_path, standalone_tex_path, standalone_pdf_rel_path, export_directory_rel_path):

        self.parent_directory_path = parent_directory_path
        self.standalone_pdf_path = standalone_pdf_path
        self.standalone_tex_path = standalone_tex_path
        self.standalone_pdf_rel_path = standalone_pdf_rel_path
        self.export_directory_rel_path = export_directory_rel_path
        self.chapter_parts, self.chapter, self.tex_section = None, None, None

        # relative path for export standalone.tex file
        self.export_tex_rel_path = None
        # website related properties
        self.export_image_rel_path = None       # relative path to where the figure is stored on the website

    def update_figure_section(self, chapter_parts, chapter, tex_section):
        """Update the section number and name of the figure"""
        self.chapter_parts, self.chapter, self.tex_section = chapter_parts, chapter, tex_section
        # extract name of the exported files (normally standalone.tex and standlone.PNG), and 
        exported_pdf_name = self.standalone_pdf_path.split("/")[-1].replace(".pdf", ".PNG")
        tex_file_name = self.standalone_tex_path.split("/")[-1]

        # define relative paths of the destination (export) .PNG and .tex file
        self.destination_PNG_rel = os.path.join(self.export_directory_rel_path, exported_pdf_name)   
        self.destination_tex_rel = os.path.join(self.export_directory_rel_path, tex_file_name)

    def make_figure_data_file(self):
        prefix_path = "assets/generated_figures/"
        """Returns the YAML front matter used for displaying figures on a website"""
        image_abs_path = os.path.join(prefix_path, self.destination_PNG_rel)
        self.YAML_data = {
            "title": self.chapter,
            "image": image_abs_path,
            "properties": {
                "format" : "PNG"
            }
        }
    
#%% Compiler class

# compiler class which uses the figure class
class tex_compiler:
    def __init__(self, folder):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))                # Current file's directory  
        parent_dir = os.path.abspath(os.path.join(current_dir,  '..'))          # Go up two level's (parent of parent directory)
        script_dir = os.path.join(parent_dir, folder)                           # Join with another folder or file
        self.script_dir = script_dir

        self.project_name = self.script_dir.split("/")[-1]                      # name of the project
        self.standalone_tex_files_abs, self.standalone_tex_files_rel = find_files(self.script_dir, filename="standalone.tex")   # find the relevant tex files     
        self.sorted_standalone_tex_files_abs = sorted(self.standalone_tex_files_abs, key=sorting_key)                           # sort files according to ascending chapter
        
        self.figure_dict = self.create_figure_dict()

        # initialise variables for certain methods
        self.summary_pdf_path = None    # path for the summary pdf
        # variables for web export
        self.asset_directory = None
        self.yml_path = None

        #Get the local directory where files are supposed to be stored. By default this the parent folder of the repository
        self.repo_dir = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')     # retrieve repository root directory
        self.local_export_directory = os.path.join(self.repo_dir, "export")   # local export folder: parent folder of repo


    def create_figure_dict(self):
        """create dictionary containing path to tex files as keys and the corresponding figure objects as values"""
        figure_dict = {}
        for i, standalone_tex_path in enumerate(self.sorted_standalone_tex_files_abs):
            # get the relevant paths
            parent_directory_path = os.path.dirname(standalone_tex_path)
            standalone_pdf_path = standalone_tex_path.replace(".tex", ".pdf")
            standalone_pdf_rel_path = os.path.relpath(standalone_pdf_path, self.script_dir)

            # relative path of standalone pdf directory, for export to syllabus or website
            export_directory_rel_path = os.path.join(self.project_name, os.path.relpath(parent_directory_path, self.script_dir)).replace(".tex", "")

            figure_object = figure(parent_directory_path = parent_directory_path, standalone_pdf_path=standalone_pdf_path, standalone_tex_path=standalone_tex_path, standalone_pdf_rel_path=standalone_pdf_rel_path, export_directory_rel_path=export_directory_rel_path)
            figure_dict[standalone_tex_path] = figure_object
        return figure_dict
    
    def update_figures_section(self):
        """Update the sections for every figure object"""
        for standalone_tex_path in self.figure_dict:
            figure_object = self.figure_dict[standalone_tex_path]
            if os.path.exists(standalone_tex_path):
                # extract the section number and actual section code
                chapter_parts, chapter = chapter_and_number(standalone_tex_path)                  
                tex_section = get_section(chapter, chapter_parts)
                
                figure_object.update_figure_section(chapter_parts=chapter_parts, chapter=chapter, tex_section=tex_section)
            else:
                print("File: %s doesn't exist" % (figure_object.standalone_pdf_path))
                break

    def run_standalone_tex_files(self, reset):
        """checks for pdf output of standalone.tex files for integration into syllabus"""
        for standalone_tex_path in self.figure_dict:
            figure_object = self.figure_dict[standalone_tex_path]

            # check if pdf output exists
            pdf_exists = os.path.exists(figure_object.standalone_pdf_path)
            # compile pdf if it doesn't exist
            if pdf_exists is False or reset is True:
                subprocess.run(['pdflatex', '-output-directory', figure_object.parent_directory_path, figure_object.standalone_tex_path])
        

    def get_tex_begin(self, resulting_packages_list, title, authors):
        """create the beginning of the tex document"""
        assert isinstance(title, str)
        assert isinstance(authors, str)

        # everything before \begin{document}
        resulting_packages_string = ''
        resulting_packages_string += "\\documentclass{book}\n"
        for package in resulting_packages_list:
                resulting_packages_string += "%s\n" % (package)
        resulting_packages_string += "\\title{%s}\n" % (title)
        resulting_packages_string += "\\author{%s}\n" % (authors)
        
        # everything after \begin{document}
        resulting_packages_string += "\\begin{document}\n"
        resulting_packages_string += "\\maketitle\n"
        return resulting_packages_string

    def create_include_fig(self, relative_path):
        """create the include fig statement for in the summary file"""
        string = r"\begin{figure}[H]"
        string += "\n" + r"\centering"
        string += "\n"
        string += r"\includegraphics{%s}" % (relative_path)
        string += "\n" + r"\end{figure}" + "\n" + "\n"
        return string

    def create_summary_file(self, title, authors, reset=False):
        """Create summary tex file containing all figures
        
        Args: 
        Reset: compiles all standalone .tex, even if the pdf output already exists
        """
        tex_middle = ""     # middle part of the tex file

        # check all pdf outputs and update the figure sections
        self.run_standalone_tex_files(reset=reset)
        self.update_figures_section()

        for standalone_tex_path in self.figure_dict:
            figure_object = self.figure_dict[standalone_tex_path]
                                   
            print(os.path.relpath(figure_object.standalone_pdf_path, self.script_dir))

            # create the includegraphics part
            tex_middle_sub = self.create_include_fig(figure_object.standalone_pdf_rel_path)
            # append to body
            tex_middle += figure_object.tex_section + tex_middle_sub

        packages_list=[r"\usepackage{float}", r"\usepackage{graphicx}"]     # used pacakges for summary file

        # combine all into a tex file
        tex_begin = self.get_tex_begin(packages_list, title = "Figures " + title.replace("_", " "), authors=authors)  
        tex_string = tex_begin + tex_middle + "\\end{document}"

        # create paths for summary file
        summary_tex_path = os.path.join(self.script_dir, self.project_name + ".tex")
        self.summary_pdf_path = summary_tex_path.replace(".tex", ".pdf")
        # write to summary tex file 
        with open(summary_tex_path, 'w') as tex_file:
            tex_file.write(tex_string)
        # compile summary .tex file
        subprocess.run(['pdflatex', '-output-directory', self.script_dir, summary_tex_path])

    def ensure_directories_exist(self, parent_dir):
        """Ensure that all parent directories in the file_path exist, creating them by backtracking if necessary"""
        missing_dirs = []
        # start from the parent directory and work upwards
        while not os.path.exists(parent_dir) and parent_dir != os.path.dirname(parent_dir):
            missing_dirs.append(parent_dir)
            parent_dir = os.path.dirname(parent_dir)    # take the next parent directory and repeat

        # create all missing directories, starting from the most overarching directory
        for dir_to_create in reversed(missing_dirs):
            os.makedirs(dir_to_create)

    def export_for_syllabus(self):
        """Export all standalone.tex files in a structured folder for integration into syllabus"""
        for standalone_tex_path in self.figure_dict:
            figure_object = self.figure_dict[standalone_tex_path]
            # define the absolute paths of the destination directory and PNG
            destination_tex = os.path.join(self.local_export_directory, figure_object.destination_tex_rel)  
            destination_directory = os.path.join(self.local_export_directory, figure_object.export_directory_rel_path)
           
            self.ensure_directories_exist(destination_directory)        # ensure all parent directories exists
            
            # copy the file
            shutil.copy(figure_object.standalone_tex_path, destination_directory)
            # compile standalone.tex file
            subprocess.run(['pdflatex', '-output-directory', destination_directory, destination_tex])

            # Check generated files and only retain .tex and .pdf (the rest are auxiliary files)
            generated_files = glob.glob(os.path.join(destination_directory, "standalone.*"))
            print("generated files")
            print(generated_files)
            for file in generated_files:
                if not (file.endswith(".pdf") or file.endswith(".tex")): 
                    os.remove(file)

        print("Exported all figures to %s" % (self.local_export_directory))

    def convert_to_PNG_and_export(self, export_directory, dpi_used=200):
        """Convert all figures to PNG (websites have bad support for pdf viewing) and export"""
        for standalone_tex_path in self.figure_dict:
            figure_object = self.figure_dict[standalone_tex_path]
            # define the absolute paths of the destination directory and PNG
            destination_PNG = os.path.join(export_directory, figure_object.destination_PNG_rel)        # file path of the copied file
            destination_directory = os.path.join(export_directory, figure_object.export_directory_rel_path)

            self.ensure_directories_exist(destination_directory)         # ensure all parent directories exists

            # Convert PDF to image (first page only)
            image = pdf2image.convert_from_path(figure_object.standalone_pdf_path , dpi=dpi_used)   # dpi=Dots per inch, determines quality
            image[0].save(destination_PNG, 'PNG')                                                   # Save the first page as PNG
        # also copy the summary pdf
        shutil.copy(self.summary_pdf_path, self.asset_directory)
        
    def make_figures_yml(self):
        figures_yml_data = []   # list containing all figure data
        for main_tex_path in self.figure_dict:
            figure_object = self.figure_dict[main_tex_path]
            figure_object.make_figure_data_file()
            figures_yml_data.append(figure_object.YAML_data)
        
        # write to a .yml file
        with open(self.yml_path, 'w') as file:
            yaml.dump(figures_yml_data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def push_content_to_gh_pages(self):
        # define names of the asset directory and .yml file
        asset_directory_name = self.project_name
        yml_file_name =  self.project_name + "_figures.yml"

        # define paths for temporary storage
        self.asset_directory = os.path.join(self.local_export_directory, asset_directory_name)
        self.yml_path = os.path.join(self.local_export_directory, yml_file_name) 

        # paths in the gh-pages branch of parent directories
        gh_pages_asset_parent_path = os.path.join(self.repo_dir, 'assets', 'generated_figures')
        gh_pages_yml_parent_path = os.path.join(self.repo_dir, '_data')
        # ensure parent directories exist
        self.ensure_directories_exist(gh_pages_asset_parent_path)
        self.ensure_directories_exist(gh_pages_yml_parent_path)

        # paths in the gh-pages branch of actual directory/file
        gh_pages_asset_path = os.path.join(gh_pages_asset_parent_path, asset_directory_name)
        gh_pages_yml_path = os.path.join(gh_pages_yml_parent_path, yml_file_name)

        # export figures and .yml file to temporary location
        self.convert_to_PNG_and_export(self.local_export_directory, dpi_used=200)
        self.make_figures_yml()
        
        # navigate to repo_dir:
        os.chdir(self.repo_dir)
        
        # Step 2: Checkout gh-pages branch (this assumes you already have it)
        subprocess.run(['git', 'checkout', 'gh-pages'])

        if os.path.exists(gh_pages_asset_path):
            shutil.rmtree(gh_pages_asset_path)  # removes the directory and its contents

        if os.path.exists(gh_pages_yml_path):
            os.remove(gh_pages_yml_path) # removes the file

        # Step 4: Move the generated files into place (provide full path -> will overwrite if already exists)
        shutil.move(self.yml_path, gh_pages_yml_path)  # Move the .yml file
        shutil.move(self.asset_directory, gh_pages_asset_parent_path)  # Move the asset file

        current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')
        assert current_branch=='gh-pages', "in wrong branch: %s (make sure all changes are comitted)" % (current_branch)

        # Step 5: Add, commit, and push changes
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', f'Automatic update: {self.project_name} assets and YAML for gh-pages'])
        subprocess.run(['git', 'push', 'origin', 'gh-pages'])

        print("Files of %s successfully pushed to gh-pages branch!" % (self.project_name))
