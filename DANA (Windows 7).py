def DANA(directory):
    import matplotlib.pyplot as plt
    import os
    from pathlib import Path
    import pandas as pd
    import warnings
    import xlrd
    warnings.filterwarnings('ignore')

    try:
        directory = str(directory)

        directory_str = 'C:\\Users\\Bioconsortia Inc\\Desktop\\HPLC Export Files\\{}\\'.format(directory)
        l = os.listdir(directory_str)
        file_names = [x.split('.')[0] for x in l if x.endswith('.xls')]

        # Grabbing all sample names within the directory
        samples_list = []
        # pathlist = Path(directory_str).rglob('*.xls')
        pathnames = []
        for item in l:
            if item.endswith('.xls'):
                pathnames.append(directory_str + item)

        for path in pathnames:
            path_in_str = str(path)
            wb = xlrd.open_workbook(path_in_str, logfile = open(os.devnull, 'w'))
            samples_list.append(pd.read_excel(wb, 'Integration')[41:])


    except:
        print('Sorry, I could not find that directory')

    try:
        # Adding back the column names to avoid confusion
        new_list = []
        for isolate in samples_list:
            isolate.rename(columns={'Chromatogram and Results': 'No.', 'Unnamed: 1': 'Peak Name',
                                    'Unnamed: 2': 'Retention Time (min)', 'Unnamed: 3': 'Area (mAU*min)',
                                    'Unnamed: 4': 'Height (mAU)', 'Unnamed: 5': 'Relative Area %',
                                    'Unnamed: 6': 'Relative Height %', 'Unnamed: 7': 'Amount'}, inplace=True)
            new_list.append(isolate[isolate['No.'] != 'n.a.'])

        # Splitting the data by retention time into iturins (<10.3), fengycins (10.3<x<17.3), and surfactins (>17.3)
        iturin = []
        fengycin = []
        surfactin = []
        for each in new_list:
            each.drop(each.tail(1).index, inplace=True)
            iturins = each[each['Retention Time (min)'] <= 10.3]['Area (mAU*min)'].sum()
            fengycins = each[(each['Retention Time (min)'] < 17.3) & (each['Retention Time (min)'] > 10.3)][
                'Area (mAU*min)'].sum()
            surfactins = each[each['Retention Time (min)'] >= 17.3]['Area (mAU*min)'].sum()

            iturin.append(iturins)
            fengycin.append(fengycins)
            surfactin.append(surfactins)
        
        temp = [sum(x) for x in zip(iturin, fengycin)]
        temp2 = [sum(y) for y in zip(temp, surfactin)]

        df = pd.DataFrame({'Iturins': iturin, 'Fengycins': fengycin, 'Surfactins': surfactin, 'Total': temp2},
                          index=file_names)
        print(df)
        
        # Plotting the I, F, S, and total lipopeptides.
        plt.bar(file_names, iturin)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Iturin Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        plt.bar(file_names, fengycin)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Fengycin Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        plt.bar(file_names, surfactin)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Surfactin Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        plt.bar(file_names, temp2)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Total Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        df.plot.bar()
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('All Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

    except:
        print('Something went wrong!')



def main():
    count = 0
    print('My name is DANA, your HPLC data analysis assistant.')
    while count == 0:
        directory = input('Please enter the folder name where your HPLC excel data is stored: ')
        DANA(directory)
        mid_var = input('Would you like to analyze another experiment? (Y/N) ')
        if mid_var.upper() == 'Y' or mid_var.upper() == 'YES'.upper() or mid_var == 'Yes':
            continue
        elif mid_var.upper() == 'N' or mid_var.upper() == 'NO'.upper() or mid_var == 'No':
            count += 1
        else:
            print("I'll pretend your said yes.")
    end_var = input('Glad I could assist you today. Please press ENTER to exit.')

if __name__ == '__main__':
    main()
