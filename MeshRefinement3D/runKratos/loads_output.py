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

def write_figures_cl(cl_data_directory_name, AOA, work_dir, Domain_Size, Wing_Span, Smallest_Airfoil_Element_Size):
    with open(work_dir + '/plots/cl/figures_cl.tex', 'a') as cl_figures_file:
        cl_figures_file.write('\n\pgfplotsset{table/search path={' + cl_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_data_directory_name + '/cl.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size)
                               + ', Wing Span = ' + str(Wing_Span) + ', Smallest Element Size = ' + str(Smallest_Airfoil_Element_Size) +'}\n' +
                           '\t\label{fig:cl_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_figures_file.flush()

def write_figures_cd(cd_data_directory_name, AOA, work_dir, Domain_Size, Wing_Span, Smallest_Airfoil_Element_Size):
    with open(work_dir + '/plots/cd/figures_cd.tex', 'a') as cd_figures_file:
        cd_figures_file.write('\n\pgfplotsset{table/search path={' + cd_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cd_data_directory_name + '/cd.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size)
                               + ', Wing Span = ' + str(Wing_Span) + ', Smallest Element Size = ' + str(Smallest_Airfoil_Element_Size) +'}\n' +
                           '\t\label{fig:cd_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cd_figures_file.flush()

def write_figures_cm(cm_data_directory_name, AOA, work_dir, Domain_Size, Wing_Span, Smallest_Airfoil_Element_Size):
    with open(work_dir + '/plots/cm/figures_cm.tex', 'a') as cm_figures_file:
        cm_figures_file.write('\n\pgfplotsset{table/search path={' + cm_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cm_data_directory_name + '/cm.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size)
                               + ', Wing Span = ' + str(Wing_Span) + ', Smallest Element Size = ' + str(Smallest_Airfoil_Element_Size) +'}\n' +
                           '\t\label{fig:cm_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cm_figures_file.flush()

def write_figures_cl_error(cl_error_data_directory_name, AOA, work_dir, Domain_Size, Wing_Span, Smallest_Airfoil_Element_Size):
    with open(work_dir + '/plots/cl_error/figures_cl_error.tex', 'a') as cl_error_figures_file:
        cl_error_figures_file.write('\n\pgfplotsset{table/search path={' + cl_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cl_error_data_directory_name + '/cl_error.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size)
                               + ', Wing Span = ' + str(Wing_Span) + ', Smallest Element Size = ' + str(Smallest_Airfoil_Element_Size) +'}\n' +
                           '\t\label{fig:cl_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cl_error_figures_file.flush()

def write_figures_cd_error(cd_error_data_directory_name, AOA, work_dir, Domain_Size, Wing_Span, Smallest_Airfoil_Element_Size):
    with open(work_dir + '/plots/cd_error/figures_cd_error.tex', 'a') as cd_error_figures_file:
        cd_error_figures_file.write('\n\pgfplotsset{table/search path={' + cd_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cd_error_data_directory_name + '/cd_error.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size)
                               + ', Wing Span = ' + str(Wing_Span) + ', Smallest Element Size = ' + str(Smallest_Airfoil_Element_Size) +'}\n' +
                           '\t\label{fig:cd_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cd_error_figures_file.flush()

def write_figures_cm_error(cm_error_data_directory_name, AOA, work_dir, Domain_Size, Wing_Span, Smallest_Airfoil_Element_Size):
    with open(work_dir + '/plots/cm_error/figures_cm_error.tex', 'a') as cm_error_figures_file:
        cm_error_figures_file.write('\n\pgfplotsset{table/search path={' + cm_error_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + cm_error_data_directory_name + '/cm_error.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size)
                               + ', Wing Span = ' + str(Wing_Span) + ', Smallest Element Size = ' + str(Smallest_Airfoil_Element_Size) +'}\n' +
                           '\t\label{fig:cm_error_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        cm_error_figures_file.flush()

def write_figures_newton_convergence(newton_convergence_data_directory_name, AOA, work_dir, Domain_Size, Wing_Span, Smallest_Airfoil_Element_Size):
    with open(work_dir + '/plots/newton_convergence/figures_newton_convergence.tex', 'a') as newton_convergence_figures_file:
        newton_convergence_figures_file.write('\n\pgfplotsset{table/search path={' + newton_convergence_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + newton_convergence_data_directory_name + '/convergence.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, Domain size = ' + str(Domain_Size)
                               + ', Wing Span = ' + str(Wing_Span) + ', Smallest Element Size = ' + str(Smallest_Airfoil_Element_Size) +'}\n' +
                           '\t\label{fig:newton_convergence_DS_' + str(Domain_Size) + '_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        newton_convergence_figures_file.flush()

def write_cl(cl,work_dir):
    cl_aoa_file = open(work_dir + 'plots/aoa/cl_aoa.dat','a')
    cl_aoa_file.write('{0:15f}\n'.format(cl))
    cl_aoa_file.flush()

def write_cp_figures(cp_data_directory_name, AOA, case, Growth_Rate_Domain,  Growth_Rate_Wing, work_dir, section):
    with open(work_dir + '/plots/' + section + '/figures_cp.tex', 'w') as cp_figures_file:
        cp_figures_file.write('\n\pgfplotsset{table/search path={' + cp_data_directory_name + '},}\n\n' +
                       '\\begin{figure}\n' +
                       '\t\centering\n' +
                       '\t\input{' + cp_data_directory_name + '/cp.tikz}\n' +
                       '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Growth rate domain = ' + str(Growth_Rate_Domain) + ' Growth rate wing = ' + str(Growth_Rate_Wing)+ '}\n' +
                       '\t\label{fig:cp_AOA_' + str(AOA) + '}\n' +
                       '\end{figure}\n'
                       )
        cp_figures_file.flush()

def write_jump_figures(jump_data_directory_name, AOA, case, Growth_Rate_Domain,  Growth_Rate_Wing, work_dir):
    with open(work_dir + '/plots/potential_jump/figures_jump.tex', 'w') as jump_figures_file:
        jump_figures_file.write('\n\pgfplotsset{table/search path={' + jump_data_directory_name + '},}\n\n' +
                           '\\begin{figure}\n' +
                           '\t\centering\n' +
                           '\t\input{' + jump_data_directory_name + '/jump.tikz}\n' +
                           '\t\caption{$\\alpha = ' + str(AOA) + '\degree$, case = ' + str(case) +
                           ' Growth rate domain = ' + str(Growth_Rate_Domain) + ' Growth rate wing = ' + str(Growth_Rate_Wing)+ '}\n' +
                           '\t\label{fig:jump_AOA_' + str(AOA) + '}\n' +
                           '\end{figure}\n'
                           )
        jump_figures_file.flush()

def write_figures_cd_aoa(aoa_data_directory_name):
    with open(aoa_data_directory_name + '/figures_cd_aoa.tex', 'w') as aoa_figures_file:
        aoa_figures_file.write('\n\pgfplotsset{table/search path={' + aoa_data_directory_name + '/data/cd_aoa},}\n\n' +
                              '\\begin{figure}\n' +
                              '\t\centering\n' +
                              '\t\input{' + aoa_data_directory_name + '/data/cd_aoa/cd_aoa.tikz}\n' +
                              '\t\caption{cd vs $\\alpha$}\n' +
                              '\end{figure}\n'
                              )
        aoa_figures_file.flush()

def write_figures_cl_aoa(aoa_data_directory_name):
    with open(aoa_data_directory_name + '/figures_cl_aoa.tex', 'w') as aoa_figures_file:
        aoa_figures_file.write('\n\pgfplotsset{table/search path={' + aoa_data_directory_name + '/data/cl_aoa},}\n\n' +
                              '\\begin{figure}\n' +
                              '\t\centering\n' +
                              '\t\input{' + aoa_data_directory_name + '/data/cl_aoa/cl_aoa.tikz}\n' +
                              '\t\caption{cl vs $\\alpha$}\n' +
                              '\end{figure}\n'
                              )
        aoa_figures_file.flush()

def write_figures_cm_aoa(aoa_data_directory_name):
    with open(aoa_data_directory_name + '/figures_cm_aoa.tex', 'w') as aoa_figures_file:
        aoa_figures_file.write('\n\pgfplotsset{table/search path={' + aoa_data_directory_name + '/data/cm_aoa},}\n\n' +
                              '\\begin{figure}\n' +
                              '\t\centering\n' +
                              '\t\input{' + aoa_data_directory_name + '/data/cm_aoa/cm_aoa.tikz}\n' +
                              '\t\caption{cm vs $\\alpha$}\n' +
                              '\end{figure}\n'
                              )
        aoa_figures_file.flush()



def read_cl_reference(AOA):
    #values computed with the panel method from xfoil
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

def SetColor(GRD_counter):
    # Set the color
    if GRD_counter < 1:
        return 'red'
    elif GRD_counter < 2:
        return 'blue'
    elif GRD_counter < 3:
        return 'purple'
    elif GRD_counter < 4:
        return 'brown'
    elif GRD_counter < 5:
        return 'violet'
    elif GRD_counter < 6:
        return 'orange'
    elif GRD_counter < 7:
        return 'magenta'
    elif GRD_counter < 8:
        return 'gray'
    elif GRD_counter < 9:
        return 'teal'
    elif GRD_counter < 10:
        return 'black'

def add_cl_to_tikz(input_dir_path, cl_data_directory_name, GRD, GRD_counter):

    color = SetColor(GRD_counter)

    cl_tikz_file_name = input_dir_path + '/plots/cl/' + cl_data_directory_name + '/cl.tikz'
    cl_p_results_file_name_tmp = 'cl_p_results_GRD_' +  str(GRD) + '.dat'
    with open(cl_tikz_file_name, 'a') as cl_tikz_file:
        cl_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {' + cl_p_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Pressure GRD '+ str(GRD) +'}\n\n')
        cl_tikz_file.flush()

    cl_f_results_file_name_tmp = 'cl_f_results_GRD_' +  str(GRD) + '.dat'
    with open(cl_tikz_file_name, 'a') as cl_tikz_file:
        cl_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=diamond,\n' +
            '    ]\n' +
            '    table {' + cl_f_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Far Field GRD '+ str(GRD) +'}\n\n')
        cl_tikz_file.flush()

    cl_j_results_file_name_tmp = 'cl_j_results_GRD_' +  str(GRD) + '.dat'
    with open(cl_tikz_file_name, 'a') as cl_tikz_file:
        cl_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=o,\n' +
            '    ]\n' +
            '    table {' + cl_j_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Jump GRD '+ str(GRD) +'}\n\n')
        cl_tikz_file.flush()

def add_cd_to_tikz(input_dir_path, cd_data_directory_name, GRD, GRD_counter):

    color = SetColor(GRD_counter)

    cd_tikz_file_name = input_dir_path + '/plots/cd/' + cd_data_directory_name + '/cd.tikz'
    cd_p_results_file_name_tmp = 'cd_p_results_GRD_' +  str(GRD) + '.dat'
    with open(cd_tikz_file_name, 'a') as cd_tikz_file:
        cd_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {' + cd_p_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Pressure GRD '+ str(GRD) +'}\n\n')
        cd_tikz_file.flush()

    cd_f_results_file_name_tmp = 'cd_f_results_GRD_' +  str(GRD) + '.dat'
    with open(cd_tikz_file_name, 'a') as cd_tikz_file:
        cd_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=diamond,\n' +
            '    ]\n' +
            '    table {' + cd_f_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Far Field GRD '+ str(GRD) +'}\n\n')
        cd_tikz_file.flush()

def add_cm_to_tikz(input_dir_path, cm_data_directory_name, GRD, GRD_counter):

    color = SetColor(GRD_counter)

    cm_tikz_file_name = input_dir_path + '/plots/cm/' + cm_data_directory_name + '/cm.tikz'
    cm_p_results_file_name_tmp = 'cm_p_results_GRD_' +  str(GRD) + '.dat'
    with open(cm_tikz_file_name, 'a') as cm_tikz_file:
        cm_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {' + cm_p_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Pressure GRD '+ str(GRD) +'}\n\n')
        cm_tikz_file.flush()

def add_cl_error_to_tikz(input_dir_path, cl_error_data_directory_name, GRD, GRD_counter):

    color = SetColor(GRD_counter)

    cl_error_tikz_file_name = input_dir_path + '/plots/cl_error/' + cl_error_data_directory_name + '/cl_error.tikz'
    cl_error_p_results_file_name_tmp = 'cl_error_p_results_GRD_' +  str(GRD) + '.dat'
    with open(cl_error_tikz_file_name, 'a') as cl_error_tikz_file:
        cl_error_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {' + cl_error_p_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Pressure GRD '+ str(GRD) +'}\n\n')
        cl_error_tikz_file.flush()

def add_cd_error_to_tikz(input_dir_path, cd_error_data_directory_name, GRD, GRD_counter):

    color = SetColor(GRD_counter)

    cd_error_tikz_file_name = input_dir_path + '/plots/cd_error/' + cd_error_data_directory_name + '/cd_error.tikz'
    cd_error_p_results_file_name_tmp = 'cd_error_p_results_GRD_' +  str(GRD) + '.dat'
    with open(cd_error_tikz_file_name, 'a') as cd_error_tikz_file:
        cd_error_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {' + cd_error_p_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Pressure GRD '+ str(GRD) +'}\n\n')
        cd_error_tikz_file.flush()

def add_cm_error_to_tikz(input_dir_path, cm_error_data_directory_name, GRD, GRD_counter):

    color = SetColor(GRD_counter)

    cm_error_tikz_file_name = input_dir_path + '/plots/cm_error/' + cm_error_data_directory_name + '/cm_error.tikz'
    cm_error_p_results_file_name_tmp = 'cm_error_p_results_GRD_' +  str(GRD) + '.dat'
    with open(cm_error_tikz_file_name, 'a') as cm_error_tikz_file:
        cm_error_tikz_file.write('\n\n\\addplot[\n' +
            '    color=' + color + ',\n' +
            '    mark=square,\n' +
            '    ]\n' +
            '    table {' + cm_error_p_results_file_name_tmp + '};  \n' +
            '    \\addlegendentry{Pressure GRD '+ str(GRD) +'}\n\n')
        cm_error_tikz_file.flush()

def add_cl_reference_to_tikz(input_dir_path, cl_data_directory_name):
    cl_tikz_file_name = input_dir_path + '/plots/cl/' + cl_data_directory_name + '/cl.tikz'
    cl_ref_file_name_tmp = 'cl_ref.dat'
    with open(cl_tikz_file_name, 'a') as cl_tikz_file:
        cl_tikz_file.write('\n\n\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    ]\n' +
            '    table {' + cl_ref_file_name_tmp + '};  \n' +
            '    \\addlegendentry{XFLR5}\n\n')
        cl_tikz_file.flush()

def add_cd_reference_to_tikz(input_dir_path, cd_data_directory_name):
    cd_tikz_file_name = input_dir_path + '/plots/cd/' + cd_data_directory_name + '/cd.tikz'
    cd_ref_file_name_tmp = 'cd_ref.dat'
    with open(cd_tikz_file_name, 'a') as cd_tikz_file:
        cd_tikz_file.write('\n\n\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    ]\n' +
            '    table {' + cd_ref_file_name_tmp + '};  \n' +
            '    \\addlegendentry{XFLR5}\n\n')
        cd_tikz_file.flush()

def add_cm_reference_to_tikz(input_dir_path, cm_data_directory_name):
    cm_tikz_file_name = input_dir_path + '/plots/cm/' + cm_data_directory_name + '/cm.tikz'
    cm_ref_file_name_tmp = 'cm_ref.dat'
    with open(cm_tikz_file_name, 'a') as cm_tikz_file:
        cm_tikz_file.write('\n\n\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    ]\n' +
            '    table {' + cm_ref_file_name_tmp + '};  \n' +
            '    \\addlegendentry{XFLR5}\n\n')
        cm_tikz_file.flush()


def close_cl_tikz(input_dir_path, cl_data_directory_name):
    cl_tikz_file_name = input_dir_path + '/plots/cl/' + cl_data_directory_name + '/cl.tikz'
    with open(cl_tikz_file_name, 'a') as cl_tikz_file:
        cl_tikz_file.write('\end{axis}\n' +
            '\end{tikzpicture}')
        cl_tikz_file.flush()

def close_cd_tikz(input_dir_path, cd_data_directory_name):
    cd_tikz_file_name = input_dir_path + '/plots/cd/' + cd_data_directory_name + '/cd.tikz'
    with open(cd_tikz_file_name, 'a') as cd_tikz_file:
        cd_tikz_file.write('\end{axis}\n' +
            '\end{tikzpicture}')
        cd_tikz_file.flush()

def close_cm_tikz(input_dir_path, cm_data_directory_name):
    cm_tikz_file_name = input_dir_path + '/plots/cm/' + cm_data_directory_name + '/cm.tikz'
    with open(cm_tikz_file_name, 'a') as cm_tikz_file:
        cm_tikz_file.write('\end{axis}\n' +
            '\end{tikzpicture}')
        cm_tikz_file.flush()

def close_cl_error_tikz(input_dir_path, cl_error_data_directory_name):
    cl_error_tikz_file_name = input_dir_path + '/plots/cl_error/' + cl_error_data_directory_name + '/cl_error.tikz'
    with open(cl_error_tikz_file_name, 'a') as cl_error_tikz_file:
        cl_error_tikz_file.write('\end{axis}\n' +
            '\end{tikzpicture}')
        cl_error_tikz_file.flush()

def close_cd_error_tikz(input_dir_path, cd_error_data_directory_name):
    cd_error_tikz_file_name = input_dir_path + '/plots/cd_error/' + cd_error_data_directory_name + '/cd_error.tikz'
    with open(cd_error_tikz_file_name, 'a') as cd_error_tikz_file:
        cd_error_tikz_file.write('\end{axis}\n' +
            '\end{tikzpicture}')
        cd_error_tikz_file.flush()

def close_cm_error_tikz(input_dir_path, cm_error_data_directory_name):
    cm_error_tikz_file_name = input_dir_path + '/plots/cm_error/' + cm_error_data_directory_name + '/cm_error.tikz'
    with open(cm_error_tikz_file_name, 'a') as cm_error_tikz_file:
        cm_error_tikz_file.write('\end{axis}\n' +
            '\end{tikzpicture}')
        cm_error_tikz_file.flush()

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

def start_tikz_refinement_plot_file(file_name, title, ylabel):
        with open(file_name, 'w') as tikz_file:
            tikz_file.write('\\begin{tikzpicture}\n' +
                               '\\begin{semilogxaxis}[\n' +
                               '    title={' + title + '},\n' +
                               '    xlabel={ndof},\n' +
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
                               ']\n\n')
            tikz_file.flush()

def create_aoa_tikz_plot_file(file_name, title, ylabel, dat_name, reference_dat_name):
    with open(file_name, 'w') as tikz_file:
        tikz_file.write('\\begin{tikzpicture}\n' +
                           '\\begin{axis}[\n' +
                           '    title={' + title + '},\n' +
                           '    xlabel={$\\alpha\\ [\\degree]$},\n' +
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
                           '    solid,\n' +
                           '    mark=oplus*,\n' +
                           '    mark options={solid},\n' +
                           '    ]\n' +
                           '    table {' + dat_name + '};  \n' +
                           '    \\addlegendentry{Kratos Integral}\n\n' +
                           '\\addplot[\n' +
                           '    color=black,\n' +
                           '    solid,\n' +
                           '    mark=oplus*,\n' +
                           '    mark options={solid},\n' +
                           '    ]\n' +
                           '    table {' + reference_dat_name + '};  \n' +
                           '    \\addlegendentry{XFLR5}\n\n' +
                           '\end{axis}\n' +
                           '\end{tikzpicture}')
        tikz_file.flush()

def create_cd_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cd/data/cd')
    start_tikz_refinement_plot_file(work_dir + '/plots/cd/data/cd/cd.tikz', 'Mesh refinement study', '$c_d[\\unit{-}]$')
    create_main_tex_file(work_dir + '/plots/cd/main_cd.tex', 'figures_cd.tex')

def create_cd_error_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cd_error/data/cd_error')
    start_tikz_refinement_plot_file(work_dir + '/plots/cd_error/data/cd_error/cd_error.tikz', 'Induced drag coefficient relative error', '$\\frac{|c_d - c_{dref}|}{|c_{dref}|}\\cdot100$')
    create_main_tex_file(work_dir + '/plots/cd_error/main_cd_error.tex', 'figures_cd_error.tex')

def create_cl_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cl/data/cl')
    start_tikz_refinement_plot_file(work_dir + '/plots/cl/data/cl/cl.tikz', 'Mesh refinement study', '$c_l[\\unit{-}]$')
    create_main_tex_file(work_dir + '/plots/cl/main_cl.tex', 'figures_cl.tex')

def create_cl_error_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cl_error/data/cl_error')
    start_tikz_refinement_plot_file(work_dir + '/plots/cl_error/data/cl_error/cl_error.tikz', 'Lift coefficient relative error', '$\\frac{|c_l - c_{lref}|}{|c_{lref}|}\\cdot100$')
    create_main_tex_file(work_dir + '/plots/cl_error/main_cl_error.tex', 'figures_cl_error.tex')

def create_cm_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cm/data/cm')
    start_tikz_refinement_plot_file(work_dir + '/plots/cm/data/cm/cm.tikz', 'Mesh refinement study', '$c_m[\\unit{-}]$')
    create_main_tex_file(work_dir + '/plots/cm/main_cm.tex', 'figures_cm.tex')

def create_cm_error_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cm_error/data/cm_error')
    start_tikz_refinement_plot_file(work_dir + '/plots/cm_error/data/cm_error/cm_error.tikz', 'Moment coefficient relative error', '$\\frac{|c_m - c_{mref}|}{|c_{mref}|}\\cdot100$')
    create_main_tex_file(work_dir + '/plots/cm_error/main_cm_error.tex', 'figures_cm_error.tex')

def create_cd_aoa_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cd_aoa/data/cd_a')
    create_aoa_tikz_plot_file(work_dir + '/plots/cd_aoa/data/cd_a/cd_aoa.tikz',  # file_name
                                        'Drag coefficient vs. angle of attack', # title
                                        '$c_d[\\unit{-}]$',                     # ylabel
                                        'cd_aoa.dat',                     # dat_name
                                        'cd_aoa_ref.dat')                   # reference_dat_name

    write_figures_cd_aoa(work_dir + '/plots/cd_aoa')
    create_main_tex_file(work_dir + '/plots/cd_aoa/main_cd_aoa.tex', 'figures_cd_aoa.tex')

def create_cl_aoa_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cl_aoa/data/cl_a')
    create_aoa_tikz_plot_file(work_dir + '/plots/cl_aoa/data/cl_a/cl_aoa.tikz',  # file_name
                                        'Lift vs. angle of attack', # title
                                        '$c_l[\\unit{-}]$',                     # ylabel
                                        'cl_aoa.dat',                     # dat_name
                                        'cl_aoa_ref.dat')                   # reference_dat_name

    write_figures_cl_aoa(work_dir + '/plots/cl_aoa')
    create_main_tex_file(work_dir + '/plots/cl_aoa/main_cl_aoa.tex', 'figures_cl_aoa.tex')

def create_cm_aoa_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cm_aoa/data/cm_a')
    create_aoa_tikz_plot_file(work_dir + '/plots/cm_aoa/data/cm_a/cm_aoa.tikz',  # file_name
                                        'Moment vs. angle of attack', # title
                                        '$c_m[\\unit{-}]$',                     # ylabel
                                        'cm_aoa.dat',                     # dat_name
                                        'cm_aoa_ref.dat')                   # reference_dat_name

    write_figures_cm_aoa(work_dir + '/plots/cm_aoa')
    create_main_tex_file(work_dir + '/plots/cm_aoa/main_cm_aoa.tex', 'figures_cm_aoa.tex')

def create_cp_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cp/plots')
    create_plot_directory_tree(work_dir + '/plots/cp/data/cp')

    references_input_directory_name = os.getcwd() + '/references/cp'
    references_output_directory_name = work_dir + '/plots/cp/data/cp'
    if os.path.exists(references_output_directory_name):
        shutil.rmtree(references_output_directory_name)
    shutil.copytree(references_input_directory_name,
                    references_output_directory_name)

    create_main_tex_file(work_dir + '/plots/cp/main_cp.tex', work_dir + '/plots/cp/figures_cp.tex')

def create_cp_100_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cp_section_100/plots')
    create_plot_directory_tree(work_dir + '/plots/cp_section_100/data/cp')

    references_input_directory_name = os.getcwd() + '/references/cp'
    references_output_directory_name = work_dir + '/plots/cp_section_100/data/cp'
    if os.path.exists(references_output_directory_name):
        shutil.rmtree(references_output_directory_name)
    shutil.copytree(references_input_directory_name,
                    references_output_directory_name)

    create_main_tex_file(work_dir + '/plots/cp_section_100/main_cp_100.tex', work_dir + '/plots/cp_section_100/figures_cp.tex')

def create_cp_150_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cp_section_150/plots')
    create_plot_directory_tree(work_dir + '/plots/cp_section_150/data/cp')

    references_input_directory_name = os.getcwd() + '/references/cp'
    references_output_directory_name = work_dir + '/plots/cp_section_150/data/cp'
    if os.path.exists(references_output_directory_name):
        shutil.rmtree(references_output_directory_name)
    shutil.copytree(references_input_directory_name,
                    references_output_directory_name)

    create_main_tex_file(work_dir + '/plots/cp_section_150/main_cp_150.tex', work_dir + '/plots/cp_section_150/figures_cp.tex')

def create_cp_180_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/cp_section_180/plots')
    create_plot_directory_tree(work_dir + '/plots/cp_section_180/data/cp')

    references_input_directory_name = os.getcwd() + '/references/cp'
    references_output_directory_name = work_dir + '/plots/cp_section_180/data/cp'
    if os.path.exists(references_output_directory_name):
        shutil.rmtree(references_output_directory_name)
    shutil.copytree(references_input_directory_name,
                    references_output_directory_name)

    create_main_tex_file(work_dir + '/plots/cp_section_180/main_cp_180.tex', work_dir + '/plots/cp_section_180/figures_cp.tex')

def create_potential_jump_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/potential_jump/plots')
    create_plot_directory_tree(work_dir + '/plots/potential_jump/data/potential_jump')

    with open(work_dir + '/plots/potential_jump/data/potential_jump/jump.tikz', 'w') as tikz_file:
        tikz_file.write('\\begin{tikzpicture}\n' +
                           '\\begin{axis}[\n' +
                           '    title={Potential jump},\n' +
                           '    xlabel={$y$},\n' +
                           '    ylabel={Potential jump($y$)},\n' +
                           '    ymajorgrids=true,\n' +
                           '    xmajorgrids=true,\n' +
                           '    grid style=dashed,\n' +
                           '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
                           '    width=12cm\n' +
                           ']\n\n' +
                           '\\addplot[\n' +
                           '    color=blue,\n' +
                           '    only marks,\n' +
                           '    mark=*,\n' +
                           '    ]\n' +
                           '    table {potential_jump_results.dat};  \n' +
                           '    \\addlegendentry{Trailing edge}\n\n' +
                           '\\addplot[\n' +
                           '    color=red,\n' +
                           '    only marks,\n' +
                           '    mark=*,\n' +
                           '    ]\n' +
                           '    table {potential_jump_trefftz_results.dat};  \n' +
                           '    \\addlegendentry{Trefftz plane outlet cut}\n\n' +
                           '\end{axis}\n' +
                           '\end{tikzpicture}')
        tikz_file.flush()

    create_main_tex_file(work_dir + '/plots/potential_jump/main_potential_jump.tex', work_dir + '/plots/potential_jump/figures_jump.tex')

def create_newton_convergence_plots_directory_tree(work_dir):
    create_plot_directory_tree(work_dir + '/plots/newton_convergence/data/convergence')

    with open(work_dir + '/plots/newton_convergence/data/convergence/convergence.tikz', 'w') as tikz_file:
        tikz_file.write('\\begin{tikzpicture}\n' +
                           '\\begin{semilogyaxis}[\n' +
                           '    title={Nonlinear Convergence Analysis},\n' +
                           '    xlabel={Number of iterations},\n' +
                           '    ylabel={Residual absolute norm $\\nicefrac{|{\\bf R}|}{n_{dof}}$},\n' +
                           '    ymajorgrids=true,\n' +
                           '    xmajorgrids=true,\n' +
                           '    grid style=dashed,\n' +
                           '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
                           '    width=12cm\n' +
                           ']\n\n' +
                           '\\addplot[\n' +
                           '    color=red,\n' +
                           '    mark=square,\n' +
                           '    ]\n' +
                           '    table {convergence_results.dat};  \n' +
                           '\end{semilogyaxis}\n' +
                           '\end{tikzpicture}')
        tikz_file.flush()

    create_main_tex_file(work_dir + '/plots/newton_convergence/main_convergence.tex', work_dir + '/plots/newton_convergence/figures_newton_convergence.tex')


def create_plots_directory_tree(work_dir):
    create_cd_plots_directory_tree(work_dir)
    create_cd_error_plots_directory_tree(work_dir)
    create_cl_plots_directory_tree(work_dir)
    create_cl_error_plots_directory_tree(work_dir)
    create_cm_plots_directory_tree(work_dir)
    create_cm_error_plots_directory_tree(work_dir)
    create_cd_aoa_plots_directory_tree(work_dir)
    create_cl_aoa_plots_directory_tree(work_dir)
    create_cm_aoa_plots_directory_tree(work_dir)
    create_cp_plots_directory_tree(work_dir)
    create_cp_100_plots_directory_tree(work_dir)
    create_cp_150_plots_directory_tree(work_dir)
    create_cp_180_plots_directory_tree(work_dir)
    create_potential_jump_plots_directory_tree(work_dir)
    create_newton_convergence_plots_directory_tree(work_dir)



