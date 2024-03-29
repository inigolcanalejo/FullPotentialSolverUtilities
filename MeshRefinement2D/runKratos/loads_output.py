import os
import shutil


def write_header(work_dir):
    refinement_file = open(work_dir + "mesh_refinement_loads.dat", 'w')
    refinement_file.write("FULL POTENTIAL APPLICATION LOADS FILE\n\n")
    refinement_file.write('%4s %6s %15s %15s %15s %15s %15s %15s %15s %15s %15s %15s %15s\n\n' %
                          ("Case", "AOA", "FF_MS", "A_MS", "Con Numb", "# Nodes", "Cl_u", "Cl_l", "Cl_jump", "Cl_ref", "Cd_u", "Cd_l", "Rz"))
    refinement_file.flush()


def write_header_all_cases(work_dir):
    create_plot_directory_tree(work_dir + '/plots/results')
    all_cases = open(work_dir + "/plots/results/all_cases.dat", 'w')
    all_cases.write("FULL POTENTIAL APPLICATION ALL CASES LOADS FILE\n\n")
    all_cases.write('%4s %6s %15s %15s %15s %15s %15s %15s %15s\n\n' %
                   ("Case", "AOA", "FF_MS", "A_MS", "# Nodes", "Cl", "Cl_jump", "Cl_ref", "Cd"))
    all_cases.flush()


def write_case(case, AOA, FarField_MeshSize, Airfoil_MeshSize, work_dir):
    #refinement_file = open(work_dir + "mesh_refinement_loads.dat",'a')
    #refinement_file.write('{0:4d} {1:6.2f} {2:15.2f} {3:15.2e}'.format(case, AOA, FarField_MeshSize, Airfoil_MeshSize))
    # refinement_file.flush()

    aoa_file = open(work_dir + "/plots/results/all_cases.dat", 'a')
    aoa_file.write('{0:4d} {1:6.2f} {2:15.2f} {3:15.2e}'.format(
        case, AOA, FarField_MeshSize, Airfoil_MeshSize))
    aoa_file.flush()


def write_figures_cl(cl_data_directory_name, AOA, work_dir, Domain_Size):
    with open(work_dir + '/plots/cl/figures_cl.tex', 'a') as cl_figures_file:
        cl_figures_file.write('\n\pgfplotsset{table/search path={' + cl_data_directory_name + '},}\n\n' +
                              '\\begin{figure}\n' +
                              '\t\centering\n' +
                              '\t\input{' + cl_data_directory_name + '/cl.tikz}\n' +
                              '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
                              '\t\label{fig:cl_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                              '\end{figure}\n'
                              )
        cl_figures_file.flush()

    with open(work_dir + '/plots/cl/figures_cl_h.tex', 'a') as cl_figures_file:
        cl_figures_file.write('\n\pgfplotsset{table/search path={' + cl_data_directory_name + '},}\n\n' +
                              '\\begin{figure}\n' +
                              '\t\centering\n' +
                              '\t\input{' + cl_data_directory_name + '/clh.tikz}\n' +
                              '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
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
                              '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
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
                              '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
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
                                    '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size) + '}\n' +
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


def write_cl(cl, work_dir):
    cl_aoa_file = open(work_dir + 'plots/aoa/cl_aoa.dat', 'a')
    cl_aoa_file.write('{0:15f}\n'.format(cl))
    cl_aoa_file.flush()


def write_cp_figures(cp_data_directory_name, AOA, case, Airfoil_MeshSize,  FarField_MeshSize, work_dir):
    figures_file = open(work_dir + '/plots/cp/figures.tex', 'w')
    figures_file.write('\n\pgfplotsset{table/search path={' + cp_data_directory_name + '},}\n\n' +
                       '\\begin{figure}\n' +
                       '\t\centering\n' +
                       '\t\input{' + cp_data_directory_name + '/cp.tikz}\n' +
                       '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                       ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
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
                                ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
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
                             ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
                             '\t\label{fig:velocity_norm_x_AOA_' + str(AOA) + '}\n' +
                             '\end{figure}\n\n'
                             '\\begin{figure}\n' +
                             '\t\centering\n' +
                             '\t\input{' + far_field_data_directory_name + '/velocity_u_x.tikz}\n' +
                             '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                             ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
                             '\t\label{fig:velocity_u_x_AOA_' + str(AOA) + '}\n' +
                             '\end{figure}\n\n'
                             '\\begin{figure}\n' +
                             '\t\centering\n' +
                             '\t\input{' + far_field_data_directory_name + '/velocity_v_x.tikz}\n' +
                             '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                             ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
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
                             ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
                             '\t\label{fig:velocity_norm_y_AOA_' + str(AOA) + '}\n' +
                             '\end{figure}\n\n'
                             '\\begin{figure}\n' +
                             '\t\centering\n' +
                             '\t\input{' + far_field_data_directory_name + '/velocity_u_y.tikz}\n' +
                             '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                             ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
                             '\t\label{fig:velocity_u_y_AOA_' + str(AOA) + '}\n' +
                             '\end{figure}\n\n'
                             '\\begin{figure}\n' +
                             '\t\centering\n' +
                             '\t\input{' + far_field_data_directory_name + '/velocity_v_y.tikz}\n' +
                             '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                             ' Far field mesh size = ' + str(FarField_MeshSize) + ' Airfoil mesh size = ' + str(Airfoil_MeshSize) + '}\n' +
                             '\t\label{fig:velocity_v_y_AOA_' + str(AOA) + '}\n' +
                             '\end{figure}\n'
                             )
        figures_file_y.flush()

def write_figures_aoa(aoa_data_directory_name):
    with open(aoa_data_directory_name + '/figures_aoa.tex', 'w') as aoa_figures_file:
        aoa_figures_file.write('\n\pgfplotsset{table/search path={' + aoa_data_directory_name + '},}\n\n' +
                              '\\begin{figure}\n' +
                              '\t\centering\n' +
                              '\t\input{' + aoa_data_directory_name + '/cl_aoa.tikz}\n' +
                              '\t\caption{cl vs $\\alpha$}\n' +
                              '\end{figure}\n'
                              )
        aoa_figures_file.flush()

def create_plot_directory_tree(data_directory_name):
    if not os.path.exists(data_directory_name):
        os.makedirs(data_directory_name)

def create_main_tex_file(file_name, figures_file_name):
    with open(file_name, 'w') as tex_file:
        tex_file.write('\\documentclass{article}\n' +
                       '\\usepackage{tikz}\n' +
                       '\\usepackage{pgfplots}\n' +
                       '\\pgfplotsset{compat=1.13}\n' +
                       '\\usepackage[]{units}\n' +
                       '\\usepackage{gensymb}\n' +
                       '\\usepackage{graphicx}\n\n' +
                       '\\begin{document}\n' +
                       '\\scrollmode\n\n' +
                       '\\input{' + figures_file_name + '}\n\n' +
                       '\\batchmode\n' +
                       '\\end{document}\n')
        tex_file.flush()

def create_tikz_refinement_plot_file(file_name, ylabel, dat_name, reference_dat_name, reference_case_name):
    with open(file_name, 'w') as tikz_file:
        tikz_file.write('\\begin{tikzpicture}\n' +
                           '\\begin{semilogxaxis}[\n' +
                           '    title={Mesh refinement study},\n' +
                           '    xlabel={h},\n' +
                           '    ylabel={' + ylabel + '},\n' +
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
                           '    table {' + dat_name + '};  \n' +
                           '    \\addlegendentry{Kratos Integral}\n\n' +
                           '\\addplot[\n' +
                           '    color=black,\n' +
                           '    mark=none,\n' +
                           '    ]\n' +
                           '    table {' + reference_dat_name + '};  \n' +
                           '    \\addlegendentry{' + reference_case_name + '}\n\n' +
                           '\end{semilogxaxis}\n' +
                           '\end{tikzpicture}')
        tikz_file.flush()

def create_tikz_error_plot_file(file_name, title, xlabel, ylabel, dat_name, jump_dat_name):
    with open(file_name, 'w') as tikz_file:
        tikz_file.write('\\begin{tikzpicture}\n' +
                        '\\begin{semilogxaxis}[\n' +
                        '    title={' + title + '},\n' +
                        '    xlabel={' + xlabel + '},\n' +
                        '    ylabel={' + ylabel + '},\n' +
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
                        '    table {' + dat_name + '};  \n' +
                        '    \\addlegendentry{Integral}\n\n' +
                        '\\addplot[\n' +
                        '    color=red,\n' +
                        '    mark=square,\n' +
                        '    ]\n' +
                        '    table {' + jump_dat_name + '};  \n' +
                        '    \\addlegendentry{Jump}\n\n' +
                        '\end{semilogxaxis}\n' +
                        '\end{tikzpicture}')
        tikz_file.flush()

def create_cp_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cp/data/0_original')
    create_plot_directory_tree(work_dir + '/plots/cp/plots')

    create_main_tex_file(work_dir + '/plots/cp/cp.tex',work_dir + '/plots/cp/figures.tex')

    references_input_directory_name = os.getcwd() + '/references/cp'
    references_output_directory_name = work_dir + '/plots/cp/data/0_original/references'
    if os.path.exists(references_output_directory_name):
        shutil.rmtree(references_output_directory_name)
    shutil.copytree(references_input_directory_name,
                    references_output_directory_name)

def create_cl_plots_directory_tree(work_dir, reference_case_name):
    create_plot_directory_tree(work_dir + '/plots/cl/data/cl')

    create_main_tex_file(work_dir + '/plots/cl/main_cl_h.tex', 'figures_cl_h.tex')

    create_tikz_refinement_plot_file(work_dir + '/plots/cl/data/cl/clh.tikz', # file_name
                                        '$c_l[\\unit{-}]$',                   # ylabel
                                        'cl_results_h.dat',                   # dat_name
                                        'cl_reference_h.dat',                 # reference_dat_name
                                        reference_case_name)

def create_cl_error_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cl_error/data/cl')

    create_main_tex_file(work_dir + '/plots/cl_error/main_cl_error_h.tex', 'figures_cl_error_h.tex')

    create_tikz_error_plot_file(work_dir + '/plots/cl_error/data/cl/cl_error_h.tikz',   # file_name
                                'Lift coefficient relative error',                      # title
                                'h',                                                    # xlabel
                                '$\\frac{|c_l - c_{lref}|}{|c_{lref}|}\\cdot100$',      # ylabel
                                'cl_error_results_h.dat',                               # dat_name
                                'cl_jump_error_results_h.dat')                          # jump_dat_name


def create_cl_error_domain_size_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cl_error_domain_size/data/domain')

    create_main_tex_file(work_dir + '/plots/cl_error_domain_size/cl_domain.tex', 'figures_cl_domain.tex')

    create_tikz_error_plot_file(work_dir + '/plots/cl_error_domain_size/data/domain/domain_cl_error.tikz',  # file_name
                                'Lift coefficient relative error',                                          # title
                                'Domain\'s size',                                                           # xlabel
                                '$\\frac{|c_l - c_{lref}|}{|c_{lref}|}\\cdot100$',                          # ylabel
                                'cl_error_results_domain.dat',                                              # dat_name
                                'cl_jump_error_results.dat')                                                # jump_dat_name

def create_cm_plots_directory_tree(work_dir, reference_case_name):
    create_plot_directory_tree(work_dir + '/plots/cm/data/cm')

    create_main_tex_file(work_dir + '/plots/cm/main_cm_h.tex', 'figures_cm_h.tex')

    create_tikz_refinement_plot_file(work_dir + '/plots/cm/data/cm/cm_h.tikz',  # file_name
                                        '$c_m[\\unit{-}]$',                     # ylabel
                                        'cm_results_h.dat',                     # dat_name
                                        'cm_reference_h.dat',                 # reference_dat_name
                                        reference_case_name)

def create_cm_error_plots_directory_tree(work_dir):
    create_plot_directory_tree( work_dir + '/plots/cm_error/data/cm_error')

    create_main_tex_file(work_dir + '/plots/cm_error/main_cm_error_h.tex', 'figures_cm_error_h.tex')

    create_tikz_error_plot_file(work_dir + '/plots/cm_error/data/cm_error/cm_error_h.tikz', # file_name
                                'Pitch moment coefficient relative error',                  # title
                                'h',                                                        # xlabel
                                '$\\frac{|c_m - c_{mref}|}{|c_{mref}|}\\cdot100$',          # ylabel
                                'cm_error_results_h.dat',                                   # dat_name
                                'cm_error_jump_results_h.dat')                              # jump_dat_name

def create_aoa_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/aoa/data')
    write_figures_aoa(work_dir + '/plots/aoa/data')
    create_main_tex_file(work_dir + '/plots/aoa/data/cl_aoa.tex', 'figures_aoa.tex')

    with open(work_dir + '/plots/aoa/data/cl_aoa.tikz', 'w') as tikz_file:
        tikz_file.write('\\begin{tikzpicture}\n' +
                            '\\begin{axis}[\n' +
                            '    scaled ticks=false,\n' +
                            '    tick label style={/pgf/number format/fixed},\n' +
                            '    title={Lift coefficient vs. angle of attack},\n' +
                            '    xlabel={$\\alpha\\ [\\degree]$},\n' +
                            '    ylabel={$c_l\\ [-]$},\n' +
                            '    ymajorgrids=true,\n' +
                            '    xmajorgrids=true,\n' +
                            '    grid style=dashed,\n' +
                            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
                            '    width=12cm\n' +
                            ']\n\n' +
                            '\\addplot[\n' +
                            '    color=blue,\n' +
                            '    mark=oplus*,\n' +
                            '    mark options={solid},\n' +
                            '    smooth\n' +
                            '    ]\n' +
                            '    table {cl_aoa.dat};  \n' +
                            '    \\addlegendentry{Kratos Integral}\n\n' +
                            '\\addplot[\n' +
                            '    color=black,\n' +
                            '    mark=none,\n' +
                            '    ]\n' +
                            '    table {references/xfoil/cl_aoa.dat};  \n' +
                            '    \\addlegendentry{XFOIL}\n\n' +
                            '\end{axis}\n' +
                            '\end{tikzpicture}')
        tikz_file.flush()

    references_input_directory_name = os.getcwd() + '/references/aoa'
    references_output_directory_name = work_dir + '/plots/aoa/data/references'
    if os.path.exists(references_output_directory_name):
        shutil.rmtree(references_output_directory_name)
    shutil.copytree(references_input_directory_name,
                    references_output_directory_name)

def create_plots_directory_tree(work_dir, reference_case_name):
    write_header_all_cases(work_dir)
    create_cp_plots_directory_tree(work_dir)
    create_cl_plots_directory_tree(work_dir, reference_case_name)
    create_cl_error_plots_directory_tree(work_dir)
    create_cl_error_domain_size_directory_tree(work_dir)
    create_cm_plots_directory_tree(work_dir, reference_case_name)
    create_cm_error_plots_directory_tree(work_dir)
    create_aoa_plots_directory_tree(work_dir)


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
    elif(abs(AOA - 11.0) < 1e-3):
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
