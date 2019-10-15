#Removing files
rm cp*
#rm main*
rm validation.post.lst

#Running Latex
cd $input_dir_path/plots/cl
#pdflatex -interaction=batchmode main_cl.tex > main_cl_out.txt
pdflatex -interaction=batchmode main_cl_h.tex > main_cl_h_out.txt
cd $input_dir_path/plots/cl_error
#pdflatex -interaction=batchmode main_cl_error.tex > main_cl_error_out.txt
pdflatex -interaction=batchmode main_cl_error_h.tex > main_cl_error_h_out.txt
#pdflatex -interaction=batchmode main_cl_error_h_log.tex > main_cl_error_h_log_out.txt
#pdflatex -interaction=batchmode main_cl_error_h_log_ok.tex > main_cl_error_h_log_ok_out.txt
#cd $input_dir_path/plots/relative_error_energy_norm
#pdflatex -interaction=batchmode main_energy_h.tex > main_energy_h_out.txt
#pdflatex -interaction=batchmode main_energy_n.tex > main_energy_n_out.txt
#pdflatex -interaction=batchmode main_energy_variant_h.tex > main_energy_variant_h_out.txt
#pdflatex -interaction=batchmode main_energy_variant_n.tex > main_energy_variannt_n_out.txt
#cd $input_dir_path/plots/cd
#pdflatex -interaction=batchmode main_cd.tex > main_cd_out.txt
#cd $input_dir_path/plots/aoa/data
#pdflatex -interaction=batchmode cl_aoa.tex > main_aoa_out.txt
#cd $input_dir_path/plots/condition_number/
#pdflatex -interaction=batchmode main_condition.tex > main_condition_out.txt
cd $input_dir_path/plots/cl_error_domain_size/
pdflatex -interaction=batchmode cl_domain.tex > cl_domain_out.txt

cd $input_dir_path/plots/cm
pdflatex -interaction=batchmode main_cm_h.tex > main_cm_h_out.txt

cd $input_dir_path/plots/cm_error
pdflatex -interaction=batchmode main_cm_error_h.tex > main_cm_error_h_out.txt

cd /home/inigo/software/FullPotentialSolverUtilities/MeshRefinement/validation

