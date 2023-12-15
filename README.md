# PTM Structure Viewer (PSV)

## Description
PTM Structure Viewer (PSV) is a PyMOL plugin that allows the user a fast localization of the PTMs in the protein’s structure, integrating on the one side the data provided by the user and on the other side the capabilities offered by PyMOL. Besides, it allows the possibility of doing a cross search with the databases dbPTM and Appris and remodel protein structures using Rosetta


<center>

[![image.png](https://i.postimg.cc/NMsyJVJJ/image.png)](https://postimg.cc/McLKXs8V)

</center>

## Instalation

List of python libraries that are needed:
* tkinter
* multiprocessing
* datetime
* os
* pandas

PSV requires the installation of the Pyrosetta suite. This installation needs a Rosetta license, which is freely available to academic and government laboratories and can be obtained at https://els2.comotion.uw.edu/product/pyrosetta. The installation of this suite can be carried out by following the tutorial provided in https://www.pyrosetta.org/downloads.

In addition to this, to do the cross search in Appris database, it will also be needed the htslib from the samtools. https://www.htslib.org/download/

Finally the PyMOL plugin manager can be used to install the _.zip_ file in the Releases section of this profile.

## Use

#### Load file
This option allows the user to select between data containing proteins with only one PTM or data that could contain several modifications. In both cases, the file imported must have a .tsv or .xlsl   extension and contain the following columns:
1.	ID_uniprot: Protein Uniprot identifiers;
2.	Modification: One or more modifications separated by a comma, where every element must be between quotes;
3.	Positions: Position(s) of the modification(s) in the protein separated by a comma;
4.	Peptide Start: Start position of the peptide that contains the modification. In case a protein contains more than one modified peptide, the format will be [x, y, z, …]   ;
5.	Peptide End: End position of the peptide that contains the modification. In case a protein contains more than one modified peptide, the format will be [x, y, z, …]  .
Then the user can choose one of the proteins or several of them by clicking the multiprotein button and, once the submit button has been clicked, the search in dbPTM option will be enabled and the protein menu will show.
#### Search in dbPTM
In this option, PSV searches the dbPTM database for the protein PTMs provided by the user. Then the plugin will display the proteins with positive matches together with their link to the dbPTM database and a score based on the level of match:
- One point if there are any experimentally validated modifications in the peptide described in dbPTM;
- Two points if there are any modifications in dbPTM in the same position as those provided by the user;
- Three points if the modification is the same in dbPTM and in the user’s data.
PSV includes the data from dbPTM downloaded on 28/09/2023 to make the search locally and reduce processing time.
 
#### Search in Appris
In this case, PSV will create a “query_id_uniprot.txt” file in PSV_reports/logs for each protein that the user wants to search. This file contains a single column with the following format:

q
Id_uniprot:peptide_start-peptide_end

After that, a search in Appris will be carried out for all the regions in the protein described in the query file. The results will be stored in PSV_reports/logs as a “results_query_id_uniprot.gft” file. This file contains the information retrieved from SPADE, CRASH, THUMP, and FIREDB for the different regions queried.
As was the case for dbPTM, PSV includes the data annotated in Appris as of 31/10/2023 to reduce search time. Note that ‘hstlib’ from samtools will be needed for this functionality.

#### Enter data manually
In this case, three text fileds will show where the user can type the protein Uniprot identifier, the modifications (separated by commas) and the positions of these modifications in the protein. After clicking submit, the protein menu will show.
####Import local pdb
In this option the user can work with his/her own structure file. After load this file, the protein menu will show.
####Protein menu
The content of this menu depends on the number of proteins that have been submitted.

  
  * Multiple proteins:
  
In this case the user can select only the submit option. This option searches for the structure of the selected proteins in AlphaFolddb, downloads the pdb files and the Predicted Aligned Error (PAE) figure in the PSV_reports/PDBs directory and creates a PyMOL session file in PSV_reports/PyMolSessions folder. This file stores the protein structure (coloured in white) with its modifications and a label indicating the name of the modification. Those residues bearing a PTM will show their sidechain and will be coloured in different random colours, excluding white. Besides, if there is a file with results from Appris for a protein in this process, the plugin will also colour the regions with annotations and place a label indicating the source and the feature found.
  
  * Single protein:  
  
  The user must select a structure file to work by clicking the get pdb button. Then a pop-up window will show the structure files for this protein retrieved from Uniprot so that the user can select any of them. If the selected structure file has been predicted by AlphaFold, the header indicating the protein identifier will show the average predicted local distance difference test (pLDDT)  to assess the structure reliability, as this value represents the model confidence prediction.  

Then clicking the get properties button will download the pdb file selected by the user and place it in the PSV_reports/PDBs directory. If the structure is predicted, the PAE image will be also downloaded. Besides, the name of the protein, the length of the sequence and the sequence will be retrieved as well. For this process, instead of retrieving those properties from Uniprot or AlphaFolddb, the plugin uses the pose_from_rcsb function from the Pyrosetta library. This function downloads the pdb and removes water molecules and ligands that do not have a role in our workflow.  

After that, the modify sequence button will be enabled. The function of this option is to replace the residue in the selected position with a modified residue at this position. However, this function is limited by the need to have the structure files of these modified residues in the Pyrosetta database. In case this file exists, the plugin will show another sequence with de corresponding amino acid coloured in green and will generate a modified pdb in PSV_reports/Modified_Proteins. Besides, the remodel button will be enabled too after retrieving the protein’s properties. This option will do a remodel of the structure based on a few options that the user should fill in a top window. The remodel will follow the aforementioned FastRelax strategy with two principal options: local and global.  

The local remodel will only repack the side chains of the amino acids that are within a sphere of user specified radius, taking a user-specidfied residue as the centre of this sphere. Moreover, the number of cycles for the relaxing process can be set by the user for a precise procedure.  

The global remodel option will repack all the side chains in the protein structure. To select this option the user must enter a 0 in the “Set aa to focus” and “Set sphere radium to relax” fields. It is also available for the user to select the number of cycles of repacking for the relaxing process. Regardless of the selected process, a relaxed.pdb file will be stored in PSV_reports/Relaxed_structures.  

Finally, the user can press the visualize button to see in PyMOL the structure of any pdb file, where the residues containing modifications will show in different colours. The PTMs will be indicated by labels and their side chains will be shown to indicate the possible orientation of the PTM. Also, if there is a file for this protein with results from an Appris search, the plugin will colour the annotated regions and will place a label indicating the database and the feature. The user can change the modification or the position with the change modification or position button at any time.
