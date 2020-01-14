import os
import shutil

def write_header(work_dir):
    refinement_file = open(work_dir + "mesh_refinement_loads.dat",'w')
    refinement_file.write("FULL POTENTIAL APPLICATION LOADS FILE\n\n")
    refinement_file.write('%4s %6s %15s %15s %15s %15s %15s %15s %15s %15s %15s %15s %15s\n\n' %
                          ("Case", "AOA", "FF_MS", "A_MS", "Con Numb", "# Nodes", "Cl_u", "Cl_l", "Cl_jump", "Cl_ref", "Cd_u", "Cd_l", "Rz"))
    refinement_file.flush()

def write_header_all_cases(work_dir):
    aoa_file = open(work_dir + "/plots/results/all_cases.dat",'w')
    aoa_file.write("FULL POTENTIAL APPLICATION ALL CASES LOADS FILE\n\n")
    aoa_file.write('%4s %6s %15s %15s %15s %15s %15s %15s %15s\n\n' %
                          ("Case", "AOA", "FF_MS", "A_MS", "# Nodes", "Cl", "Cl_jump", "Cl_ref", "Cd"))
    aoa_file.flush()


def write_case(case, AOA, FarField_MeshSize, Airfoil_MeshSize,work_dir):
    #refinement_file = open(work_dir + "mesh_refinement_loads.dat",'a')
    #refinement_file.write('{0:4d} {1:6.2f} {2:15.2f} {3:15.2e}'.format(case, AOA, FarField_MeshSize, Airfoil_MeshSize))
    #refinement_file.flush()

    aoa_file = open(work_dir + "/plots/results/all_cases.dat",'a')
    aoa_file.write('{0:4d} {1:6.2f} {2:15.2f} {3:15.2e}'.format(case, AOA, FarField_MeshSize, Airfoil_MeshSize))
    aoa_file.flush()

def write_figures_cl(cl_data_directory_name, AOA, work_dir, Domain_Size):
    with open(work_dir + '/plots/cl/figures_cl.tex', 'a') as cl_figures_file:
        cl_figures_file.write('\n\pgfplotsset{table/search path={' + cl_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_data_directory_name + '/cl.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) +'}\n' +
                           '\t\label{fig:cl_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_figures_file.flush()

    with open(work_dir + '/plots/cl/figures_cl_h.tex', 'a') as cl_figures_file:
        cl_figures_file.write('\n\pgfplotsset{table/search path={' + cl_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_data_directory_name + '/clh.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) +'}\n' +
                           '\t\label{fig:cl_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_figures_file.flush()

def write_figures_cm(cm_data_directory_name, AOA, work_dir, Domain_Size):
    with open(work_dir + '/plots/cm/figures_cm_h.tex', 'a') as cm_figures_file:
        cm_figures_file.write('\n\pgfplotsset{table/search path={' + cm_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cm_data_directory_name + '/cm_h.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) +'}\n' +
                           '\t\label{fig:cm_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cm_figures_file.flush()

def write_figures_cm_error(cm_data_directory_name, AOA, work_dir, Domain_Size):
    with open(work_dir + '/plots/cm_error/figures_cm_error_h.tex', 'a') as cm_figures_file:
        cm_figures_file.write('\n\pgfplotsset{table/search path={' + cm_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cm_data_directory_name + '/cm_error_h.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) +'}\n' +
                           '\t\label{fig:cm_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cm_figures_file.flush()

def write_figures_domain_cl_error(cl_error_data_directory_name, AOA, work_dir):
    with open(work_dir + '/plots/cl_error_domain_size/figures_cl_domain.tex', 'a') as cl_error_figures_file:
        cl_error_figures_file.write('\n\pgfplotsset{table/search path={' + cl_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_error_data_directory_name + '/domain_cl_error.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$}\n' +
                           '\t\label{fig:cl_error_domain_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_error_figures_file.flush()

def write_figures_cl_error(cl_error_data_directory_name, AOA, work_dir, Domain_Size):
    with open(work_dir + '/plots/cl_error/figures_cl_error.tex', 'a') as cl_error_figures_file:
        cl_error_figures_file.write('\n\pgfplotsset{table/search path={' + cl_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_error_data_directory_name + '/cl_error.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) +'}\n' +
                           '\t\label{fig:cl_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_error_figures_file.flush()

    with open(work_dir + '/plots/cl_error/figures_cl_error_h.tex', 'a') as cl_error_figures_file:
        cl_error_figures_file.write('\n\pgfplotsset{table/search path={' + cl_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_error_data_directory_name + '/cl_error_h.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
                           '\t\label{fig:cl_error_h_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_error_figures_file.flush()

    with open(work_dir + '/plots/cl_error/figures_cl_error_h_log.tex', 'a') as cl_error_figures_file:
        cl_error_figures_file.write('\n\pgfplotsset{table/search path={' + cl_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_error_data_directory_name + '/cl_error_h_log.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
                           '\t\label{fig:cl_error_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_error_figures_file.flush()

    with open(work_dir + '/plots/cl_error/figures_cl_error_h_log_ok.tex', 'a') as cl_error_figures_file:
        cl_error_figures_file.write('\n\pgfplotsset{table/search path={' + cl_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_error_data_directory_name + '/cl_error_h_log_ok.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
                           '\t\label{fig:cl_error_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_error_figures_file.flush()

def write_figures_energy(energy_data_directory_name, AOA, work_dir):
    with open(work_dir + '/plots/relative_error_energy_norm/figures_energy_h.tex', 'a') as energy_h_figures_file:
        energy_h_figures_file.write('\n\pgfplotsset{table/search path={' + energy_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + energy_data_directory_name + '/energy_h.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$}\n' +
                           '\t\label{fig:energy_h_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        energy_h_figures_file.flush()

    with open(work_dir + '/plots/relative_error_energy_norm/figures_energy_n.tex', 'a') as energy_n_figures_file:
        energy_n_figures_file.write('\n\pgfplotsset{table/search path={' + energy_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + energy_data_directory_name + '/energy_n.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$}\n' +
                           '\t\label{fig:energy_n_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        energy_n_figures_file.flush()

    with open(work_dir + '/plots/relative_error_energy_norm/figures_energy_variant_h.tex', 'a') as energy_variant_h_figures_file:
        energy_variant_h_figures_file.write('\n\pgfplotsset{table/search path={' + energy_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + energy_data_directory_name + '/energy_variant_h.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$}\n' +
                           '\t\label{fig:energy_variant_h_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        energy_variant_h_figures_file.flush()

    with open(work_dir + '/plots/relative_error_energy_norm/figures_energy_variant_n.tex', 'a') as energy_variant_n_figures_file:
        energy_variant_n_figures_file.write('\n\pgfplotsset{table/search path={' + energy_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + energy_data_directory_name + '/energy_variant_n.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$}\n' +
                           '\t\label{fig:energy_variant_n_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        energy_variant_n_figures_file.flush()

def write_figures_cd(cd_data_directory_name, AOA, work_dir):
    with open(work_dir + '/plots/cd/figures_cd.tex', 'a') as cd_figures_file:
        cd_figures_file.write('\n\pgfplotsset{table/search path={' + cd_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cd_data_directory_name + '/cd.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$}\n' +
                           '\t\label{fig:cd_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cd_figures_file.flush()

def write_figures_condition(condition_data_directory_name, AOA, work_dir):
    with open(work_dir + '/plots/condition_number/figures_condition.tex', 'a') as condition_figures_file:
        condition_figures_file.write('\n\pgfplotsset{table/search path={' + condition_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + condition_data_directory_name + '/condition.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$}\n' +
                           '\t\label{fig:condition_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        condition_figures_file.flush()

def write_cl(cl,work_dir):
    cl_aoa_file = open(work_dir + 'plots/aoa/cl_aoa.dat','a')
    cl_aoa_file.write('{0:15f}\n'.format(cl))
    cl_aoa_file.flush()

def write_cp_figures(cp_data_directory_name, AOA, case, Airfoil_MeshSize,  FarField_MeshSize, work_dir):
    figures_file = open(work_dir + '/plots/cp/figures.tex', 'w')
    figures_file.write('\n\pgfplotsset{table/search path={' + cp_data_directory_name + '},}\n\n' +
                       '\\begin{figure}\n' +
                       '\t\centering\n' +
                       '\t\input{' + cp_data_directory_name + '/cp.tikz}\n' +
                       '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                       ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                       '\t\label{fig:cp_AOA_' + str(AOA) + '}\n' +
                       '\end{figure}\n'
                       )
    figures_file.flush()

def write_jump_figures(jump_data_directory_name, AOA, case, Airfoil_MeshSize,  FarField_MeshSize, work_dir):
    with open(work_dir + 'plots/potential_jump/figures_jump.tex', 'w') as jump_figures_file:
        jump_figures_file.write('\n\pgfplotsset{table/search path={' + jump_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + jump_data_directory_name + '/jump.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                           '\t\label{fig:jump_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        jump_figures_file.flush()

def write_figures_far_field(far_field_data_directory_name, AOA, case, Airfoil_MeshSize,  FarField_MeshSize, work_dir):
    with open(work_dir + 'plots/far_field/figures_far_field_x.tex', 'w') as figures_file_x:
        figures_file_x.write('\n\pgfplotsset{table/search path={' + far_field_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + far_field_data_directory_name + '/velocity_norm_x.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                           '\t\label{fig:velocity_norm_x_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n\n'
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + far_field_data_directory_name + '/velocity_u_x.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                           '\t\label{fig:velocity_u_x_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n\n'
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + far_field_data_directory_name + '/velocity_v_x.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                           '\t\label{fig:velocity_v_x_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        figures_file_x.flush()

    with open(work_dir + 'plots/far_field/figures_far_field_y.tex', 'w') as figures_file_y:
        figures_file_y.write('\n\pgfplotsset{table/search path={' + far_field_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + far_field_data_directory_name + '/velocity_norm_y.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                           '\t\label{fig:velocity_norm_y_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n\n'
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + far_field_data_directory_name + '/velocity_u_y.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                           '\t\label{fig:velocity_u_y_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n\n'
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + far_field_data_directory_name + '/velocity_v_y.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize)+ '}\n' +
                           '\t\label{fig:velocity_v_y_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        figures_file_y.flush()

def create_cp_plots_directory_tree(work_dir):
    cp_plots_directory_name = work_dir + '/plots/cp'
    if not os.path.exists(cp_plots_directory_name):
        os.makedirs(cp_plots_directory_name)

    data_directory_name = work_dir + '/plots/cp/data/0_original'
    if not os.path.exists(data_directory_name):
        os.makedirs(data_directory_name)

    plots_directory_name = work_dir + '/plots/cp/plots'
    if not os.path.exists(plots_directory_name):
        os.makedirs(plots_directory_name)

    with open(work_dir + '/plots/cp/cp.tex', 'w') as tex_file:
        tex_file.write('\\documentclass{article}\n' +
                        '\\usepackage{tikz}\n' +
                        '\\usepackage{pgfplots}\n' +
                        '\\pgfplotsset{compat=1.13}\n' +
                        '\\usepackage[]{units}\n' +
                        '\\usepackage{gensymb}\n' +
                        '\\usepackage{graphicx}\n\n' +
                        '\\begin{document}\n' +
                        '\\scrollmode\n' +
                        '\\input{' + work_dir + '/plots/cp/figures.tex}\n' +
                        '\\batchmode\n' +
                        '\\end{document}\n'
                       )
        tex_file.flush()

    references_input_directory_name = os.getcwd() + '/references'
    references_output_directory_name = data_directory_name + '/references'
    if os.path.exists(references_output_directory_name):
        shutil.rmtree(references_output_directory_name)
    shutil.copytree(references_input_directory_name, references_output_directory_name)

def create_cl_plots_directory_tree(work_dir):
    data_directory_name = work_dir + '/plots/cl/data/cl'
    if not os.path.exists(data_directory_name):
        os.makedirs(data_directory_name)

    with open(work_dir + '/plots/cl/main_cl_h.tex', 'w') as tex_file:
        tex_file.write('\\documentclass{article}\n' +
                        '\\usepackage{tikz}\n' +
                        '\\usepackage{pgfplots}\n' +
                        '\\pgfplotsset{compat=1.13}\n' +
                        '\\usepackage[]{units}\n' +
                        '\\usepackage{gensymb}\n' +
                        '\\usepackage{graphicx}\n\n' +
                        '\\begin{document}\n' +
                        '\\scrollmode\n\n' +
                        '\\input{figures_cl_h.tex}\n\n' +
                        '\\batchmode\n' +
                        '\\end{document}\n')
        tex_file.flush()

    with open(work_dir + '/plots/cl/data/cl/clh.tikz', 'w') as cl_tikz_file:
        cl_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{semilogxaxis}[\n' +
            '    title={Mesh refinement study},\n' +
            '    xlabel={h},\n' +
            '    ylabel={$c_l[\\unit{-}]$},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    y tick label style={\n' +
            '       \t/pgf/number format/.cd,\n' +
            '       \tfixed,\n' +
            '       \tfixed zerofill,\n' +
            '       \tprecision=4,\n' +
            '       \t/tikz/.cd \n' +
            '    },\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    color=blue,\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {cl_results_h.dat};  \n' +
            '    \\addlegendentry{Kratos Integral}\n\n' +
            '\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    ]\n' +
            '    table {cl_reference_h.dat};  \n' +
            '    \\addlegendentry{XFOIL}\n\n' +
            '\end{semilogxaxis}\n' +
            '\end{tikzpicture}')
        cl_tikz_file.flush()

def create_cl_error_plots_directory_tree(work_dir):
    data_directory_name = work_dir + '/plots/cl_error/data/cl'
    if not os.path.exists(data_directory_name):
        os.makedirs(data_directory_name)

    with open(work_dir + '/plots/cl_error/main_cl_error_h.tex', 'w') as tex_file:
        tex_file.write('\\documentclass{article}\n' +
                        '\\usepackage{tikz}\n' +
                        '\\usepackage{pgfplots}\n' +
                        '\\pgfplotsset{compat=1.13}\n' +
                        '\\usepackage[]{units}\n' +
                        '\\usepackage{gensymb}\n' +
                        '\\usepackage{graphicx}\n\n' +
                        '\\begin{document}\n' +
                        '\\scrollmode\n\n' +
                        '\\input{figures_cl_error_h.tex}\n\n' +
                        '\\batchmode\n' +
                        '\\end{document}\n')
        tex_file.flush()

    with open(work_dir + '/plots/cl_error/data/cl/cl_error_h.tikz', 'w') as cl_tikz_file:
        cl_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{semilogxaxis}[\n' +
            '    title={Lift coefficient relative error},\n' +
            '    xlabel={h},\n' +
            '    ylabel={$\\frac{|c_l - c_{lref}|}{|c_{lref}|}\\cdot100$},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    color=blue,\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {cl_error_results_h.dat};  \n' +
            '    \\addlegendentry{Integral}\n\n' +
            '\\addplot[\n' +
            '    color=red,\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {cl_jump_error_results_h.dat};  \n' +
            '    \\addlegendentry{Jump}\n\n' +
            '\end{semilogxaxis}\n' +
            '\end{tikzpicture}')
        cl_tikz_file.flush()

def create_cl_error_domain_size_directory_tree(work_dir):
    data_directory_name = work_dir + '/plots/cl_error_domain_size/data/domain'
    if not os.path.exists(data_directory_name):
        os.makedirs(data_directory_name)

    with open(work_dir + '/plots/cl_error_domain_size/cl_domain.tex', 'w') as tex_file:
        tex_file.write('\\documentclass{article}\n' +
                        '\\usepackage{tikz}\n' +
                        '\\usepackage{pgfplots}\n' +
                        '\\pgfplotsset{compat=1.13}\n' +
                        '\\usepackage[]{units}\n' +
                        '\\usepackage{gensymb}\n' +
                        '\\usepackage{graphicx}\n\n' +
                        '\\begin{document}\n' +
                        '\\scrollmode\n\n' +
                        '\\input{figures_cl_domain.tex}\n\n' +
                        '\\batchmode\n' +
                        '\\end{document}\n')
        tex_file.flush()

    with open(work_dir + '/plots/cl_error_domain_size/data/domain/domain_cl_error.tikz', 'w') as cl_tikz_file:
        cl_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{semilogxaxis}[\n' +
            '    title={Lift coefficient relative error},\n' +
            '    xlabel={Domain\'s size},\n' +
            '    ylabel={$\\frac{|c_l - c_{lref}|}{|c_{lref}|}\\cdot100$},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    color=blue,\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {cl_error_results_domain.dat};  \n' +
            '    \\addlegendentry{Integral}\n\n' +
            '\\addplot[\n' +
            '    color=red,\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {cl_jump_error_results.dat};  \n' +
            '    \\addlegendentry{Jump}\n\n' +
            '\end{semilogxaxis}\n' +
            '\end{tikzpicture}')
        cl_tikz_file.flush()

def create_cm_plots_directory_tree(work_dir):
    data_directory_name = work_dir + '/plots/cm/data/cm'
    if not os.path.exists(data_directory_name):
        os.makedirs(data_directory_name)

    with open(work_dir + '/plots/cm/main_cm_h.tex', 'w') as tex_file:
        tex_file.write('\\documentclass{article}\n' +
                        '\\usepackage{tikz}\n' +
                        '\\usepackage{pgfplots}\n' +
                        '\\pgfplotsset{compat=1.13}\n' +
                        '\\usepackage[]{units}\n' +
                        '\\usepackage{gensymb}\n' +
                        '\\usepackage{graphicx}\n\n' +
                        '\\begin{document}\n' +
                        '\\scrollmode\n\n' +
                        '\\input{figures_cm_h.tex}\n\n' +
                        '\\batchmode\n' +
                        '\\end{document}\n')
        tex_file.flush()

    with open(work_dir + '/plots/cm/data/cm/cm_h.tikz', 'w') as cl_tikz_file:
        cl_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{semilogxaxis}[\n' +
            '    title={Mesh refinement study},\n' +
            '    xlabel={h},\n' +
            '    ylabel={$c_m[\\unit{-}]$},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    y tick label style={\n' +
            '       \t/pgf/number format/.cd,\n' +
            '       \tfixed,\n' +
            '       \tfixed zerofill,\n' +
            '       \tprecision=4,\n' +
            '       \t/tikz/.cd \n' +
            '    },\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    color=blue,\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {cm_results_h.dat};  \n' +
            '    \\addlegendentry{Kratos Integral}\n\n' +
            '\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    ]\n' +
            '    table {cm_reference_h.dat};  \n' +
            '    \\addlegendentry{XFOIL}\n\n' +
            '\end{semilogxaxis}\n' +
            '\end{tikzpicture}')
        cl_tikz_file.flush()


def create_plots_directory_tree(work_dir):
    create_cp_plots_directory_tree(work_dir)
    create_cl_plots_directory_tree(work_dir)
    create_cl_error_plots_directory_tree(work_dir)
    create_cl_error_domain_size_directory_tree(work_dir)
    create_cm_plots_directory_tree(work_dir)

def read_cl_reference(AOA):
    # values computed with the panel method from xfoil for naca0012
    if(abs(AOA - 0.0) < 1e-3):
        return 0.0
    elif(abs(AOA - 1.0) < 1e-3):
        return 0.1208
    elif(abs(AOA - 2.0) < 1e-3):
        return 0.2416
    elif(abs(AOA - 3.0) < 1e-3):
        return 0.3623
    elif(abs(AOA - 4.0) < 1e-3):
        return 0.4829
    elif(abs(AOA - 5.0) < 1e-3):
        return 0.6033
    elif(abs(AOA - 6.0) < 1e-3):
        return 0.7235
    elif(abs(AOA - 7.0) < 1e-3):
        return 0.8436
    elif(abs(AOA - 8.0) < 1e-3):
        return 0.9634
    elif(abs(AOA - 9.0) < 1e-3):
        return 1.0828
    elif(abs(AOA - 10.0) < 1e-3):
        return 1.202
    elif(abs(AOA -11.0) < 1e-3):
        return 1.3208
    elif(abs(AOA - 12.0) < 1e-3):
        return 1.4392
    elif(abs(AOA - 13.0) < 1e-3):
        return 1.5572
    elif(abs(AOA - 14.0) < 1e-3):
        return 1.6746
    elif(abs(AOA - 15.0) < 1e-3):
        return 1.7916
    else:
        return 0.0



