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


