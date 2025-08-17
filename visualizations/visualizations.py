import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from statsbombpy import sb
import streamlit as st

from mplsoccer import VerticalPitch, Pitch
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import to_rgba

import seaborn as sns



DICTIONARY_NAMES = {
    #Spain
    'Catalina Thomas Coll Lluch': 'Cata Coll', 
    'Ona Batlle Pascual': 'Ona Batlle', 
    'Irene Paredes Hernandez': 'Irene Paredes',
    'Laia Aleixandri López': 'Laia Aleixandri', 
    'Olga  Carmona García': 'Olga Carmona', 
    'Patricia Guijarro Gutiérrez': 'Patri Guijarrro',
    'Aitana Bonmati Conca': 'Aitana Bonmati',
    'Alexia Putellas Segura': 'Alexia Putellas',
    'Athenea del Castillo Belvide': 'Athenea',
    'María Francesca Caldentey Oliver': 'M. Caldentey',
    'Esther Gonzalez Rodríguez': 'Esther Gonzalez',
    'Leila Ouahabi El Ouahabi':'Leila Ouahabi' ,  
    'Lucía García Córdoba':'Lucía García',
    'Claudia Pina Medina': 'Claudia Pina' ,  
    'Jana Fernandez Velasco':'Jana Fernandez' ,         
    'Cristina Martín-Prieto Gutierrez' : 'C. Martín-Prieto',   
    'Alba María Redondo Ferrer' : 'Alba Redondo',
    'Adriana Nanclares Romero' : 'Adriana Nanclares' ,  
    'María Méndez Fernández' : 'María Méndez' ,  
    'Victoria López':'Vicky López',   
    'Maite Zubieta Aranbarri':'Maite Zubieta',
    'Salma Paralluelo Ayingono' : 'Salma Paralluelo', 

    #England
    'Georgia Stanway': 'Georgia Stanway',
    'Esme Beth Morgan': 'Esme Morgan',    
    'Keira Walsh': 'Keira Walsh',                       
    'Lucy Bronze':'Lucy Bronze',             
    'Alex Greenwood' : 'Alex Greenwood'  ,            
    'Lauren Hemp': 'Lauren Hemp',                 
    'Chloe Kelly': 'Chloe Kelly',                     
    'Bethany Mead': 'Bethany Mead',                     
    'Niamh Charles' : 'Niamh Charles',                      
    'Leah Williamson': 'Leah Williamson',                       
    'Jessica Carter': 'Jessica Carter',          
    'Jessica Park'  : 'Jessica Park',            
    'Anne Moorhouse' :'Anne Moorhouse',             
    'Hannah Hampton': 'Hannah Hampton',
    'Maya Le Tissier' : 'Maya Le Tissier',          
    'Lauren James': 'Lauren James',      
    'Ella Toone':'Ella Toone' ,             
    'Grace Clinton':'Grace Clinton',        
    'Alessia Russo':'Alessia Russo',                 
    'Carlotte Wubben-Moy':  'Lotte Wubben-Moy',         
    'Agnes Beever-Jones': 'Beever-Jones',         
    'Khiara Keating': 'Khiara Keating',                    
    'Michelle Agyemang' :  'Michelle Agyemang', 

    #WALES
    'Josie Green' :  'Josie Green',                         
    'Jessica Fishlock' : 'Jessica Fishlock' ,            
    'Sophie Louise Ingle':'Sophie Ingle ',              
    'Angharad James':     'Angharad James',                       
    'Charlotte Estcourt':    'C. Estcourt', 
    'Lily Woodham':   'Lily Woodham',                           
    'Gemma Evans':'Gemma Evans', 
    'Hannah Cain'   : 'Hannah Cain',                         
    'Hayley Ladd'   :  'Hayley Ladd',                      
    'Rhiannon Roberts' : 'Rhiannon Roberts' ,                          
    'Rachel Rowe' : 'Rachel Rowe',                           
    'Elise Hughes': 'Elise Hughes',
    'Ella Powell'  : 'Ella Powell',                           
    'Lois Joel'  : 'Lois Joel' ,                           
    'Esther Morgan' : 'Esther Morgan',
    'Carrie Jones' : 'Carrie Jones',                        
    'Ffion Morgan': 'Ffion Morgan',                      
    'Safia Middleton-Patel': 'Middleton-Patel',
    'Poppy Soper' : 'Poppy Soper'   ,                 
    'Alice Griffiths'  : 'Alice Griffiths' ,                         
    'Ceri Holland'  : 'Ceri Holland' ,                     
    'Olivia Clarke':'Olivia Clarke',
    'Kayleigh Anne Marie Barton':  'Kayleigh Barton',

    #FRANCE
    'Sakina Karchaoui': 'Sakina Karchaoui', 
    'Kadidiatou Diani': 'Kadidiatou Diani', 
    'Griedge Mbock Bathy Nka':    'Griedge Mbock',         
    'Onema Grace Geyoro' :   'Grace Geyoro',     
    'Amel Majri': 'Amel Majri',
    'Marie-Antoinette Katoto' : 'M-A. Katoto',
    'Delphine Cascarino': 'Delphine Cascarino',
    'Selma Bacha'   : 'Selma Bacha',                  
    'Pauline Peyraud Magnin'   : 'Peyraud-Magnin'  ,              
    'Sandy Baltimore': 'Sandy Baltimore',
    'Elisa De Almeida'  : 'De Almeida',                  
    'Sandie Toletti': 'Sandie Toletti' ,
    'Justine Lerond': 'Justine Lerond',
    'Melvine Malard': 'Melvine Malard', 
    'Oriane Jean-François': 'Jean-François', 
    'Clara Mateo' : 'Clara Mateo',             
    'Maëlle Lakrar' :'Maëlle Lakrar', 
    'Constance Picaud': 'Constance Picaud', 
    'Alice Sombath': 'Alice Sombath',
    'Melween Ndongala' : 'Melween Ndongala',                   
    'Kelly Gago': 'Kelly Gago', 
    'Thiniba Samoura' : 'Thiniba Samoura',
    'Lou Bogaert': 'Lou Bogaert',

    #BELGIUM
    'Tessa Wullaert': 'Tessa Wullaert',                      
    'Janice Cayman'  :'Janice Cayman',                 
    'Tinne De Caigny' :'T. De Caigny',
    'Davina Philtjens' : 'Davina Philtjens',                     
    'Laura Deloose': 'Laura Deloose',
    'Justine Vanhaevermaet':'J. Vanhaevermaet', 
    'Lisa Lichtfus': 'Lisa Lichtfus', 
    'Jassina Blom':'Jassina Blom', 
    'Elena Dhont':'Elena Dhont',                    
    'Nicky Evrard': 'Nicky Evrard', 
    'Ella Van Kerkhoven': 'E. Van Kerkhoven',
    'Sarah Wijnants': 'Sarah Wijnants',                     
    'Kassandra Ndoutou Eboa Missipo':'K. Missipo',
    'Hannah Eurlings':'Hannah Eurlings', 
    'Sari Kees':   'Sari Kees',                   
    'Amber Tysiak':'Amber Tysiak', 
    'Femke Bastiaen':'Femke Bastiaen',
    'Jarne Teulings': 'Jarne Teulings', 
    'Isabelle Iliano' : 'Isabelle Iliano',                      
    'Marie Detruyer': 'Marie Detruyer' ,                       
    'Mariam Abdulai Toloba': 'M. Toloba',
    'Jill Janssens': 'Jill Janssens',
    'Zenia Mertens':'Zenia Mertens',


    #ITALY
    'Cristiana Girelli': 'C. Girelli',
    'Elena Linari' : 'Elena Linari',           
    'Barbara Bonansea' : 'Barbara Bonansea',         
    'Laura Giuliani' :'Laura Giuliani',
    'Manuela Giugliano' : 'M. Giugliano',          
    'Cecilia Salvai' : 'Cecilia Salvai',            
    'Valentina Bergamaschi': 'V. Bergamaschi',
    'Lisa Boattin':'Lisa Boattin'  ,          
    'Annamaria Serturini': 'A. Serturini', 
    'Francesca Durante': 'Francesca Durante', 
    'Arianna Caruso': 'Arianna Caruso', 
    'Sofia Cantore': 'Sofia Cantore' , 
    'Martina Piemonte' : 'Martina Piemonte' ,            
    'Giada Greggi':'Giada Greggi',             
    'Michela Cambiaghi': 'Michela Cambiaghi', 
    'Rachele Baldi': 'Rachele Baldi', 
    'Lucia Di Guglielmo'  : 'L. Di Guglielmo' ,         
    'Elisabetta Oliviero'   : 'Elisabetta Oliviero',          
    'Eleonora Goldoni' : 'Eleonora Goldoni',             
    'Julie Piga':'Julie Piga',
    'Emma Severini' : 'Emma Severini' ,          
    'Martina Lenzini' : 'Martina Lenzini' ,           
    'Eva Schatzer': 'Eva Schatzer'  ,
    
    #NETHERLANDS
    'Sherida Spitse': 'Sherida Spitse',                    
    'Jill Roord' : 'Jill Roord',                
    'Jackie Groenen'  : 'Jackie Groenen' ,                 
    'Lineth Beerensteyn': 'L. Beerensteyn', 
    'Danielle van de Donk' : 'Van de Donk',                  
    'Renate Jansen' : 'Renate Jansen' ,                
    'Dominique Johanna Anna Petrone Janssen':'Dominique Bloodworth',  
    'Vivianne Miedema': 'V. Miedema', 
    'Lynn Wilms': 'Lynn Wilms',
    'Daphne van Domselaar' :'Van Domselaar', 
    'Katja Snoeijs': 'Katja Snoeijs',
    'Damaris Berta Egurrola Wienke': 'Damaris Egurrola',
    'Romée Leuchter': 'Romée Leuchter', 
    'Esmee Brugts'  : 'Esmee Brugts',                  
    'Caitlin Dijkstra' : 'C. Dijkstra', 
    'Lize Kop'   : 'Lize Kop',                 
    'Victoria Pelova': 'V. Pelova',                 
    'Chasity Grant': 'Chasity Grant' ,                   
    'Daniëlle de Jong' : 'D. de Jong',                  
    'Wieke Hendrikje Maria Kaptein':'Wieke Kaptein',                   
    'Kerstin Yasmijn Casparij' : 'Kerstin Casparij',
    'Veerle Buurman' : 'Veerle Buurman',                   
    'Ilse van der Zanden'   : 'Van der Zanden' ,  
     
    #ICELAND
    'Glódís Perla Viggósdóttir': 'G. Viggósdóttir',
    'Dagný Brynjarsdóttir':'D. Brynjarsdóttir',
    'Agla María Albertsdóttir': 'A.Albertsdóttir', 
    'Ingibjörg Sigurðardóttir' : 'I. Sigurðardóttir',                  
    'Sandra María Jessen': 'Sandra Jessen',   
    'Alexandra Jóhannsdóttir' : 'A. Jóhannsdóttir' ,                 
    'Karólína Lea Vilhjálmsdóttir': 'K. Vilhjálmsdóttir',                    
    'Áslaug Munda Gunnlaugsdóttir'  : 'Á. Gunnlaugsdóttir',                  
    'Hildur Antonsdóttir': 'H. Antonsdóttir',                     
    'Guðný Árnadóttir' : 'Guðný Árnadóttir',                 
    'Diljá Ýr Zomers': 'D. Ýr Zomers', 
    'Telma Ívarsdóttir'  : 'T. Ívarsdóttir' ,                
    'Hafrún Rakel Halldórsdóttir'  : 'H. Halldórsdóttir',                  
    'Sveindís Jane Jónsdóttir' : 'S. Jónsdóttir', 
    'Cecilía Rán Rúnarsdóttir' : 'C. Rúnarsdóttir' ,                  
    'Amanda Jacobsen Andradóttir'  : 'A. Andradóttir',
    'Hlín Eiríksdóttir' : 'H. Eiríksdóttir',                
    'Berglind Rós Ágústsdóttir': 'B. Ágústsdóttir',
    'Guðrún Arnardóttir': 'Guðrún Arnardóttir',                    
    'Fanney Inga Birkisdóttir':  'Fanney Birkisdóttir',   
    'Sædís Rún Heiðarsdóttir' : 'Sædís Heiðarsdóttir',
    'Katla Tryggvadóttir': 'K. Tryggvadóttir',
    'Natasha Anasi-Erlingsson' :'N. Anasi-Erlingsson',

    #FINLAND
    'Linda Sällström': 'Linda Sällström' , 
    'Tinja-Riikka Tellervo Korpela' : 'Tinja-Riikka',                           
    'Nora Heroum': 'Nora Heroum' ,
    'Natalia Kuikka' :'Natalia Kuikka',                           
    'Sanni Maija Franssi' : 'Sanni Franssi',                            
    'Emma Wilhelmina Koivisto' : 'Emma Koivisto',                           
    'Eveliina Summanen' : 'Eveliina Summanen',                           
    'Eva Nyström': 'Eva Nyström',
    'Jutta Rantala'  : 'Jutta Rantala',
    'Anna Koivunen' :'Anna Koivunen' ,                          
    'Saara Katariina Kosola': 'Saara Kosola' ,
    'Vilma Emilia Koivisto': 'Vilma Koivisto', 
    'Heidi Kollanen'  : 'Heidi Kollanen',                     
    'Ria Öling'  : 'Ria Öling', 
    'Anna Tamminen': 'Anna Tamminen', 
    'Olga Ahtinen'  : 'Olga Ahtinen',                      
    'Oona Sevenius':  'Oona Sevenius',                          
    'Maaria Roth'  :'Maaria Roth', 
    'Joanna Tynnilä': 'Joanna Tynnilä',                      
    'Oona Siren':'Oona Siren', 
    'Emmi Siren' : 'Emmi Siren' ,                       
    'Nea Lehtola' : 'Nea Lehtola',                      

    #DENMARK
    'Nadia Nadim': 'Nadia Nadim',                          
    'Katrine Veje': 'Katrine Veje', 
    'Frederikke Thøgersen'  : 'F. Thøgersen',                         
    'Pernille Mosegaard Harder': 'Pernille Harder',
    'Sanne Troelsgaard-Nielsen'  : 'S. Troelsgaard-Nielsen' ,                       
    'Signe Kallesøe Bruun': 'Signe Bruun',            
    'Sara Gedsted Thrige Andersen': 'Sara Thrige',
    'Sara Holmgaard' : 'Sara Holmgaard' ,                       
    'Karen Holmgaard' : 'Karen Holmgaard',                      
    'Josefine Hasbo': 'Josefine Hasbo' ,                       
    'Stine Ballisager Pedersen': 'Stine Pedersen' ,
    'Rikke Marie Madsen' : 'Rikke Madsen',                         
    'Janni Thomsen': 'Janni Thomsen' ,
    'Emma Skou Færge': 'Emma Færge',
    'Isabella Bryld Obaze': 'Isabella Obaze',
    'Cornelia Kramer'  : 'Cornelia Kramer' ,                        
    'Alberte Vingum Andersen' : 'Alberte Vingum' ,                         
    'Kathrine Østergaard Larsen' : 'Kathrine Larsen' ,                        
    'Sofie Bruun Bredgaard':'Sofie Bredgaard',
    'Amalie Jørgensen Vangsgaard':'Amalie Vangsgaard',            
    'Kathrine Møller Kühl':'Kathrine Kühl',               
    'Maja Bay Østergaard'  : 'Maja Østergaard',

    #POLAND
    'Ewa Pajor': 'Ewa Pajor', 
    'Paulina Dudek':'Paulina Dudek',                  
    'Kayla Joan Zophia Adamek': 'Kayla Adamek', 
    'Dominika Grabowska'  : 'D. Grabowska',               
    'Sylwia Matysik' : 'Sylwia Matysik',                 
    'Małgorzata Mesjasz' : 'M. Mesjasz' ,              
    'Tanja Pawollek': 'Tanja Pawollek',
    'Ewelina Kamczyk': 'Ewelina Kamczyk' , 
    'Weronika Zawistowska' : 'W. Zawistowska',                 
    'Adriana Achcińska' : 'Adriana Achcińska',                 
    'Natalia Padilla-Bidas': 'N. Padilla-Bidas', 
    'Kinga Szemik' : 'Kinga Szemik' , 
    'Martyna Wiankowska': 'M. Wiankowska', 
    'Oliwia Woś' : 'Oliwia Woś',                 
    'Klaudia Jedlińska'  : 'K. Jedlińska',                
    'Emilia Urszula Szymczak':'Emilia Szymczak' ,          
    'Wiktoria Zieniewicz'   : 'W. Zieniewicz'  ,              
    'Nadia Krezyman':'Nadia Krezyman', 
    'Natalia Radkiewicz'   : 'N Radkiewicz'  ,             
    'Kinga Seweryn'  : 'Kinga Seweryn',             
    'Milena Kokosz' : 'Milena Kokosz',              
    'Paulina Tomasiak'  : 'Paulina Tomasiak',               
    'Klaudia Słowińska' : 'Klaudia Słowińska' ,     

    #SWITZERLAND
    'Noelle Maritz': 'Noelle Maritz',
    'Lia Wälti': 'Lia Wälti',                            
    'Ana-Maria Crnogorčević' : 'A-M. Crnogorčević' ,                   
    'Viola Calligaris' : 'Viola Calligaris',                          
    'Géraldine Reuteler': 'G. Reuteler',                            
    'Meriame Terchoun' : 'Meriame Terchoun',                            
    'Alisha Lehmann': 'Meriame Terchoun',                          
    'Coumba Sow' : 'Coumba Sow',                           
    'Livia Peng' : 'Livia Peng',                          
    'Julia Stierli': 'Julia Stierli', 
    'Sandrine Mauron': 'Sandrine Mauron' ,                        
    'Elvira Herzog' : 'Elvira Herzog',                    
    'Laia Balleste' : 'Laia Balleste',              
    'Svenja Fölmli'  : 'Svenja Fölmli',                         
    'Riola Xhemaili'  : 'Riola Xhemaili', 
    'Nadine Riesen' : 'Nadine Riesen' ,                             
    'Alayah Pilgrim'  : 'Alayah Pilgrim' ,                      
    'Smilla Vallotto': 'Smilla Vallotto', 
    'Leila Wandeler': 'Leila Wandeler', 
    'Sydney Schertenleib' : 'S. Schertenleib', 
    'Iman Beney' : 'Iman Beney',                        
    'Nadine Katja Böhi' :'Nadine Böhi', 
    'Noemi Ivelj': 'Noemi Ivelj' ,          


    #SWEDEN
    'Magdalena Lilly Eriksson' : 'Magdalena Eriksson',   
    'Fridolina Rolfö': 'F. Rolfö', 
    'Kosovare Asllani' : 'K. Asllani',                  
    'Jonna Ann-Charlotte Andersson': 'Jonna Andersson' ,  
    'Emma Stina Blackstenius':'S. Blackstenius' ,  
    'Linda Brigitta Sembrant':'Linda Sembrant',   
    'Eva Sofia Jakobsson' : 'Sofia Jakobsson',                    
    'Amanda Nildén': 'Amanda Nildén'  ,                 
    'Madelen Fatimma Maria Janogy'  : 'Madelen Janogy',                  
    'Lina Mona Andréa Hurtig' : 'Lina Hurtig' ,  
    'Amanda Ilestedt': 'Amanda Ilestedt'  ,                                    
    'Gun Nathalie Björn': 'Nathalie Björn', 
    'Julia Zigiotti-Olme' : 'J. Zigiotti-Olme',                      
    'Rebecka Blomqvist' : 'R. Blomqvist' ,                
    'Hanna Ulrika Bennison' : 'Hanna Bennison',                   
    'Ingrid Filippa Angeldal': 'Filippa Angeldal' ,               
    'Jennifer Miley Falk' : 'Jennifer Falk' ,                 
    'Johanna Rytting-Kaneryd': 'J. Rytting-Kaneryd' ,                 
    'Emma Holmgren': 'Emma Holmgren',                    
    'Hanna Lundkvist' : 'Hanna Lundkvist',                   
    'Ellen Wangerheim': 'Ellen Wangerheim' ,                    
    'Tove Enblom' : 'Tove Enblom' , 
    'Smilla Holmberg': 'Smilla Holmberg',

    #GERMANY
    'Linda Dallmann': 'Linda Dallmann',                        
    'Sara Däbritz': 'Sara Däbritz' ,                        
    'Kathrin Julia Hendrich':  'Kathrin Hendrich' ,             
    'Ann-Katrin Berger' : 'A-K Berger',                          
    'Sydney Lohmann': 'Sydney Lohmann', 
    'Lea Schüller' : 'Lea Schüller' ,                        
    'Klara Bühl' :'Klara Bühl' ,                        
    'Carlotta Wamser' : 'Carlotta Wamser',                         
    'Elisa Senß': 'Elisa Senß' ,
    'Stina Johannes': 'Stina Johannes' ,                          
    'Giovanna Hoffmann' : 'G. Hoffmann'  ,                       
    'Janina Minge':'Janina Minge' , 
    'Rebecca Knaak': 'Rebecca Knaak' ,                      
    'Selina Cerci' : 'Selina Cerci',                          
    'Jule Brand' :  'Jule Brand',                      
    'Sophia Kleinherne' :'S. Kleinherne',                           
    'Sjoeke Nüsken' : 'Sjoeke Nüsken',                         
    'Laura Freigang' : 'Laura Freigang',                          
    'Ena Mahmutovic' : 'Ena Mahmutovic' ,                         
    'Cora Zicai' :'Cora Zicai',                      
    'Sarai Linder': 'Sarai Linder',                         
    'Franziska Kett':'Franziska Kett',                        

    #NORWAY
    'Ada Stolsmo Hegerberg' : 'Ada Hegerberg' ,             
    'Caroline Graham Hansen' :  'Caroline Hansen' ,                           
    'Maren Nævdal Mjelde' :  'Maren Mjelde',             
    'Guro Reiten': 'Guro Reiten', 
    'Frida Maanum' : 'Frida Maanum',                               
    'Cecilie Fiskerstrand': 'C. Fiskerstrand',
    'Ingrid Syrstad Engen' :'Ingrid Engen',                 
    'Emilie Marie Woldvik' : 'Emilie Woldvik',                                
    'Vilde Bøe Risa' : 'V. Bøe Risa',                           
    'Karina Sævik' : 'Karina Sævik' ,                             
    'Aurora Watten Mikalsen' :'Aurora Mikalsen',                                
    'Synne Jensen'  : 'Synne Jensen',                            
    'Celin Bizet Ildhusøy' : 'C. Ildhusøy' ,                           
    'Tuva Hansen': 'Tuva Hansen', 
    'Elisabeth Terland' : 'E. Terland',                             
    'Thea Bjelde': 'Thea Bjelde' ,
    'Lisa Fjeldstad Naalsund' : 'Lisa Naalsund',
    'Mathilde Hauge Harviken':'Mathilde Harviken' ,          
    'Marit Bratberg Lund':'Marit Lund'  ,          
    'Marthine Østenstad' :'M. Østenstad',                      
    'Signe Gaupset' : 'Signe Gaupset',                         
    'Justine Kvaleng Kielland'  : 'Justine Kielland' ,         
    'Selma Panengstuen':'S. Panengstuen',


    #PORTUGAL
    'Dolores Isabel Jacome Silva' : 'Dolores Silva' ,
    'Ana Borges' : 'Ana Borges',                
    'Patricia Isabel Sousa Barros Morais' :  'Patricia Sousa' ,  
    'Diana Micaela Abreu de Sousa e Silva' :  'Diana Silva',
    'Carole da Silva Costa' :  'Carole Costa'  , 
    'Tatiana Vanessa Ferreira Pinto' :'Tatiana Pinto' ,  
    'Jéssica da Silva': 'J. da Silva' ,
    'Diana Catarina Ribeiro Gomes':'Diana Gomes' ,  
    'Inês Teixeira Pereira': 'Inês Pereira',
    'Fátima Alexandra Figueira Pinto' : 'Fátima Pinto' ,  
    'Andreia Alexandra Norton':'Andreia Norton' ,  
    'Joana Filipa Gaspar Silva Marchão' : 'Joana Marchão' , 
    'Andreia Martins Faria' :'Andreia Faria' ,  
    'Catarina Amado' : 'Catarina Amado',
    'Ana Rita Silva Seiça' : 'Ana Seiça' ,  
    'Francisca Ramos Ribeiro Nazareth Sousa' : 'Francisca Nazareth' ,  
    'Carolina Costa Malheiro Dias Correia' : 'Carolina Correia' ,  
    'Lúcia Catarina Sousa Alves': 'Lúcia Alves' ,  
    'Telma Raquel Velosa Encarnação' : 'Telma Encarnação' ,
    'Andreia de Jesus Jacinto' :  'Andreia Jacinto'  ,    
    'Ana Ines Palma Capeta' : 'Ana Capeta',  
    'Sierra Cota-Yarde': 'S. Cota-Yarde',
    'Beatriz Pina Fonseca' :  'B.Pina Fonseca' 

    }


#----------------------------------------------------------LINEUPS----------------------------------------

def search_lineups_match(df, DICTIONARY_NAMES): 
    formations= df[df['type']=='Starting XI']
    
    df_home_lineup= formations['tactics'][0]['lineup']
    df_home_lineup = pd.json_normalize(df_home_lineup)
    df_home_lineup['player.name'] = df_home_lineup['player.name'].replace(DICTIONARY_NAMES)

    formation_home= formations['tactics'][0]['formation']
    
    df_away_lineup= formations['tactics'][1]['lineup']
    df_away_lineup = pd.json_normalize(df_away_lineup)
    df_away_lineup['player.name'] = df_away_lineup['player.name'].replace(DICTIONARY_NAMES)

    formation_away= formations['tactics'][1]['formation']
    

    return df_home_lineup, formation_home, df_away_lineup, formation_away

def create_df_formations():
    pitch = VerticalPitch()
    dataframe_formations_mplsoccer= pitch.formations_dataframe
    return dataframe_formations_mplsoccer


def extractions_df_formations(df, formation_team_home, formation_team_away):
    home_formation_df = df[df['formation'].astype(str) == str(formation_team_home)]
    away_formation_df = df[df['formation'].astype(str) == str(formation_team_away)]
    
    return home_formation_df, away_formation_df

def plot_lineups(df_logos , formation, formation_df , home= True):
    # dibujas el pitch
    pitch = VerticalPitch(goal_type='box', pitch_color='none',  # sin fondo
    line_color='white')   # líneas blancas
    fig, ax = pitch.draw(figsize=(6, 8.72))

    # añadimos los nombres con kind='text'
    ax_text = pitch.formation(
        str(formation),
        positions=formation_df['position.id'],
        kind='text',
        text=formation_df['player.name'],
        va='center', ha='center', fontsize=8,
        ax=ax,
        bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.3', edgecolor='white')
    )

    if home== True: 
        # Cargamos una sola imagen del equipo
        team_logo = mpimg.imread(df_logos.iloc[0]['home_logo_path'])
    else:
        team_logo = mpimg.imread(df_logos.iloc[0]['away_logo_path'])
    # Creamos una lista de 11 imágenes idénticas
    images = [team_logo] * len(formation_df)

    ax_image = pitch.formation(
        str(formation),
        positions=formation_df['position.id'],
        kind='image',
        image=images,
        width=11,   # ancho de cada imagen
        xoffset=-8,
        ax=ax
    )
    ax.set_axis_off()
    fig.patch.set_alpha(0)
    plt.close(fig) 
    return fig

#----------------------------------------------------------NETWORK PASS----------------------------------------
TEAM_COLORS_PRIMARY = {
    "Iceland Women's": "#0044FF",       # Azul (código uniforme masculino, compartido por selección femenina) :contentReference[oaicite:0]{index=0}
    "Switzerland Women's": "#FF0000",   # Rojo (Swiss red), común en su uniforme
    "Belgium Women's": "#000000",       # Negro (común en el home negro tradicional)
    "Spain Women's": "#FF0000",         # Rojo (#FF0000) :contentReference[oaicite:1]{index=1}
    "Denmark Women's": "#C60C30",       # Rojo oscuro (color clásico danés)
    "Germany Women's": "#FFFFFF",       # Blanco (home jersey) :contentReference[oaicite:2]{index=2}
    "Wales": "#FF0000",                 # Rojo (tradicional en camiseta local)
    "France Women's": "#021850",        # Azul oscuro (“Blue Void”) :contentReference[oaicite:3]{index=3}
    "Norway Women's": "#EF2B2D",        # Rojo (Noruega home clásico)
    "Portugal Women's": "#006600",      # Verde escuro (color típico local)
    "Poland Women's": "#FFFFFF",        # Blanco (home tradicional)
    "England Women's": "#FFFFFF",       # Blanco (home) :contentReference[oaicite:4]{index=4}
    "WNT Finland": "#003580",           # Azul (color principal de la camiseta local)
    "Italy Women's": "#0048BA",         # Azul “azzurro” italiano
    "Sweden Women's": "#FFCD00",        # Amarillo (equipación local amarilla) 
    "Netherlands Women's": "#FF6600",   # Naranja (color icónico de la camiseta local)
}

def get_colors_team(home_team, away_team, TEAM_COLORS_PRIMARY):
    colors_home = TEAM_COLORS_PRIMARY.get(home_team)
    colors_away = TEAM_COLORS_PRIMARY.get(away_team)

    return colors_home, colors_away

def dataframe_pass_for_teams(df, home_name_team, away_name_team, DICTIONARY_NAMES): 
    pass_event= df[df['type']=='Pass']
    pass_event[['x', 'y']]= pass_event['location'].apply(pd.Series)
    pass_event[['pass_end_x', 'pass_end_y']]= pass_event['pass_end_location'].apply(pd.Series)
    pass_event['player'] = pass_event['player'].replace(DICTIONARY_NAMES) 
    pass_event['passer']= pass_event['player']
    pass_event['reciver']= pass_event['player'].shift(-1)
    pass_event_home= pass_event[pass_event['team']== home_name_team]
    pass_event_away= pass_event[pass_event['team']== away_name_team]
    return pass_event_home, pass_event_away

def preparation_plot_networkpass(df,pass_event, home_team, DICTIONARY_NAMES):
    
    firstsub= int(df[(df['type']=='Substitution') & (df['team']==home_team)].minute.min())
    pass_complete_total= pass_event[pass_event['pass_outcome'].isnull()]
    pass_complete_total_subs = pass_complete_total[pass_complete_total['minute']<firstsub]
    pass_complete_total_subs['player'] = pass_complete_total_subs['player'].replace(DICTIONARY_NAMES) 
    average_locations_sub= pass_complete_total_subs.groupby('player').agg({'x': ['mean'], 'y': ['mean', 'count']})

    pass_between=pass_complete_total_subs.groupby(['passer', 'reciver']).id.count().reset_index()
    pass_between.rename({'id':'pass_count'}, axis= 'columns', inplace=True)

    average_locations_sub.columns= average_locations_sub.columns.droplevel(0)

    average_locations_sub['x']= average_locations_sub.iloc[:, 0]
    average_locations_sub['y']= average_locations_sub.iloc[:,1]
    average_locations_sub = average_locations_sub.drop(columns=['mean'])

    pass_between= pass_between.merge(average_locations_sub, left_on = 'passer', right_index=True)
    pass_between= pass_between.merge(average_locations_sub, left_on = 'reciver', right_index=True, suffixes= ['', '_end'])
    pass_between= pass_between[pass_between['pass_count']>1]
    pass_between['width']= pass_between['pass_count']

    return pass_between, average_locations_sub

def preparation_plot_networkpass_2half(df,pass_event, home_team, DICTIONARY_NAMES):

    pass_complete_total= pass_event[pass_event['pass_outcome'].isnull()]
    pass_complete_total['player'] = pass_complete_total['player'].replace(DICTIONARY_NAMES) 
    average_locations= pass_complete_total.groupby('player').agg({'x': ['mean'], 'y': ['mean', 'count']})

    pass_between=pass_complete_total.groupby(['passer', 'reciver']).id.count().reset_index()
    pass_between.rename({'id':'pass_count'}, axis= 'columns', inplace=True)

    average_locations.columns= average_locations.columns.droplevel(0)

    average_locations['x']= average_locations.iloc[:, 0]
    average_locations['y']= average_locations.iloc[:,1]
    average_locations = average_locations.drop(columns=['mean'])

    pass_between= pass_between.merge(average_locations, left_on = 'passer', right_index=True)
    pass_between= pass_between.merge(average_locations, left_on = 'reciver', right_index=True, suffixes= ['', '_end'])
    pass_between['width']= pass_between['pass_count']

    return pass_between, average_locations

def plot_network_pass(pass_between, average_locations_sub, color_team):

    MAX_LINE_WIDTH = 13
    pass_between['width'] = (pass_between.pass_count/ pass_between.pass_count.max()* MAX_LINE_WIDTH)

    MIN_TRANSPARENCY= 0.000001
    color = np.array(to_rgba('yellow'))
    color= np.tile(color, (len(pass_between),1))
    c_transparency= pass_between.pass_count/ pass_between.pass_count.max()
    c_transparency= (c_transparency * (1- MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color[:, 3]= c_transparency

    MAX_MAKER_SIZE= 800
    average_locations_sub['marker_size'] = (average_locations_sub['count']/ average_locations_sub['count'].max() * MAX_MAKER_SIZE)

    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color="None", line_color='white', goal_type='box', goal_alpha=.8)
    fig, ax = pitch.draw(figsize=(6, 8.72), constrained_layout=False, tight_layout=True)
    fig.set_facecolor('#22312b')

    arrows = pitch.arrows(pass_between.x, pass_between.y, pass_between.x_end, pass_between.y_end, ax=ax, color=color, zorder=.99)

    node_edge = to_rgba(color_team, alpha=0.6)
    nodes = pitch.scatter(average_locations_sub.x, average_locations_sub.y, ax=ax, color=color_team, ec=node_edge, s=average_locations_sub['marker_size'])
    
    for index, row in pass_between[['passer', 'x', 'y']].drop_duplicates(subset='passer').iterrows():
        pitch.annotate(row.passer, xy=(row.x-3.5, row.y), c='black', va='center',
                        ha='center', size=8, weight='bold', ax=ax, bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.3', edgecolor='white'))
    fig.patch.set_alpha(0)
    plt.close(fig)
    return fig

