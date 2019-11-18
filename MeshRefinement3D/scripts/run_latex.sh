# Removing files
# rm cp*
# #rm main*
# rm validation.post.lst

# Running Latex
cd $input_dir_path/plots/cl
#pdflatex main_cl.tex > main_cl_out.txt
pdflatex -interaction=batchmode main_cl.tex > main_cl_out.txt

cd $input_dir_path/plots/cd
#pdflatex main_cd.tex > main_cd_out.txt
pdflatex -interaction=batchmode main_cd.tex > main_cd_out.txt

cd $input_dir_path/plots/cm
#pdflatex main_cm.tex > main_cm_out.txt
pdflatex -interaction=batchmode main_cm.tex > main_cm_out.txt

cd $input_dir_path/plots/cl_error
pdflatex -interaction=batchmode main_cl_error.tex > main_cl_error_out.txt

cd $input_dir_path/plots/cd_error
pdflatex -interaction=batchmode main_cd_error.tex > main_cd_error_out.txt

cd $input_dir_path/plots/cm_error
pdflatex -interaction=batchmode main_cm_error.tex > main_cm_error_out.txt

cd $input_dir_path/plots/cl_aoa
pdflatex -interaction=batchmode main_cl_aoa.tex > main_cl_aoa_out.txt

cd $input_dir_path/plots/cd_aoa
pdflatex -interaction=batchmode main_cd_aoa.tex > main_cd_aoa_out.txt

cd $input_dir_path/plots/cm_aoa
pdflatex -interaction=batchmode main_cm_aoa.tex > main_cm_aoa_out.txt

cd $input_dir_path/plots/newton_convergence
pdflatex main_convergence.tex > main_convergence.txt
#pdflatex -interaction=batchmode main_convergence.tex > main_convergence.txt

cd /home/inigo/software/FullPotentialSolverUtilities/MeshRefinement3D

