from tkinter import *

def load_method():
    output_message = ""

    #split required concentration values by space
    conc_string = conc.get()
    conc_values = conc_string.split()
    concentrations = {f'c{i+1}': float(value) for i, value in enumerate(conc_values)}
    globals().update(concentrations)
    
   
    #convert to mmol/L
    conversion_factors = {
        "mol/L": 1e3,
        "mmol/L": 1,
        "Mmol/L": 1e-3,
        "nmol/L": 1e-6
    }
    
    C0 = float(stocksol.get()) * conversion_factors[clicked.get()]
    globals()['C0'] = C0
    

    V1 = float(initialvol.get())
    globals()['V1'] = V1

    min_vol = float(minvol.get())
    max_vol = float(maxvol.get())

    if min_vol > V1:
        result_text.delete('1.0', END)
        result_text.insert(END, "Not valid: Minimum volume of beaker is greater than initial volume.")
        return
    

    if 'c1' in concentrations:
        C1 = concentrations['c1']
        V0 = C1 * V1 / C0
        Vh2O = V1 - V0
        
        output_message += f"Add {V0:.2f} mL of stock solution\n"
        output_message += f"Add {Vh2O:.2f} mL of water\n"
        output_message += "*****************************************************************\n"
    

    total_volume = V1
    current_conc = concentrations['c1']
    
    for i in range(2, len(concentrations) + 1):
        next_conc = concentrations[f'c{i}']
        Vi_0 = ((next_conc - current_conc) * total_volume) / (C0 - next_conc)
        Vi_plus_1 = Vi_0 + total_volume

        if current_conc < next_conc:
            Vi_0 = ((next_conc - current_conc) * total_volume) / (C0 - next_conc)
            Vi_plus_1 = Vi_0 + total_volume
            if Vi_plus_1 > max_vol:
                output_message += f"Total volume {Vi_plus_1:.2f} mL exceeds maximum beaker volume.\n"
                output_message += f"Last valid volume: {total_volume:.2f} mL, concentration: {current_conc:.2f} mmol/L.\n"
                output_message += "Continuing calculations with last valid volume and concentration.\n"
                total_volume = max_vol  # Set total volume to max volume
                
                Vh2O_i = Vi_plus_1 - total_volume
                next_conc = (C0 * total_volume) / (total_volume - Vi_0)  # Adjust next_conc for continuation
                C0 = (current_conc * total_volume) / (total_volume - Vh2O_i)  # Update C0 for next steps

                output_message += f"New concentration: {next_conc:.2f} mmol/L\n"
                output_message += "*****************************************************************\n"
                break
        
            else:
                output_message += f"Add {Vi_0:.2f} mL of stock solution.\n"
                output_message += f"Total volume is {Vi_plus_1:.2f} mL.\n"
                output_message += "*****************************************************************\n"
                total_volume = Vi_plus_1

        elif current_conc > next_conc:
            Vi_plus_1 = (current_conc * total_volume) / next_conc
            Vh2O_i = Vi_plus_1 - total_volume
            if Vi_plus_1 > max_vol:
                output_message += f"Total volume {Vi_plus_1:.2f} mL exceeds maximum beaker volume.\n"
                output_message += f"Last valid volume: {total_volume:.2f} mL, concentration: {current_conc:.2f} mmol/L.\n"
                output_message += "Continuing calculations with last valid volume and concentration.\n"
                total_volume = max_vol  # Set total volume to max volume
                next_conc = (current_conc * total_volume) / (total_volume - Vh2O_i)  # Adjust next_conc for continuation
                output_message += f"New concentration: {next_conc:.2f} mmol/L\n"
                output_message += "*****************************************************************\n"
                break
            
        else:
            output_message += f"Add {Vh2O_i:.2f} mL of water.\n"
            output_message += f"Total volume is {Vi_plus_1:.2f} mL.\n"
            output_message += "****************************************************************\n"
            total_volume = Vi_plus_1

    remaining_concentrations = dict(list(concentrations.items())[i-1:])

    for i, (key, next_conc) in enumerate(remaining_concentrations.items(), start=i):
        if current_conc < next_conc:
            Vi_0 = ((next_conc - current_conc) * total_volume) / (C0 - next_conc)
            Vi_plus_1 = Vi_0 + total_volume
            if Vi_plus_1 > max_vol:
                output_message += f"Total volume {Vi_plus_1:.2f} mL exceeds maximum beaker volume.\n"
                output_message += f"Add {max_vol - total_volume:.2f} mL of water to reach maximum volume.\n"
                next_conc = (current_conc * max_vol) / (max_vol - (max_vol - total_volume))
                output_message += f"New concentration: {next_conc:.2f} mmol/L.\n"
                total_volume = max_vol
                output_message += "Continuing calculations with the remaining volume and new concentration.\n"
                current_conc = next_conc
                break
            
            else:
                output_message += f"Add {Vi_0:.2f} mL of stock solution.\n"
                output_message += f"Total volume is {Vi_plus_1:.2f} mL.\n"
                output_message += "*****************************************************************\n"
                total_volume = Vi_plus_1

        elif current_conc > next_conc:
            Vi_plus_1 = (current_conc * total_volume) / next_conc
            Vh2O_i = Vi_plus_1 - total_volume
            if Vi_plus_1 > max_vol:
                output_message += f"Total volume {Vi_plus_1:.2f} mL exceeds maximum beaker volume.\n"
                output_message += f"Add {max_vol - total_volume:.2f} mL of water to reach maximum volume.\n"
                next_conc = (current_conc * max_vol) / max_vol
                output_message += f"New concentration: {next_conc:.2f} mmol/L.\n"
                total_volume = max_vol
                output_message += "Continuing calculations with the remaining volume and new concentration.\n"
                current_conc = next_conc
                break
            
            else:
                output_message += f"Add {Vh2O_i:.2f} mL of water.\n"
                output_message += f"Total volume is {Vi_plus_1:.2f} mL.\n"
                output_message += "*****************************************************************\n"
                total_volume = Vi_plus_1

        current_conc = next_conc

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

main = Tk()
main.title("Dilution Calculator")
main.configure(bg="#afd7ed")

#file name
fileName_label = Label(main, text = "File name", bg="#afd7ed", fg="black")
fileName_label.grid(row=0, column=0)

file_name = Entry(main)
file_name.grid(row=0, column=1)
filetxt = Label(main, text = ".txt", bg="#afd7ed", fg="black")
filetxt.grid(row=0, column = 2)

#[stock solution]
stocksol_label = Label(main, text="Concentration of Stock Solution", bg="#afd7ed", fg="black")
stocksol_label.grid(row=1, column=0)

stocksol = Entry(main)
stocksol.grid(row=1, column=1)

clicked = StringVar()
clicked.set("mmol/L")
drop = OptionMenu(main, clicked, "mol/L", "mmol/L", "Mmol/L", "nmol/L")
drop.grid(row=1, column=2)
drop.configure(bg="#afd7ed", fg="black")

#required concentrations 
conc_label = Label(main, text="Required Concentrations (seperated by a space)", bg="#afd7ed", fg="black")
conc_label.grid(row=2, column=0)

conc = Entry(main)
conc.grid(row=2, column=1)

clicked = StringVar()
clicked.set("mmol/L")
drop = OptionMenu(main, clicked, "mol/L", "mmol/L", "Mmol/L", "nmol/L")
drop.grid(row=2, column=2)
drop.configure(bg="#afd7ed", fg="black")

#max vol of beaker
maxvol_label = Label(main, text="Maximum Volume of Beaker", bg="#afd7ed", fg="black")
maxvol_label.grid(row=3, column=0)

maxvol = Entry(main)
maxvol.grid(row=3, column=1)
unit1 = Label(main, text="mL", bg="#afd7ed", fg="black")
unit1.grid(row=3,column=2)

#min vol of beaker
minvol_label = Label(main, text="Minimum Volume of Beaker", bg="#afd7ed", fg="black")
minvol_label.grid(row=4, column=0)

minvol = Entry(main)
minvol.grid(row=4, column=1)
unit2 = Label(main, text="mL", bg="#afd7ed", fg="black")
unit2.grid(row=4,column=2)

#min vol of pipette
minpip_label = Label(main, text="Minimum Volume of Pipette Gun", bg="#afd7ed", fg="black")
minpip_label.grid(row=5, column=0)

minpip = Entry(main)
minpip.grid(row=5, column=1)
unit3 = Label(main, text="mL", bg="#afd7ed", fg="black")
unit3.grid(row=5,column=2)

#initial volume
initialvol_label = Label(main, text="Initial Volume", bg="#afd7ed", fg="black")
initialvol_label.grid(row=6, column=0)

initialvol = Entry(main)
initialvol.grid(row=6, column=1)
unit4 = Label(main, text="mL", bg="#afd7ed", fg="black")
unit4.grid(row=6,column=2)

#load method
loadmethod_button = Button(main, text="Load Method", command=load_method, bg="#afd7ed")
loadmethod_button.grid(row=7, column=0)

var = IntVar()
c = Checkbutton(main, text="Export Method", variable=var, bg="#afd7ed", fg="black")
c.grid(row=7, column=1)

var1 = IntVar()
c1 = Checkbutton(main, text="Export Results", variable=var1, bg="#afd7ed", fg="black")
c1.grid(row=7, column=2)

#results widget
result_text = Text(main, height=20, width=65)
result_text.grid(row=9, column=0, columnspan=3)

main.mainloop()
