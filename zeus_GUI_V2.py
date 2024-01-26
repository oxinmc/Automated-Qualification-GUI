
import tkinter as tk
from tkinter import GROOVE, RIDGE, Listbox, Scrollbar, ttk
from PIL import Image, ImageTk




def stylename_elements_options(stylename):
    '''Function to expose the options of every element associated to a widget
       stylename.'''
    try:
        # Get widget elements
        style = ttk.Style()
        layout = str(style.layout(stylename))
        print('Stylename = {}'.format(stylename))
        print('Layout    = {}'.format(layout))
        elements=[]
        for n, x in enumerate(layout):
            if x=='(':
                element=""
                for y in layout[n+2:]:
                    if y != ',':
                        element=element+str(y)
                    else:
                        elements.append(element[:-1])
                        break
        print('\nElement(s) = {}\n'.format(elements))

        # Get options of widget elements
        for element in elements:
            print('{0:30} options: {1}'.format(
                element, style.element_options(element)))

    except tk.TclError:
        print('_tkinter.TclError: "{0}" in function'
              'widget_elements_options({0}) is not a recognised stylename.'
              .format(stylename))




def define_custom_styles():

    # Define styles (winnative clam alt default classic vista xpnative)

    my_new_style = ttk.Style()
    my_new_style.theme_use('vista') #Main style of choice

    my_new_style.element_create("plain.field", "from", "clam")
    my_new_style.layout("Custom.TEntry",
                    [('Entry.plain.field', {'children': [(
                        'Entry.background', {'children': [(
                            'Entry.padding', {'children': [(
                                'Entry.textarea', {'sticky': 'nswe'})],
                        'sticky': 'nswe'})], 'sticky': 'nswe'})],
                        'border':'2', 'sticky': 'nswe'})])
    my_new_style.configure("Custom.TEntry", foreground="#ffffff", fieldbackground="#333333", background='#333333', insertcolor='#ffffff', highlightbackground='#007fff') #, relief='flat'
    my_new_style.map('Custom.TEntry', lightcolor=[('focus', '#007fff')])

    my_new_style.configure('TLabelframe', background='#333333', foreground ='#aaaaaa', bordercolor='#aaaaaa', borderwidth=1)
    my_new_style.configure("TMenubutton", foreground='#ffffff', background='#737373')

    return(my_new_style)




def import_constants():

    page_selection_font = ("Verdana", 14)
    in_page_heading_font = ("Verdana", 10)
    in_page_heading_font_bold = ("Verdana", 10, 'bold')

    white_colour = '#ffffff'
    page_selected = '#666666'
    page_not_selected = '#adadad'

    background_dark_grey = '#333333'
    header_blue = '#007fff'
    header_background_box = '#737373' 
    dark_blue_textbox = '#002a55' #d9ead3
    button_colour = header_background_box
    text_colour = white_colour #'#aaaaaa'

    return(page_selected, page_not_selected, header_blue, header_background_box, button_colour, text_colour, dark_blue_textbox, background_dark_grey, page_selection_font, in_page_heading_font, in_page_heading_font_bold, white_colour)




def define_framelabel(self, label_text):

    label = tk.Label(self, text=label_text, fg='white', bg='#333333')

    return(label)



def create_container(self):
    
    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand = True) #Find out what this is doing **
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)

    return(container)




class myGUI(tk.Tk):  
  
    def __init__(self, *args, **kwargs):  
          
        tk.Tk.__init__(self, *args, **kwargs)  
        
        container = create_container(self)
          
        self.title("Zeus Control Centre")  # set window title  
        self.frames = {}  
      
        for F in [MainPage, XHatchPage, AdhesionPage, ImagingPage]:

            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")
            frame.config(bg="#333333")

        self.show_page(MainPage) #First page to be shown
  
    def show_page(self, cont):  
  
        frame = self.frames[cont]  
        frame.tkraise()
        
        
          
class MainPage(tk.Frame):

    def __init__(self, parent, controller):

        #Constants
        page_selected, page_not_selected, header_blue, header_background_box, button_colour, text_colour, dark_blue_textbox, background_dark_grey, page_selection_font, in_page_heading_font, in_page_heading_font_bold, white_colour = import_constants()
        
        tk.Frame.__init__(self,parent)
        style = define_custom_styles()

        #=========================================================================================================================================
        # Page Selecting Buttons

        button_style = GROOVE # unselected, selected = RIDGE

        main_page_button = tk.Button(self, text="Main Page", background=page_selected, relief=RIDGE, font=page_selection_font, command='')
        x_hatch_page_button = tk.Button(self, text="X-Hatch", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(XHatchPage))
        adhesion_page_button = tk.Button(self, text="Adhesion", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(AdhesionPage))
        imaging_page_button = tk.Button(self, text="Imaging", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(ImagingPage))

        for e,label in enumerate([main_page_button,x_hatch_page_button,adhesion_page_button, imaging_page_button]):
            label.place(relx=((e*2)+1)/8,rely=0.00, relwidth=0.25, anchor='n')

        #=========================================================================================================================================
        # Test Scenario (ts) Selection Box
        
        self.test_scenario_label = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "Test Scenario Selection"))
        self.test_scenario_label.grid(row=2, column=0, columnspan=4, rowspan=21, pady=(30,5), padx=(20,0), sticky='nesw')

        test_options_box = Listbox(self.test_scenario_label, background=header_background_box, foreground=text_colour, font=("Verdana", 13))
        test_options_box.grid(row=1, column=1, columnspan=6, rowspan=6, sticky='nesw')
        options_scrollbar = Scrollbar(self.test_scenario_label)
        options_scrollbar.grid(row=1, column=1, columnspan=6, rowspan=6, sticky='nes')
        test_options_box.config(yscrollcommand = options_scrollbar.set)
        options_scrollbar.config(command = test_options_box.yview)

        self.test_scenario_label.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.test_scenario_label.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')

        # ** Just an example text **
        test_options_box.insert("end", '')
        for entry in ['Test Profile - Xhatch A', 'Test Profile - Xhatch B', 'Test Profile - Xhatch C', 'Test Profile - Adhesion A', 'Test Profile - Image',]:
            test_options_box.insert("end", '    • '+entry)
        #####################

        #=========================================================================================================================================
        # Centre Page Buttons

        self.profile_control = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "Profile Control"))
        self.profile_control.grid(row=4, column=4, columnspan=2, rowspan=7, padx=(20,20), sticky='nesw')

        run_profile_button = tk.Button(self.profile_control, text="Run Profile", foreground=text_colour, background=button_colour, command='')
        run_profile_button.grid(row=1, column=0, columnspan=4, padx=(10,10), sticky='ew')
        modify_profile_button = tk.Button(self.profile_control, text="Modify Profile", foreground=text_colour, background=button_colour, command='')
        modify_profile_button.grid(row=3, column=0, columnspan=4, padx=(10,10), sticky='ew')

        self.profile_control.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.profile_control.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a')

        exit_program_button = tk.Button(self, text="Exit Program", foreground=text_colour, background=button_colour, command=lambda: exit_popupmsg(controller, 'Are you sure you wish to exit?'))
        exit_program_button.grid(row=22, column=4, columnspan=2, padx=(30,30), sticky='ew')

        #=========================================================================================================================================
        # Right Page Options

        testID_row = 1
        testID_column = 0
        vs_widget_columnspan = 4

        self.variable_selection = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "Variable Selection"))
        self.variable_selection.grid(row=4, column=6, columnspan=2, rowspan=19, padx=(0,20), sticky='nesw')
        self.variable_selection.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.variable_selection.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight=1, uniform='a')

        test_id_label = tk.Label(self.variable_selection, text="Test ID:", background=header_blue, foreground=white_colour, font=in_page_heading_font_bold) #Could use ttk.Treeview here to show variables in selection
        test_id_label.grid(row=testID_row, column=testID_column, columnspan=vs_widget_columnspan, padx=(10,10), pady=(0,5), sticky='ews')
        test_id_entry = ttk.Entry(self.variable_selection, style='Custom.TEntry')
        test_id_entry.insert(1, 'Example_Test_Name_Sample_A.test')
        test_id_entry.grid(row=testID_row+1, column=testID_column, columnspan=vs_widget_columnspan, padx=(10,10), sticky='ewn')

        test_storage_label = tk.Label(self.variable_selection, text="Test Storage:", background=header_blue, foreground=white_colour, font=in_page_heading_font_bold)
        test_storage_label.grid(row=testID_row+2, column=testID_column, columnspan=vs_widget_columnspan, padx=(10,10), pady=(0,5), sticky='ews')
        test_storage_entry = ttk.Entry(self.variable_selection, style='Custom.TEntry')
        test_storage_entry.insert(1, 'C:/Example/path/A')
        test_storage_entry.grid(row=testID_row+3, column=testID_column, columnspan=vs_widget_columnspan, padx=(10,10), sticky='ewn')
        
        path_select_button = tk.Button(self.variable_selection, text="Path - Select", foreground=text_colour, background=button_colour, command='')
        path_select_button.grid(row=testID_row+4, column=testID_column, columnspan=vs_widget_columnspan, padx=(10,10), sticky='ew')

        cycles_label = tk.Label(self.variable_selection, text="Cycles", background=header_blue, foreground=white_colour, font=in_page_heading_font_bold)
        cycles_label.grid(row=testID_row+6, column=testID_column, columnspan=vs_widget_columnspan-1, padx=(10,0), sticky='ew')
        cycles_choice = tk.StringVar(self.variable_selection)
        cycles_choice.set('1') # default value
        cycles_options = ['', '1', '2', '3']
        cycles_dropdwn = ttk.OptionMenu(self.variable_selection, cycles_choice, *cycles_options)
        cycles_dropdwn.config(width=3)
        cycles_dropdwn.grid(row=testID_row+6, column=testID_column+3, padx=(4,15), sticky='w')

        samples_label = tk.Label(self.variable_selection, text="Number of Samples", background=header_blue, foreground=white_colour, font=in_page_heading_font_bold)
        samples_label.grid(row=testID_row+7, column=testID_column, columnspan=vs_widget_columnspan-1, padx=(10,0), sticky='ew')
        samples_choice = tk.StringVar(self.variable_selection)
        samples_choice.set('1') # default value
        samples_options = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        samples_dropdwn = ttk.OptionMenu(self.variable_selection, samples_choice, *samples_options)
        samples_dropdwn.config(width=3)
        samples_dropdwn.grid(row=testID_row+7, column=testID_column+3, padx=(4,15), sticky='w')

        system_status_text = tk.Text(self.variable_selection, background=dark_blue_textbox, foreground=white_colour, height=2, width=2)
        system_status_text.tag_configure('tag-center', justify='center')
        system_status_text.insert('end', '\nSystem Status\n\n', 'tag-center')
        status_message = "  Communications:\n  Module - X-Hatch\n\t++ Sensors\t[Y]\n\t++ Motors\t[Y]\n  Module - Adhesion\n\t++ Sensors\t[Y]\n\t++ Motors\t[Y]\n  Module - Imaging\n\t++ Camera\t[Y]\n\t++ Illuminations\t[Y]"
        system_status_text.insert(tk.END, status_message)
        system_status_text.configure(state='disabled')
        system_status_text.grid(row=testID_row+9, column=testID_column, columnspan=vs_widget_columnspan, rowspan=7, padx=(10,10), pady=(0,10), sticky='nesw')

        #=========================================================================================================================================

        colour_last_row = tk.Label(self, text="", background=page_not_selected, font=page_selection_font)
        colour_last_row.grid(row=24, column=0, columnspan=8, sticky='nesw')

        #Maybe add all this into a column/row defining function for each page
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')

        self.grid_rowconfigure((2), weight=1)
        self.grid_rowconfigure((0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), weight=5, uniform='a')
        self.grid_rowconfigure((24), weight=8)




class XHatchPage(tk.Frame):

    def __init__(self, parent, controller):
        
        #Constants
        page_selected, page_not_selected, header_blue, header_background_box, button_colour, text_colour, dark_blue_textbox, background_dark_grey, page_selection_font, in_page_heading_font, in_page_heading_font_bold, white_colour = import_constants()
        
        tk.Frame.__init__(self,parent)
        
        #=========================================================================================================================================
        # Page Selecting Buttons

        #label.config(bg= "gray51", fg= "white")
        button_style = GROOVE # unselected, selected = RIDGE
        main_page_button = tk.Button(self, text="Main Page", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(MainPage))  
        x_hatch_page_button = tk.Button(self, text="X-Hatch", background=page_selected, relief=RIDGE, font=page_selection_font, command='')
        adhesion_page_button = tk.Button(self, text="Adhesion", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(AdhesionPage))  
        imaging_page_button = tk.Button(self, text="Imaging", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(ImagingPage))  

        for e,label in enumerate([main_page_button,x_hatch_page_button,adhesion_page_button, imaging_page_button]):
            label.place(relx=((e*2)+1)/8,rely=0.00, relwidth=0.25, anchor='n')

        #=========================================================================================================================================
        # Position Sensor Display (psd)
        
        self.psd_label = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "Position Sensor Display"))
        self.psd_label.grid(row=2, column=0, columnspan=4, rowspan=21, pady=(30,5), padx=(20,0), sticky='nesw')
        self.psd_label.grid_columnconfigure((0,1,2), weight=1, uniform='a')
        self.psd_label.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1, uniform='a')

        #==================================================================
        # X-Hatch Position Sub-Box

        x_pos_row = 0
        x_pos_col = 0

        self.x_position_label = ttk.LabelFrame(self.psd_label, labelwidget=define_framelabel(self, "X-Hatch Position"))
        self.x_position_label.grid(row=0, column=0, columnspan=2, rowspan=7, padx=(10,10), pady=(20,10), sticky='nesw')
        self.x_position_label.grid_columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.x_position_label.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight=1, uniform='a')

        x_axis_label = tk.Label(self.x_position_label, text="X-Axis Position", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        x_axis_label.grid(row=x_pos_row+1, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        x_axis_entry = ttk.Entry(self.x_position_label, style='Custom.TEntry')
        x_axis_entry.grid(row=x_pos_row+1, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        x_axis_units = tk.Label(self.x_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        x_axis_units.grid(row=x_pos_row+1, column=x_pos_col+4, pady=(0,3), sticky='nsw')
        
        y_axis_label = tk.Label(self.x_position_label, text="Y-Axis Position", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        y_axis_label.grid(row=x_pos_row+3, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        y_axis_entry = ttk.Entry(self.x_position_label, style='Custom.TEntry')
        y_axis_entry.grid(row=x_pos_row+3, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        y_axis_units = tk.Label(self.x_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        y_axis_units.grid(row=x_pos_row+3, column=x_pos_col+4, pady=(0,3), sticky='nsw')
        
        z_axis_label = tk.Label(self.x_position_label, text="Z-Axis Position", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        z_axis_label.grid(row=x_pos_row+5, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        z_axis_entry = ttk.Entry(self.x_position_label, style='Custom.TEntry')
        z_axis_entry.grid(row=x_pos_row+5, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        z_axis_units = tk.Label(self.x_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        z_axis_units.grid(row=x_pos_row+5, column=x_pos_col+4, pady=(0,3), sticky='nsw')
        
        rz_label = tk.Label(self.x_position_label, text="RZ", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        rz_label.grid(row=x_pos_row+7, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        rz_entry = ttk.Entry(self.x_position_label, style='Custom.TEntry')
        rz_entry.grid(row=x_pos_row+7, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        rz_units = tk.Label(self.x_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        rz_units.grid(row=x_pos_row+7, column=x_pos_col+4, pady=(0,3), sticky='nsw')
        
        x_sensor1_label = tk.Label(self.x_position_label, text="Sensor 1", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        x_sensor1_label.grid(row=x_pos_row+9, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        x_sensor1_entry = ttk.Entry(self.x_position_label, style='Custom.TEntry')
        x_sensor1_entry.grid(row=x_pos_row+9, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        
        x_sensor2_label = tk.Label(self.x_position_label, text="Sensor 2", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        x_sensor2_label.grid(row=x_pos_row+11, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        x_sensor2_entry = ttk.Entry(self.x_position_label, style='Custom.TEntry')
        x_sensor2_entry.grid(row=x_pos_row+11, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')

        #==================================================================
        # Adhesion Position Sub-Box
        
        first_sensor_row = 1
        first_sensor_column = 0

        self.adhesion_position_label = ttk.LabelFrame(self.psd_label, labelwidget=define_framelabel(self, "Adhesion Position"))
        self.adhesion_position_label.grid(row=0, column=2, rowspan=12, padx=(10,10), pady=(20,20), sticky='nesw')
        self.adhesion_position_label.grid_columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.adhesion_position_label.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18), weight=1, uniform='a')

        a_sensor1_label = tk.Label(self.adhesion_position_label, text="Sensor 1", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        a_sensor1_label.grid(row=first_sensor_row, column=first_sensor_column, columnspan=2, padx=(10,5), pady=(0,3), sticky='nesw')
        a_sensor1_entry = ttk.Entry(self.adhesion_position_label, style='Custom.TEntry')
        a_sensor1_entry.grid(row=first_sensor_row, column=first_sensor_column+2, columnspan=2, padx=(0,5), pady=(0,3), sticky='nesw')
        a_sensor1_units = tk.Label(self.adhesion_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        a_sensor1_units.grid(row=first_sensor_row, column=first_sensor_column+4, padx=(0,10), pady=(0,3), sticky='nsw')

        a_sensor2_label = tk.Label(self.adhesion_position_label, text="Sensor 2", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        a_sensor2_label.grid(row=first_sensor_row+2, column=first_sensor_column, columnspan=2, padx=(10,5), pady=(0,3), sticky='nesw')
        a_sensor2_entry = ttk.Entry(self.adhesion_position_label, style='Custom.TEntry')
        a_sensor2_entry.grid(row=first_sensor_row+2, column=first_sensor_column+2, columnspan=2, padx=(0,5), pady=(0,3), sticky='nesw')
        a_sensor2_units = tk.Label(self.adhesion_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        a_sensor2_units.grid(row=first_sensor_row+2, column=first_sensor_column+4, padx=(0,10), pady=(0,3), sticky='nsw')
        
        a_sensor3_label = tk.Label(self.adhesion_position_label, text="Sensor 3", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        a_sensor3_label.grid(row=first_sensor_row+4, column=first_sensor_column, columnspan=2, padx=(10,5), pady=(0,3), sticky='nesw')
        a_sensor3_entry = ttk.Entry(self.adhesion_position_label, style='Custom.TEntry')
        a_sensor3_entry.grid(row=first_sensor_row+4, column=first_sensor_column+2, columnspan=2, padx=(0,5), pady=(0,3), sticky='nesw')
        a_sensor3_units = tk.Label(self.adhesion_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        a_sensor3_units.grid(row=first_sensor_row+4, column=first_sensor_column+4, padx=(0,10), pady=(0,3), sticky='nsw')

        #==================================================================
        # Rail Position (rp) Sub-Box

        x_pos_row = 0
        x_pos_col = 0

        self.rail_position_label = ttk.LabelFrame(self.psd_label, labelwidget=define_framelabel(self, "Rail Position"))
        self.rail_position_label.grid(row=7, column=0, columnspan=2, rowspan=5, padx=(10,10), pady=(10,20), sticky='nesw')
        self.rail_position_label.grid_columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.rail_position_label.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')

        rp_x_axis_label = tk.Label(self.rail_position_label, text="X-Axis Position", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        rp_x_axis_label.grid(row=x_pos_row+1, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        rp_x_axis_entry = ttk.Entry(self.rail_position_label, style='Custom.TEntry')
        rp_x_axis_entry.grid(row=x_pos_row+1, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        rp_x_axis_units = tk.Label(self.rail_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        rp_x_axis_units.grid(row=x_pos_row+1, column=x_pos_col+4, pady=(0,3), sticky='nsw')
        
        rp_y_axis_label = tk.Label(self.rail_position_label, text="Y-Axis Position", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        rp_y_axis_label.grid(row=x_pos_row+3, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        rp_y_axis_entry = ttk.Entry(self.rail_position_label, style='Custom.TEntry')
        rp_y_axis_entry.grid(row=x_pos_row+3, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        rp_y_axis_units = tk.Label(self.rail_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        rp_y_axis_units.grid(row=x_pos_row+3, column=x_pos_col+4, pady=(0,3), sticky='nsw')
        
        rp_z_axis_label = tk.Label(self.rail_position_label, text="Z-Axis Position", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        rp_z_axis_label.grid(row=x_pos_row+5, column=x_pos_col, columnspan=2, padx=(10,10), pady=(0,3), sticky='nesw')
        rp_z_axis_entry = ttk.Entry(self.rail_position_label, style='Custom.TEntry')
        rp_z_axis_entry.grid(row=x_pos_row+5, column=x_pos_col+2, columnspan=2, padx=(0,10), pady=(0,3), sticky='nesw')
        rp_z_axis_units = tk.Label(self.rail_position_label, text="mm", background=background_dark_grey, foreground=white_colour, font=in_page_heading_font)
        rp_z_axis_units.grid(row=x_pos_row+5, column=x_pos_col+4, pady=(0,3), sticky='nsw')

        #=========================================================================================================================================
        # Centre Page Buttons

        self.a_b_control = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "A + B Control"))
        self.a_b_control.grid(row=4, column=4, rowspan=4, padx=(20,20), sticky='nesw')

        A_button = tk.Button(self.a_b_control, text="A", foreground=text_colour, background=button_colour, command='')
        A_button.grid(row=1, column=0, columnspan=4, padx=(10,10), sticky='ew')
        B_profile_button = tk.Button(self.a_b_control, text="B", foreground=text_colour, background=button_colour, command='')
        B_profile_button.grid(row=3, column=0, columnspan=4, padx=(10,10), sticky='ew')

        self.a_b_control.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.a_b_control.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a')
        
        exit_program_button = tk.Button(self, text="Exit Program", foreground=text_colour, background=button_colour, command=lambda: exit_popupmsg(controller, 'Are you sure you wish to exit?'))
        exit_program_button.grid(row=22, column=4, padx=(30,30), sticky='ew')

        #==================================================================
        # System Position Control (spc) Panel

        self.spc_label = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "System Position Control"))
        self.spc_label.grid(row=10, column=4, columnspan=4, rowspan=7, padx=(20,20), sticky='nesw')
        
        self.spc_label.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.spc_label.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight=1, uniform='a')

        auto_home_label = tk.Label(self.spc_label, text="Auto-Home", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        auto_home_label.grid(row=1, column=0, rowspan=2, padx=(15,15), pady=(5,5), sticky='nesw')
        calibration_label = tk.Label(self.spc_label, text="Calibration", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        calibration_label.grid(row=1, column=1, rowspan=2, padx=(15,15), pady=(5,5), sticky='nesw')
        question_label = tk.Label(self.spc_label, text="?", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        question_label.grid(row=1, column=2, rowspan=2, padx=(15,15), pady=(5,5), sticky='nesw')
        save_pos_label = tk.Label(self.spc_label, text="Save Position", background=header_blue, foreground=white_colour, font=in_page_heading_font)
        save_pos_label.grid(row=1, column=3, rowspan=2, padx=(15,35), pady=(5,5), sticky='nesw')

        #=========================================================================================================================================
        # Right Page Options

        test_storage_row = 2
        test_storage_column = 0
        vs_widget_columnspan = 4

        self.variable_selection2 = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "Variable Selection"))
        self.variable_selection2.grid(row=4, column=5, columnspan=3, rowspan=4, padx=(0,20), sticky='nesw')
        self.variable_selection2.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.variable_selection2.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')

        test_storage_label = tk.Label(self.variable_selection2, text="Test Storage:", background=header_blue, foreground=white_colour, font=in_page_heading_font_bold)
        test_storage_label.grid(row=test_storage_row, column=test_storage_column, columnspan=vs_widget_columnspan, padx=(10,10), sticky='ews')
        test_storage_entry = ttk.Entry(self.variable_selection2, style='Custom.TEntry')
        test_storage_entry.insert(1, 'C:/Example/path/A')
        test_storage_entry.grid(row=test_storage_row+1, column=test_storage_column, columnspan=vs_widget_columnspan, padx=(10,10), sticky='ewn')

        path_select_button = tk.Button(self.variable_selection2, text="Path - Select", foreground=text_colour, background=button_colour, command='')
        path_select_button.grid(row=test_storage_row+3, column=test_storage_column, columnspan=vs_widget_columnspan, padx=(10,10), sticky='ew')

        x_system_status_text = tk.Text(self, background=dark_blue_textbox, foreground=white_colour, height=2, width=2)
        x_status_message = "\n  Module Status - X-Hatch\n\t++ Sensors\t[Y]\n\t++ Motors\t[Y]"
        x_system_status_text.insert(tk.END, x_status_message)
        x_system_status_text.configure(state='disabled')
        x_system_status_text.grid(row=18, column=5, columnspan=3, rowspan=5, padx=(0,20), sticky='nesw')
        
        #=========================================================================================================================================
        
        colour_last_row = tk.Label(self, text="", background=page_not_selected, font=page_selection_font)
        colour_last_row.grid(row=24, column=0, columnspan=8, sticky='nesw')
        
        #Maybe add all this into a column/row defining function for each page
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')

        self.grid_rowconfigure((2), weight=1)
        self.grid_rowconfigure((0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), weight=5, uniform='a')
        self.grid_rowconfigure((24), weight=8)




class AdhesionPage(tk.Frame):

    def __init__(self, parent, controller):
        
        #Constants
        page_selected, page_not_selected, header_blue, header_background_box, button_colour, text_colour, dark_blue_textbox, background_dark_grey, page_selection_font, in_page_heading_font, in_page_heading_font_bold, white_colour = import_constants()
        
        tk.Frame.__init__(self,parent)
        
        #=========================================================================================================================================
        # Page Selecting Buttons

        #label.config(bg= "gray51", fg= "white")
        button_style = GROOVE # unselected, selected = RIDGE
        main_page_button = tk.Button(self, text="Main Page", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(MainPage))
        x_hatch_page_button = tk.Button(self, text="X-Hatch", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(XHatchPage))
        adhesion_page_button = tk.Button(self, text="Adhesion", background=page_selected, relief=RIDGE, font=page_selection_font, command='')
        imaging_page_button = tk.Button(self, text="Imaging", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(ImagingPage))

        for e,label in enumerate([main_page_button,x_hatch_page_button,adhesion_page_button, imaging_page_button]):
            label.place(relx=((e*2)+1)/8,rely=0.00, relwidth=0.25, anchor='n')

        #=========================================================================================================================================

        colour_last_row = tk.Label(self, text="", background=page_not_selected, font=page_selection_font)
        colour_last_row.grid(row=24, column=0, columnspan=8, sticky='nesw')

        #Maybe add all this into a column/row defining function for each page
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')

        self.grid_rowconfigure((2), weight=1)
        self.grid_rowconfigure((0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), weight=5, uniform='a')
        self.grid_rowconfigure((24), weight=8)




class ImagingPage(tk.Frame):

    def __init__(self, parent, controller):
        
        #Constants
        page_selected, page_not_selected, header_blue, header_background_box, button_colour, text_colour, dark_blue_textbox, background_dark_grey, page_selection_font, in_page_heading_font, in_page_heading_font_bold, white_colour = import_constants()
        
        tk.Frame.__init__(self,parent)
        
        #=========================================================================================================================================
        # Page Selecting Buttons

        #label.config(bg= "gray51", fg= "white")
        button_style = GROOVE # unselected, selected = RIDGE
        main_page_button = tk.Button(self, text="Main Page", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(MainPage))
        x_hatch_page_button = tk.Button(self, text="X-Hatch", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(XHatchPage))
        adhesion_page_button = tk.Button(self, text="Adhesion", background=page_not_selected, relief=button_style, font=page_selection_font, command=lambda: controller.show_page(AdhesionPage))
        imaging_page_button = tk.Button(self, text="Imaging", background=page_selected, relief=RIDGE, font=page_selection_font, command='')

        for e,label in enumerate([main_page_button,x_hatch_page_button,adhesion_page_button, imaging_page_button]):
            label.place(relx=((e*2)+1)/8,rely=0.00, relwidth=0.25, anchor='n')
        
        #=========================================================================================================================================
        # Test Images (left page)
        
        self.test_images_label = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "Test Images"))
        self.test_images_label.grid(row=2, column=0, columnspan=4, rowspan=21, pady=(30,5), padx=(20,20), sticky='nesw')
        self.test_images_label.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.test_images_label.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')

        open_lens_image = Image.open("default_lens_image.jpg")
        width, height = open_lens_image.size
        lens_image_resized = open_lens_image.resize((int(width/1.3), int(height/1.3)), Image.ANTIALIAS) #Original image is 699x176
        lens_image = ImageTk.PhotoImage(lens_image_resized)
        lens_photo = tk.Label(self.test_images_label, image=lens_image, borderwidth=0, background=dark_blue_textbox)
        lens_photo.photo = lens_image
        lens_photo.grid(row=0, column=0, columnspan=8, rowspan=8, padx=20, pady=20, sticky='nesw')

        #=========================================================================================================================================
        # Imaging Inputs (right page)

        ii_row = 0
        ii_column = 0

        self.imaging_inputs_label = ttk.LabelFrame(self, labelwidget=define_framelabel(self, "Imaging Inputs"))
        self.imaging_inputs_label.grid(row=2, column=4, columnspan=4, rowspan=21, pady=(30,5), padx=(10,20), sticky='nesw')
        self.imaging_inputs_label.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.imaging_inputs_label.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight=1, uniform='a')

        test_storage_label = tk.Label(self.imaging_inputs_label, text="Test Storage:", background=header_blue, foreground=white_colour, font=in_page_heading_font_bold)
        test_storage_label.grid(row=ii_row, column=ii_column, columnspan=4, padx=(20,10), pady=(20,5), sticky='esw')
        test_storage_entry = ttk.Entry(self.imaging_inputs_label, style='Custom.TEntry')
        test_storage_entry.insert(1, 'C:/Example/path/A')
        test_storage_entry.grid(row=ii_row+1, column=ii_column, columnspan=4, padx=(20,10), sticky='ewn')
        
        path_select_button = tk.Button(self.imaging_inputs_label, text="Path - Select", foreground=text_colour, background=button_colour, command='')
        path_select_button.grid(row=ii_row+3, column=ii_column, columnspan=2, padx=(20,5), sticky='ew')
        display_image_button = tk.Button(self.imaging_inputs_label, text="Display Image", foreground=text_colour, background=button_colour, command='')
        display_image_button.grid(row=ii_row+3, column=ii_column+2, columnspan=2, padx=(5,10), sticky='ew')

        i_system_status_text = tk.Text(self.imaging_inputs_label, background=dark_blue_textbox, foreground=white_colour, height=2, width=2)
        i_status_message = "\n Module Status: Imaging\n   ++ Sensors\t[Y]\n   ++ Motors\t[Y]"
        i_system_status_text.insert(tk.END, i_status_message)
        i_system_status_text.configure(state='disabled')
        i_system_status_text.grid(row=ii_row, column=ii_column+4, columnspan=4, rowspan=4, padx=(0,20), pady=(20,0), sticky='nesw')

        #==================================================================
        # Camera Control Panel (ccp)

        ccp_row = 1
        ccp_column = 0

        self.camera_control_label = ttk.LabelFrame(self.imaging_inputs_label, labelwidget=define_framelabel(self, "Camera Control"))
        self.camera_control_label.grid(row=ii_row+4, column=ii_column, columnspan=8, rowspan=6, pady=(20,0), padx=(20,20), sticky='nesw')
        self.camera_control_label.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.camera_control_label.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        
        capture_image_button = tk.Button(self.camera_control_label, text="Capture Image", foreground=text_colour, background=button_colour, command='')
        capture_image_button.grid(row=ccp_row, column=ccp_column, columnspan=4, padx=(20,10), sticky='ew')
        calibration_button = tk.Button(self.camera_control_label, text="Calibration", foreground=text_colour, background=button_colour, command='')
        calibration_button.grid(row=ccp_row, column=ccp_column+4, columnspan=4, padx=(10,20), sticky='ew')
        
        save_image_button = tk.Button(self.camera_control_label, text="Save Image", foreground=text_colour, background=button_colour, command='')
        save_image_button.grid(row=ccp_row+2, column=ccp_column, columnspan=4, padx=(20,10), sticky='ew')
        unknown_button = tk.Button(self.camera_control_label, text="?", foreground=text_colour, background=button_colour, command='')
        unknown_button.grid(row=ccp_row+2, column=ccp_column+4, columnspan=4, padx=(10,20), sticky='ew')
        
        process_button = tk.Button(self.camera_control_label, text="Process", foreground=text_colour, background=button_colour, command='')
        process_button.grid(row=ccp_row+4, column=ccp_column, columnspan=4, padx=(20,10), sticky='ew')
        analyse_button = tk.Button(self.camera_control_label, text="Analyse", foreground=text_colour, background=button_colour, command='')
        analyse_button.grid(row=ccp_row+4, column=ccp_column+4, columnspan=4, padx=(10,20), sticky='ew')

        #==================================================================
        # Lens Position Control Panel

        self.lens_control_label = ttk.LabelFrame(self.imaging_inputs_label, labelwidget=define_framelabel(self, "Lens Position Control"))
        self.lens_control_label.grid(row=ii_row+10, column=ii_column, columnspan=8, rowspan=3, pady=(20,20), padx=(20,20), sticky='nesw')
        self.lens_control_label.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.lens_control_label.grid_rowconfigure((0,1,2), weight=1, uniform='a')

        load_lens_button = tk.Button(self.lens_control_label, text="Load Lens", foreground=text_colour, background=button_colour, command='')
        load_lens_button.grid(row=1, column=0, columnspan=4, padx=(20,10), sticky='ew')
        rotate_lens_button = tk.Button(self.lens_control_label, text="Rotate Lens", foreground=text_colour, background=button_colour, command='')
        rotate_lens_button.grid(row=1, column=4, columnspan=4, padx=(10,20), sticky='ew')

        #=========================================================================================================================================

        colour_last_row = tk.Label(self, text="", background=page_not_selected, font=page_selection_font)
        colour_last_row.grid(row=24, column=0, columnspan=8, sticky='nesw')

        #Maybe add all this into a column/row defining function for each page
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')

        self.grid_rowconfigure((2), weight=1)
        self.grid_rowconfigure((0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), weight=5, uniform='a')
        self.grid_rowconfigure((24), weight=8)



def exit_popupmsg(master, msg):

    popup=tk.Toplevel()
    popup.protocol("WM_DELETE_WINDOW", master.attributes('-disabled', False)) #capture close event
    master.attributes('-disabled', True) #disable the main window  <- ** Don't know if this is working
    popup.geometry('400x100+600+350')
    popup.wm_title('Search Filter')
    label = ttk.Label(popup, text=msg, font=("Helvetica", 10))
    label.pack(side="top", pady=10, anchor='center')
    B1 = tk.Button(popup, text="Yes", command=lambda: exit_gui(master,popup, 'yes'))
    B1.place(relx=0.3, rely=0.7, width=50)
    B1 = tk.Button(popup, text="No", command=lambda: exit_gui(master,popup))
    B1.place(relx=0.7, rely=0.7, width=50)


def exit_gui(master, popup, text='no'):
    
    if text == 'yes':
        master.attributes('-disabled', False)
        popup.destroy()
        master.destroy()
    else:
        master.attributes('-disabled', False)
        popup.destroy()




if __name__ == "__main__":
    
    app = myGUI()

    # Set the initial theme
    # app.tk.call("source", "azure.tcl")
    # app.tk.call("set_theme", "dark")

    app.state('zoomed') #Opens tkinter full screen
    #app.geometry('1400x750+0+0')  
    
    # style = ttk.Style()
    # style.theme_use('clam')
    #print('** ', style.layout('TEntry'))
    app.mainloop()
    

'''
print out ttk.entry layout, then copy to new DIY element and change what is necessary

v1 (azure): [('Entry.field', {'sticky': 'nswe', 'border': '1', 'children': [('Entry.padding', {'sticky': 'nswe', 'children': [('Entry.textarea', {'sticky': 'nswe'})]})]})]
V2 (clam):  [('Entry.field', {'sticky': 'nswe', 'border': '1', 'children': [('Entry.padding', {'sticky': 'nswe', 'children': [('Entry.textarea', {'sticky': 'nswe'})]})]})]
default:    [('Entry.field', {'sticky': 'nswe', 'children': [('Entry.background', {'sticky': 'nswe', 'children': [('Entry.padding', {'sticky': 'nswe', 'children': [('Entry.textarea', {'sticky': 'nswe'})]})]})]})]
'''