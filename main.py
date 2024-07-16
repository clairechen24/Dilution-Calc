from tkinter import *

# calculations 
def load_method():
    output_message = ""

    #step 1
    conc_string = conc.get()
    conc_values = conc_string.split()
    concentrations = {f'c{i+1}': float(value) for i, value in enumerate(conc_values)}
    globals().update(concentrations)
    
   
    #step 2
    conversion_factors = {
        "mol/L": 1e3,
        "mmol/L": 1,
        "Mmol/L": 1e-3,
        "nmol/L": 1e-6
    }
    
    C0 = float(stocksol.get()) * conversion_factors[clicked.get()]
    globals()['C0'] = C0
    
    #step 3
    V1 = float(initialvol.get())
    globals()['V1'] = V1

    if 'c1' in concentrations:
        C1 = concentrations['c1']
        V0 = C1 * V1 / C0
        Vh2O = V1 - V0
        
        output_message += f"Add {V0:.2f} mL of stock solution\n"
        output_message += f"Add {Vh2O:.2f} mL of water\n"
        output_message += "******************************************\n"
    
    #step 4 
    total_volume = V1
    for i in range(1, len(concentrations)):
        current_conc = concentrations[f'c{i}']
        next_conc = concentrations[f'c{i+1}']

        if current_conc < next_conc:
            Vi_0 = ((next_conc - current_conc) * total_volume) / (C0 - next_conc)
            Vi_plus_1 = Vi_0 + total_volume
            output_message += f"Add {Vi_0:.2f} mL of stock solution.\n"
            output_message += f"Total volume is {Vi_plus_1:.2f} mL.\n"
            output_message += "******************************************\n"
            total_volume = Vi_plus_1
        elif current_conc > next_conc:
            Vi_plus_1 = (current_conc * total_volume) / next_conc
            Vh2O_i = Vi_plus_1 - total_volume
            output_message += f"Add {Vh2O_i:.2f} mL of water.\n"
            output_message += f"Total volume is {Vi_plus_1:.2f} mL. \n"
            output_message += "******************************************"
            total_volume = Vi_plus_1

    #export method & results
    result_text.delete('1.0', END)

    result_text.insert(END, output_message)

    if var.get() == 1:
        export_method(output_message)

    if var1.get() == 1:
        export_results(output_message)


def export_method(method_details):
    filename = file_name.get() + "_method.txt"
    with open(filename, 'w') as file:
        file.write("Method Details:\n")
        file.write(method_details)
    print(f"Method details exported to {filename}")


def export_results(results):
    filename = file_name.get() + "_results.txt"
    with open(filename, 'w') as file:
        file.write("Calculation Results:\n")
        file.write(results)
    print(f"Calculation results exported to {filename}")

# interface
main = Tk()
main.title("Dilution Calculator")

#file name
fileName_label = Label(main, text = "File name")
fileName_label.grid(row=0, column=0)

file_name = Entry(main)
file_name.grid(row=0, column=1)
filetxt = Label(main, text = ".txt")
filetxt.grid(row=0, column = 2)

#[stock solution]
stocksol_label = Label(main, text="Concentration of Stock Solution")
stocksol_label.grid(row=1, column=0)

stocksol = Entry(main)
stocksol.grid(row=1, column=1)

clicked = StringVar()
clicked.set("mmol/L")
drop = OptionMenu(main, clicked, "mol/L", "mmol/L", "Mmol/L", "nmol/L")
drop.grid(row=1, column=2)

#required concentrations 
conc_label = Label(main, text="Required Concentrations (seperated by a space)")
conc_label.grid(row=2, column=0)

conc = Entry(main)
conc.grid(row=2, column=1)

clicked = StringVar()
clicked.set("mmol/L")
drop = OptionMenu(main, clicked, "mol/L", "mmol/L", "Mmol/L", "nmol/L")
drop.grid(row=2, column=2)

#max vol of beaker
maxvol_label = Label(main, text="Maximum Volume of Beaker")
maxvol_label.grid(row=3, column=0)

maxvol = Entry(main)
maxvol.grid(row=3, column=1)
unit1 = Label(main, text="mL")
unit1.grid(row=3,column=2)

#min vol of beaker
minvol_label = Label(main, text="Minimum Volume of Beaker")
minvol_label.grid(row=4, column=0)

minvol = Entry(main)
minvol.grid(row=4, column=1)
unit2 = Label(main, text="mL")
unit2.grid(row=4,column=2)

#min vol of pipette
minpip_label = Label(main, text="Minimum Volume of Pipette Gun")
minpip_label.grid(row=5, column=0)

minpip = Entry(main)
minpip.grid(row=5, column=1)
unit3 = Label(main, text="mL")
unit3.grid(row=5,column=2)

#initial volume
initialvol_label = Label(main, text="Initial Volume")
initialvol_label.grid(row=6, column=0)

initialvol = Entry(main)
initialvol.grid(row=6, column=1)
unit4 = Label(main, text="mL")
unit4.grid(row=6,column=2)

#load method
loadmethod_button = Button(main, text="Load Method", command=load_method)
loadmethod_button.grid(row=7, column=0)

var = IntVar()
c = Checkbutton(main, text="Export Method", variable=var)
c.grid(row=7, column=1)

var1 = IntVar()
c1 = Checkbutton(main, text="Export Results", variable=var1)
c1.grid(row=7, column=2)

#results widget
result_text = Text(main, height=10, width=50)
result_text.grid(row=9, column=0, columnspan=3)

main.mainloop()
