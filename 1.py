from sklearn.svm import LinearSVC
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import wx
import os
import sys
import nltk
import math
import copy

reload(sys)  
sys.setdefaultencoding('latin-1')

tr = []
new_autho = []
docss = []
author_list = []
novel_list = [[]]
path = os.path.dirname(os.path.realpath(sys.argv[0]))




class main_window(wx.Frame) :
	def __init__(self,parent,id) :
		wx.Frame.__init__(self,parent,id,'Authorship Predictor',size=(500,500),style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
		panel=wx.Panel(self,-1)
		panel.SetBackgroundColour(wx.Colour(220,220,250))
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
		font.SetPointSize(20)
		training_button=wx.Button(panel,label="Training",pos=(90,130),size=(300,100))
		training_button.SetBackgroundColour(wx.Colour(200,250,200))
		training_button.SetFont(font)
		self.Bind(wx.EVT_BUTTON, self.show_training_window, training_button)
		testing_button=wx.Button(panel,label="Testing",pos=(90,280),size=(300,100))
		testing_button.SetBackgroundColour(wx.Colour(200,250,200))
		testing_button.SetFont(font)
		self.Bind(wx.EVT_BUTTON, self.show_testing_window, testing_button)
		status_bar=self.CreateStatusBar()
		menubar=wx.MenuBar()
		file_menu=wx.Menu()
		tools_menu=wx.Menu()
		help_menu=wx.Menu()
		quit = wx.MenuItem(file_menu, wx.NewId(), '&Quit\tCtrl+Q')
		exit_img=wx.Bitmap('icons/exit_ico.png')
		quit.SetBitmap(exit_img)
		file_menu.AppendItem(quit)
		self.Bind(wx.EVT_MENU, self.close_window, id=quit.GetId())
		training = wx.MenuItem(help_menu, wx.NewId(), '&Training')
		tools_menu.AppendItem(training)
		testing_menu=wx.Menu()
		test1=wx.MenuItem(testing_menu, wx.NewId(), 'Binary Testing')
		test2=wx.MenuItem(testing_menu, wx.NewId(), 'One versus All Testing')
		self.Bind(wx.EVT_MENU, self.show_testing_window, id=test1.GetId())
		self.Bind(wx.EVT_MENU, self.show_testing_window, id=test2.GetId())
		self.Bind(wx.EVT_MENU, self.show_training_window, id=training.GetId())
		testing_menu.AppendItem(test1)
		testing_menu.AppendItem(test2)
		tools_menu.AppendMenu(wx.NewId(),'Testing',testing_menu)
		help_topics = wx.MenuItem(help_menu, wx.NewId(), '&Help Topics')
		help_topics.SetBitmap(wx.Bitmap('icons/help_ico.jpg'))
		help_menu.AppendItem(help_topics)
		about = wx.MenuItem(help_menu, wx.NewId(), '&About')
		help_menu.AppendItem(about)
		self.Bind(wx.EVT_MENU, self.show_about_window, id=about.GetId())
		menubar.Append(file_menu,"File")
		menubar.Append(tools_menu,"Tools")
		menubar.Append(help_menu,"Help")
		self.SetMenuBar(menubar)
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		font.SetPointSize(30)
		appname=wx.StaticText(panel,-1,"Authorship Predictor",(10,30),(460,-1),wx.ALIGN_CENTER)
		appname.SetFont(font)
		appname.SetForegroundColour(wx.Colour(250,100,150))
		appname.SetFont(font)
		#appname=wx.StaticText(panel,-1,"----------------------------",(10,80),(360,-1),wx.ALIGN_CENTER)
		appname.SetFont(font)
		self.Centre()


	def close_window(self,event) :
		self.Close()

	
	def show_about_window(self,event) :
		about_frame=about_window(parent=None,id=0)
		about_frame.Show()


	def show_training_window(self,event) :
		training_frame=training_window(parent=None,id=1)
		training_frame.Show()


	def show_testing_window(self,event) :
		testing_frame=testing_window(parent=None,id=1)
		testing_frame.Show()





class about_window(wx.Frame) :
	def __init__(self,parent,id) :
		wx.Frame.__init__(self,parent,id,'About',size=(400,350),style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		panel1=wx.Panel(self)
		panel1.SetBackgroundColour(wx.Colour(220,220,250))
		font.SetPointSize(30)
		appname=wx.StaticText(panel1,-1,"About",(110,30),(360,-1),wx.ALIGN_CENTER)
		appname.SetFont(font)
		appname.SetForegroundColour('blue')
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		font.SetPointSize(10)
		appname=wx.StaticText(panel1,-1,"Automatic Authorship Predictor Version : 1.0.0.1",(15,100),(360,-1),wx.ALIGN_CENTER)
		appname.SetFont(font)
		font.SetPointSize(15)
		appname.SetForegroundColour('red')
		appname=wx.StaticText(panel1,-1,"Authors",(150,140),(360,-1),wx.ALIGN_CENTER)
		appname.SetFont(font)
		appname=wx.StaticText(panel1,-1,"---------------------",(150,165),(360,-1),wx.ALIGN_CENTER)
		appname=wx.StaticText(panel1,-1,"Anjana.R\nDeepika.M\nNithin.P\nPanchami Raj.B\nRanjana.V",(110,190),(360,-1),wx.ALIGN_CENTER)
		appname.SetFont(font)






class training_window(wx.Frame) :
	global author_list
	global novel_list
	global docss
	def __init__(self,parent,id) :
		self.author_list=[]
		self.novel_list=[]
		self.numberOfAuthors=0
		self.authors=[]
		wx.Frame.__init__(self,parent,id,'Training',size=(600,620),style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
		self.panel=wx.Panel(self)
		self.panel.SetBackgroundColour(wx.Colour(220,220,250))
		font1 = wx.Font(10, wx.DEFAULT, wx.NORMAL,wx.FONTWEIGHT_NORMAL)
		font1.SetPointSize(12)
		add_author_button=wx.Button(self.panel,label="Add New Author",pos=(190,90),size=(200,30))
		add_author_button.SetFont(font1)
		self.Bind(wx.EVT_BUTTON, self.show_add_author, add_author_button)
		self.authorNameText=wx.StaticText(self.panel,-1,"Author Name\t : ",pos=(20,150),size=(30,50))
		self.authorNameText.SetFont(font1)
		self.authorNameChoices=wx.Choice(self.panel,-1,pos=(155,150),size=(290,30),choices=self.author_list)
		self.authorNameChoices.SetSelection(0)
		self.novelNameText=wx.StaticText(self.panel,-1,"Novel Name\t : ",pos=(20,200),size=(30,50))
		self.novelNameText.SetFont(font1)
		self.novelNameChoices=wx.Choice(self.panel,-1,pos=(155,200),size=(290,30))
		self.novelNameChoices.SetSelection(0)
		self.novelPrev=wx.TextCtrl(self.panel,-1,"",pos=(50,260),size=(500,200),style=wx.TE_MULTILINE)
		self.novelPrev.SetInsertionPoint(0)
		self.Bind(wx.EVT_CHOICE, self.set_new_author_novel_preview, self.authorNameChoices)
		self.Bind(wx.EVT_CHOICE, self.set_new_novel_preview, self.novelNameChoices)
		extract_features_button=wx.Button(self.panel,label="Extract Features",pos=(80,500),size=(200,40))
		extract_features_button.SetFont(font1)
		self.Bind(wx.EVT_BUTTON, self.start_extract_features_dialog, extract_features_button)
		#start_training_button=wx.Button(self.panel,label="Start Training",pos=(300,500),size=(200,40))
		#start_training_button.SetFont(font1)
		start_training_button=wx.Button(self.panel,label="Start Training",pos=(190,560),size=(220,40))
		start_training_button.SetFont(font1)
		feature_analysis_button=wx.Button(self.panel,label="Show Feature Analysis",pos=(300,500),size=(220,40))
		feature_analysis_button.SetFont(font1)
		self.Bind(wx.EVT_BUTTON, self.show_feature_analysis_window, feature_analysis_button)
		self.Bind(wx.EVT_BUTTON, self.start_training, start_training_button)
		self.numberAuthors=wx.StaticText(self.panel,-1,"Number Of Authors Selected : "+str(self.numberOfAuthors),(120,30),(360,-1),wx.ALIGN_CENTER)
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		font.SetPointSize(15)
		self.numberAuthors.SetFont(font)
		self.Bind(wx.EVT_CLOSE, self.close_all)

	def set_new_author_novel_preview(self,event) :
		self.novelNameChoices.SetItems(self.novel_list[self.authorNameChoices.GetSelection()])
		self.novelNameChoices.SetSelection(0)
		file1 = self.authors[self.authorNameChoices.GetSelection()][0]+"/"+self.authors[self.authorNameChoices.GetSelection()][1+self.novelNameChoices.GetSelection()]
		#print file1
		text1 = open(file1,"r").read()
		#print text1
		self.novelPrev.SetValue(text1)	
		self.Refresh()



	def show_feature_analysis_window(self,event) :
		try :
			tmp = os.listdir(path+'/generated_files')[0]
			self.features_analysis_frame=feature_analysis_window(parent=None,id=1)
			self.features_analysis_frame.Show()
		except :
			box=wx.MessageDialog(None,"Please extract features first.",'Alert',wx.OK)
			answer=box.ShowModal()
			box.Destroy()


	def show_features_window(self) :
		global author_list
		global novel_list
		global docss
		try :
			tmp=self.show_features_frame.GetSize()
		except :
			self.docs = []
			for auth in self.authors :
				for doc in auth[1:-1] :
					#print doc
					self.docs.append(features(doc,auth[-1],auth[0]))
			author_list = self.author_list
			novel_list = self.novel_list
			docss = self.docs
			self.show_features_frame=self.features_window(parent=None,id=1)
			self.show_features_frame.Show()
			#self.show_features_frame.Bind(wx.EVT_CLOSE, self.add_new_author,self.new_author_frame)



	def set_new_novel_preview(self,event) :
		file1 = self.authors[self.authorNameChoices.GetSelection()][0]+"/"+self.authors[self.authorNameChoices.GetSelection()][1+self.novelNameChoices.GetSelection()]
		#print file1
		text1 = open(file1,"r").read()
		#print text1
		self.novelPrev.SetValue(text1)			
		self.Refresh()

	def close_all(self,event) :
		try :
			self.new_author_frame.Destroy()
			self.Destroy()
		except :
			self.Destroy()


	def show_add_author(self,event) :
		try :
			tmp=self.new_author_frame.GetSize()
		except :
			self.new_author_frame=self.select_new_author_window(parent=None,id=1)
			self.new_author_frame.Show()
			self.new_author_frame.Bind(wx.EVT_CLOSE, self.add_new_author,self.new_author_frame)


	def add_new_author(self,event) :
		try :
			global new_autho
			if len(new_autho)>=3 and len(new_autho[-1])>0 :
				self.numberOfAuthors+=1
				self.authors.append(new_autho)
				#print new_autho[0::-1]
				self.novel_list.append(new_autho[1:-1])
				self.author_list.append(new_autho[-1])
				self.authorNameChoices.SetItems(self.author_list)
				self.authorNameChoices.SetSelection(0)
				#print self.novel_list
				self.novelNameChoices.SetItems(self.novel_list[self.authorNameChoices.GetSelection()])
				self.novelNameChoices.SetSelection(0)
				file1 = self.authors[self.authorNameChoices.GetSelection()][0]+"/"+self.authors[self.authorNameChoices.GetSelection()][1+self.novelNameChoices.GetSelection()]
				#print file1
				text1 = open(file1,"r").read()
				#print text1
				self.novelPrev.SetValue(text1)			
				self.Refresh()
			self.new_author_frame.Destroy()
			self.numberAuthors.SetLabel("Number Of Authors Selected : "+str(self.numberOfAuthors))
		except :
			self.new_author_frame.Destroy()
			
	def start_training(self,event) :
		try :
			#print path+'generated_files'
			tmp = os.listdir(path+'/generated_files')[0]
			box=wx.MessageDialog(None,"Start Training..!!???",'Alert',wx.YES_NO)
			answer=box.ShowModal()
			box.Destroy()
			if answer==wx.ID_YES :
				#print "Training Started"
				## Place to call the start trainin Function!!!!!!!
				global tr
				tr = TrainingTesting()
				tr.train()
				box=wx.MessageDialog(None,"Training Completed..!!",'Alert',wx.OK)
				answer=box.ShowModal()
				box.Destroy()

		except :
			box=wx.MessageDialog(None,"Please extract features first.",'Alert',wx.OK)
			answer=box.ShowModal()
			box.Destroy()


	def start_extract_features_dialog(self,event) :
		#self.show_features_window()
		
		if self.numberOfAuthors==0 :
			box=wx.MessageDialog(None,"Please input atleast one author details..!!!",'Alert',wx.OK)
			answer=box.ShowModal()
			box.Destroy()
		else :
			box=wx.MessageDialog(None,"Extract Features..!!???",'Alert',wx.YES_NO)
			answer=box.ShowModal()
			box.Destroy()
			#print "haiiii"
			if answer==wx.ID_YES :
				#pass
				#print "Feature extraction Started with data!!!!","\n",self.authors
				## Place to call the feature extraction Function!!!!!!!
				#box=wx.MessageDialog(None,"Feature extraction Started!!!",'Alert',wx.OK)
				#answer=box.ShowModal()
				#box.Destroy()
				self.show_features_window()
		
		



	class select_new_author_window(wx.Frame) :
		new_author=[]
		author_name=""
		
		
		def __init__(self,parent,id) :
			self.new_author=[]
			wx.Frame.__init__(self,parent,id,'Add New Author..!!!!!',size=(500,200),style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
			panel=wx.Panel(self)
			panel.SetBackgroundColour(wx.Colour(220,220,250))
			font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			font.SetPointSize(12)
			font1 = wx.Font(10, wx.DEFAULT, wx.NORMAL,wx.FONTWEIGHT_NORMAL)
			font1.SetPointSize(12)
			self.authorText=wx.StaticText(panel,-1,"Author Name  \t :",pos=(8,30),size=(130,25))
			self.authorText.SetFont(font1)
			self.nameText=wx.TextCtrl(panel,-1,"Enter name of author...!!",pos=(150,30),size=(300,-1))
			self.nameText.SetInsertionPoint(0)
			select_novels_button=wx.Button(panel,label="Select Novels",pos=(8,70),size=(130,25))
			select_novels_button.SetFont(font1)
			self.Bind(wx.EVT_BUTTON, self.show_select_novels, select_novels_button)
			self.novelText=wx.TextCtrl(panel,-1,"",pos=(150,70),size=(300,-1))#,style=wx.TE_READONLY)
			self.novelText.Bind(wx.EVT_LEFT_DOWN, self.show_select_novels)
			self.novelText.SetInsertionPoint(0)
			ok_button=wx.Button(panel,label="OK",pos=(150,120),size=(100,40))
			ok_button.SetFont(font1)
			self.Bind(wx.EVT_BUTTON, self.return_new_author, ok_button)
		
		
		def show_select_novels(self,event) :
			wcd = 'Text Files (*.txt)|*.txt'
			open_dlg = wx.FileDialog(self, message='Choose Novels', defaultDir=os.getcwd(), defaultFile='',wildcard=wcd, style=wx.OPEN|wx.CHANGE_DIR|wx.MULTIPLE)
			ans=open_dlg.ShowModal()
			open_dlg.Destroy()
			self.new_author=[]
			novels=""
			novels+=open_dlg.GetDirectory()
			self.new_author.append(open_dlg.GetDirectory())
			for i in range(len(open_dlg.GetFilenames())) :
				novels+=open_dlg.GetFilenames()[i]
				novels+=","
				self.new_author.append(open_dlg.GetFilenames()[i])

			self.novelText.SetValue(novels)
		
		
		def return_new_author(self,event) :
			self.new_author.append(self.nameText.GetValue())
			global new_autho
			new_autho=self.new_author
			self.Close()



	class features_window(wx.Frame) :
		global docss
		global author_list
		global novel_list
		def __init__(self,parent,id) :
			global author_list
			global novel_list
			self.author_list = copy.copy(author_list)
			self.novel_list = copy.copy(novel_list)
			self.features_list = []
			for i in self.novel_list :
				a = []
				for j in i :
					a.append(0)
				self.features_list.append(a)
			#print self.author_list
			#print self.novel_list
			global docss
			self.docs = docss
			for doc in self.docs :
				doc.extract_features()
				doc.create_csv_file()
				i = self.author_list.index(doc.authorname)
				j = self.novel_list[i].index(doc.docname)
				self.features_list[i][j] = doc.full_features

			wx.Frame.__init__(self,parent,id,'Feature Extraction',size=(600,450),style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
			self.panel=wx.Panel(self)
			self.panel.SetBackgroundColour(wx.Colour(220,220,250))
			font1 = wx.Font(10, wx.DEFAULT, wx.NORMAL,wx.FONTWEIGHT_NORMAL)
			font1.SetPointSize(12)
			self.authorNameText=wx.StaticText(self.panel,-1,"Author Name\t : ",pos=(20,30),size=(30,50))
			self.authorNameText.SetFont(font1)
			self.authorNameChoices=wx.Choice(self.panel,-1,pos=(155,30),size=(290,30),choices=self.author_list)
			self.authorNameChoices.SetSelection(0)
			self.novelNameText=wx.StaticText(self.panel,-1,"Novel Name\t : ",pos=(20,80),size=(30,50))
			self.novelNameText.SetFont(font1)
			self.novelNameChoices=wx.Choice(self.panel,-1,pos=(155,80),size=(290,30),choices=self.novel_list[self.authorNameChoices.GetSelection()])
			self.novelNameChoices.SetSelection(0)
			self.novelPrev=wx.TextCtrl(self.panel,-1,self.features_list[0][0],pos=(50,130),size=(500,200),style=wx.TE_MULTILINE)
			self.novelPrev.SetInsertionPoint(0)
			self.Bind(wx.EVT_CHOICE, self.set_new_author_features_preview, self.authorNameChoices)
			self.Bind(wx.EVT_CHOICE, self.set_new_novel_features_preview, self.novelNameChoices)
			start_training_button=wx.Button(self.panel,label="Start Training",pos=(300,370),size=(200,40))
			self.Bind(wx.EVT_BUTTON, self.start_training, start_training_button)
			start_training_button.SetFont(font1)
			save_features_button=wx.Button(self.panel,label="Save Features",pos=(70,370),size=(190,40))
			save_features_button.SetFont(font1)
			self.Bind(wx.EVT_BUTTON, self.save_features_as_a_file, save_features_button)
			font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			font.SetPointSize(15)
			#self.numberAuthors.SetFont(font)
			#self.Bind(wx.EVT_CLOSE, self.close_all)
			#print self.authors
		
		def save_features_as_a_file(self,event) :
			global path
			try :
				os.mkdir(path+"/Features")
			except :
				pass
			for doc in self.docs :
				#print doc.full_features
				#print os.path.dirname(os.path.abspath(os.__file__))
				#print os.path.dirname(os.path.realpath(os.__file__))
				#print os.path.dirname(os.path.realpath(sys.argv[0]))
				#print os.getcwd()
				try :
					os.mkdir(path+"/Features/"+doc.authorname)
				except :
					pass
				#print path+"/output/"+doc.authorname+"/"+doc.docname
				file1 = open(path+"/Features/"+doc.authorname+"/"+doc.docname,"w")
				file1.write(doc.full_features)
				file1.close()
			box=wx.MessageDialog(None,"Features saved in a folder named Features.",'Alert',wx.OK)
			answer=box.ShowModal()
			box.Destroy()
			
		def start_training(self,event) :
			try :
				tmp = os.listdir(path+'/generated_files')[0]
				box=wx.MessageDialog(None,"Start Training..!!???",'Alert',wx.YES_NO)
				answer=box.ShowModal()
				box.Destroy()
				if answer==wx.ID_YES :
					#print "Training Started"
					## Place to call the start trainin Function!!!!!!!
					global tr
					tr = TrainingTesting()
					tr.train()
					box=wx.MessageDialog(None,"Training Completed..!!",'Alert',wx.OK)
					answer=box.ShowModal()
					box.Destroy()

			except :
				box=wx.MessageDialog(None,"Please extract features first.",'Alert',wx.OK)
				answer=box.ShowModal()
				box.Destroy()

				
		
		def set_new_author_features_preview(self,event) :
			self.novelNameChoices.SetItems(self.novel_list[self.authorNameChoices.GetSelection()])
			self.novelNameChoices.SetSelection(0)
			self.novelPrev.SetValue(self.features_list[self.authorNameChoices.GetSelection()][0])			
			self.Refresh()

		def set_new_novel_features_preview(self,event) :
			self.novelPrev.SetValue(self.features_list[self.authorNameChoices.GetSelection()][self.novelNameChoices.GetSelection()])			
			self.Refresh()


		def close_all(self,event) :
			try :
				self.Destroy()
			except :
				pass







class feature_analysis_window(wx.Frame) :
	def __init__(self,parent,id) :
		self.author_list = []
		self.feature_name_list = []

		self.draw_graph = DrawGraph()
		
		docs = os.listdir(path+"/generated_files/")

		for doc in docs :
			self.author_list.append(doc[:-4])
		feats = open(path+"/generated_files/"+docs[0],"r").read().split("\n")[0].split(",")
		self.feature_name_list = feats[1:]
		self.feature_list = []

		for doc in docs :
			t = []
			feats = open(path+"/generated_files/"+doc,"r").read().split("\n")
			for feat in feats[1:-1] :
				tt = []
				feat = feat.split(",")
				for f in feat [1:-1] :
					tt.append(float(f))
				t.append(tt)
			
			self.feature_list.append(t)

		#print self.feature_list[0]



		
		wx.Frame.__init__(self,parent,id,'Features Analysis',size=(600,600),style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
		self.panel=wx.Panel(self)
		self.panel.SetBackgroundColour(wx.Colour(220,220,250))
		font1 = wx.Font(10, wx.DEFAULT, wx.NORMAL,wx.FONTWEIGHT_NORMAL)
		font1.SetPointSize(10)
		font2 = wx.Font(10, wx.DEFAULT, wx.NORMAL,wx.FONTWEIGHT_NORMAL)
		font2.SetPointSize(12)
		self.Bind(wx.EVT_CLOSE, self.close_all)

		self.type1=wx.RadioButton(self.panel, -1, 'Single Author VS documents feature analysis',pos=(120,20), style=wx.RB_GROUP)
		self.type1.SetFont(font1)
		self.type2=wx.RadioButton(self.panel, -1, 'Multiple authors feature analysis',pos=(120,55))
		self.type2.SetFont(font1)
		self.Bind(wx.EVT_RADIOBUTTON, self.draw_new_graph, self.type2)
		self.Bind(wx.EVT_RADIOBUTTON, self.draw_new_graph, self.type1)
		self.authorNameText=wx.StaticText(self.panel,-1,"Author Name\t : ",pos=(50,105))
		self.authorNameText.SetFont(font2)
		self.authorNameChoices=wx.Choice(self.panel,-1,pos=(185,105),size=(290,30),choices=self.author_list)
		self.authorNameChoices.SetSelection(0)
		self.featureNameText=wx.StaticText(self.panel,-1,"Feature Name\t : ",pos=(50,145))
		self.featureNameText.SetFont(font2)
		self.featureNameChoices=wx.Choice(self.panel,-1,pos=(185,145),size=(290,30),choices=self.feature_name_list)
		self.featureNameChoices.SetSelection(0)

		self.Bind(wx.EVT_CHOICE, self.draw_new_graph, self.authorNameChoices)
		self.Bind(wx.EVT_CHOICE, self.draw_new_graph, self.featureNameChoices)


		tt = self.feature_list[self.authorNameChoices.GetSelection()]
		tt = np.array(tt)
		y_data = tt.T[self.featureNameChoices.GetSelection()]
		x_data = []
		t = 1
		for i in y_data :
			x_data.append(t)
			t+=1

		self.draw_graph.draw_single_graph(x_data,y_data,'Books','feature_value',self.feature_name_list[self.featureNameChoices.GetSelection()])

		png = wx.Image(path+"/temp_img.png",wx.BITMAP_TYPE_ANY)
		png = png.Scale(400,300,wx.IMAGE_QUALITY_HIGH)
		png = png.ConvertToBitmap()
		self.graph_img = wx.StaticBitmap(self.panel,-1,png,(100,200),(png.GetWidth(),png.GetHeight()))

		self.graph_img.Bind(wx.EVT_LEFT_DOWN, self.show_graph_photo_viewer)

		save_features_button = wx.Button(self.panel,label="Save Graphs as PDF",pos=(180,530),size=(250,40))
		save_features_button.SetFont(font2)

		self.Bind(wx.EVT_BUTTON, self.save_graph_as_a_file, save_features_button)


	def save_graph_as_a_file(self,event) :
		graph_data = []
		if self.type1.GetValue() :
			graph_data.append(True)
			graph_data.append(path+"/graph_analysis1")
			tmp = []
			temp2 = 0
			for tt in self.feature_list :
				
				tt = np.array(tt)
				temp1 = 0
				for t in tt.T :
					y_data = t
					x_data = []
					ttt = 1
					for i in y_data :
						x_data.append(ttt)
						ttt+=1
					#print self.feature_name_list[temp]
					tmp.append([x_data,y_data, 'Books of '+self.author_list[temp2],'features value',self.author_list[temp2]+"'s "+self.feature_name_list[temp1]])
					temp1+=1
				temp2+=1
			graph_data.append(tmp)
			#print graph_data[2][0]
			self.draw_graph.save_set_of_graphs(graph_data)
			#os.system("gnome-open graph_analysis1.pdf")

			box=wx.MessageDialog(None,"Graphs saved to file named 'graph_analysis1.pdf'..! Open it now.?",'Alert',wx.YES_NO)
			answer=box.ShowModal()
			box.Destroy()
			if answer==wx.ID_YES :
				os.system("gnome-open "+path+"/graph_analysis1.pdf")



		elif self.type2.GetValue() :
			graph_data.append(True)
			graph_data.append(path+"/graph_analysis2")
			tmp = []
			for i in range(len(self.feature_name_list))  :
				ttt = 1
				y_data = []
				x_data = []
				for t in self.feature_list :
					t = np.array(t)
					y_data.append(float(sum(t.T[i]))/float(len(t.T[i])))
					x_data.append(ttt)
					ttt+=1
				tmp.append([x_data,y_data,'Authors','feature value',self.feature_name_list[i] + " of authors"])
					
			graph_data.append(tmp)
			#print graph_data[2][0]
			self.draw_graph.save_set_of_graphs(graph_data)
			#os.system("gnome-open graph_analysis2.pdf")
			box=wx.MessageDialog(None,"Graphs saved to file named 'graph_analysis2.pdf'..! Open it now.?",'Alert',wx.YES_NO)
			answer=box.ShowModal()
			box.Destroy()
			if answer==wx.ID_YES :
				os.system("gnome-open "+path+"/graph_analysis2.pdf")
				
	

	def show_graph_photo_viewer(self,event) :
		os.system("gnome-open "+path+"/temp_img.png")

	
	def draw_new_graph(self,event) :
		#self.draw_graph()
		if self.type1.GetValue() :
			self.enable_author_choices()
			tt = self.feature_list[self.authorNameChoices.GetSelection()]
			tt = np.array(tt)
			y_data = tt.T[self.featureNameChoices.GetSelection()]
			x_data = []
			t = 1
			for i in y_data :
				x_data.append(t)
				t+=1

			self.draw_graph.draw_single_graph(x_data,y_data,'Books','feature_value',self.feature_name_list[self.featureNameChoices.GetSelection()])
			png = wx.Image(path+"/temp_img.png",wx.BITMAP_TYPE_ANY)
			png = png.Scale(400,300,wx.IMAGE_QUALITY_HIGH)
			png = png.ConvertToBitmap()
			self.graph_img.SetBitmap(png)

		elif self.type2.GetValue() :
			self.disable_author_choices()
			tt = self.feature_list
			tt = np.array(tt)
			y_data = []
			x_data = []
			ttt = 1
			for t in tt :
				t = np.array(t)
				y_data.append(float(sum(t.T[self.featureNameChoices.GetSelection()]))/float(len(t.T[self.featureNameChoices.GetSelection()])))
				x_data.append(ttt)
				ttt += 1
			#print x_data
			self.draw_graph.draw_single_graph(x_data,y_data,'Authors','feature_value',self.feature_name_list[self.featureNameChoices.GetSelection()])
			png = wx.Image(path+"/temp_img.png",wx.BITMAP_TYPE_ANY)
			png = png.Scale(400,300,wx.IMAGE_QUALITY_HIGH)
			png = png.ConvertToBitmap()
			self.graph_img.SetBitmap(png)





			

	


	def disable_author_choices(self) :
		self.authorNameChoices.Disable()



	def enable_author_choices(self) :
		self.authorNameChoices.Enable()




	def close_all(self,event) :
		try :
			self.Destroy()
		except :
			pass










class testing_window(wx.Frame) :
	def __init__(self,parent,id) :
		self.author_list = []
		try :
			a = os.listdir(path+"/generated_files/")
			for b in a :
				self.author_list.append(b[:-4])
		except :
			self.author_list.append(' ')
			self.author_list.append(' ')


		self.testing_novel=[]
		self.novel1=[]
		wx.Frame.__init__(self,parent,id,'Testing',size=(480,400),style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
		panel = wx.Panel(self)
		panel.SetBackgroundColour(wx.Colour(220,220,250))
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
		font.SetPointSize(12)
		self.test1=wx.RadioButton(panel, -1, 'One versus all testing',pos=(20,20),size=(220,50), style=wx.RB_GROUP)
		self.test1.SetFont(font)
		self.test2=wx.RadioButton(panel, -1, 'Binary testing',pos=(20,55),size=(220,50))
		self.test2.SetFont(font)
		self.Bind(wx.EVT_RADIOBUTTON, self.disable_choices, self.test1)
		self.Bind(wx.EVT_RADIOBUTTON, self.enable_choices, self.test2)
		font1 = wx.Font(10, wx.DEFAULT, wx.NORMAL,wx.FONTWEIGHT_NORMAL)
		font1.SetPointSize(12)
		select_novels_button=wx.Button(panel,label="Select a Novel",pos=(8,120),size=(130,25))
		select_novels_button.SetFont(font1)
		self.Bind(wx.EVT_BUTTON, self.show_select_novel, select_novels_button)
		self.novelText=wx.TextCtrl(panel,-1,"",pos=(150,120),size=(300,-1))
		self.novelText.Bind(wx.EVT_LEFT_DOWN, self.show_select_novel)
		self.novelText.SetInsertionPoint(0)
		self.author1Text=wx.StaticText(panel,-1,"Select Author 1 \t : ",pos=(20,180),size=(30,50))
		self.author1Text.SetFont(font1)
		self.author1Choices=wx.Choice(panel,-1,pos=(155,180),size=(290,30),choices=self.author_list)
		self.author1Choices.SetSelection(0)
		self.author2Text=wx.StaticText(panel,-1,"Select Author 2 \t : ",pos=(20,220),size=(30,50))
		self.author2Text.SetFont(font1)
		self.author2Choices=wx.Choice(panel,-1,pos=(155,220),size=(290,30),choices=self.author_list)
		self.author2Choices.SetSelection(1)
		self.author2Choices.Disable()
		self.author1Choices.Disable()
		start_test_button=wx.Button(panel,label="Start Test",pos=(170,280),size=(130,40))
		start_test_button.SetFont(font1)
		self.Bind(wx.EVT_BUTTON, self.start_test_dialog, start_test_button)


	def start_test_dialog(self,event) :
		if self.test2.GetValue() and self.author2Choices.GetSelection()==self.author1Choices.GetSelection()  :
			box=wx.MessageDialog(None,"Please select two different authors...!!!",'Alert',wx.OK)
			answer=box.ShowModal()
			box.Destroy()
		elif len(self.novel1) <2 :
			box=wx.MessageDialog(None,"Please select a novel..!!!!!",'Alert',wx.OK)
			answer=box.ShowModal()
			box.Destroy()
		else :
			box=wx.MessageDialog(None,"Start testing of the novel..!!!",'Alert',wx.YES_NO)
			answer=box.ShowModal()
			box.Destroy()
			if answer==wx.ID_YES :
				self.testing_novel=[]
				self.testing_novel.append(self.test2.GetValue())
				self.testing_novel.append(self.novel1)
				#print "Testing Started with data!!!!","\n",self.testing_novel
				## Place to call the testing Function!!!!!!!
				"""box=wx.MessageDialog(None,"Test Started!!!",'Alert',wx.OK)
				answer=box.ShowModal()
				box.Destroy()"""
				if self.testing_novel[0] :
					self.start_binary_testing()
				else :
					try : 
						tr.author_names
						self.start_all_testing()
					except :
						box=wx.MessageDialog(None,"Train the system first.",'Alert',wx.OK)
						answer=box.ShowModal()
						box.Destroy()


	


	def start_binary_testing(self) :
		doc = features(self.testing_novel[1][1],'unknown',self.testing_novel[1][0])
		doc.extract_features()
		#print doc.number_comas
		#pass
		self.test_data = []
		self.test_data.append(float(sum(doc.number_comas))/float(len(doc.number_comas)))
		self.test_data.append(float(sum(doc.number_semicolans))/float(len(doc.number_semicolans)))
		self.test_data.append(float(sum(doc.number_quotations))/float(len(doc.number_quotations)))
		self.test_data.append(float(sum(doc.number_exclamations))/float(len(doc.number_exclamations)))
		self.test_data.append(float(sum(doc.number_hyphens))/float(len(doc.number_hyphens)))
		self.test_data.append(float(sum(doc.number_ands))/float(len(doc.number_ands)))
		self.test_data.append(float(sum(doc.number_buts))/float(len(doc.number_buts)))
		self.test_data.append(float(sum(doc.number_howevers))/float(len(doc.number_howevers)))
		self.test_data.append(float(sum(doc.number_ifs))/float(len(doc.number_ifs)))

		self.test_data.append(float(sum(doc.number_thats))/float(len(doc.number_thats)))
		self.test_data.append(float(sum(doc.number_mores))/float(len(doc.number_mores)))
		self.test_data.append(float(sum(doc.number_musts))/float(len(doc.number_musts)))
		self.test_data.append(float(sum(doc.number_mights))/float(len(doc.number_mights)))
		self.test_data.append(float(sum(doc.number_thiss))/float(len(doc.number_thiss)))
		self.test_data.append(float(sum(doc.number_verys))/float(len(doc.number_verys)))
		self.test_data.append(doc.mean_word_length)
		self.test_data.append(doc.mean_sentence_length)

		self.test_data.append(doc.standard_deviation_sentence)
		docs = []
		docs.append(self.author_list[self.author1Choices.GetSelection()]+".csv")
		docs.append(self.author_list[self.author2Choices.GetSelection()]+".csv")

		y = []
		noa = 0
		author_names = []
		train_data = []
		author_files = os.listdir(path+"/generated_files")
		#print author_names
		for author in docs :
			author_names.append(author[:-4])
			text1 = open(path+"/generated_files/"+author,"r").read().split("\n")
			#print text1[1:-1]
			for txt in text1[1:-1] :
				t = []
				y.append(noa)
				#t.append(self.noa) 
				for i in txt.split(",")[1:-1] :
					t.append(float(i))
				train_data.append(t)
			noa += 1
		clfr1 = LinearSVC()
		clfr1.fit(train_data,y)
		auth_name = author_names[clfr1.predict(np.array(self.test_data).reshape(1,-1))[0]]

		box=wx.MessageDialog(None,"Author of the document is '"+auth_name+"'.",'message',wx.OK)
		answer=box.ShowModal()
		box.Destroy()

		

	def start_all_testing(self) :
		
		doc = features(self.testing_novel[1][1],'unknown',self.testing_novel[1][0])
		doc.extract_features()
		#print doc.number_comas
		#pass
		self.test_data = []
		self.test_data.append(float(sum(doc.number_comas))/float(len(doc.number_comas)))
		self.test_data.append(float(sum(doc.number_semicolans))/float(len(doc.number_semicolans)))
		self.test_data.append(float(sum(doc.number_quotations))/float(len(doc.number_quotations)))
		self.test_data.append(float(sum(doc.number_exclamations))/float(len(doc.number_exclamations)))
		self.test_data.append(float(sum(doc.number_hyphens))/float(len(doc.number_hyphens)))
		self.test_data.append(float(sum(doc.number_ands))/float(len(doc.number_ands)))
		self.test_data.append(float(sum(doc.number_buts))/float(len(doc.number_buts)))
		self.test_data.append(float(sum(doc.number_howevers))/float(len(doc.number_howevers)))
		self.test_data.append(float(sum(doc.number_ifs))/float(len(doc.number_ifs)))

		self.test_data.append(float(sum(doc.number_thats))/float(len(doc.number_thats)))
		self.test_data.append(float(sum(doc.number_mores))/float(len(doc.number_mores)))
		self.test_data.append(float(sum(doc.number_musts))/float(len(doc.number_musts)))
		self.test_data.append(float(sum(doc.number_mights))/float(len(doc.number_mights)))
		self.test_data.append(float(sum(doc.number_thiss))/float(len(doc.number_thiss)))
		self.test_data.append(float(sum(doc.number_verys))/float(len(doc.number_verys)))
		self.test_data.append(doc.mean_word_length)
		self.test_data.append(doc.mean_sentence_length)
		self.test_data.append(doc.standard_deviation_sentence)

		tr.test(self.test_data)
		
		box=wx.MessageDialog(None,"Author of the document is '"+tr.correct_author_name+"'.",'message',wx.OK)
		answer=box.ShowModal()
		box.Destroy()


	def disable_choices(self,event) :
		self.author1Choices.Disable()
		self.author2Choices.Disable()


	def enable_choices(self,event) :
		self.author1Choices.Enable()
		self.author2Choices.Enable()


	def show_select_novel(self,event) :
		wcd = 'Text Files (*.txt)|*.txt'
		open_dlg = wx.FileDialog(self, message='Choose a Novel', defaultDir=os.getcwd(), defaultFile='',wildcard=wcd, style=wx.OPEN|wx.CHANGE_DIR)
		ans=open_dlg.ShowModal()
		open_dlg.Destroy()
		if open_dlg.GetFilename()!="" :
			self.novel1=[]
			novels=""
			novels+=open_dlg.GetDirectory()
			novels+=open_dlg.GetFilename()
			self.novel1.append(open_dlg.GetDirectory())
			self.novel1.append(open_dlg.GetFilename())
			self.novelText.SetValue(novels)




class features() :
	def __init__(self,docnamee,authornamee,pathh) :
		self.docname = docnamee
		self.authorname = authornamee
		self.path = pathh
		
		self.file1 = open(self.path+"/"+self.docname,"r")
		self.data = self.file1.read().replace("\n"," ").lower()
		self.tokenized_data = nltk.tokenize.word_tokenize(self.data)

	def print_content(self) :
		#print self.tokenized_data
		#print self.data
		pass


	def create_csv_file(self) :
		global path
		try :
			os.mkdir(path+"/generated_files")
		except :
			pass
		try :
			file1 = open(path+"/generated_files/"+self.authorname+".csv","r")
		except :
			file1 = open(path+"/generated_files/"+self.authorname+".csv","a+")
			#file1.write(self.authorname+"\n")
			a = ","
			a += "Average Number of comas per thousand tokens,"
			a += "Average Number of semicolons per thousand tokens,"
			a += "Average Number of quotation marks per thousand tokens,"
			a += "Average Number of exclamation marks per thousand tokens,"
			a += "Average Number of hyphens per thousand tokens,"
			a += "Average Number of ands per thousand tokens,"
			a += "Average Number of buts per thousand tokens,"
			a += "Average Number of howevers per thousand tokens,"
			a += "Average Number of ifs per thousand tokens,"
			a += "Average Number of thats per thousand tokens,"
			a += "Average Number of mores per thousand tokens,"
			a += "Average Number of musts per thousand tokens,"
			a += "Average Number of mights per thousand tokens,"
			a += "Average Number of thiss per thousand tokens,"
			a += "Average Number of verys per thousand tokens,"
			a += "Mean Word Length,"
			a += "Mean Sentence Length,"
			a += "Standard deviation of Sentence Length\n"
			file1.write(a)
			file1.close()
			
		file1 = open(path+"/generated_files/"+self.authorname+".csv","a+")
		#file1.write(self.authorname)
		#file1.write(self.authorname+""\n)
		a = self.docname
		a += ","
		a += str(float(sum(self.number_comas))/float(len(self.number_comas)))+","
		a += str(float(sum(self.number_semicolans))/float(len(self.number_semicolans)))+","
		a += str(float(sum(self.number_quotations))/float(len(self.number_quotations)))+","
		a += str(float(sum(self.number_exclamations))/float(len(self.number_exclamations)))+","
		a += str(float(sum(self.number_hyphens))/float(len(self.number_hyphens)))+","
		a += str(float(sum(self.number_ands))/float(len(self.number_ands)))+","
		a += str(float(sum(self.number_buts))/float(len(self.number_buts)))+","
		a += str(float(sum(self.number_howevers))/float(len(self.number_howevers)))+","
		a += str(float(sum(self.number_ifs))/float(len(self.number_ifs)))+","
		a += str(float(sum(self.number_thats))/float(len(self.number_thats)))+","
		a += str(float(sum(self.number_mores))/float(len(self.number_mores)))+","
		a += str(float(sum(self.number_musts))/float(len(self.number_musts)))+","

		a += str(float(sum(self.number_mights))/float(len(self.number_mights)))+","
		a += str(float(sum(self.number_thiss))/float(len(self.number_thiss)))+","
		a += str(float(sum(self.number_verys))/float(len(self.number_verys)))+","
		a += str(self.mean_word_length)+","
		a += str(self.mean_sentence_length)+","
		a += str(self.standard_deviation_sentence)+","
		a += "\n"
		file1.write(a)
		file1.close()

	def extract_features(self) :
		self.full_features = "----Features-----\n\n"
		## Number of comas per thousand tokens
		self.number_comas = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == ',' :
				count2 += 1
			if count1 == 1000 :
				self.number_comas.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of comas per thousand tokens = "
		self.full_features += str(self.number_comas)
		self.full_features += "\n\n"
		#print self.number_comas

		## Number of semicolons per thousand tokens
		self.number_semicolans = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == ';' :
				count2 += 1
			if count1 == 1000 :
				self.number_semicolans.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of semicolons per thousand tokens = "
		self.full_features += str(self.number_semicolans)
		self.full_features += "\n\n"
		#print self.number_semicolans

		## Number of quotation marks per thousand tokens
		self.number_quotations = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == '"' or token =="'":
				count2 += 1
			if count1 == 1000 :
				self.number_quotations.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of quotation marks per thousand tokens = "
		self.full_features += str(self.number_quotations)
		self.full_features += "\n\n"
		#print self.number_quotations

		## Number of exclamation marks per thousand tokens
		self.number_exclamations = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == '!' :
				count2 += 1
			if count1 == 1000 :
				self.number_exclamations.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of exclamation marks per thousand tokens = "
		self.full_features += str(self.number_exclamations)
		self.full_features += "\n\n"
		#print self.number_exclamations

		## Number of hyphens per thousand tokens
		self.number_hyphens = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == '-' :
				count2 += 1
			if count1 == 1000 :
				self.number_hyphens.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of hyphens per thousand tokens = "
		self.full_features += str(self.number_hyphens)
		self.full_features += "\n\n"
		#print self.number_hyphens

		## Number of ands per thousand tokens
		self.number_ands = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'and' :
				count2 += 1
			if count1 == 1000 :
				self.number_ands.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of ands per thousand tokens = "
		self.full_features += str(self.number_ands)
		self.full_features += "\n\n"
		#print self.number_ands

		## Number of buts per thousand tokens
		self.number_buts = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'but' :
				count2 += 1
			if count1 == 1000 :
				self.number_buts.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of buts per thousand tokens = "
		self.full_features += str(self.number_buts)
		self.full_features += "\n\n"
		#print self.number_buts

		## Number of howevers per thousand tokens
		self.number_howevers = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'however' :
				count2 += 1
			if count1 == 1000 :
				self.number_howevers.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of howevers per thousand tokens = "
		self.full_features += str(self.number_howevers)
		self.full_features += "\n\n"
		#print self.number_howevers

		## Number of ifs per thousand tokens
		self.number_ifs = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'if' :
				count2 += 1
			if count1 == 1000 :
				self.number_ifs.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of ifs per thousand tokens = "
		self.full_features += str(self.number_ifs)
		self.full_features += "\n\n"
		#print self.number_ifs

		## Number of thats per thousand tokens
		self.number_thats = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'that' :
				count2 += 1
			if count1 == 1000 :
				self.number_thats.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of thats per thousand tokens = "
		self.full_features += str(self.number_thats)
		self.full_features += "\n\n"
		#print self.number_thats

		## Number of mores per thousand tokens
		self.number_mores = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'more' :
				count2 += 1
			if count1 == 1000 :
				self.number_mores.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of mores per thousand tokens = "
		self.full_features += str(self.number_mores)
		self.full_features += "\n\n"
		#print self.number_mores

		## Number of musts per thousand tokens
		self.number_musts = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'must' :
				count2 += 1
			if count1 == 1000 :
				self.number_musts.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of musts per thousand tokens = "
		self.full_features += str(self.number_musts)
		self.full_features += "\n\n"
		#print self.number_musts

		## Number of mights per thousand tokens
		self.number_mights = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'might' :
				count2 += 1
			if count1 == 1000 :
				self.number_mights.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of mights per thousand tokens = "
		self.full_features += str(self.number_mights)
		self.full_features += "\n\n"
		#print self.number_mights

		## Number of thiss per thousand tokens
		self.number_thiss = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'this' :
				count2 += 1
			if count1 == 1000 :
				self.number_thiss.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of thiss per thousand tokens = "
		self.full_features += str(self.number_thiss)
		self.full_features += "\n\n"
		#print self.number_thiss

		## Number of verys per thousand tokens
		self.number_verys = []
		count1 = 0
		count2 = 0
		for token in self.tokenized_data :
			count1 += 1
			if token == 'very' :
				count2 += 1
			if count1 == 1000 :
				self.number_verys.append(count2)
				count1=0
				count2=0
		self.full_features += "Number of verys per thousand tokens = "
		self.full_features += str(self.number_verys)
		self.full_features += "\n\n"
		#print self.number_verys


		## Mean word length
		data = str(self.data)
		data = data.replace("."," ")
		data = data.replace(","," ")
		data = data.replace("!"," ")
		words = data.split()
		words.sort()
		count1=0
		count2=0
		for word in words :
			if word[:1].isalpha() == False :
				words.remove(word)
			else :
				#print word
				count1+=len(word)
				count2+=1
		self.mean_word_length = float(float(count1)/float(count2))
		self.full_features += "Mean word length = "
		self.full_features += str(self.mean_word_length)
		self.full_features += "\n\n"

		## Mean Sentence Length
		data = str(self.data)
		#print data
		#data = data.replace(".",".")
		#data = data.replace("!",".")
		#data = data.replace("?",".")
		sentences = nltk.tokenize.sent_tokenize(data)
		sentences.sort()
		#print sentences
		count1=0
		count2=0
		for sentence in sentences :
			#print sentence
			#if len(sentence)>5 :
			count1+=len(sentence)
			count2+=1
		self.mean_sentence_length = float(float(count1)/float(count2))
		self.full_features += "Mean Sentence length = "
		self.full_features += str(self.mean_sentence_length)
		self.full_features += "\n\n"

		## Standard Deviation of Sentence Length
		count1=0
		count2=0
		for sentence in sentences :
			t = float(len(sentence))-self.mean_sentence_length
			tt = t*t
			count1+=tt
			count2+=1
		self.standard_deviation_sentence =  math.sqrt(float(float(count1)/(float(count2))))
		self.full_features += "Standard Deviation of Sentence Length = "
		self.full_features += str(self.standard_deviation_sentence)
		self.full_features += "\n\n"
		#print self.full_features
		#print "Features of ",self.docname," is extracted."
		#self.create_csv_file()





class DrawGraph() :
	def __init__(self) :
		pass

	def draw_single_graph(self,x_data,y_data,x_label,y_label,title) :
		try :
			plt.close()
		except :
			pass
		fig = plt.figure()
		axis = fig.add_subplot(111)
		axis.set_title(title)
		axis.set_xlabel(x_label)
		axis.set_ylabel(y_label)
		axis.grid(True)
		plt.xticks(x_data)
		plt.plot(x_data,y_data,marker='*',c = 'red')
		plt.savefig(path+'/temp_img.png')

	def save_set_of_graphs(self,graph_data) :
		#pp = PdfPages(graph_data[0]+'.pdf')
		if graph_data[0] :
			pp = PdfPages(graph_data[1]+'.pdf')
			for data in graph_data[2] :
				try :
					plt.close()
				except :
					pass
				
				fig = plt.figure()
				axis = fig.add_subplot(111)
				axis.set_title(data[4])
				axis.set_xlabel(data[2])
				axis.set_ylabel(data[3])
				axis.grid(True)
				plt.xticks(data[0])
				plt.plot(data[0],data[1],marker='*',c = 'red')
				pp.savefig(fig)
		pp.close()




class TrainingTesting() :
	def __init__(self) :
		self.y = []
		self.noa = 0
		self.author_names = []
		self.train_data = []
		self.author_files = os.listdir(path+"/generated_files")
		#print author_names
		for author in self.author_files :
			self.author_names.append(author[:-4])
			text1 = open(path+"/generated_files/"+author,"r").read().split("\n")
			#print text1[1:-1]
			for txt in text1[1:-1] :
				t = []
				self.y.append(self.noa)
				#t.append(self.noa) 
				for i in txt.split(",")[1:-1] :
					t.append(float(i))
				self.train_data.append(t)
			self.noa += 1
		#print self.y
		#print self.train_data
	def train(self) :
		self.clfr = LinearSVC()
		self.clfr.fit(self.train_data,self.y)
		#print self.author_names[clfr.predict(self.train_data[0])[0]]
	def test(self,test_data) :
		self.correct_author_name = self.author_names[self.clfr.predict(np.array(test_data).reshape(1,-1))[0]]




def main() :
	app=wx.App()
	frame=main_window(parent=None,id=-1)
	frame.Show()
	app.MainLoop()


																																					

if __name__ == '__main__' :
	main()
