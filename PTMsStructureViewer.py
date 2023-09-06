import tkinter as tk
from tkinter import ttk
import Pmw
# from pyrosetta import *



psvroot=tk.Tk()


#############################################################################################

class ptmstructure:

    '''Main window for PTMS`s Structure Viewer'''

    def __init__(self, parent):

        ######## frames ########

        self.header=tk.Frame(psvroot,height=50,bg='black')
        self.main=tk.Frame(psvroot, bg='#DADADA')
        self.bottom=tk.Frame(psvroot,height=25,bg='#887404')

        Pmw.initialise(fontScheme='pmwl')

        ######## menubar ########

        menubar=Pmw.MenuBar(parent,
                            hull_borderwidth=1,
                            hull_relief='raised')
        menubar.addmenu('File','select file')
        menubar.addmenuitem('File','command',
                            command=self.load_table,
                            label='Load file', underline=True)
        menubar.addmenuitem('File','separator')
        menubar.addmenuitem('File','command',
                            command=print('ciao'),
                            label='Enter manually')
        
        self.menubar=menubar
        self.menubar.pack(fill='x')

        ######## label for header ########

        header=tk.Label(self.header,
                        text="PTMs's Structure Viewer",
                        font=('arial',12,'bold'),
                        bg='black',
                        fg='white',
                        )
        self.header_text=header

        ######## frame for loaded data ########


        self.main_load=tk.LabelFrame(self.main,height=50,
                                bg='#DADADA',
                                padx=10,
                                pady=20,
                                text='Load Data from file')
    
        


        ######## frame for manually data ########

        self.main_manually=tk.LabelFrame(self.main,
                                bg='#DADADA',
                                text='Load protein manually',
                                height=50)
        
        id_label=tk.Label(self.main_manually, text='ID_uniprot:')
        id_uniprot=tk.StringVar()
        self.id_uniprot=tk.Entry(self.main_manually, textvariable=id_uniprot)

        pdb_label=tk.Label(self.main_manually,text='PDB_id')
        id_pdb=tk.StringVar()
        self.id_pdb=tk.Entry(self.main_manually, textvariable=id_pdb)

        modification_label=tk.Label(self.main_manually,text='Modification')
        modification=tk.StringVar()
        self.modification=tk.Entry(self.main_manually, textvariable=modification)

        residue_label=tk.Label(self.main_manually, text='Residue')
        residue=tk.StringVar()
        self.residue=tk.Entry(self.main_manually, textvariable=residue)

        position_label=tk.Label(self.main_manually, text='Position')
        position=tk.StringVar()
        self.position=tk.Entry(self.main_manually, textvariable=position)

        self.buton_manually=tk.Button(self.main_manually,
                                    text='Submit',
                                    command=self.get_values)
        

        id_label.grid(row=0,column=0, sticky='nsew')
        self.id_uniprot.grid(row=0, column=1,sticky='nswe')

        pdb_label.grid(row=0,column=2,sticky='nsew')
        self.id_pdb.grid(row=0, column=3,sticky='nsew')

        modification_label.grid(row=0, column=4, sticky='nsew')
        self.modification.grid(row = 0, column = 5,sticky='nwe')

        residue_label.grid(row=0, column=6, sticky='nswe')
        self.residue.grid(row = 0, column = 7, sticky = 'nswe')

        position_label.grid(row=0, column=8, sticky='nswe')
        self.position.grid(row = 0, column = 9, sticky = 'nswe')

        self.buton_manually.grid(row=1, column=5, sticky='swe')

        self.main_manually.grid_rowconfigure(1, weight=1)
        self.main_manually.grid_columnconfigure(5, weight=1)


        #### Pack frames ####
        
        self.header.pack(fill='both', side='top',pady=0)
        self.header_text.pack(fill='both')
        self.main.pack(fill='both', expand=1)
        self.bottom.pack(fill='both',side='bottom')
        self.main_load.pack(fill='x',side='top',pady=20)
        self.main_manually.pack(fill='both', expand=0)
        


    def load_table(self):

        '''
        Create a tree to visualize data from a local file
        and select a protein to visualize with PTMS
        '''
        import pandas as pd
        from tkinter import filedialog
        path=filedialog.askopenfilename()
        file=pd.read_excel(path)
        total_rows=len(file)

        #### code for creating tree ####

        tree=ttk.Treeview(self.main_load, columns=tuple(file.columns), show='headings')
        tree.heading('ID_uniprot', text='ID_uniprot')
        tree.heading('PDB_id', text='PDB_id')
        tree.heading('Modification', text='Modification')
        tree.heading('Residue', text='Residue')
        tree.heading('Position', text='Position')


        #### code for creating table ####
        values=[]
        for i in range(total_rows):
            values.append(tuple(file.iloc[i,:].values))

        for value in values:
            tree.insert('',tk.END, values=value)

        scrollbar = ttk.Scrollbar(self.main_load, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right',fill='y')

        scrollbar_x=ttk.Scrollbar(self.main_load,orient=tk.HORIZONTAL,command=tree.xview)
        tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(side='bottom', fill='x')

        tree.pack(fill='both', side='top', padx=20)

    def get_values(self):

        from tkinter.messagebox import showerror,showinfo

        ### get values ###

        try:

            valores={}
            valores['id_uniprot']=self.id_uniprot.get()
            valores['pdb']=self.id_pdb.get()
            valores['modification']=self.modification.get()
            valores['residue']=self.residue.get()
            valores['position']=self.position.get()

            self.id_uniprot.delete(0, tk.END)
            self.id_pdb.delete(0, tk.END)
            self.modification.delete(0, tk.END)
            self.residue.delete(0, tk.END)
            self.position.delete(0, tk.END)

            print(valores)

            if valores['id_uniprot']!='':

                showinfo(message='Protein {} was succesfully loaded'.format(valores['id_uniprot']),
                                title='Great!')

                return valores

            else:

                showerror(message='Something is wrong with the protein',
                                title='Ups!')
                    
        except:
            print('bruh')
        

        

        ### success message ###
        



ejemplo=ptmstructure(psvroot)
psvroot.title("PTMs's Structure Viewer")
psvroot.geometry('1000x500')
psvroot.mainloop()


# def __init__(self):
#     '''Add PyTMs to PyMOL Plugin menu'''
#     # trigger PyMOL 2.0 legacy initialization
#     self.root

#     self.menuBar.addmenuitem('Plugin', 'separator')
#     self.menuBar.addmenuitem('Plugin', 'command',
#                              "PTMS's Structure Viewer",
#                              label = 'PSV',
#                              command = open_pytms)
#     self.menuBar.addmenuitem('Plugin', 'separator')


# def open_pytms():
#     '''opens main dialog'''
#     global psvroot
#     global pytmsvar
#     psvroot = tk.Tk()
#     psvroot.title("PTMs's Structure Viewer")
#     psvroot.geometry('1000x500')
#     psvroot.resizable(1,1) # prevent/allow rezise
#     Pmw.initialise()
#     pytmsvar = ptmstructure(psvroot)
#     psvroot.mainloop()