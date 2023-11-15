import tkinter as tk
from tkinter import ttk
import Pmw
from tkinter.messagebox import *
from pyrosetta import *
pyrosetta.init()
from pymol import cmd
#

# psvroot=tk.Tk()


#############################################################################################

class ptmstructure:

    '''Main window for PTMS`s Structure Viewer'''

    def __init__(self, parent):

        
        ######## frames ########

        self.header=tk.Frame(psvroot,height=50,bg='black')
        self.main=tk.Frame(psvroot, bg='#DADADA')
        self.bottom=tk.Frame(psvroot,height=25,bg='#887404')
        self.valores={'id_uniprot':'',
        'pdb':'',
        'modification':'',
        'residue':'',
        'position':''}
        self.len_protein=''
        self.annotated_sequence=''

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
                            label='Enter manually',
                            command=self.display_manually,
                            underline=True)
        
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
        self.tree_frame=tk.Frame(self.main_load,
                                 bg='#DADADA')
        self.load_button=tk.Button(self.main_load, text='submit',
                                   command=self.get_file_values)

    
        ######## frame for manually data ########

        self.main_manually=tk.LabelFrame(self.main,
                                bg='#DADADA',
                                text='Load protein manually',
                                height=50)
        
        id_label=tk.Label(self.main_manually, text='ID_uniprot:')
        id_uniprot=tk.StringVar()
        self.id_uniprot=tk.Entry(self.main_manually, textvariable=id_uniprot,
                                 validate='focusin',validatecommand=self.check_values)

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

        self.button_manually=tk.Button(self.main_manually,
                                    text='Submit',
                                    command=self.get_manually_values)
        

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

        self.button_manually.grid(row=1, column=4, columnspan=2,sticky='swe')

        self.main_manually.grid_rowconfigure(1, weight=1)
        self.main_manually.grid_columnconfigure(0, weight=1)
        self.main_manually.grid_columnconfigure(2, weight= 1)
        self.main_manually.grid_columnconfigure(3, weight=1)
        self.main_manually.grid_columnconfigure(6, weight=1)
        self.main_manually.grid_columnconfigure(8, weight=1)

        ######## frame for protein ########

        self.protein=tk.LabelFrame(self.main, text='Protein',
                                   bg='#DADADA',
                                   relief='groove', height=150)
        
        ### header_protein ### 

        if self.valores['id_uniprot']=='':
            self.header_protein=tk.Label(self.protein,
                             bg='#DADADA',
                             text='No protein loaded',
                             font=('arial',20))
            self.header_protein.pack(side='top')

        ### properties ###

        self.properties=tk.Frame(self.protein,
                                 bg='#DADADA')

        self.total_residues=tk.Label(self.properties,
                                     text='Total residues: {}'.format(self.len_protein),
                                     anchor='w',
                                     bg='#DADADA')
        
        self.total_residues.grid(row=0, column=0, columnspan=2,sticky='nsew')

        self.sequence_label=tk.Label(self.properties,
                                     text='Sequence:',
                                     anchor='w',
                                     bg='#DADADA')
        
        self.sequence_text=tk.Text(self.properties, height=10, width=50
                                   )
        self.sequence_text.insert('1.0',self.annotated_sequence)
        self.sequence_text.grid(row=1, column=1, rowspan=2, sticky='nsew',padx=5)
        self.sequence_text.config(state='disabled')
        self.sequence_text.tag_config('justified',justify='center')

        self.label_modification=tk.Label(self.properties,
                                         text='Modification: {}'.format(self.valores['modification']),
                                        anchor='w',
                                        bg='#DADADA')
        self.label_modification.grid(row=3, column=0, sticky='nswe',padx=5)

        self.label_position=tk.Label(self.properties,
                                     text='Position: {}'.format(str(self.valores['position'])),
                                     bg='#DADADA',
                                     anchor='w')
        self.label_position.grid(row=4, column=0, pady=15, padx=5, sticky='nsew')
                                         
                                    
        

        self.properties.grid_columnconfigure(1, weight=1)
        
        self.sequence_label.grid(row=1, column=0,rowspan=2,sticky='nsew',pady=15)

        self.properties.pack(fill='both',expand=1)

        ### buttons ###

        self.buttons=tk.Frame(self.protein,
                              bg='blue',
                              height=30)

        properties_button=tk.Button(self.buttons, text='Get properties',
                                    command= self.get_properties)
        properties_button.pack(side='left', pady=5, padx=5)

        modify=tk.Button(self.buttons, text='Modify sequence', command=self.modify)
        
        modify.pack(side='left', padx=5, pady=5)

        visualize=tk.Button(self.buttons, text='Visualize',
                            command=self.visualize)
        
        visualize.pack(side='left', padx=5, pady=5)
        self.buttons.pack(fill='both', expand=0, side='bottom')

    
        #### Pack frames ####
        
        self.header.pack(fill='both', side='top',pady=0)
        self.header_text.pack(fill='both')
        self.main.pack(fill='both', expand=1)
        self.bottom.pack(fill='both',side='bottom')


    ######################## Methods ########################


    def load_table(self):

        '''
        Create a tree to visualize data from a local file
        and select a protein to visualize with PTMS
        '''

        ### import modules ###
        import pandas as pd
        from tkinter import filedialog
        path=filedialog.askopenfilename()



        try:

            ### read file ###
            
            file=pd.read_excel(path)
            total_rows=len(file)

            #### code packing frames and destroy if exist ####

            if not self.tree_frame.winfo_exists():
                self.tree_frame=tk.Frame(self.main_load,
                    bg='#DADADA')
                self.load_button=tk.Button(self.main_load, text='submit',
                                           command=self.get_file_values)
            else:
                self.tree_frame.destroy()
                self.tree_frame=tk.Frame(self.main_load,
                                 bg='#DADADA')
                self.load_button.destroy()
                self.load_button=tk.Button(self.main_load, text='submit',
                                           command=self.get_file_values)

            self.main_load.pack(fill='x',side='top',pady=20, padx=5)
            self.tree_frame.pack(fill='x', side='top')
            self.main_manually.pack_forget()
            self.protein.pack_forget()


            #### code for creating tree ####
            
            self.tree=ttk.Treeview(self.tree_frame, columns=tuple(file.columns), show='headings')
            self.tree.heading('ID_uniprot', text='ID_uniprot')
            self.tree.heading('PDB_id', text='PDB_id')
            self.tree.heading('Modification', text='Modification')
            self.tree.heading('Residue', text='Residue')
            self.tree.heading('Position', text='Position')


            #### code for creating table ####
            values=[]
            for i in range(total_rows):
                values.append(tuple(file.iloc[i,:].values))

            for value in values:
                self.tree.insert('',tk.END, values=value)

            scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side='right',fill='y')

            scrollbar_x=ttk.Scrollbar(self.tree_frame,orient=tk.HORIZONTAL,command=self.tree.xview)
            self.tree.configure(xscroll=scrollbar_x.set)
            scrollbar_x.pack(side='bottom', fill='x')

            self.tree.pack(fill='both', side='top', padx=20)

            psvroot.update_idletasks()
            psvroot.geometry("")

            self.load_button.pack(side='bottom',anchor='se', pady=10)

        except FileNotFoundError:

            showwarning(title='Be careful!', message='You didn\'t select a file')
            pass


    def display_manually(self):

        '''
        Display a frame to manually enter the protein data and destroy
        the frame for loading data from a file
        '''

        self.main_manually.pack(fill='both', expand=0, padx=5, pady=20)
        psvroot.update_idletasks()
        psvroot.geometry("")

        if self.tree_frame:

            self.tree_frame.destroy()
            self.load_button.destroy()

        else:
            pass
        self.main_load.pack_forget()
        self.protein.pack_forget()



    def check_values(self):

        '''
        Check if the data contains at least the uniprot ID, the modification
        and the position in the sequence
        '''

        if self.valores['id_uniprot'].isalnum():# and self.valores['modification'].isalpha() and self.valores['position'].isdigit():
            return True
        else:
            return False


    def get_file_values(self):
        
        '''
        Function to return the values from file in a dictionary
        '''

        selected_item=self.tree.selection()
        item_data=self.tree.item(selected_item)
        values=item_data['values']
        self.valores={}
        self.valores['id_uniprot']=values[0]
        self.valores['pdb']=values[1]
        self.valores['modification']=values[2]
        self.valores['residue']=values[3]
        self.valores['position']=values[4]

        print(self.valores)

        self.header_protein.config(text='{}'.format(self.valores['id_uniprot']),
                                           font=('arial',20,'bold'))

        self.protein.pack(fill='both', expand=1, padx=5, pady=5)
        psvroot.update_idletasks()
        psvroot.geometry("")

        return self.valores

    def get_manually_values(self):

        '''
        Function to return the values from manually enter in a dictionary
        '''


        ### get values ###

        try:

            self.valores={}
            self.valores['id_uniprot']=self.id_uniprot.get()
            self.valores['pdb']=self.id_pdb.get()
            self.valores['modification']=self.modification.get().upper()
            self.valores['residue']=self.residue.get()
            self.valores['position']=int(self.position.get())

            self.id_uniprot.delete(0, tk.END)
            self.id_pdb.delete(0, tk.END)
            self.modification.delete(0, tk.END)
            self.residue.delete(0, tk.END)
            self.position.delete(0, tk.END)

            print(self.valores)

            if self.valores['id_uniprot']!='':

                self.header_protein.config(text='{}'.format(self.valores['id_uniprot']),
                                           font=('arial',20,'bold'))
                
                self.protein.pack(fill='both', expand=1, padx=5, pady=5)
                psvroot.update_idletasks()
                psvroot.geometry("")

                return self.valores

            else:

                showerror(message='Something is wrong with the protein',
                                title='Ups!')
                self.header_protein.config(text='No protein loaded',
                                           font=('arial',20))
                    
        except:
            print('bruh')
        

    def set_pose(self):

        '''
        Function to set a pose from the data
        '''

        pose=pyrosetta.toolbox.rcsb.pose_from_rcsb(self.valores['pdb'])
        return pose

        
    def get_properties(self):

        '''
        Show the pose properties in the properties frame
        '''

        from pyrosetta.toolbox import rcsb
        self.pose=self.set_pose()
        self.total_residues.config(text='Total residues: {}'.format(len(self.pose.sequence())))
        self.sequence_text.config(state='normal')
        self.sequence_text.delete('1.0','end')
        self.sequence_text.insert('1.0',self.pose.annotated_sequence())
        self.sequence_text.config(state='disabled')
        self.label_modification['text']='Modification: {}'.format(self.valores['modification'])
        self.label_position['text']='Position: {}'.format(str(self.valores['position']))
        
        return self.pose

    def modify(self):

        '''
        Function to modify the pose to apply the PTM modification
        in the indicated residue
        '''

        pose=self.set_pose()


        pyrosetta.rosetta.core.pose.add_variant_type_to_pose_residue(
            pose,self.valores['modification'], self.valores['position'])

        self.sequence_text.config(state='normal')
        self.sequence_text.insert('end','\n'+'\n'+pose.annotated_sequence())
        self.sequence_text.config(state='disabled')

        pose.dump_pdb('modified_{}.pdb'.format(self.valores['pdb']))

        ### CAMBIO DE COLOR DE LA LETRA ####

        # self.prueba='hdfasioufhasñfhasfasfasf'
        # self.sequence_text.config(state='normal')
        # self.sequence_text.insert('end','\n'+'\n'+self.prueba)
        # self.sequence_text.tag_configure('color',font=('arial',15,'bold'),
        #                                  foreground='green')
        # position=str(self.valores['position'])
        # index='3.'+position
        # index_2='3.'+position+'+1c'
        # self.sequence_text.tag_add('color',index,index_2)
        # print(index,index_2)

        return pose
    
    def visualize(self):

        '''
        Visualize the protein in pymol
        '''

        cmd.set('seq_view')
        cmd.load('modified_2CPO.pdb')
        
        

# ejemplo=ptmstructure(psvroot)
# psvroot.title("PTMs's Structure Viewer")
# psvroot.geometry('1200x700')
# psvroot.mainloop()


def __init__(self):
    '''Add PyTMs to PyMOL Plugin menu'''
    # trigger PyMOL 2.0 legacy initialization
    self.root

    self.menuBar.addmenuitem('Plugin', 'separator')
    self.menuBar.addmenuitem('Plugin', 'command',
                             "PTMS's Structure Viewer",
                             label = 'PSV',
                             command = open_pytms)
    self.menuBar.addmenuitem('Plugin', 'separator')


def open_pytms():
    '''opens main dialog'''
    global psvroot
    global pytmsvar
    psvroot = tk.Tk()
    psvroot.title("PTMs's Structure Viewer")
    psvroot.geometry('1000x500')
    psvroot.resizable(1,1) # prevent/allow rezise
    Pmw.initialise()
    pytmsvar = ptmstructure(psvroot)
    psvroot.mainloop()
