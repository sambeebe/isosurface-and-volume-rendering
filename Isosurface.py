import vtk

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        # self.parent.SetRenderWindow(renwin)
        self.isovalue=.5
        isoExtractor.SetValue(0,self.isovalue)
        txt.SetInput("Isovalue: " + str(self.isovalue))

        if(parent is not None):
          self.parent = parent
        self.AddObserver("KeyPressEvent",self.keyPress)


    def keyPress(self,obj,event):
      key = self.parent.GetKeySym()

      if(key == "Up"):
        self.isovalue += .02

      if(key == "Down"):
        self.isovalue -= .02

      if(key == "Left"):
        colorCells()
        randomColors.SetExecuteMethod(colorCells)

      isoExtractor.SetValue(0,self.isovalue)
      txt.SetInput("Isovalue: " + str(self.isovalue))
      renwin.Render()



tableSize = 10000
ctf = vtk.vtkColorTransferFunction()
ctf.SetColorSpaceToRGB()
ctf.AddRGBPoint(0.0, 0.0, 1.0, 0.0)
ctf.AddRGBPoint(1.0, 1.0, 1.0, 1.0)

LUT = vtk.vtkLookupTable()
LUT.SetNumberOfTableValues(tableSize)
LUT.Build()

for i in range(0, tableSize):
    rgb = list(ctf.GetColor(float(i) / tableSize)) + [1]
    LUT.SetTableValue(i, rgb)

color = vtk.vtkUnsignedCharArray()
color.SetName('colors')  # Any name will work here.
color.SetNumberOfComponents(3)


#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("/Users/sambeebe/vis-2019/assignment-4-sambeebe/data/hydrogen.vtk")
imageReader.Update()

#Print dimensions and range of the 3d image
dims = imageReader.GetOutput().GetDimensions()
print("Dimensions of image: " + str(dims[0]) + " x "
      + str(dims[1]) + " x " + str(dims[2]))
range = imageReader.GetOutput().GetScalarRange();
print("Range of image: " + str(range[0]) + " to " +  str(range[1]))

#create an outline that shows the bounds of our dataset
outline = vtk.vtkOutlineFilter();
outline.SetInputConnection(imageReader.GetOutputPort());

#mapper to push the outline geometry to the graphics library
outlineMapper = vtk.vtkPolyDataMapper();
outlineMapper.SetInputConnection(outline.GetOutputPort());

#actor for the outline to add to our renderer
outlineActor = vtk.vtkActor();
outlineActor.SetMapper(outlineMapper);
outlineActor.GetProperty().SetLineWidth(4.0);

isoExtractor = vtk.vtkMarchingCubes()
interactor = vtk.vtkRenderWindowInteractor()
renwin = vtk.vtkRenderWindow()
txt = vtk.vtkTextActor()
isoExtractor.SetInputConnection(imageReader.GetOutputPort())
isoExtractor.ComputeNormalsOn()
isoExtractor.GetOutput().GetCellData().SetScalars(color)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(isoExtractor.GetOutputPort())

mapper.SetScalarRange(0, tableSize - 1)
mapper.SetLookupTable(LUT)

isoMapper = vtk.vtkDataSetMapper()
isoMapper.SetInputConnection(isoExtractor.GetOutputPort())
isoMapper.SetLookupTable(mapper.GetLookupTable())


iso = vtk.vtkActor()
iso.SetMapper(isoMapper)

# create a text actor
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(isoMapper.GetLookupTable())
scalarBar.SetTitle("Probability")
scalarBar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalarBar.GetPositionCoordinate().SetValue(0.8,0.05)
scalarBar.SetOrientationToVertical()

scalarBar.SetWidth(0.17)
scalarBar.SetHeight(0.8)

txtprop=txt.GetTextProperty()
txtprop.SetFontFamilyToArial()
txtprop.SetFontSize(30)
txtprop.SetColor(1,1,1)
txt.SetDisplayPosition(20,30)

#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
# renderer.AddViewProp(iso)
renderer.AddActor(iso)
renderer.AddActor(txt)
renderer.AddActor(scalarBar)
renderer.AddActor(outlineActor)
renderer.SetBackground(0.1, 0.1, 0.2)

#Add actors to our renderer


#The render window

renwin.SetSize( 512, 512);
renwin.AddRenderer(renderer)

#Interactor to handle mouse and keyboard events

interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)

interactor.Initialize()
interactor.Start()
